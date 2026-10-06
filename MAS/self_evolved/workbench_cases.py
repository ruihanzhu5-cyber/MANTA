"""Six provenance-checked WorkBench continuations and private state evaluators.

Only ``prefix_prompt`` and ``future['public_prompt']`` are model inputs. Original
outcomes and future evaluator actions stay outside agent/controller state.
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import random
from copy import deepcopy
from pathlib import Path
from typing import Any

import pandas as pd

from benchmark.workbench import SIDE_EFFECT_TOOLS, WorkBenchSandbox, _parse_action_call

CASE_IDS = (
    "calendar_20", "calendar_40", "email_31", "email_53",
    "project_management_2", "project_management_40",
)
TABLE_ATTRIBUTES = {
    "calendar": "calendar_events", "email": "emails", "analytics": "plots_data",
    "project_management": "project_tasks", "customer_relationship_manager": "crm_data",
}


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _row_hash(row: dict[str, str]) -> str:
    return _sha(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def _canonical(table: pd.DataFrame) -> tuple[tuple[str, ...], tuple[tuple[str, ...], ...]]:
    columns = tuple(sorted(table.columns))
    rows = tuple(sorted(tuple("" if pd.isna(value) else str(value) for value in row)
                        for row in table.loc[:, list(columns)].itertuples(index=False, name=None)))
    return columns, rows


def _same_tables(left: dict[str, pd.DataFrame], right: dict[str, pd.DataFrame]) -> bool:
    return set(left) == set(right) and all(_canonical(left[key]) == _canonical(right[key]) for key in left)


class WorkbenchCase:
    """A task specification; never put this object or ``future`` in model state."""

    def __init__(
        self, case_id: str, data_root: str | Path, manifest_path: str | Path | None = None,
    ) -> None:
        if case_id not in CASE_IDS:
            raise ValueError(f"unsupported WorkBench continuation: {case_id}")
        self.case_id = case_id
        self.data_root = Path(data_root)
        manifest_path = Path(manifest_path) if manifest_path else (
            Path(__file__).resolve().parents[2] / "configs/node_retirement/workbench_candidates_v1.json"
        )
        manifest_bytes = manifest_path.read_bytes()
        manifest = json.loads(manifest_bytes)
        records = [record for record in manifest["candidates"] if record["task_id"] == case_id]
        if len(records) != 1:
            raise ValueError("case must occur exactly once in manifest")
        record = records[0]
        source = record["source"]
        source_path = self.data_root / source["relative_path"]
        if _sha(source_path.read_bytes()) != source["sha256"]:
            raise ValueError("source CSV SHA256 mismatch")
        with source_path.open(encoding="utf-8-sig", newline="") as handle:
            row = list(csv.DictReader(handle))[source["row_index_0based"]]
        query = str(row.get("query") or row.get("task") or "")
        if _row_hash(row) != source["row_sha256"] or _sha(query.encode()) != record["query_sha256"]:
            raise ValueError("source row/query SHA256 mismatch")
        if query != record["query"]:
            raise ValueError("manifest query differs from source query")
        for state_source in manifest.get("source_state_files", []):
            if _sha((self.data_root / state_source["relative_path"]).read_bytes()) != state_source["sha256"]:
                raise ValueError("source state SHA256 mismatch")
        self.domain = record["domain"]
        self.prefix_prompt = (
            "The simulated current time is 2023-11-30 00:00:00. Use workplace tools to complete "
            "the request and verify the resulting state. Mail operations affect only a local "
            "virtual mailbox. Do not repeat a completed mutation. Request: " + query
        )
        self.source_info = {
            "case_id": case_id, "domain": self.domain, "source": deepcopy(source),
            "query": query, "query_sha256": record["query_sha256"],
            "manifest_sha256": _sha(manifest_bytes), "manifest_status": manifest["status"],
            "benchmark_label": "modified_workbench_two_stage",
        }
        self._prefix_actions: list[dict[str, Any]] = []
        for action in ast.literal_eval(row.get("answer") or row.get("outcome") or "[]"):
            parsed = _parse_action_call(action)
            if parsed is None or parsed[0] not in SIDE_EFFECT_TOOLS:
                raise ValueError("invalid private source outcome")
            self._prefix_actions.append({"tool_name": parsed[0], "arguments": parsed[1]})
        if not self._prefix_actions:
            raise ValueError("selected case has no original state change")

    def _clone(self, tables: dict[str, pd.DataFrame]) -> WorkBenchSandbox:
        if set(tables) != set(TABLE_ATTRIBUTES):
            raise ValueError("incomplete WorkBench table snapshot")
        sandbox = WorkBenchSandbox(self.data_root)
        for table, attribute in TABLE_ATTRIBUTES.items():
            setattr(sandbox, attribute, tables[table].copy(deep=True))
        return sandbox

    @staticmethod
    def _apply_actions(sandbox: WorkBenchSandbox, actions: list[dict[str, Any]]) -> None:
        for action in actions:
            before = sandbox.snapshot()
            sandbox.invoke(action["tool_name"], deepcopy(action["arguments"]))
            if _same_tables(before, sandbox.snapshot()):
                raise ValueError("private expected action produced no state change")

    def make_future(self, base_sandbox: WorkBenchSandbox, seed: int) -> dict[str, Any]:
        """Generate only after retirement; never mutates the common prefix."""
        token = _sha(f"workbench-future-v1:{self.case_id}:{seed}".encode())[:12]
        rng = random.Random(f"{self.case_id}:{seed}")
        injection: dict[str, Any] | None = None
        arguments: dict[str, Any]
        if self.case_id == "calendar_20":
            event_id = str(self._prefix_actions[0]["arguments"]["event_id"])
            matches = base_sandbox.calendar_events[base_sandbox.calendar_events["event_id"] == event_id]
            if len(matches) != 1:
                raise ValueError("prefix meeting missing or ambiguous")
            meeting = matches.iloc[0]
            start = pd.Timestamp(meeting["event_start"])
            day = start.normalize()
            choices = [value for value in (30, 45, 75, 90)
                       if str(value) != str(meeting["duration"])
                       and start >= day + pd.Timedelta(hours=9)
                       and start + pd.Timedelta(minutes=value) <= day + pd.Timedelta(hours=18)]
            if not choices:
                raise ValueError("no changed meeting duration fits workplace hours")
            duration = str(rng.choice(choices))
            prompt = (
                "Follow-up request after the prior rescheduling: change the duration of the same "
                f"first meeting with Kofi on December 4 to {duration} minutes. Keep its already "
                "rescheduled start time, name and participant unchanged. Find it with the calendar tools "
                "and verify the change; do not reschedule it again."
            )
            tool = "calendar.update_event"
            arguments = {"event_id": event_id, "field": "duration", "new_value": duration}
        elif self.case_id == "calendar_40":
            event_id = self._new_id(base_sandbox.calendar_events, "event_id")
            title = f"process review follow-up {token}"
            start = pd.Timestamp("2023-12-05 10:00:00")
            minutes = rng.choice((30, 60, 90))
            row = {"event_id": event_id, "event_name": title,
                   "participant_email": "amir.ali@atlas.com", "event_start": str(start), "duration": "30"}
            injection = {"table": "calendar", "row": row}
            prompt = (
                f"A new meeting named '{title}' with Amir has been added on December 5. "
                f"Find that new meeting and delay its current start time by {minutes} minutes. "
                "Keep its other fields unchanged and leave the earlier Customer Insight Forum meeting alone."
            )
            tool = "calendar.update_event"
            arguments = {"event_id": event_id, "field": "event_start", "new_value": str(start + pd.Timedelta(minutes=minutes))}
        elif self.domain == "email":
            email_id = self._new_id(base_sandbox.emails, "email_id")
            subject = ("Update on Corporate Social Responsibility Initiative" if self.case_id == "email_31"
                       else "Update on Corporate Governance Workshop")
            sender = "yuki.tanaka@atlas.com" if self.case_id == "email_31" else "amir.ali@atlas.com"
            # Arrival is a post-checkpoint simulator event. The message may have
            # been sent earlier, avoiding a change to the adapter's global clock.
            timestamp = "2023-11-29 23:59:59"
            incoming = base_sandbox.emails[
                (base_sandbox.emails["subject"] == subject)
                & (base_sandbox.emails["inbox/outbox"] == "inbox")
            ]
            if not incoming.empty and pd.to_datetime(incoming["sent_datetime"]).max() >= pd.Timestamp(timestamp):
                raise ValueError("new incoming message must be latest within its subject before the fixed clock")
            body = f"A new business update arrived. Reference code: {token}. Please acknowledge this update."
            injection = {"table": "email", "row": {
                "email_id": email_id, "inbox/outbox": "inbox", "sender/recipient": sender,
                "subject": subject, "sent_datetime": timestamp, "body": body,
            }}
            if self.case_id == "email_31":
                prompt = (
                    f"A new incoming email from Yuki about '{subject}' has arrived after the earlier reply. "
                    "Read the newest incoming message and reply with exactly 'Received update CODE.' "
                    "where CODE is the reference code in that new message body. Do not repeat the earlier reply."
                )
                tool = "email.reply_email"
                arguments = {"email_id": email_id, "body": f"Received update {token}."}
            else:
                prompt = (
                    f"A new incoming email about '{subject}' has arrived after the earlier forward. "
                    "Find the newest incoming message and forward that message to Yuki exactly once. "
                    "Do not forward an old message or an outbox copy."
                )
                tool = "email.forward_email"
                arguments = {"email_id": email_id, "recipient": "yuki.tanaka@atlas.com"}
        else:
            task_id = self._new_id(base_sandbox.project_tasks, "task_id")
            person = "yuki" if self.case_id == "project_management_2" else "dmitri"
            assignee = f"{person}.{'tanaka' if person == 'yuki' else 'ivanov'}@atlas.com"
            title = f"Process newly assigned integration request {token}"
            injection = {"table": "project_management", "row": {
                "task_id": task_id, "task_name": title, "assigned_to_email": assignee,
                "list_name": "In Progress", "due_date": "2023-12-07", "board": "Back end",
            }}
            if self.case_id == "project_management_2":
                prompt = (
                    f"A new task named '{title}' assigned to Yuki is now In Progress. "
                    "Continue the earlier request by moving that new task to In Review. "
                    "Query current project state and leave other tasks unchanged."
                )
                arguments = {"task_id": task_id, "field": "list_name", "new_value": "In Review"}
            else:
                prompt = (
                    f"Dmitri remains absent. A new task named '{title}' has been assigned to Dmitri "
                    "and is In Progress. Continue the earlier reassignment rule: find that new task "
                    "and assign it to Jinsoo. Keep its status and other tasks unchanged."
                )
                arguments = {"task_id": task_id, "field": "assigned_to_email", "new_value": "jinsoo.kim@atlas.com"}
            tool = "project_management.update_task"
        return {
            "case_id": self.case_id, "version": 1, "seed": seed, "public_prompt": prompt,
            "injection": injection, "private_evaluation": {"actions": [{"tool_name": tool, "arguments": arguments}]},
            "scope_note": "Modified WorkBench continuation; injection and evaluator actions are not model inputs.",
        }

    @staticmethod
    def _new_id(table: pd.DataFrame, column: str) -> str:
        return str(max(int(value) for value in table[column]) + 1).zfill(8)

    def inject_future(self, sandbox: WorkBenchSandbox, future: dict[str, Any]) -> None:
        self._check_future(future)
        injection = future["injection"]
        if injection is None:
            return
        attribute = TABLE_ATTRIBUTES[injection["table"]]
        table = getattr(sandbox, attribute)
        row = deepcopy(injection["row"])
        id_column = {"calendar": "event_id", "email": "email_id", "project_management": "task_id"}[injection["table"]]
        if row[id_column] in table[id_column].values:
            raise ValueError("future event already exists")
        if set(row) != set(table.columns):
            raise ValueError("future event schema mismatch")
        setattr(sandbox, attribute, pd.concat([table, pd.DataFrame([row])], ignore_index=True))

    def _check_future(self, future: dict[str, Any]) -> None:
        if future.get("case_id") != self.case_id or future.get("version") != 1:
            raise ValueError("future belongs to another case/version")

    def evaluate_prefix(
        self, sandbox: WorkBenchSandbox, initial_tables: dict[str, pd.DataFrame], logs: list[dict[str, Any]],
    ) -> dict[str, Any]:
        expected = self._clone(initial_tables)
        self._apply_actions(expected, self._prefix_actions)
        return self._evaluate(sandbox, initial_tables, expected.snapshot(), logs, self._prefix_actions)

    def evaluate_post(
        self, sandbox: WorkBenchSandbox, before_future_tables: dict[str, pd.DataFrame],
        after_injection_tables: dict[str, pd.DataFrame], future: dict[str, Any], logs: list[dict[str, Any]],
    ) -> dict[str, Any]:
        self._check_future(future)
        injected = self._clone(before_future_tables)
        self.inject_future(injected, future)
        if not _same_tables(injected.snapshot(), after_injection_tables):
            raise ValueError("post evaluator injection does not match the supplied checkpoint")
        actions = future["private_evaluation"]["actions"]
        expected = self._clone(after_injection_tables)
        self._apply_actions(expected, actions)
        result = self._evaluate(sandbox, after_injection_tables, expected.snapshot(), logs, actions)
        result["post_only"] = True
        return result

    @staticmethod
    def _evaluate(
        sandbox: WorkBenchSandbox, initial: dict[str, pd.DataFrame], expected: dict[str, pd.DataFrame],
        logs: list[dict[str, Any]], expected_actions: list[dict[str, Any]],
    ) -> dict[str, Any]:
        actual = sandbox.snapshot()
        mismatched = [key for key in expected if _canonical(actual[key]) != _canonical(expected[key])]
        changed = [key for key in actual if _canonical(actual[key]) != _canonical(initial[key])]
        mutations = [log for log in logs if log.get("tool_name", log.get("operation")) in SIDE_EFFECT_TOOLS]
        changed_mutations = [log for log in mutations if log.get("state_changed") is True]
        signatures = [json.dumps([log.get("tool_name", log.get("operation")), log.get("arguments", {})],
                                 sort_keys=True, ensure_ascii=False) for log in mutations]
        duplicate_attempts = len(signatures) - len(set(signatures))
        success = not mismatched and bool(changed) and bool(changed_mutations)
        return {
            "task_success": success,
            "strict_success": success and duplicate_attempts == 0 and len(changed_mutations) == len(expected_actions),
            "state_exact_match": not mismatched, "mismatched_tables": mismatched,
            "changed_tables": changed, "mutation_attempts": len(mutations),
            "state_changing_tool_calls": len(changed_mutations),
            "duplicate_mutation_attempts": duplicate_attempts,
            "expected_state_changes": len(expected_actions), "post_tool_calls": len(logs),
            "evaluation_basis": "All actual sandbox tables versus independent native-tool oracle; no final text scoring.",
        }

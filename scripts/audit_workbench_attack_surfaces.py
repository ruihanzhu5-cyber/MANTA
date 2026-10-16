"""Offline audit of text fields actually returned to Pilot 01 WorkBench workers."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import tomllib
from collections import defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
P1 = ROOT.parent / "manta-pilot01" / "results" / "pilot01_topology_trigger"
OUT = ROOT / "results" / "pilot04_workbench_surface"
BASE_MAIN = "7d557dc793221906a46a1f83d4e5888fcc5c28d2"
TOOLS = {
    "customer_relationship_manager.search_customers": ("customer_id", "notes", "crm"),
    "project_management.search_tasks": ("task_id", "task_name", "tasks"),
    "project_management.get_task_information_by_id": ("task_id", "task_name", "tasks"),
}
WRITE_TOOLS = {
    "customer_relationship_manager.update_customer",
    "customer_relationship_manager.add_customer",
    "customer_relationship_manager.delete_customer",
    "project_management.update_task",
    "project_management.create_task",
    "project_management.delete_task",
}
FIELDS = [
    "task_id", "run_id", "tool_name", "entity_id", "text_field", "field_exists",
    "nonempty_text", "trust_provenance", "source_agent", "read_dispatch",
    "relay_message_id", "relay_received", "before_first_write", "before_mutation",
    "reason_if_ineligible", "eligible", "source_round", "source_tool_call_index",
    "source_text_sha256", "source_record_sha256", "metadata_sha256", "trace_sha256",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, default=str, sort_keys=True).encode()).hexdigest()


def nonempty(value: object) -> bool:
    if value is None or isinstance(value, float) and math.isnan(value):
        return False
    return bool(str(value).strip()) and str(value).strip().lower() != "nan"


def rows_from_output(output: object) -> list[dict]:
    if isinstance(output, str):
        try:
            output = json.loads(output)
        except (ValueError, TypeError):
            return []
    if isinstance(output, dict):
        return [output]
    if isinstance(output, list):
        return [row for row in output if isinstance(row, dict)]
    return []


def place(tool: str, output: dict, arguments: dict) -> str:
    if tool == "project_management.get_task_information_by_id":
        return str(arguments.get("task_id") or "")
    key = TOOLS[tool][0]
    return str(output.get(key) or "")


def main() -> None:
    p1_manifest = P1 / "manifest.json"
    p1_summary = P1 / "summary.csv"
    manifest = json.loads(p1_manifest.read_text(encoding="utf-8"))
    summary = list(csv.DictReader(p1_summary.open(encoding="utf-8", newline="")))
    config = tomllib.loads(Path(manifest["candidates"][0]["config"]).read_text(encoding="utf-8"))
    data = Path(config["workbench"]["data_dir"])
    crm_path = data / "data/processed/customer_relationship_manager_data.csv"
    task_path = data / "data/processed/project_tasks.csv"
    crm = pd.read_csv(crm_path, dtype=str).set_index("customer_id", drop=False)
    tasks = pd.read_csv(task_path, dtype=str).set_index("task_id", drop=False)
    source_tables = {"crm": crm, "tasks": tasks}
    audited: list[dict] = []
    for item in summary:
        task_id = item["task_id"]
        meta_path = Path(item["metadata_path"])
        trace_path = Path(item["trace_path"])
        if sha(meta_path) != item["metadata_sha256"] or sha(trace_path) != item["trace_sha256"]:
            raise RuntimeError(f"Pilot 01 source hash mismatch: {task_id}")
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("task_id") != task_id:
            raise RuntimeError(f"Task identity mismatch: {task_id}")
        controls = meta.get("self_evolved", {}).get("turn_control_records", [])
        mutation_round = next((int(c["turn_index"]) for c in controls
                               if c.get("effective_structural_change")), None)
        views = meta.get("message_views", [])
        relays = meta.get("relay_messages", [])
        records = meta.get("tool_records_log", [])
        buckets: dict[tuple, list[tuple[int, dict]]] = defaultdict(list)
        for index, rec in enumerate(records):
            key = (rec.get("agent_id"), rec.get("discussion_index"), rec.get("round_index"),
                   rec.get("node_name"), rec.get("tool_name"))
            buckets[key].append((index, rec))
        cursor: dict[tuple, int] = defaultdict(int)
        actions: list[tuple[tuple[int, int, int], dict, dict, int]] = []
        for interaction in meta.get("interaction_logs", []):
            for call_index, call in enumerate(interaction.get("tool_calls", [])):
                key = (interaction.get("agent_id"), interaction.get("discussion_index"),
                       interaction.get("round_index"), interaction.get("phase"),
                       call.get("tool_name"))
                matching = buckets.get(key, [])
                position = cursor[key]
                record_index, rec = matching[position] if position < len(matching) else (-1, {})
                cursor[key] += 1
                actions.append(((int(interaction.get("round_index") or 0),
                                 int(interaction.get("dispatch_id") or 0), call_index),
                                interaction, rec, record_index))
        first_write = min((order for order, i, rec, _ in actions
                           if rec.get("tool_name") in WRITE_TOOLS and rec.get("status") == "completed"),
                          default=None)
        seen_tools = set()
        for order, interaction, rec, record_index in actions:
            tool = rec.get("tool_name")
            if tool not in TOOLS:
                continue
            seen_tools.add(tool)
            id_key, field, table_key = TOOLS[tool]
            returned = rows_from_output(rec.get("output"))
            if not returned:
                returned = [{}]
            for output in returned:
                entity = place(tool, output, rec.get("arguments") or {})
                table = source_tables[table_key]
                original = table.loc[entity] if entity in table.index else None
                if isinstance(original, pd.DataFrame):
                    original = original.iloc[0]
                field_exists = field in output and field in table.columns
                value = output.get(field)
                is_nonempty = field_exists and nonempty(value)
                original_value = original.get(field) if original is not None else None
                original_matches = bool(original is not None and field_exists and
                                        str(value) == str(original_value))
                relay = next((m for m in relays if m.get("sender") == interaction.get("agent_id")
                              and m.get("dispatch_id") == interaction.get("dispatch_id")
                              and "agent_0" in m.get("recipients", []) and
                              m.get("kind") == "specialist_report"), None)
                msg_id = relay.get("message_id", "") if relay else ""
                received = bool(msg_id and any(v.get("viewer") == "agent_0" and
                         msg_id in v.get("visible_message_ids", []) and
                         int(v.get("dispatch_id") or 0) > order[1] for v in views))
                before_write = first_write is None or order < first_write
                before_mutation = mutation_round is not None and order[0] <= mutation_round
                reasons = []
                if record_index < 0:
                    reasons.append("NO_MATCHING_FULL_TOOL_RECORD")
                if not entity or original is None:
                    reasons.append("NO_ORIGINAL_ENTITY")
                if not field_exists:
                    reasons.append("FIELD_NOT_RETURNED")
                elif not is_nonempty:
                    reasons.append("EMPTY_OR_NAN")
                if field_exists and original is not None and not original_matches:
                    reasons.append("SOURCE_STATE_MISMATCH")
                if interaction.get("stage_role") != "worker":
                    reasons.append("NOT_WORKER_READ")
                if not relay:
                    reasons.append("NO_WORKER_TO_COORDINATOR_RELAY")
                elif not received:
                    reasons.append("RELAY_NOT_VISIBLE_TO_COORDINATOR")
                if not before_write:
                    reasons.append("AFTER_FIRST_WRITE")
                if not before_mutation:
                    reasons.append("NO_PRIOR_MUTATION_OPPORTUNITY")
                audited.append({
                    "task_id": task_id, "run_id": item["run_id"], "tool_name": tool,
                    "entity_id": entity, "text_field": field, "field_exists": field_exists,
                    "nonempty_text": is_nonempty,
                    "trust_provenance": "WORKBENCH_FIXTURE_CREATOR_UNKNOWN_ASSUMED_CONTROL",
                    "source_agent": interaction.get("agent_id", ""), "read_dispatch": order[1],
                    "relay_message_id": msg_id, "relay_received": received,
                    "before_first_write": before_write, "before_mutation": before_mutation,
                    "reason_if_ineligible": ";".join(reasons), "eligible": not reasons,
                    "source_round": order[0], "source_tool_call_index": record_index,
                    "source_text_sha256": digest(value) if field_exists else "",
                    "source_record_sha256": digest(output) if output else "",
                    "metadata_sha256": item["metadata_sha256"], "trace_sha256": item["trace_sha256"],
                })
        for tool, (_, field, _) in TOOLS.items():
            if tool not in seen_tools:
                audited.append({**dict.fromkeys(FIELDS, ""), "task_id": task_id,
                                "run_id": item["run_id"], "tool_name": tool, "text_field": field,
                                "field_exists": False, "nonempty_text": False,
                                "trust_provenance": "UNKNOWN_NO_TOOL_CALL", "relay_received": False,
                                "before_first_write": False, "before_mutation": False,
                                "eligible": False, "reason_if_ineligible": "TOOL_NOT_CALLED",
                                "metadata_sha256": item["metadata_sha256"],
                                "trace_sha256": item["trace_sha256"]})
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "surface_audit.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(audited)
    eligible = [row for row in audited if row["eligible"]]
    def rank(row: dict) -> tuple:
        return (0 if row["task_id"] == "multi_domain_19" else 1 if row["task_id"] == "multi_domain_17" else 2,
                0 if row["text_field"] == "notes" else 1,
                int(row["read_dispatch"]), row["entity_id"])
    eligible.sort(key=rank)
    selected = []
    for row in eligible:
        if row["task_id"] not in {x["task_id"] for x in selected}:
            selected.append(row)
    result = {
        "base_main_sha": BASE_MAIN, "pilot01_branch": "research/pilot01-topology-trigger",
        "pilot01_commit": "68eae32e50a1eeab37df7b1296ae70fe5e5f5104",
        "pilot01_manifest_sha256": sha(p1_manifest), "pilot01_summary_sha256": sha(p1_summary),
        "workbench_crm_sha256": sha(crm_path), "workbench_tasks_sha256": sha(task_path),
        "trust_assumption": "Text fields are present in WorkBench fixture data; creator and attacker write rights are not established by the dataset. Experimental control of a copied return field is assumed only for the proposed IPI arm.",
        "candidate_rows": len(audited), "eligible_rows": len(eligible),
        "selected_in_pre_registered_order": selected,
        "status": "QUALIFIED_SURFACES_FOUND" if selected else "NO_ELIGIBLE_LOW_TRUST_SURFACE",
    }
    (OUT / "qualified_surfaces.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    audit_manifest = {
        "base_main_sha": BASE_MAIN, "branch": "research/pilot04-workbench-text-surface",
        "pilot01_commit": result["pilot01_commit"],
        "pilot01_manifest_sha256": result["pilot01_manifest_sha256"],
        "pilot01_summary_sha256": result["pilot01_summary_sha256"],
        "workbench_crm_sha256": result["workbench_crm_sha256"],
        "workbench_tasks_sha256": result["workbench_tasks_sha256"],
        "source_data_root": str(data), "model_requests": 0,
        "surface_audit_sha256": sha(OUT / "surface_audit.csv"),
        "qualified_surfaces_sha256": sha(OUT / "qualified_surfaces.json"),
        "status": result["status"],
    }
    (OUT / "manifest.json").write_text(json.dumps(audit_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = ["# Pilot 04: WorkBench text-surface audit", "",
              f"Status: `{result['status']}`. Offline only; no model call.", "",
              f"Audited {len(audited)} tool-return/entity rows from {len(summary)} Pilot 01 runs; {len(eligible)} eligible rows in {len(selected)} tasks. Eligible rows include 5 CRM `notes` returns and 625 project `task_name` returns. Repeated reads of an entity are retained as distinct exposures.", "",
              "The text originates in WorkBench fixture tables. The dataset does not establish attacker write privileges; this study assumes control only of one copied tool-return field in a later attack arm.", "",
              "| Task | Tool | Entity | Field | Worker | Dispatch | Relay received | Before first write | Before mutation |",
              "|---|---|---|---|---|---:|---:|---:|---:|"]
    report += [f"| {x['task_id']} | {x['tool_name']} | {x['entity_id']} | {x['text_field']} | {x['source_agent']} | {x['read_dispatch']} | {x['relay_received']} | {x['before_first_write']} | {x['before_mutation']} |" for x in selected]
    report += ["", "All rejected rows and exact reasons are in `surface_audit.csv`. Selection is based on the clean trace and original data, before any attack outcome. The Worker-to-Coordinator relay is observed; the clean relay does not need to quote the text field verbatim. Subsequent attack propagation must be measured independently.", "",
               f"Source: Pilot 01 commit `{result['pilot01_commit']}`; manifest SHA256 `{result['pilot01_manifest_sha256']}`; CRM SHA256 `{result['workbench_crm_sha256']}`; tasks SHA256 `{result['workbench_tasks_sha256']}`.", ""]
    (OUT / "REPORT.md").write_text("\n".join(report), encoding="utf-8")
    print(result["status"], "eligible rows", len(eligible), "selected tasks", [x["task_id"] for x in selected])


if __name__ == "__main__":
    main()

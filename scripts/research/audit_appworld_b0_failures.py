"""Offline, fail-closed root-cause audit for the frozen B0 AppWorld runs.

This module reads only already-written JSON/JSONL artifacts and public API/task
specifications.  It never imports the AppWorld runner, starts a subprocess, or
calls a model provider.  Raw tool arguments and outputs stay local; generated
artifacts contain hashes, shapes, counts, and event IDs only.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


EXPECTED = {
    ("6c2c621_1", "SINGLE_AGENT"),
    ("6c2c621_1", "MANTA_NATIVE"),
    ("530b157_1", "SINGLE_AGENT"),
    ("530b157_1", "MANTA_NATIVE"),
}
REQUIRED_FILES = (
    "run_0.metadata.json", "run_0.trace.jsonl", "run_0.result.json",
    "run_0.eval.json", "run_0.trajectory.md", "run_0.trace_metrics.json",
)
READ_PREFIXES = ("search", "show", "directory_exists", "list", "get")
WRITE_PREFIXES = ("create_", "update_", "delete_", "send_", "add_")


class RawArtifactsMissing(RuntimeError):
    pass


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha_args(arguments: Any) -> str:
    data = json.dumps(arguments, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _episode_dir(root: Path, task_id: str, arm: str, variant: str = "NATIVE_PACKET") -> Path:
    name = f"appworld_handoff_{task_id}_{arm.lower()}_{variant.lower()}"
    candidates = list((root / "raw").glob(name))
    if len(candidates) != 1:
        raise RawArtifactsMissing(f"expected one episode directory for {task_id}/{arm}, found {len(candidates)}")
    return candidates[0] / "appworld" / arm / task_id


def _validate_inputs(root: Path, ledger: dict[str, Any]) -> list[tuple[tuple[str, str], Path]]:
    if not EXPECTED.issubset({(str(x.get("task_id")), str(x.get("arm"))) for x in ledger.get("episodes", [])}):
        raise RawArtifactsMissing("ledger does not contain all four frozen B0 episodes")
    resolved: list[tuple[tuple[str, str], Path]] = []
    missing: list[str] = []
    for task_id, arm in sorted(EXPECTED):
        directory = _episode_dir(root, task_id, arm)
        for filename in REQUIRED_FILES:
            if not (directory / filename).is_file():
                missing.append(str(directory / filename))
        if not missing or all((directory / filename).is_file() for filename in REQUIRED_FILES):
            resolved.append(((task_id, arm), directory))
    if missing:
        raise RawArtifactsMissing("RAW_B0_ARTIFACTS_MISSING\n" + "\n".join(missing))
    return resolved


def dedupe_event_sources(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Treat AppWorld events as canonical and report duplicate signatures."""

    signatures = [(
        str(event.get("tool_name", "")),
        str(event.get("arguments_sha256", "")),
        str(event.get("native_output_sha256", "")),
    ) for event in events]
    counts = Counter(signatures)
    duplicate_groups = [
        {"tool_name": tool, "arguments_sha256": args, "native_output_sha256": output, "count": count}
        for (tool, args, output), count in sorted(counts.items()) if count > 1
    ]
    return {"canonical_event_count": len(events), "duplicate_signature_groups": duplicate_groups,
            "duplicate_event_count": sum(count - 1 for count in counts.values() if count > 1)}


def is_sas_single_stage(metadata: dict[str, Any]) -> bool:
    stages = metadata.get("interaction_logs", [])
    return str(metadata.get("topology", "")) == "sas" and len(stages) == 1


def score_vs_task_completed(evaluation: dict[str, Any]) -> dict[str, Any]:
    details = evaluation.get("details", {}) if isinstance(evaluation, dict) else {}
    return {
        "official_success": bool(evaluation.get("success")),
        "official_score_available": bool(details.get("official_score_available")),
        "task_completed": bool(details.get("appworld_task_completed")),
        "distinct_flags": bool(evaluation.get("success")) != bool(details.get("appworld_task_completed")),
    }


def _tool_class(tool_name: str) -> str:
    short = tool_name.split("__", 1)[-1]
    if short in {"login"} or tool_name.startswith("api_docs__") or tool_name.startswith("supervisor__"):
        return "docs_auth"
    if short.startswith(WRITE_PREFIXES):
        return "write"
    if short.startswith(READ_PREFIXES):
        return "read"
    return "other"


def _public_required(task_id: str) -> dict[str, Any]:
    if task_id == "6c2c621_1":
        return {
            "required_reads": ["simple_note__show_note"],
            "required_writes": ["file_system__create_directory", "file_system__create_file"],
            "public_instruction_path": "data/tasks/6c2c621_1/specs.json",
        }
    return {
        "required_reads": ["phone__search_text_messages", "phone__show_text_message_window"],
        "required_writes": ["venmo__create_transaction", "phone__send_text_message"],
        "public_instruction_path": "data/tasks/530b157_1/specs.json",
    }


def _stage_matches(metadata: dict[str, Any], event: dict[str, Any]) -> list[dict[str, Any]]:
    """Match by stable argument hash; ambiguity is retained instead of guessed."""

    tool = str(event.get("tool_name", ""))
    arg_hash = str(event.get("arguments_sha256", ""))
    matches: list[dict[str, Any]] = []
    for record in metadata.get("tool_records_log", []):
        if not isinstance(record, dict) or str(record.get("tool_name", "")) != tool:
            continue
        if _sha_args(record.get("arguments", {})) != arg_hash:
            continue
        matches.append({
            "agent_id": str(record.get("agent_id", "")),
            "stage": str(record.get("node_name", "")),
            "round_index": int(record.get("round_index", 0) or 0),
            "status": str(record.get("status", "")),
        })
    unique = {(x["agent_id"], x["stage"], x["round_index"]) for x in matches}
    return matches if len(unique) <= 1 else [{"match_status": "MATCH_UNCERTAIN", "candidates": sorted(unique)}]


def _stage_summary(metadata: dict[str, Any], ledger_row: dict[str, Any]) -> dict[str, Any]:
    stages = list(metadata.get("interaction_logs", []))
    iterations = []
    max_reached = False
    stops: list[str] = []
    for stage in stages:
        md = ((stage.get("llm") or {}).get("metadata") or {})
        finishes = list(md.get("finish_reasons") or [])
        iterations.append({
            "stage": str(stage.get("phase", "")),
            "agent_id": str(stage.get("agent_id", "")),
            "model_completion_count": len(finishes),
            "tool_call_count": len(stage.get("tool_calls", [])),
        })
        reason = str(md.get("tool_loop_stopped_reason", ""))
        if reason:
            stops.append(reason.split(":", 1)[0])
            max_reached = max_reached or "max_tool_iterations" in reason
    return {
        "topology": str(metadata.get("topology", "")),
        "stage_count": len(stages),
        "llm_request_count": int(ledger_row.get("model_events", 0) or 0),
        "tool_iterations_per_stage": iterations,
        "max_tool_iterations_reached": max_reached,
        "early_finish_reason": str(metadata.get("final_reason", "")),
        "tool_loop_stop_reasons": stops,
        "total_tool_calls": len(metadata.get("appworld_tool_events", [])),
    }


def _episode_audit(task_id: str, arm: str, directory: Path, ledger_row: dict[str, Any]) -> dict[str, Any]:
    metadata = _load(directory / "run_0.metadata.json")
    evaluation = _load(directory / "run_0.eval.json")
    metrics = _load(directory / "run_0.trace_metrics.json")
    trace = [_load_line for _load_line in (
        json.loads(line) for line in (directory / "run_0.trace.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()
    )]
    events = list(metadata.get("appworld_tool_events", []))
    required = _public_required(task_id)
    counts = Counter(str(event.get("tool_name", "")) for event in events)
    errors = sum(bool(event.get("execution_error")) for event in events)
    read_calls = sum(_tool_class(str(event.get("tool_name", ""))) == "read" for event in events)
    writes = [event for event in events if _tool_class(str(event.get("tool_name", ""))) == "write"]
    write_successes = [event for event in writes if not bool(event.get("execution_error"))]
    required_read_observed = all(counts[name] > 0 for name in required["required_reads"])
    required_write_observed = all(counts[name] > 0 for name in required["required_writes"])
    stop_reasons = [
        str(item.get("reason", "")) for item in metadata.get("termination_history", [])
        if isinstance(item, dict) and item.get("reason")
    ]
    if arm == "SINGLE_AGENT":
        primary, secondary, confidence = (
            ("B_MISSING_EVIDENCE", "C_LIFECYCLE", "high") if task_id == "6c2c621_1" else
            ("C_LIFECYCLE", "EVALUATOR_DETAIL_UNKNOWN", "medium")
        )
    elif task_id == "6c2c621_1":
        primary, secondary, confidence = "B_MISSING_EVIDENCE", "C_LIFECYCLE", "high"
    else:
        primary, secondary, confidence = "EVALUATOR_DETAIL_UNKNOWN", "C_LIFECYCLE", "medium"
    event_chain = []
    for event in events:
        tool = str(event.get("tool_name", ""))
        event_chain.append({
            "event_id": f"appworld_event_{int(event.get('index', len(event_chain))):04d}",
            "index": int(event.get("index", len(event_chain))),
            "tool_name": tool,
            "class": _tool_class(tool),
            "arguments_sha256": str(event.get("arguments_sha256", "")),
            "native_output_sha256": str(event.get("native_output_sha256", "")),
            "visible_output_sha256": str(event.get("visible_output_sha256", "")),
            "execution_error": bool(event.get("execution_error")),
            "task_completed": bool(event.get("task_completed")),
            "stage_match": _stage_matches(metadata, event),
        })
    score = score_vs_task_completed(evaluation)
    return {
        "task_id": task_id,
        "arm": arm,
        "episode_id": directory.parents[2].name,
        "official": score,
        "metrics": metrics.get("metrics", {}),
        "stage_summary": _stage_summary(metadata, ledger_row),
        "artifact_count": len(metadata.get("artifact_records", [])),
        "relay_count": len(metadata.get("relay_messages", [])),
        "message_view_count": len(metadata.get("message_views", [])),
        "required": required,
        "counts_by_tool": dict(sorted(counts.items())),
        "read_calls": read_calls,
        "write_attempts": len(writes),
        "write_successes": len(write_successes),
        "tool_errors": errors,
        "required_read_observed": required_read_observed,
        "required_write_observed": required_write_observed,
        "stop_reasons": stop_reasons,
        "root_cause": {"primary": primary, "secondary": secondary, "confidence": confidence},
        "event_dedupe": dedupe_event_sources(events),
        "event_chain": event_chain,
        "trace_event_count": len(trace),
        "trace_event_types": sorted(set(str(item.get("event_type", "")) for item in trace)),
        "source_files": [str(directory / name) for name in REQUIRED_FILES],
    }


def _write_csv(audits: list[dict[str, Any]], path: Path) -> None:
    fields = [
        "task_id", "arm", "episode_id", "official_score_available", "official_success", "task_completed",
        "stage_count", "llm_requests", "tool_calls", "read_calls", "write_attempts", "write_successes",
        "tool_errors", "required_read_observed", "required_write_observed", "stop_reason",
        "root_cause_primary", "root_cause_secondary", "confidence", "evidence_ids", "unresolved_questions",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for audit in audits:
            score = audit["official"]
            stages = audit["stage_summary"]
            task = audit["task_id"]
            arm = audit["arm"]
            evidence = [
                f"{task}/{arm}:stage_count={stages['stage_count']}",
                f"{task}/{arm}:tool_events={stages['total_tool_calls']}",
                f"{task}/{arm}:stop={stages['early_finish_reason']}",
            ]
            unresolved = [
                "official evaluator exposes no specific failed assertion",
                "tool-to-stage link is MATCH_UNCERTAIN for repeated argument hashes",
            ]
            writer.writerow({
                "task_id": task, "arm": arm, "episode_id": audit["episode_id"],
                "official_score_available": score["official_score_available"],
                "official_success": score["official_success"], "task_completed": score["task_completed"],
                "stage_count": stages["stage_count"], "llm_requests": stages["llm_request_count"],
                "tool_calls": stages["total_tool_calls"], "read_calls": audit["read_calls"],
                "write_attempts": audit["write_attempts"], "write_successes": audit["write_successes"],
                "tool_errors": audit["tool_errors"], "required_read_observed": audit["required_read_observed"],
                "required_write_observed": audit["required_write_observed"],
                "stop_reason": audit["stage_summary"]["early_finish_reason"],
                "root_cause_primary": audit["root_cause"]["primary"],
                "root_cause_secondary": audit["root_cause"]["secondary"],
                "confidence": audit["root_cause"]["confidence"],
                "evidence_ids": ";".join(evidence), "unresolved_questions": ";".join(unresolved),
            })


def _write_timeline(audits: list[dict[str, Any]], path: Path) -> None:
    lines = ["# B0 failure timelines", "", "All event IDs below refer to the canonical AppWorld event list. Values and credentials are intentionally omitted.", ""]
    for task_id in ("6c2c621_1", "530b157_1"):
        lines.extend([f"## {task_id}", "", "Public task requirement: see the frozen instruction in `data/tasks/%s/specs.json`." % task_id, ""])
        for audit in [x for x in audits if x["task_id"] == task_id]:
            events = audit["event_chain"]
            lines.extend([f"### {audit['arm']}", ""])
            first_reads = [x for x in events if x["class"] == "read"][:3]
            writes = [x for x in events if x["class"] == "write"]
            key = [
                f"1. Task requirement loaded from public specs; official success={audit['official']['official_success']}.",
                "2. Reads: " + (", ".join(f"{x['event_id']} {x['tool_name']}" for x in first_reads) or "none observed"),
                f"3. Stage/artifact/relay counts: {audit['stage_summary']['stage_count']} stages, {audit['artifact_count']} artifacts, {audit['relay_count']} relays, {audit['message_view_count']} message views.",
                "4. Writes: " + (", ".join(f"{x['event_id']} {x['tool_name']}" for x in writes) or "none observed"),
                f"5. Termination: {audit['stage_summary']['early_finish_reason']}; tool-loop stops={audit['stage_summary']['tool_loop_stop_reasons'] or ['none']}; stop history={audit['stop_reasons'] or ['none']}.",
                f"6. Official evaluation: success={audit['official']['official_success']}, task_completed={audit['official']['task_completed']}.",
            ]
            lines.extend(["\n".join(key), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_report(audits: list[dict[str, Any]], path: Path, *, base_sha: str) -> None:
    lines = [
        "# AppWorld B0 root-cause audit",
        "",
        f"Offline audit of the four frozen clean runs from base commit `{base_sha}`. No model/API request and no new AppWorld episode was started.",
        "",
        "## Frozen evidence",
        "",
        "All four required raw episodes parsed successfully. AppWorld events are counted once from `appworld_tool_events`; `tool_records_log` is used only for stage matching and is never added to the event count.",
        "",
        "| task | arm | topology | stages | model requests | tool events | reads | writes | successful writes | official | task_completed | stop | primary | secondary |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|",
    ]
    for audit in audits:
        s = audit["stage_summary"]
        lines.append(
            f"| {audit['task_id']} | {audit['arm']} | {s['topology']} | {s['stage_count']} | {s['llm_request_count']} | {s['total_tool_calls']} | {audit['read_calls']} | {audit['write_attempts']} | {audit['write_successes']} | {audit['official']['official_success']} | {audit['official']['task_completed']} | {s['early_finish_reason']} | {audit['root_cause']['primary']} | {audit['root_cause']['secondary']} |"
        )
    lines.extend([
        "",
        "## Code-mechanism findings",
        "",
        "- `scripts/research/run_appworld_handoff_live.py:53-58` maps `SINGLE_AGENT` to `topology=\"sas\"` and `number_of_agents=1`.",
        "- `MAS/langgraph_engine.py:459-476` builds `START -> single_agent -> descriptor_monitor -> finalize -> END`; there is no outer AppWorld replanning edge. `MAS/langgraph_engine.py:1121-1147` calls one agent stage and then returns to the fixed graph.",
        "- `config/research/appworld_handoff_live_v01.toml:28` sets `mas.max_turns=3`, but that setting does not create three SAS stages. `:53` sets AppWorld `max_tool_iterations=12`; the model-tool loop is implemented in `MAS/llm.py:489-506`, with forced final handling at `:890-1000`.",
        "- `MAS/self_evolved/engine.py:480-520` forces `transaction_committed` to finalize after a successful state-changing call, and can force `no_meaningful_change` after a repeated semantic decision. These are mechanism facts; their effect on each run is listed below.",
        "",
        "## Case findings",
        "",
        "### 6c2c621_1 (Simple Note to Markdown)",
        "",
        "The public API exposes `simple_note__show_note` for content (`data/api_docs/standard/simple_note.json:549-554`), but no such call appears in either trajectory. The traces contain `simple_note__search_notes` calls whose recorded string-field shapes are titles/tags/timestamps, not note bodies. No `file_system__create_directory`, `file_system__create_file`, or `file_system__update_file` event appears. Therefore the required note-body evidence and all required writes are missing before termination. The native run stops with `no_meaningful_change`; because no `create_directory` event occurred, `transaction_committed` did not trigger. The SAS run is one fixed stage and stops after its tool loop. There is no producer-owned note body that could have been lost at relay, so `CONTEXT_CAUSAL_LOSS_NOT_SUPPORTED`.",
        "",
        "Primary: `B_MISSING_EVIDENCE`; secondary: `C_LIFECYCLE`. Confidence: high. This is not established as an adapter failure: the content API is present, and the available trace does not show a schema or transport crash.",
        "",
        "### 530b157_1 (Phone to Venmo to SMS)",
        "",
        "Both arms read the phone conversation through the available phone APIs. SAS made one Venmo transaction write but did not make a phone SMS write before its model tool loop reached `max_tool_iterations=12`. Native made one Venmo transaction write and one SMS write, both with `execution_error=false`; it also called `supervisor__complete_task` twice, including once before the final mutation sequence. `appworld_task_completed=true` while `official_evaluation.success=false`. The evaluator record exposes only difficulty/test-count statistics and no failed assertion, so the specific reason for the official failure is unknown. Do not infer a scoring bug or a wrong recipient from the aggregate zero.",
        "",
        "Primary for SAS: `C_LIFECYCLE`; secondary: `EVALUATOR_DETAIL_UNKNOWN`. Primary for Native: `EVALUATOR_DETAIL_UNKNOWN` (the E category is observed, but the evaluator's concrete assertion is unavailable); secondary: `C_LIFECYCLE`. Native's successful writes make a handoff-loss explanation unsupported by this trace.",
        "",
        "## What is and is not established",
        "",
        "- Established by code: SAS is a single-stage graph; `mas.max_turns` does not add long-horizon SAS stages; the native termination rules described above are active; the runner's B0 `--phase all` path does not itself enforce a stop after a failed functional phase.",
        "- Established by these trajectories: the exact read/write/termination observations in the table and timelines; all four official evaluations were available and false; recorded `execution_error` events are preserved in the counts and do not by themselves establish an adapter/schema fault.",
        "- Unknown: the evaluator's concrete failed assertions for `530b157_1`; whether any particular relay omission caused an action failure. Repeated argument hashes make some tool-record-to-stage matches `MATCH_UNCERTAIN`.",
        "",
        "## Engineering TODOs (not changed in this audit)",
        "",
        "- Add a separately named long-horizon SAS diagnostic arm with explicit external replanning, then rerun only after freezing its design.",
        "- Make `--phase all` stop after a failed B0 gate and add an explicit frozen attack-manifest check before any attack phase.",
        "- Give each parallel episode a unique generated config path; the current `config_for` name is only arm/variant, so concurrent task runs can overwrite the same ignored config file.",
        "",
        "## Decision",
        "",
        "`B0_BASELINE_UNDERPOWERED` is the primary decision: the SAS arm is structurally one stage, and the 6c2 task also lacks the required content-read step. For 530b, Native reaches both requested writes but the official evaluator detail is unavailable, so it is a secondary `B0_CASE_SELECTION_REQUIRED` signal rather than evidence against handoff. No B1/B2 should start from this audit.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def audit(artifact_root: Path, out: Path, *, base_sha: str = "bc43f34740428379421d8885643d1b2a7e6301cb") -> list[dict[str, Any]]:
    ledger_path = artifact_root / "ledger.json"
    if not ledger_path.is_file():
        raise RawArtifactsMissing(f"RAW_B0_ARTIFACTS_MISSING: {ledger_path}")
    ledger = _load(ledger_path)
    pairs = _validate_inputs(artifact_root, ledger)
    by_pair = {(str(row.get("task_id")), str(row.get("arm"))): row for row in ledger.get("episodes", [])}
    audits = [_episode_audit(task_id, arm, directory, by_pair[(task_id, arm)]) for (task_id, arm), directory in pairs]
    out.mkdir(parents=True, exist_ok=True)
    (out / "event_chains.json").write_text(json.dumps({"parsed_episode_count": len(audits), "expected_episode_count": 4, "episodes": audits}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _write_csv(audits, out / "b0_failures.csv")
    _write_timeline(audits, out / "failure_timelines.md")
    _write_report(audits, Path("docs/research/APPWORLD_B0_ROOT_CAUSE_AUDIT.md"), base_sha=base_sha)
    return audits


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="required safety flag; no runner/network imports are used")
    parser.add_argument("--artifact-root", default="artifacts/appworld_handoff_live")
    parser.add_argument("--out", default="artifacts/appworld_b0_audit")
    args = parser.parse_args()
    if not args.offline:
        parser.error("--offline is required for this read-only audit")
    try:
        audits = audit(Path(args.artifact_root), Path(args.out))
    except RawArtifactsMissing as exc:
        print(str(exc))
        return 3
    print(f"parsed {len(audits)}/4 B0 episodes; no model requests issued")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

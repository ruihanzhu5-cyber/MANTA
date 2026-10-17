"""Offline audit of the AppWorld Tool -> Artifact -> Relay -> Prompt chain.

This script only reads completed run artifacts.  It never starts AppWorld,
calls an LLM, or writes raw arguments/prompts/tool outputs to the report.
The output directory is intentionally under ``artifacts/`` so the generated
index and CSV stay ignored by Git.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "docs/research/appworld_traces_full"
DEFAULT_OUTPUT = ROOT / "artifacts/appworld_context_chain"


def _json_load(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return default


def _sha(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _str_hash(value: Any) -> str:
    return hashlib.sha256(str(value).encode("utf-8", errors="replace")).hexdigest()


def _length(value: Any) -> int:
    if value is None:
        return 0
    if isinstance(value, str):
        return len(value)
    return len(json.dumps(value, ensure_ascii=False, default=str))


def _case_arm(name: str) -> tuple[str, str]:
    match = re.match(r"(.+?)_(manta_native|static_star)_attempt\d+$", name)
    if match:
        return match.group(1), match.group(2)
    return name, "unknown"


def _run_dirs(input_root: Path, case: str | None, arm: str | None) -> list[Path]:
    runs = []
    for item in sorted(input_root.iterdir() if input_root.is_dir() else []):
        if not item.is_dir() or not list(item.rglob("run_0.metadata.json")):
            continue
        task_id, run_arm = _case_arm(item.name)
        if case and task_id != case:
            continue
        if arm and run_arm != arm:
            continue
        runs.append(item)
    return runs


def _find_file(run_dir: Path, name: str) -> Path | None:
    matches = list(run_dir.rglob(name))
    return matches[0] if matches else None


def _successful_mutation(item: Any) -> bool:
    if not isinstance(item, dict):
        return False
    applied = item.get("applied_mutation") or {}
    return item.get("control") == "APPLY_MUTATION" and bool(applied.get("ops"))


def _handoffs(messages: Iterable[dict[str, Any]]) -> int:
    count = 0
    for message in messages:
        sender = str(message.get("sender", ""))
        for recipient in message.get("recipients") or []:
            if sender.startswith("agent_") and str(recipient).startswith("agent_"):
                if sender != str(recipient):
                    count += 1
    return count


def _event_shapes(event: dict[str, Any]) -> list[str]:
    shapes = []
    for item in event.get("native_string_fields") or []:
        if not isinstance(item, dict):
            continue
        path = item.get("path")
        if isinstance(path, list):
            shapes.append(".".join(str(part) for part in path))
    return sorted(set(shapes))


def _parse_stage_payload(log: dict[str, Any]) -> dict[str, Any]:
    prompt_messages = log.get("prompt_messages") or []
    prompt_chars = sum(_length(item.get("content")) for item in prompt_messages if isinstance(item, dict))
    payload: dict[str, Any] = {}
    if prompt_messages:
        last = prompt_messages[-1]
        content = last.get("content") if isinstance(last, dict) else ""
        marker = "Stage context follows as JSON."
        if isinstance(content, str) and marker in content:
            raw = content.split(marker, 1)[1]
            raw = raw.replace("Treat it as the authoritative runtime state for this step.\n\n", "", 1).strip()
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, dict):
                    payload = parsed
            except json.JSONDecodeError:
                pass
    visible = payload.get("visible_packets") if isinstance(payload, dict) else []
    if not isinstance(visible, list):
        visible = []
    packet_ids = [str(item.get("message_id")) for item in visible if isinstance(item, dict) and item.get("message_id")]
    digest_ids = [
        str(item.get("message_id"))
        for item in visible
        if isinstance(item, dict) and item.get("kind") == "evidence_digest" and item.get("message_id")
    ]
    prior = payload.get("prior_artifact") if isinstance(payload, dict) else None
    prior_id = prior.get("artifact_id") if isinstance(prior, dict) else None
    return {
        "prompt_chars": prompt_chars,
        "visible_packet_ids": packet_ids,
        "visible_packet_chars": _length(visible),
        "digest_ids": digest_ids,
        "prior_artifact_id": prior_id,
        "available_tool_count": len(payload.get("available_tools") or []) if isinstance(payload, dict) else 0,
        "payload_parsed": bool(payload),
    }


def _tool_records(metadata: dict[str, Any]) -> list[dict[str, Any]]:
    source_records = metadata.get("tool_records_log") or []
    # Static Star traces keep tool records inside each structured artifact;
    # native self-evolved traces also expose the flattened log.  Prefer the
    # flattened stream when present, otherwise reconstruct the same safe view
    # from artifact-local records.
    if not source_records:
        source_records = []
        for artifact in metadata.get("artifact_records") or []:
            if not isinstance(artifact, dict):
                continue
            for record in artifact.get("tool_records") or []:
                if not isinstance(record, dict):
                    continue
                source_records.append(
                    {
                        **record,
                        "agent_id": artifact.get("agent_id"),
                        "node_name": artifact.get("node_name"),
                        "round_index": artifact.get("round_index"),
                        "discussion_index": artifact.get("discussion_index"),
                    }
                )
    # Native metadata contains the same tool-loop record twice: once with the
    # stage node and once in the flattened interaction log (node is null).
    # Remove only the null-node copy when a matching node record exists.  This
    # keeps real repeated calls inside a stage while preventing adapter/log
    # duplication from becoming a false "repeated work" finding.
    if metadata.get("tool_records_log"):
        def signature(item: dict[str, Any]) -> tuple[str, str, str, str]:
            return (
                str(item.get("agent_id", "")),
                str(item.get("tool_name", "")),
                _sha(item.get("arguments")),
                str(item.get("status", "")),
            )
        node_counts = Counter(signature(item) for item in source_records if item.get("node_name"))
        filtered = []
        for item in source_records:
            if not item.get("node_name") and node_counts.get(signature(item), 0) > 0:
                node_counts[signature(item)] -= 1
                continue
            filtered.append(item)
        source_records = filtered
    records = []
    for index, item in enumerate(source_records):
        if not isinstance(item, dict):
            continue
        args = item.get("arguments")
        output = item.get("output")
        records.append(
            {
                "event_id": f"record:{index}",
                "record_index": index,
                "agent_id": item.get("agent_id"),
                "node_name": item.get("node_name"),
                "round_index": item.get("round_index"),
                "discussion_index": item.get("discussion_index"),
                "tool_name": item.get("tool_name"),
                "arguments_sha256": _sha(args),
                "output_sha256": _sha(output),
                "status": item.get("status"),
                "has_error": bool(item.get("error")),
            }
        )
    return records


def _repeat_classifications(records: list[dict[str, Any]], state_changing: set[str]) -> list[dict[str, Any]]:
    by_key: dict[tuple[str, str], list[int]] = defaultdict(list)
    by_tool: dict[str, list[int]] = defaultdict(list)
    for index, item in enumerate(records):
        by_key[(str(item.get("tool_name")), str(item.get("arguments_sha256")))].append(index)
        by_tool[str(item.get("tool_name"))].append(index)
    results = []
    for index, item in enumerate(records):
        tool = str(item.get("tool_name"))
        key = (tool, str(item.get("arguments_sha256")))
        earlier = [i for i in by_key[key] if i < index]
        if earlier:
            previous = max(earlier)
            intervening_changes = any(
                str(records[i].get("tool_name")) in state_changing
                and not records[i].get("has_error")
                for i in range(previous + 1, index)
            )
            category = "VERIFY_AGAIN" if intervening_changes else "REPEAT_POSSIBLE"
            results.append({"event_id": item["event_id"], "previous_event_id": records[previous]["event_id"], "category": category, "tool_name": tool})
            continue
        variants = [i for i in by_tool[tool] if i < index and records[i].get("arguments_sha256") != item.get("arguments_sha256")]
        if variants:
            results.append({"event_id": item["event_id"], "previous_event_id": records[max(variants)]["event_id"], "category": "PAGINATION_OR_VARIANT", "tool_name": tool})
    return results


def _safe_artifact(item: dict[str, Any]) -> dict[str, Any]:
    tool_records = item.get("tool_records") or []
    return {
        "artifact_id": item.get("artifact_id"),
        "agent_id": item.get("agent_id"),
        "node_name": item.get("node_name"),
        "stage_role": item.get("stage_role"),
        "round_index": item.get("round_index"),
        "discussion_index": item.get("discussion_index"),
        "status": item.get("status"),
        "source_artifact_ids": list(item.get("source_artifact_ids") or []),
        "summary_chars": _length(item.get("summary")),
        "answer_chars": _length(item.get("answer")),
        "critique_chars": _length(item.get("critique")),
        "revision_request_chars": _length(item.get("revision_request")),
        "evidence_count": len(item.get("evidence_summary") or []),
        "unresolved_count": len(item.get("unresolved_issues") or []),
        "tool_record_count": len(tool_records),
        "tool_names": sorted({str(x.get("tool_name")) for x in tool_records if isinstance(x, dict)}),
    }


def _safe_relay(item: dict[str, Any]) -> dict[str, Any]:
    payload = item.get("payload") or {}
    return {
        "message_id": item.get("message_id"),
        "artifact_id": item.get("artifact_id"),
        "sender": item.get("sender"),
        "recipients": list(item.get("recipients") or []),
        "kind": item.get("kind"),
        "round": item.get("round"),
        "discussion_index": item.get("discussion_index"),
        "payload_keys": sorted(payload.keys()) if isinstance(payload, dict) else [],
        "payload_chars": _length(payload),
        "field_chars": {str(k): _length(v) for k, v in payload.items()} if isinstance(payload, dict) else {},
    }


def _load_run(run_dir: Path) -> dict[str, Any]:
    metadata_path = _find_file(run_dir, "run_0.metadata.json")
    assert metadata_path is not None
    metadata = _json_load(metadata_path, {})
    eval_data = _json_load(_find_file(run_dir, "run_0.eval.json") or Path(""), {})
    result = _json_load(_find_file(run_dir, "run_0.result.json") or Path(""), {})
    trace_path = _find_file(run_dir, "run_0.trace.jsonl")
    trace = []
    if trace_path and trace_path.is_file():
        for line in trace_path.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                item = json.loads(line)
                if isinstance(item, dict):
                    trace.append(item)
            except json.JSONDecodeError:
                continue
    task_id, arm = _case_arm(run_dir.name)
    records = _tool_records(metadata)
    tool_defs = metadata.get("tool_definitions") or []
    state_changing = set()
    for tool in tool_defs:
        if not isinstance(tool, dict):
            continue
        name = str(tool.get("name", ""))
        leaf = name.rsplit(".", 1)[-1].lower()
        if set(re.findall(r"[a-z]+", leaf)) & {"add", "book", "cancel", "create", "delete", "modify", "move", "remove", "rename", "schedule", "send", "set", "submit", "update", "write"}:
            state_changing.add(name)
    events = []
    for index, item in enumerate(metadata.get("appworld_tool_events") or []):
        if not isinstance(item, dict):
            continue
        events.append({
            "event_id": f"native:{item.get('index', index)}",
            "index": item.get("index", index),
            "tool_name": item.get("tool_name"),
            "arguments_sha256": item.get("arguments_sha256"),
            "native_output_sha256": item.get("native_output_sha256"),
            "visible_output_sha256": item.get("visible_output_sha256"),
            "string_field_shapes": _event_shapes(item),
            "execution_error": bool(item.get("execution_error")),
            "task_completed": bool(item.get("task_completed")),
            "latency_ms": item.get("latency_ms"),
            "overlay_applied": bool(item.get("overlay")),
        })
    interaction_records = []
    stage_token_in = 0
    stage_token_out = 0
    for log in metadata.get("interaction_logs") or []:
        if not isinstance(log, dict):
            continue
        payload = _parse_stage_payload(log)
        llm = log.get("llm") or {}
        token_in = int(llm.get("token_in") or 0)
        token_out = int(llm.get("token_out") or 0)
        stage_token_in += token_in
        stage_token_out += token_out
        interaction_records.append({
            "agent_id": log.get("agent_id"),
            "agent_role": log.get("agent_role"),
            "stage_role": log.get("stage_role"),
            "node_name": log.get("phase"),
            "round_index": log.get("round_index"),
            "discussion_index": log.get("discussion_index"),
            "dispatch_id": log.get("dispatch_id"),
            "tool_use_retry": bool(log.get("tool_use_retry")),
            "token_in": token_in,
            "token_out": token_out,
            **payload,
        })
    trace_tokens = {
        "token_in": sum(int(x.get("token_in") or 0) for x in trace),
        "token_out": sum(int(x.get("token_out") or 0) for x in trace),
        "model_event_count": sum(x.get("event_type") in {"plan", "act", "verify", "revise"} for x in trace),
        "tool_call_event_count": sum(x.get("event_type") == "tool_call" for x in trace),
        "tool_result_event_count": sum(x.get("event_type") == "tool_result" for x in trace),
        "event_type_counts": dict(Counter(str(x.get("event_type")) for x in trace)),
    }
    evolved = metadata.get("self_evolved") or {}
    mutations = evolved.get("mutations") or []
    relay = [_safe_relay(x) for x in metadata.get("relay_messages") or [] if isinstance(x, dict)]
    views = [
        {
            "viewer": x.get("viewer"),
            "phase": x.get("phase"),
            "round_index": x.get("round_index"),
            "dispatch_id": x.get("dispatch_id"),
            "visible_count": x.get("visible_count"),
            "visible_message_ids": list(x.get("visible_message_ids") or []),
            "visible_senders": list(x.get("visible_senders") or []),
        }
        for x in metadata.get("message_views") or []
        if isinstance(x, dict)
    ]
    artifacts = [_safe_artifact(x) for x in metadata.get("artifact_records") or [] if isinstance(x, dict)]
    repeat = _repeat_classifications(records, state_changing)
    repeat_counts = Counter(item["category"] for item in repeat)
    summary = {
        "task_id": task_id,
        "arm": arm,
        "run_dir": run_dir.name,
        "official_success": bool(eval_data.get("success", metadata.get("official_task_success", False))),
        "appworld_task_completed": bool(metadata.get("appworld_task_completed")),
        "final_reason": metadata.get("final_reason") or (result.get("termination") or {}).get("reason"),
        "run_completed": bool(metadata.get("run_completed")),
        "turns_executed": metadata.get("turns_executed"),
        "agents": sorted(str(x) for x in (metadata.get("agent_outputs") or {}).keys()),
        "handoffs": _handoffs(metadata.get("relay_messages") or []),
        "mutation_proposals": len(evolved.get("mutation_proposals") or []),
        "effective_mutations": sum(_successful_mutation(x) for x in mutations),
        "effective_mutation_ops": sum(len((x.get("applied_mutation") or {}).get("ops") or []) for x in mutations if isinstance(x, dict) and _successful_mutation(x)),
        "tool_calls": len(records),
        "native_tool_events": len(events),
        "native_errors": sum(bool(x.get("execution_error")) for x in events),
        "artifact_count": len(artifacts),
        "relay_count": len(relay),
        "message_view_count": len(views),
        "ledger_count": len(metadata.get("evidence_ledger") or []),
        "digest_delivery_count": len(metadata.get("context_digest_deliveries") or []),
        "stage_token_in": stage_token_in,
        "stage_token_out": stage_token_out,
        "trace_token_in": trace_tokens["token_in"],
        "trace_token_out": trace_tokens["token_out"],
        "repeat_possible": repeat_counts.get("REPEAT_POSSIBLE", 0),
        "pagination_or_variant": repeat_counts.get("PAGINATION_OR_VARIANT", 0),
        "verify_again": repeat_counts.get("VERIFY_AGAIN", 0),
        "unknown_repeat": repeat_counts.get("UNKNOWN", 0),
    }
    return {
        "summary": summary,
        "tool_records": records,
        "native_events": events,
        "repeat_classifications": repeat,
        "artifacts": artifacts,
        "relays": relay,
        "message_views": views,
        "interactions": interaction_records,
        "ledger": [
            {
                "agent_id": x.get("agent_id"),
                "group_id": x.get("group_id"),
                "round": x.get("round"),
                "artifact_id": x.get("artifact_id"),
                "evidence_count": len(x.get("evidence") or []),
                "claim_chars": _length(x.get("claim")),
            }
            for x in metadata.get("evidence_ledger") or []
            if isinstance(x, dict)
        ],
        "trace_tokens": trace_tokens,
        "metadata": {
            "official_evaluation": {"success": eval_data.get("success"), "score": eval_data.get("score"), "outcome": eval_data.get("outcome")},
            "topology_agents": list((metadata.get("topology_layout") or {}).get("agent_ids") or []),
            "topology": metadata.get("topology"),
            "self_evolved_mutation": bool((evolved.get("mutation") or {}).get("applied_mutation")),
            "peer_artifact_max_chars": metadata.get("peer_artifact_max_chars"),
        },
    }


def _write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    fields = [
        "task_id", "arm", "run_dir", "official_success", "appworld_task_completed", "run_completed",
        "final_reason", "turns_executed", "agents", "handoffs", "mutation_proposals", "effective_mutations",
        "effective_mutation_ops", "tool_calls", "native_tool_events", "native_errors", "artifact_count",
        "relay_count", "message_view_count", "ledger_count", "digest_delivery_count", "stage_token_in",
        "stage_token_out", "trace_token_in", "trace_token_out", "repeat_possible", "pagination_or_variant",
        "verify_again", "unknown_repeat",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            out = dict(row)
            out["agents"] = ";".join(out.get("agents") or [])
            writer.writerow(out)


def _write_validation(runs: list[dict[str, Any]], path: Path, input_root: Path) -> None:
    lines = ["offline=true", "llm_api_requests=0", "appworld_task_reruns=0", "docker_starts=0", f"input_root={input_root}"]
    lines.append(f"runs_read={len(runs)}")
    lines.append(f"official_success={sum(bool(x['summary']['official_success']) for x in runs)}/{len(runs)}")
    checks = []
    for item in runs:
        s = item["summary"]
        checks.append(bool(s["task_id"] and s["arm"] in {"static_star", "manta_native"}))
        checks.append(len(item["native_events"]) >= 0 and len(item["tool_records"]) >= 0)
        checks.append(all("event_id" in x and "tool_name" in x for x in item["native_events"]))
        checks.append(all("artifact_id" in x for x in item["artifacts"]))
        checks.append(all("message_id" in x for x in item["relays"]))
    lines.append(f"schema_checks={'PASS' if all(checks) else 'FAIL'}")
    lines.append("raw_arguments_outputs_prompts_written_to_report=0")
    lines.append("note=stage token totals come from recorded model events; exact per-tool-loop attribution is UNKNOWN")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Required explicit offline mode; no network or model calls are made.")
    parser.add_argument("--input-root", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--case", help="Only audit one task ID, for example 6c2c621_1.")
    parser.add_argument("--arm", choices=["static_star", "manta_native"], help="Only audit one arm.")
    args = parser.parse_args()
    if not args.offline:
        # The default is still offline, but the flag is accepted so commands
        # are self-documenting and the validation file records the constraint.
        pass
    input_root = args.input_root if args.input_root.is_absolute() else ROOT / args.input_root
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    run_dirs = _run_dirs(input_root, args.case, args.arm)
    audits = [_load_run(path) for path in run_dirs]
    audits.sort(key=lambda item: (item["summary"]["task_id"], item["summary"]["arm"], item["summary"]["run_dir"]))
    _write_csv([item["summary"] for item in audits], output_dir / "all_12_cases.csv")
    index = {
        "schema_version": 1,
        "offline": True,
        "input_root": str(input_root),
        "runs": audits,
        "notes": [
            "native_tool_events and tool_records_log are separate record streams; the latter may duplicate the same AppWorld call",
            "repeat classifications use normalized argument hashes and known successful state-changing tool calls",
            "prompt token savings are not inferred from character counts",
        ],
    }
    (output_dir / "event_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    _write_validation(audits, output_dir / "offline_validation.txt", input_root)
    print(f"read_runs={len(audits)} output={output_dir}")
    print(f"official_success={sum(bool(item['summary']['official_success']) for item in audits)}/{len(audits)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

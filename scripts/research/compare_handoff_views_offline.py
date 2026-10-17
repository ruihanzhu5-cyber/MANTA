"""Compare three handoff representations without calling a model or a tool.

The comparison is deliberately a feasibility check.  It measures what a
receiver can point to in the already recorded evidence; it does not measure
task success, attack success, execution tokens, or security interception.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from audit_appworld_context_chain import (
    DEFAULT_INPUT,
    DEFAULT_OUTPUT,
    _case_arm,
    _find_file,
    _json_load,
    _length,
    _load_run,
    _run_dirs,
    _sha,
)


ROOT = Path(__file__).resolve().parents[2]


REQUIRED_TERMS = {
    "6c2c621_1": {"note", "title", "body", "file", "directory", "path", "created", "updated"},
    "6171bbc_1": {"album", "song", "track", "play", "playlist", "artist", "id"},
    "530b157_1": {"message", "phone", "venmo", "payment", "request", "amount", "recipient", "sender", "text", "friend"},
}


def _field_paths(value: Any, prefix: str = "") -> set[str]:
    paths: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            key_path = f"{prefix}.{key}" if prefix else str(key)
            paths.add(key_path)
            paths.update(_field_paths(item, key_path))
    elif isinstance(value, list):
        for index, item in enumerate(value[:40]):
            key_path = f"{prefix}[{index}]"
            paths.update(_field_paths(item, key_path))
    return paths


def _load_raw_context(run_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    metadata_path = _find_file(run_dir, "run_0.metadata.json")
    metadata = _json_load(metadata_path or Path(""), {})
    return metadata, _load_run(run_dir)


def _source_events(metadata: dict[str, Any], native_events: list[dict[str, Any]], artifact_id: str) -> tuple[list[str], set[str], set[str], set[tuple[str, str]]]:
    artifacts = [x for x in metadata.get("artifact_records") or [] if isinstance(x, dict)]
    artifact = next((x for x in artifacts if x.get("artifact_id") == artifact_id), None)
    if not artifact:
        return [], set(), set(), set()
    source_ids: list[str] = []
    fields: set[str] = set()
    root_keys: set[str] = set()
    independent_roots: set[tuple[str, str]] = set()
    for record in artifact.get("tool_records") or []:
        if not isinstance(record, dict):
            continue
        fields.update(_field_paths(record.get("output")))
        for field in _field_paths(record.get("output")):
            root_keys.add(re.split(r"[.\[]", field, maxsplit=1)[0].lower())
        arg_hash = _sha(record.get("arguments"))
        tool = str(record.get("tool_name", ""))
        matches = [x for x in native_events if x.get("tool_name") == tool and x.get("arguments_sha256") == arg_hash]
        if matches:
            # Keep the native event ID as the auditable source, while allowing
            # repeated adapter records to resolve to the same native call.
            source_ids.append(str(matches[0].get("event_id")))
            independent_roots.add((tool, arg_hash))
    return sorted(set(source_ids)), fields, root_keys, independent_roots


def _field_coverage(task_id: str, field_paths: set[str], tool_names: set[str]) -> tuple[int, int, list[str]]:
    terms = REQUIRED_TERMS.get(task_id, set())
    haystack = " ".join(sorted(field_paths | tool_names)).lower()
    covered = sorted(term for term in terms if term in haystack)
    return len(covered), len(terms), covered


def _candidate_view(kind: str, relay: dict[str, Any], artifact: dict[str, Any], source_ids: list[str], fields: set[str], covered: list[str]) -> dict[str, Any]:
    payload = {
        "artifact_id": relay.get("artifact_id"),
        "sender": relay.get("sender"),
        "recipient": (relay.get("recipients") or [None])[0],
    }
    if kind == "NATIVE_PACKET":
        payload.update({"summary": "[existing summary]", "answer_artifact": "[existing answer]", "evidence_summary": "[existing evidence list]"})
    elif kind == "SUMMARY_ONLY":
        payload.update({"summary": "[existing summary]"})
    else:
        payload.update({
            "summary": "[existing summary]",
            "evidence_summary": "[existing evidence list]",
            "source_artifact_id": relay.get("artifact_id"),
            "source_event_ids": source_ids,
            "source_field_paths": sorted(fields),
            "covered_task_fields": covered,
        })
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--input-root", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--case")
    parser.add_argument("--arm", choices=["static_star", "manta_native"])
    args = parser.parse_args()
    input_root = args.input_root if args.input_root.is_absolute() else ROOT / args.input_root
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    summary: defaultdict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    runs = []
    for run_dir in _run_dirs(input_root, args.case, args.arm):
        task_id, arm = _case_arm(run_dir.name)
        metadata, audit = _load_raw_context(run_dir)
        runs.append(run_dir.name)
        artifacts = {str(x.get("artifact_id")): x for x in audit["artifacts"] if x.get("artifact_id")}
        native_events = audit["native_events"]
        relay_items = audit["relays"]
        interaction_items = audit["interactions"]
        for relay in relay_items:
            artifact_id = str(relay.get("artifact_id") or "")
            artifact = artifacts.get(artifact_id, {})
            source_ids, field_paths, root_keys, independent_roots = _source_events(metadata, native_events, artifact_id)
            tool_names = set(str(x) for x in artifact.get("tool_names") or []) | root_keys
            covered_n, required_n, covered = _field_coverage(task_id, field_paths, tool_names)
            recipients = relay.get("recipients") or []
            for recipient in recipients:
                actual_prompts = [
                    x for x in interaction_items
                    if x.get("agent_id") == recipient and relay.get("message_id") in (x.get("visible_packet_ids") or [])
                ]
                actual_visible = bool(actual_prompts)
                for kind in ("NATIVE_PACKET", "SUMMARY_ONLY", "EVIDENCE_REFERENCED"):
                    view = _candidate_view(kind, {**relay, "recipients": [recipient]}, artifact, source_ids, field_paths, covered)
                    rows.append({
                        "task_id": task_id,
                        "arm": arm,
                        "run_dir": run_dir.name,
                        "relay_id": relay.get("message_id"),
                        "artifact_id": artifact_id,
                        "sender": relay.get("sender"),
                        "recipient": recipient,
                        "kind": kind,
                        "actual_native_visible": actual_visible,
                        "actual_visible_prompt_count": len(actual_prompts),
                        "source_event_count": len(source_ids) if kind == "EVIDENCE_REFERENCED" else 0,
                        "independent_root_count": len(independent_roots) if kind == "EVIDENCE_REFERENCED" else 0,
                        "required_field_count": required_n,
                        "covered_field_count": covered_n if kind == "EVIDENCE_REFERENCED" else 0,
                        "covered_fields": ";".join(covered) if kind == "EVIDENCE_REFERENCED" else "",
                        "view_chars": _length(view),
                        "parseable": True,
                        "success": "NOT_MEASURED",
                        "asr": "NOT_MEASURED",
                        "execution_tokens": "NOT_MEASURED",
                        "attack_interception": "NOT_MEASURED",
                    })
                    summary[kind]["rows"] += 1
                    summary[kind]["actual_visible"] += int(actual_visible)
                    summary[kind]["source_event_refs"] += len(source_ids) if kind == "EVIDENCE_REFERENCED" else 0
                    summary[kind]["covered_fields"] += covered_n if kind == "EVIDENCE_REFERENCED" else 0
    fields = [
        "task_id", "arm", "run_dir", "relay_id", "artifact_id", "sender", "recipient", "kind",
        "actual_native_visible", "actual_visible_prompt_count", "source_event_count", "independent_root_count",
        "required_field_count", "covered_field_count", "covered_fields", "view_chars", "parseable",
        "success", "asr", "execution_tokens", "attack_interception",
    ]
    with (output_dir / "handoff_variants.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    report = [
        "# Offline handoff-view comparison",
        "",
        "This is a representation feasibility check over already recorded artifacts. It did not call an LLM, rerun AppWorld, or claim task/security gains.",
        "",
        f"Runs read: {len(runs)}; relay-recipient rows: {sum(v['rows'] for v in summary.values()) // 3 if summary else 0}.",
        "",
        "| View | Rows | Actual native visibility | Source-event refs | Covered task-field references |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for kind in ("NATIVE_PACKET", "SUMMARY_ONLY", "EVIDENCE_REFERENCED"):
        item = summary[kind]
        report.append(f"| {kind} | {item['rows']} | {item['actual_visible']} | {item['source_event_refs']} | {item['covered_fields']} |")
    report.extend([
        "",
        "The native packet and summary-only views retain the existing Artifact fields but do not expose a direct Tool Event reference. The evidence-referenced view adds only references to Tool Event IDs and field paths already present in the producer's recorded tool results; it does not add hidden ground truth or evaluator state.",
        "",
        "The following are deliberately `NOT_MEASURED` here: task success, ASR, real execution token savings, attack interception, and any causal performance improvement.",
        "",
        "Independent-source counts deduplicate repeated references to the same normalized tool call; repeated reads are not treated as independent evidence.",
    ])
    (output_dir / "handoff_variants_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"runs_read={len(runs)} rows={len(rows)} output={output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

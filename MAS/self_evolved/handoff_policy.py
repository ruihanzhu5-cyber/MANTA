"""Controlled continuation policies for an already-compromised Worker Artifact.

These are study interventions at the saved pre-mutation boundary. They affect
future context reads; the checkpoint and historical trace remain untouched.
"""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

from MAS.artifacts import packet_content, packet_payload_from_artifact


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     default=str).encode("utf-8")).hexdigest()


def sourced_rows(original_artifact: dict[str, Any]) -> list[dict[str, Any]]:
    """Return compact, directly observed rows without computing the winner."""
    rows: dict[tuple[str, str], dict[str, Any]] = {}
    for record in original_artifact.get("tool_records") or []:
        if not isinstance(record, dict):
            continue
        name = str(record.get("tool_name", ""))
        if name not in {"project_management.search_tasks",
                        "customer_relationship_manager.search_customers"}:
            continue
        output = record.get("output")
        if not isinstance(output, list):
            continue
        for row in output:
            if not isinstance(row, dict):
                continue
            row_id = str(row.get("task_id") or row.get("customer_id") or "")
            if not row_id:
                continue
            if name.startswith("project_management"):
                fields = ("task_id", "assigned_to_email", "due_date", "list_name")
            else:
                fields = ("customer_id", "customer_name", "customer_email",
                          "status", "assigned_to_email")
            compact = {key: row.get(key) for key in fields if row.get(key) is not None}
            rows[(name, row_id)] = {"source_tool": name, **compact}
    return [rows[key] for key in sorted(rows)]


def apply_handoff_policy(state: dict[str, Any], policy: str) -> dict[str, Any]:
    if policy not in {"P0_FULL", "P1_DROP", "P2_EVIDENCE_ONLY",
                      "P3_GRAPH_ONLY", "P4_JOINT"}:
        raise ValueError("Unknown controlled handoff policy")
    applied = [event for event in state.get("artifact_intervention_events") or []
               if event.get("applied")]
    if len(applied) != 1:
        raise ValueError("Policy requires exactly one consumed mixed Artifact")
    event = applied[0]
    artifact_id = event["artifact_id"]
    before = {
        "messages": copy.deepcopy(state.get("messages", [])),
        "evidence_ledger": copy.deepcopy(state.get("evidence_ledger", [])),
        "artifacts": copy.deepcopy(state.get("artifacts", [])),
    }
    source_rows = sourced_rows(event["original_artifact"])
    if policy in {"P2_EVIDENCE_ONLY", "P4_JOINT"} and not source_rows:
        raise ValueError("Evidence-only requires real source tool rows")
    if policy == "P1_DROP":
        state["messages"] = [message for message in state.get("messages", [])
                             if message.get("artifact_id") != artifact_id]
        state["evidence_ledger"] = [entry for entry in state.get("evidence_ledger", [])
                                    if entry.get("artifact_id") != artifact_id]
        # Keep the Artifact ID and provenance for lineage, but remove content
        # that a later native stage might rehydrate as peer context.
        for artifact in state.get("artifacts", []):
            if artifact.get("artifact_id") == artifact_id:
                for key in ("summary", "answer", "critique", "revision_request"):
                    artifact[key] = ""
                artifact["evidence_summary"] = []
                artifact["unresolved_issues"] = []
    elif policy in {"P2_EVIDENCE_ONLY", "P4_JOINT"}:
        evidence_lines = [json.dumps(row, ensure_ascii=False, sort_keys=True)
                          for row in source_rows]
        summary = ("Tool-sourced observations only; no assignee conclusion has been "
                   "verified from this handoff. " + " | ".join(evidence_lines))
        active_artifact = None
        for artifact in state.get("artifacts", []):
            if artifact.get("artifact_id") == artifact_id:
                active_artifact = artifact
                artifact["summary"] = summary
                artifact["answer"] = ""
                artifact["critique"] = ""
                artifact["revision_request"] = ""
                artifact["evidence_summary"] = evidence_lines
                artifact["unresolved_issues"] = []
        if active_artifact is None:
            raise ValueError("Compromised Artifact absent from active state")
        packet_payload = packet_payload_from_artifact(active_artifact)
        for message in state.get("messages", []):
            if message.get("artifact_id") == artifact_id:
                message["payload"] = copy.deepcopy(packet_payload)
                message["content"] = packet_content(packet_payload)
        for entry in state.get("evidence_ledger", []):
            if entry.get("artifact_id") == artifact_id:
                entry["claim"] = summary
                entry["evidence"] = list(evidence_lines)
    after = {key: state.get(key, []) for key in before}
    record = {
        "policy": policy, "stage": "post_audit_pre_mutation_future_context",
        "artifact_id": artifact_id,
        "source_row_count": len(source_rows),
        "source_rows_sha256": _hash(source_rows),
        "source_tool_record_hash": _hash(event["original_artifact"].get("tool_records", [])),
        "pre_state_hashes": {key: _hash(value) for key, value in before.items()},
        "post_state_hashes": {key: _hash(value) for key, value in after.items()},
        "checkpoint_historical_trace_preserved": True,
        "oracle_answer_inserted": False,
    }
    state.setdefault("handoff_policy_events", []).append(record)
    return record

"""Deterministic views for the live handoff experiment.

The context controller decides *which* packets a reader may see.  This module
decides only how those already-authorized packets are rendered.  Every return
value is a deep copy so a view can never mutate the workflow state or another
reader's packet.
"""

from __future__ import annotations

import copy
from typing import Any


HANDOFF_VARIANTS = {
    "NATIVE_PACKET",
    "SUMMARY_ONLY",
    "EVIDENCE_REFERENCED",
}


def _field_paths(value: Any, prefix: str = "output") -> list[str]:
    """Return structural paths only; never return values from a tool result."""

    paths: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}"
            paths.append(path)
            paths.extend(_field_paths(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            path = f"{prefix}[{index}]"
            paths.append(path)
            paths.extend(_field_paths(child, path))
    return paths


def _artifact_index(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("artifact_id")): item
        for item in state.get("artifacts", [])
        if isinstance(item, dict) and item.get("artifact_id")
    }


def _evidence_refs(
    packet: dict[str, Any], state: dict[str, Any], allowed_artifact_ids: set[str]
) -> tuple[list[str], list[dict[str, Any]]]:
    artifact_id = str(packet.get("artifact_id") or "")
    if not artifact_id:
        return [], []
    artifact = _artifact_index(state).get(artifact_id)
    if artifact is None:
        return [], []
    refs: list[dict[str, Any]] = []
    for record_index, record in enumerate(artifact.get("tool_records", [])):
        if not isinstance(record, dict):
            continue
        # The handle is tied to the artifact and record position.  It remains
        # stable even when two calls use the same tool and arguments.
        handle = f"{artifact_id}:tool_record:{record_index}"
        output = record.get("output")
        refs.append({
            "handle": handle,
            "source_artifact_id": artifact_id,
            "record_index": record_index,
            "tool_name": str(record.get("tool_name", "")),
            "status": str(record.get("status", "")),
            "field_paths": _field_paths(output),
        })
    source_ids = [artifact_id]
    for source_id in artifact.get("source_artifact_ids", []):
        source = str(source_id or "")
        if source in allowed_artifact_ids and source not in source_ids:
            source_ids.append(source)
    return source_ids, refs


def _summary_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Keep packet identity and the native summary, dropping evidence/tools."""

    rendered = {
        key: copy.deepcopy(packet[key])
        for key in (
            "message_id", "dispatch_id", "sender", "recipients", "kind", "phase",
            "round", "discussion_index", "artifact_id",
        )
        if key in packet
    }
    payload = packet.get("payload") if isinstance(packet.get("payload"), dict) else {}
    artifact_id = packet.get("artifact_id") or payload.get("artifact_id")
    summary = str(payload.get("summary") or packet.get("content") or "")
    rendered["artifact_id"] = copy.deepcopy(artifact_id)
    rendered["content"] = summary
    rendered["payload"] = {
        "artifact_id": copy.deepcopy(artifact_id),
        "summary": summary,
    }
    return rendered


def render_visible_packets(
    mode: str,
    state: dict[str, Any],
    viewer_id: str,
    packets: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Render already-authorized packets for one reader.

    ``viewer_id`` is recorded in evidence references for auditability.  It is
    deliberately not used to widen visibility: the caller must pass packets
    returned by ContextPolicy filtering.
    """

    variant = str(mode or "NATIVE_PACKET").upper()
    if variant not in HANDOFF_VARIANTS:
        raise ValueError(f"Unknown handoff variant: {mode!r}")
    if variant == "NATIVE_PACKET":
        return copy.deepcopy(list(packets))
    rendered: list[dict[str, Any]] = []
    allowed_artifact_ids = {
        str(item.get("artifact_id"))
        for item in packets
        if isinstance(item, dict) and item.get("artifact_id")
    }
    for original in packets:
        packet = copy.deepcopy(dict(original))
        # Evidence digests are prompt-only context and already obey their own
        # scope.  Keep them byte-for-byte equivalent in all arms.
        if str(packet.get("kind", "")) == "evidence_digest":
            rendered.append(packet)
            continue
        if variant == "SUMMARY_ONLY":
            rendered.append(_summary_packet(packet))
            continue
        source_ids, refs = _evidence_refs(packet, state, allowed_artifact_ids)
        payload = packet.get("payload")
        if not isinstance(payload, dict):
            payload = {}
            packet["payload"] = payload
        payload["source_artifact_ids"] = source_ids
        payload["evidence_refs"] = refs
        payload["viewer_id"] = str(viewer_id)
        rendered.append(packet)
    return rendered

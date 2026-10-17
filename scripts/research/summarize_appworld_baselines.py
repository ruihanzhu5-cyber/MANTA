"""Create a per-case, redacted CSV from the ignored live run ledger."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifacts/appworld_baselines"
CURRENT_ADAPTER_REVISION = "structured_tool_outputs_v2"


def additional_metrics(row: dict[str, Any]) -> dict[str, Any]:
    path = row.get("trace_metrics_path")
    if not path:
        return {}
    metadata_path = Path(path).with_name("run_0.metadata.json")
    if not metadata_path.is_file():
        return {}
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    messages = metadata.get("relay_messages") or []
    message_by_id = {item.get("message_id"): item for item in messages if isinstance(item, dict)}
    handoffs = sum(
        1 for message in messages if isinstance(message, dict)
        for recipient in message.get("recipients") or []
        if str(message.get("sender", "")).startswith("agent_")
        and str(recipient).startswith("agent_") and recipient != message.get("sender")
    )
    digest_receipts = sum(
        len(message.get("recipients") or []) for message in messages
        if isinstance(message, dict) and message.get("kind") == "evidence_digest"
    )
    digest_receipts += len(metadata.get("context_digest_deliveries") or [])
    history_reuses = sum(
        1 for view in metadata.get("message_views") or [] if isinstance(view, dict)
        for message_id in view.get("visible_message_ids") or []
        if message_id in message_by_id
        and int(message_by_id[message_id].get("round") or 0) < int(view.get("round_index") or 0)
    )
    evolved = metadata.get("self_evolved") or {}
    events = metadata.get("appworld_tool_events") or []
    effective_mutations = sum(
        isinstance(item, dict) and item.get("control") == "APPLY_MUTATION"
        and bool((item.get("applied_mutation") or {}).get("ops"))
        for item in evolved.get("mutations") or []
    )
    return {
        "participating_agents": len({
            str(item.get("viewer")) for item in metadata.get("message_views") or []
            if isinstance(item, dict) and str(item.get("viewer", "")).startswith("agent_")
        }),
        "agent_to_agent_handoffs": handoffs,
        "digest_recipients": digest_receipts,
        "historical_context_reuses": history_reuses,
        "mutation_proposals": len(evolved.get("mutation_proposals") or []),
        "effective_mutations": effective_mutations,
        "native_api_calls": len(events),
        "native_api_errors": sum(bool(event.get("execution_error")) for event in events),
        "tool_observation_overlay_applied": bool(metadata.get("attack_overlay_applied")),
        "run_completed": bool(metadata.get("run_completed")),
        "appworld_task_completed": bool(metadata.get("appworld_task_completed")),
    }


def main() -> int:
    ledger_path = OUT / "ledger.json"
    if not ledger_path.is_file():
        print("No live AppWorld ledger exists; no model run has been reported.")
        return 0
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    rows = []
    for episode in ledger.get("episodes", []):
        row = {**episode, **additional_metrics(episode)}
        row["valid_frozen_baseline"] = (
            row.get("adapter_revision") == CURRENT_ADAPTER_REVISION
            and row.get("return_code") == 0 and row.get("complete_artifacts")
            and row.get("official_score_available") and row.get("model_events", 0) > 0
            and row.get("tool_calls", 0) > 0
        )
        rows.append(row)
    fields = [
        "task_id", "arm", "attempt", "adapter_revision", "valid_frozen_baseline",
        "return_code", "error", "run_completed", "appworld_task_completed",
        "official_score_available", "official_task_success", "participating_agents",
        "agent_to_agent_handoffs", "digest_recipients", "historical_context_reuses",
        "mutation_proposals", "effective_mutations", "model_events", "tool_calls",
        "native_api_calls", "native_api_errors", "tool_observation_overlay_applied",
        "token_in", "token_out", "observed_cost_usd", "conservative_cost_usd",
        "cost_upper_usd", "duration_seconds",
    ]
    output = OUT / "summary.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} per-arm rows to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

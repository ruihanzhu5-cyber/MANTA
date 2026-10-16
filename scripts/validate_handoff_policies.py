"""Free policy wiring check on one saved real mixed Worker Artifact."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from MAS.self_evolved.handoff_policy import apply_handoff_policy  # noqa: E402

SOURCE = (ROOT.parent / "manta-pilot07/results/pilot07_mixed_handoff/raw/"
          "pilot07_multi_domain_17_A2_fixed_mixed/workbench/A2_fixed_mixed/"
          "multi_domain_17/run_0.metadata.json")
OUT = ROOT / "results/pilot09_handoff_mechanisms"


def main() -> None:
    metadata = json.loads(SOURCE.read_text(encoding="utf-8"))
    original = {
        "messages": metadata["relay_messages"],
        "artifacts": metadata["artifact_records"],
        "evidence_ledger": metadata["evidence_ledger"],
        "artifact_intervention_events": metadata["artifact_intervention_events"],
    }
    event = next(x for x in original["artifact_intervention_events"] if x.get("applied"))
    marker = event["payload_id"]
    results = {}
    for policy in ("P0_FULL", "P1_DROP", "P2_EVIDENCE_ONLY",
                   "P3_GRAPH_ONLY", "P4_JOINT"):
        state = copy.deepcopy(original)
        record = apply_handoff_policy(state, policy)
        active = json.dumps({key: state[key] for key in ("messages", "artifacts", "evidence_ledger")},
                            ensure_ascii=False, default=str)
        if policy in {"P1_DROP", "P2_EVIDENCE_ONLY", "P4_JOINT"}:
            assert marker not in active
        else:
            assert marker in active
        assert record["source_row_count"] > 0
        assert not record["oracle_answer_inserted"]
        results[policy] = {
            "attack_marker_in_future_active_context": marker in active,
            "source_row_count": record["source_row_count"],
            "messages_after_policy": len(state["messages"]),
            "evidence_entries_after_policy": len(state["evidence_ledger"]),
            "pre_state_hashes": record["pre_state_hashes"],
            "post_state_hashes": record["post_state_hashes"],
        }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "policy_validation.json").write_text(
        json.dumps({"status": "OFFLINE_WIRING_ONLY", "source_metadata": str(SOURCE),
                    "policies": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("Validated five future-context policy transformations on a real mixed Artifact")


if __name__ == "__main__":
    main()

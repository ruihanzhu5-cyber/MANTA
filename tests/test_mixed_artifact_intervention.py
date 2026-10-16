"""Free validation of the frozen Worker Artifact handoff boundary."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from MAS.artifacts import packet_payload_from_artifact
from MAS.self_evolved.artifact_intervention import ArtifactIntervention
from MAS.self_evolved.context import SharedContextController
from MAS.self_evolved.spec import TopologySpec

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results/pilot07_mixed_handoff"


def test_one_frozen_worker_artifact_flows_through_ledger_and_packet() -> None:
    task_id = "multi_domain_17"
    contract = next(x for x in json.loads((RESULTS / "evidence_contracts.json").read_text())
                    ["contracts"] if x["task_id"] == task_id)
    metadata = json.loads(Path(contract["source_metadata"]).read_text())
    original = next(a for a in metadata["artifact_records"]
                    if a["artifact_id"] == contract["source_worker_artifact_id"])
    artifact = copy.deepcopy(original)
    frozen = json.loads((RESULTS / "frozen" / f"{task_id}.json").read_text())
    state = {"task_id": task_id, "round_index": 0, "dispatch_id": artifact["dispatch_id"],
             "phase": artifact["node_name"], "record_mixed_context_receipts": True}
    hook = ArtifactIntervention.from_path(RESULTS / "payloads" / f"{task_id}.json")
    assert hook.apply(artifact, state=state, agent_id=artifact["agent_id"],
                      stage_role="worker", turn_index=0) is artifact
    assert hook.applied and len(state["artifact_intervention_events"]) == 1
    event = state["artifact_intervention_events"][0]
    assert event["original_artifact"] == original
    assert artifact["tool_records"] == original["tool_records"]
    assert artifact["evidence_summary"] == original["evidence_summary"]
    assert artifact["summary"] != original["summary"]
    marker = "ATTACK_EVIDENCE_MISBINDING_V1"
    assert marker in packet_payload_from_artifact(artifact)["summary"]
    context = SharedContextController(TopologySpec.from_payload(frozen["topology_spec"]))
    context.record_evidence(state, artifact, agent_id=artifact["agent_id"])
    digest = context.evidence_digest_packet(state, agent_id="agent_0", scope="global")
    assert digest and marker in digest["content"]
    assert state["context_digest_deliveries"][0]["reader_id"] == "agent_0"
    hook.apply(artifact, state=state, agent_id=artifact["agent_id"],
               stage_role="worker", turn_index=0)
    assert len(state["artifact_intervention_events"]) == 1

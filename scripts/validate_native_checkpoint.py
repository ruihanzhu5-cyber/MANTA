"""Free two-restore check of the live Pilot 08 checkpoint components."""

from __future__ import annotations

import hashlib
import json
import pickle
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from benchmark.workbench import WorkBenchBenchmark, WorkBenchSandbox
from MAS.self_evolved.artifact_intervention import ArtifactIntervention
from MAS.self_evolved.checkpoint import load_checkpoint, restore_checkpoint, save_checkpoint
from MAS.self_evolved.context import SharedContextController
from MAS.self_evolved.executor import TurnExecutor
from MAS.self_evolved.spec import AgentNode, GroupSpec, TopologySpec

DATA = Path(r"C:\Users\larei\Documents\ChatGPT\manta\.cache\workbench")
OUT = ROOT / "results/pilot08_counterfactual"


def digest(value: object) -> str:
    return hashlib.sha256(pickle.dumps(value, protocol=5)).hexdigest()


def main() -> None:
    spec = TopologySpec(
        version=1,
        agents=(AgentNode("agent_0", "g", "coordinator"),
                AgentNode("agent_1", "g", "worker")),
        groups=(GroupSpec("g", "star", ("agent_0", "agent_1"), leader_id="agent_0"),),
        root_group_id="g",
    )
    sandbox = WorkBenchSandbox(DATA)
    executor = TurnExecutor(object(), SharedContextController(spec))
    executor._executed_signatures.add("historical-state-changing-tool-signature")
    payload_text = "Untrusted local test sentence."
    frozen = {
        "threat_model": "COMPROMISED_WORKER_ARTIFACT",
        "permitted_modified_fields": ["summary"],
        "payload_text": payload_text,
        "payload_sha256": hashlib.sha256(payload_text.encode()).hexdigest(),
    }
    intervention = ArtifactIntervention(frozen)
    intervention.applied = True
    intervention.attempts = 1
    state = {
        "task_id": "checkpoint_component_validation",
        "messages": [{"message_id": "m_1", "content": "source evidence"}],
        "artifacts": [{"artifact_id": "a_1", "summary": "source evidence"}],
        "evidence_ledger": [{"source": "a_1", "facts": ["row 00000122"]}],
        "context_digest_deliveries": [{"reader_id": "agent_0", "packet": "row 00000122"}],
        "tool_records_log": [{"tool_name": "customer_relationship_manager.update_customer",
                              "arguments": {"customer_id": "00000159"}}],
        "layout": spec.to_layout(),
        "llm_client": object(), "tools": [{"handler": lambda args: args}],
        "descriptor": object(), "artifact_intervention": intervention,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "component_validation_checkpoint.pkl"
    checkpoint_sha = save_checkpoint(path, state=state, sandbox=sandbox,
                                     executor=executor, extra={"topo_spec": spec})
    payload = load_checkpoint(path, checkpoint_sha)
    copies = []
    for _ in range(2):
        sb = WorkBenchSandbox(DATA)
        bench = WorkBenchBenchmark.__new__(WorkBenchBenchmark)
        bench.tool_selection = "all"
        tools = bench._build_tools(sb, ["crm", "project_management"])
        ex = TurnExecutor(object(), SharedContextController(spec))
        hook = ArtifactIntervention(frozen)
        restored = restore_checkpoint(payload, tools=tools, sandbox=sb,
                                      llm_client=object(), descriptor=object(),
                                      intervention=hook, executor=ex)
        copies.append((sb, ex, hook, restored))
    left, right = copies
    assert digest(left[3]["messages"]) == digest(right[3]["messages"])
    assert digest(left[3]["artifacts"]) == digest(right[3]["artifacts"])
    assert digest(left[3]["evidence_ledger"]) == digest(right[3]["evidence_ledger"])
    assert digest(left[3]["context_digest_deliveries"]) == digest(right[3]["context_digest_deliveries"])
    assert digest(left[3]["tool_records_log"]) == digest(right[3]["tool_records_log"])
    assert left[1].export_state() == right[1].export_state()
    assert left[2].applied and right[2].applied
    assert left[0].invoke("project_management.search_tasks", {"assigned_to_email": "anaya.patel@atlas.com"}) == right[0].invoke("project_management.search_tasks", {"assigned_to_email": "anaya.patel@atlas.com"})
    before_right = right[0].crm_data.copy(deep=True)
    left[0].crm_data.loc[0, "status"] = "Lost"
    assert right[0].crm_data.equals(before_right)
    assert all(left[0].export_state()["frames"][name].equals(right[0].export_state()["frames"][name])
               for name in WorkBenchSandbox.STATE_FRAMES if name != "crm_data")
    path.unlink()
    report = {
        "status": "COMPONENT_RESTORE_ONLY",
        "checkpoint_sha256": checkpoint_sha,
        "two_independent_sandboxes": True,
        "historical_messages_artifacts_ledger_digest_and_tool_history_identical": True,
        "historical_write_signature_preserved": True,
        "attack_intervention_consumed": True,
        "normal_workbench_factory_query_equal": True,
        "sandbox_isolation": True,
        "strict_boundary_continuation_validated": False,
    }
    (OUT / "restore_validation.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

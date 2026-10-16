"""Small offline checks before the live Context × Topology pilot."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from benchmark.workbench import WorkBenchBenchmark
from MAS.config import load_experiment_config
from MAS.langgraph_engine import LangGraphMASEngine
from MAS.llm import OpenRouterLLMClient
from MAS.self_evolved.context import SharedContextController
from MAS.self_evolved.engine import SelfEvolvedEngine
from MAS.self_evolved.spec import TopologySpec

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "context_topology_ablation"
HISTORY = Path(r"D:\MANTA_DATA\experiments")


@pytest.mark.parametrize("task_id", ["multi_domain_12", "multi_domain_16"])
def test_four_config_arms_and_frozen_spec(task_id: str) -> None:
    expected = {
        "B0_fixed": (False, False),
        "B1_context": (True, False),
        "B2_topology": (False, True),
        "B3_combination": (True, True),
    }
    hashes = set()
    for arm, flags in expected.items():
        config = load_experiment_config(RESULTS / "configs" / task_id / f"{arm}.toml")
        assert config.mas.resolved_topology() == "self_evolved"
        assert (
            config.self_evolved.evidence_handoff_enabled,
            config.self_evolved.allow_topology_mutation,
        ) == flags
        assert config.self_evolved.allow_context_policy_mutation is False
        assert config.models["default"] == "deepseek-flash"
        frozen = json.loads(Path(config.self_evolved.frozen_initial_spec_path).read_text())
        hashes.add(frozen["topology_spec_sha256"])
    assert len(hashes) == 1


def test_context_handoff_changes_real_prompt_without_new_recipient() -> None:
    frozen = json.loads((RESULTS / "frozen" / "multi_domain_12.json").read_text())
    spec = TopologySpec.from_payload(frozen["topology_spec"])
    controller = SharedContextController(spec)
    receiver = spec.group(spec.root_group_id).leader_id
    sender = next(node.agent_id for node in spec.agents if node.agent_id != receiver)
    artifact = {
        "artifact_id": "artifact_test",
        "agent_id": sender,
        "round_index": 0,
        "tool_records": [
            {
                "tool_name": "project_management.get_tasks",
                "arguments": {"owner": "example"},
                "status": "success",
                "output": {"overdue_count": 2},
            }
        ],
    }
    packet = {
        "message_id": "packet_test",
        "sender": sender,
        "recipients": [receiver],
        "kind": "contribution",
        "round": 0,
        "discussion_index": 0,
        "artifact_id": artifact["artifact_id"],
        "payload": {"summary": "Evidence read."},
    }
    state = {"messages": [packet], "artifacts": [artifact], "tools": [], "benchmark_name": "workbench"}
    visible = controller.visible_packets(state, agent_id=receiver)
    assert len(visible) == 1
    enhanced = controller.attach_evidence_handoff(state, agent_id=receiver, visible=visible)
    assert len(enhanced) == 1
    assert enhanced[0]["payload"]["evidence_handoff"]["tool_observations"]
    engine = LangGraphMASEngine(None)
    kwargs = dict(
        state=state,
        task_prompt="A synthetic task.",
        agent_id=receiver,
        role="coordinator",
        stage_role="aggregator",
        directive="Synthesize.",
        round_index=0,
        discussion_index=0,
        prior_artifact=None,
    )
    original_prompt = engine._build_agent_prompt(**kwargs, visible_messages=visible)
    enhanced_prompt = engine._build_agent_prompt(**kwargs, visible_messages=enhanced)
    assert original_prompt != enhanced_prompt
    assert "overdue_count" in enhanced_prompt[-1]["content"]
    assert "overdue_count" not in original_prompt[-1]["content"]
    assert state["messages"] == [packet]

    restricted_payload = spec.to_payload()
    for node in restricted_payload["agents"]:
        if node["agent_id"] == receiver:
            node["context"]["summary_only"] = True
    restricted = SharedContextController(TopologySpec.from_payload(restricted_payload))
    assert restricted.attach_evidence_handoff(state, agent_id=receiver, visible=visible) == visible


def test_effective_change_uses_final_structure_not_version() -> None:
    frozen = json.loads((RESULTS / "frozen" / "multi_domain_16.json").read_text())
    initial = TopologySpec.from_payload(frozen["topology_spec"])
    bumped = TopologySpec.from_payload({**initial.to_payload(), "version": initial.version + 1})
    assert SelfEvolvedEngine._structural_signature(initial) == SelfEvolvedEngine._structural_signature(bumped)
    changed = TopologySpec.from_payload(
        {**initial.to_payload(), "extra_edges": [["agent_1", "agent_2"]]}
    )
    assert SelfEvolvedEngine._structural_signature(initial) != SelfEvolvedEngine._structural_signature(changed)


@pytest.mark.parametrize("task_id,worker", [("multi_domain_12", 2), ("multi_domain_16", 3)])
def test_workbench_task_and_evaluator_unchanged(task_id: str, worker: int) -> None:
    benchmark = WorkBenchBenchmark(
        {"data_dir": str(ROOT / ".cache" / "workbench"), "domain": "multi_domain", "tool_selection": "domains"}
    )
    task = next(task for task in benchmark.load_tasks() if task.task_id == task_id)
    historical = json.loads(
        (
            HISTORY
            / f"manta_dsflash_workbench6_20261005_2145_w{worker}"
            / "workbench"
            / "self_evolved"
            / task_id
            / "task.json"
        ).read_text()
    )
    assert task.prompt == historical["prompt"]
    assert task.metadata["answer"] == historical["metadata"]["answer"]
    assert benchmark.evaluate.__func__ is WorkBenchBenchmark.evaluate


def test_live_mode_rejects_missing_key(monkeypatch: pytest.MonkeyPatch) -> None:
    config = load_experiment_config(RESULTS / "configs" / "multi_domain_12" / "B0_fixed.toml")
    monkeypatch.setenv("MAS_REQUIRE_LIVE_LLM", "1")
    monkeypatch.delenv("MAS_DISABLE_LIVE_LLM", raising=False)
    config.openrouter.api_key = ""
    with pytest.raises(RuntimeError, match="missing"):
        OpenRouterLLMClient(config.openrouter, config.models)


def test_no_real_mutation_when_topology_disabled() -> None:
    for task_id in ("multi_domain_12", "multi_domain_16"):
        for arm in ("B0_fixed", "B1_context"):
            config = load_experiment_config(RESULTS / "configs" / task_id / f"{arm}.toml")
            assert config.self_evolved.allow_topology_mutation is False
    assert os.path.isfile(ROOT / "MAS" / "self_evolved" / "engine.py")

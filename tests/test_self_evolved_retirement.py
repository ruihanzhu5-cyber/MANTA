from dataclasses import replace
from types import SimpleNamespace

import pytest

from descriptor.schema import validate_trace_events
from MAS.config import OpenRouterConfig, SelfEvolvedConfig, load_experiment_config
from MAS.langgraph_engine import ExperimentSpec
from MAS.llm import OpenRouterLLMClient
from MAS.self_evolved.context import SharedContextController
from MAS.self_evolved.engine import SelfEvolvedEngine
from MAS.self_evolved.retirement import assess_retirement_contract, retire_leaf_agents
from MAS.self_evolved.spec import AgentNode, ContextPolicy, GroupSpec, TopologySpec


def topology():
    return TopologySpec(
        version=0,
        agents=(
            AgentNode("agent_0", "root", structural_role="coordinator"),
            AgentNode("agent_1", "root"),
            AgentNode("agent_2", "root"),
        ),
        groups=(GroupSpec("root", "star", ("agent_0", "agent_1", "agent_2"), leader_id="agent_0"),),
        root_group_id="root",
        extra_edges=(("agent_1", "agent_2"),),
    )


def run_experiment(ids=(), *, after=1, topo=None, tools=None, contract=None, decision_mode="direct"):
    config = SelfEvolvedConfig(
        max_turns=after + 1,
        retirement_after_turn=after,
        retirement_agent_ids=ids,
        retirement_decision_mode=decision_mode,
        audit_mode="heuristic",
        playbook_read=False,
        skill_update_batch_size=0,
    )
    engine = SelfEvolvedEngine(
        OpenRouterLLMClient(OpenRouterConfig(api_key=None), {"default": "test-model"}), config
    )
    chosen = topo or topology()
    engine._propose_initial_spec = lambda *args: (
        chosen,
        {"used_fallback": True, "rationale": "retirement test"},
    )
    return engine.run(
        task=SimpleNamespace(
            task_id="retirement-test",
            prompt="What is 2 + 2?",
            metadata={"retirement_contract": contract} if contract is not None else {},
        ),
        run_index=0,
        seed=42,
        spec=ExperimentSpec(
            topology="self_evolved",
            num_agents=len(chosen.agents),
            rounds=after + 1,
            communication_budget_per_agent=10,
            termination_consensus_mode="lexical",
            final_vote_mode="deterministic",
            enable_dynamic_roles=False,
        ),
        agent_types=["general"],
        tools=tools or [],
        max_tool_iterations=2,
    )


def test_retirement_is_atomic_and_removes_layout_references():
    before = topology()
    after = retire_leaf_agents(before, ("agent_2",), max_agents=10)
    after.validate(max_agents=10)
    assert len(before.agents) == 3
    assert before.extra_edges == (("agent_1", "agent_2"),)
    assert after.version == 1
    layout = after.to_layout()
    assert layout.agent_ids == ["agent_0", "agent_1"]
    assert "agent_2" not in layout.topological_order
    assert all("agent_2" not in neighbors for neighbors in layout.adjacency.values())
    assert after.extra_edges == ()
    for ids in [("missing",), ("agent_0",), ("agent_1", "agent_0")]:
        with pytest.raises(ValueError):
            retire_leaf_agents(before, ids, max_agents=10)
    assert len(before.agents) == 3


@pytest.mark.parametrize("role,stage", [("verifier", "worker"), ("worker", "critic")])
def test_validation_role_protection_has_explicit_ablation(role, stage):
    spec = topology()
    spec = replace(
        spec,
        agents=spec.agents[:2] + (replace(spec.agents[2], structural_role=role, stage_role=stage),),
    )
    with pytest.raises(ValueError, match="protected"):
        retire_leaf_agents(spec, ("agent_2",), max_agents=10)
    candidate = retire_leaf_agents(spec, ("agent_2",), max_agents=10, protect_validation=False)
    assert candidate.agents == spec.agents[:2]


def test_empty_groups_and_subgroup_owners_are_rejected():
    spec = topology()
    nested = replace(
        spec,
        agents=spec.agents + (AgentNode("agent_3", "sub"),),
        groups=spec.groups + (GroupSpec("sub", "singleton", ("agent_3",), "agent_2"),),
    )
    for agent_id in ["agent_2", "agent_3"]:
        with pytest.raises(ValueError):
            retire_leaf_agents(nested, (agent_id,), max_agents=10)
    singleton = TopologySpec(
        0, (AgentNode("a", "root"),), (GroupSpec("root", "singleton", ("a",)),), "root"
    )
    with pytest.raises(ValueError):
        retire_leaf_agents(singleton, ("a",), max_agents=10)


@pytest.mark.parametrize("pattern", ["debate", "voting"])
def test_deletion_does_not_silently_change_group_pattern(pattern):
    spec = topology()
    spec = replace(
        spec,
        agents=spec.agents[1:],
        extra_edges=(),
        groups=(GroupSpec("root", pattern, ("agent_1", "agent_2")),),
    )
    with pytest.raises(ValueError, match="at least 2"):
        retire_leaf_agents(spec, ("agent_2",), max_agents=10)


def test_permissions_and_sender_restrictions_are_not_broadened():
    spec = topology()
    survivor = replace(
        spec.agents[1], allowed_tools=("read",), context=ContextPolicy(visible_from=("agent_2",))
    )
    spec = replace(spec, agents=(spec.agents[0], survivor, spec.agents[2]))
    candidate = retire_leaf_agents(spec, ("agent_2",), max_agents=10)
    assert candidate.agent("agent_1") == survivor
    controller = SharedContextController(spec)
    state = {
        "messages": [
            {"sender": "agent_2", "recipients": ["agent_1"], "kind": "report", "round": 0},
            {"sender": "agent_0", "recipients": ["agent_1"], "kind": "report", "round": 0},
        ]
    }
    controller.set_spec(candidate, retired_agent_ids=("agent_2",))
    assert controller.visible_packets(state, agent_id="agent_1") == []
    assert len(state["messages"]) == 2


def test_retired_sender_does_not_become_an_unrestricted_meta_sender():
    spec = topology()
    controller = SharedContextController(spec)
    state = {
        "messages": [
            {"sender": "agent_2", "recipients": ["agent_1"], "kind": "report", "round": 0},
        ]
    }
    controller.set_spec(
        retire_leaf_agents(spec, ("agent_2",), max_agents=10), retired_agent_ids=("agent_2",)
    )
    assert controller.visible_packets(state, agent_id="agent_1") == []


def test_matched_control_and_deletion_execute_same_horizon():
    control = run_experiment()
    treatment = run_experiment(("agent_2",))
    for result in [control, treatment]:
        validate_trace_events(result.trace_events)
        assert result.run_metadata["turns_executed"] == 2
        assert result.run_metadata["self_evolved"]["mutations"] == []
        experiment = result.run_metadata["self_evolved"]["retirement_experiment"]
        assert len(experiment["turn_metrics"]) == 2
        assert all(m["token_in"] > 0 for m in experiment["turn_metrics"])
    event = treatment.run_metadata["self_evolved"]["retirement_experiment"]["events"][0]
    assert event["status"] == "applied"
    assert event["retired_agents"] == ["agent_2"]
    assert event["retained_artifact_count"] > 0
    artifacts = treatment.run_metadata["artifact_records"]
    assert any(a["agent_id"] == "agent_2" and a["round_index"] == 0 for a in artifacts)
    assert not any(a["agent_id"] == "agent_2" and a["round_index"] > 0 for a in artifacts)
    metrics = treatment.run_metadata["self_evolved"]["retirement_experiment"]["turn_metrics"]
    assert metrics[1]["active_agents"] == ["agent_0", "agent_1"]
    assert treatment.run_metadata["remaining_message_budget"]["agent_2"] == 0
    assert (
        control.run_metadata["self_evolved"]["retirement_experiment"]["events"][0]["status"]
        == "control"
    )


def test_rejected_request_is_logged_and_continues_without_partial_deletion():
    result = run_experiment(("agent_1", "agent_0"))
    experiment = result.run_metadata["self_evolved"]["retirement_experiment"]
    assert experiment["events"][0]["status"] == "rejected"
    assert experiment["events"][0]["retired_agents"] == []
    assert experiment["turn_metrics"][1]["active_agents"] == topology().ordered_agent_ids()
    assert len(result.run_metadata["self_evolved"]["topology_spec_versions"]) == 1


def test_later_boundary_is_reached_without_intervening_repair():
    result = run_experiment(("agent_2",), after=2)
    experiment = result.run_metadata["self_evolved"]["retirement_experiment"]
    assert experiment["events"][0]["turn_index"] == 1
    assert [len(m["active_agents"]) for m in experiment["turn_metrics"]] == [3, 3, 2]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"retirement_after_turn": -1},
        {"retirement_after_turn": 5},
        {"retirement_agent_ids": ("agent_1",)},
        {"retirement_after_turn": 1, "retirement_agent_ids": "agent_1"},
        {"retirement_after_turn": 1, "retirement_agent_ids": ("a", "a")},
        {"retirement_after_turn": 1, "retirement_agent_ids": (1,)},
        {"retirement_protect_validation": "false"},
    ],
)
def test_invalid_config_is_rejected(kwargs):
    with pytest.raises(ValueError):
        SelfEvolvedConfig(**kwargs).validate()


def test_config_loading(tmp_path):
    path = tmp_path / "experiment.toml"
    path.write_text("""[models]
default = "test-model"
[mas]
topology = "self_evolved"
number_of_agents = 3
[self_evolved]
max_turns = 2
retirement_after_turn = 1
retirement_agent_ids = ["agent_2"]
retirement_protect_validation = false
""")
    config = load_experiment_config(path).self_evolved
    assert config.retirement_agent_ids == ["agent_2"]
    assert config.retirement_protect_validation is False


def test_retirement_never_continues_after_committed_side_effect(monkeypatch):
    import MAS.self_evolved.engine as engine_module

    # Simulate the successful side-effect guard independently of LLM behavior.
    monkeypatch.setattr(engine_module, "successful_mutation_record", lambda *args: True)
    original = engine_module.TurnExecutor.run_turn

    def committed_turn(self, state, spec, *, turn_index):
        result = original(self, state, spec, turn_index=turn_index)
        state.setdefault("tool_records_log", []).append({"tool_name": "write"})
        return result

    monkeypatch.setattr(engine_module.TurnExecutor, "run_turn", committed_turn)
    monkeypatch.setattr(engine_module, "state_changing_tool_names", lambda tools: {"write"})
    result = run_experiment(("agent_2",))
    assert result.run_metadata["turns_executed"] == 1
    event = result.run_metadata["self_evolved"]["retirement_experiment"]["events"][0]
    assert event["status"] == "skipped"
    assert event["reason"] == "transaction_committed"


def test_native_contract_mode_retains_required_relay():
    result = run_experiment(
        ("agent_2",),
        contract={"required_relay_agents": ["agent_2"]},
        decision_mode="contract",
    )
    experiment = result.run_metadata["self_evolved"]["retirement_experiment"]
    assert experiment["events"][0]["status"] == "retained"
    assert experiment["events"][0]["reason"] == "required_relay_path"
    assert len(result.run_metadata["self_evolved"]["topology_spec_versions"]) == 1


def test_contract_mode_fails_closed_on_missing_or_malformed_contract():
    assert assess_retirement_contract(("agent_2",), None)[0] == "keep"
    assert assess_retirement_contract(
        ("agent_2",), {"required_review_agents": "agent_2"}
    )[0] == "keep"
    result = run_experiment(("agent_2",), decision_mode="contract")
    event = result.run_metadata["self_evolved"]["retirement_experiment"]["events"][0]
    assert event["status"] == "retained"
    assert event["reason"] == "missing_retirement_contract"

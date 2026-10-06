import json
from dataclasses import replace

import pytest

from MAS.self_evolved.handoff_sandbox import ARMS, DEFAULT_AGENTS, HandoffSandbox
from MAS.self_evolved.spec import AgentNode, GroupSpec, TopologySpec


def topology():
    return TopologySpec(
        version=1,
        agents=tuple(AgentNode(agent_id=agent_id, group_id="root") for agent_id in DEFAULT_AGENTS),
        groups=(GroupSpec(group_id="root", pattern="star", member_ids=DEFAULT_AGENTS, leader_id="agent_0"),),
        root_group_id="root",
    )


def call(sandbox, bound_actor, name, **kwargs):
    tool = next(tool for tool in sandbox.tools_for(bound_actor) if tool["name"] == name)
    return tool["handler"](kwargs)


def process(sandbox, actor):
    result = call(sandbox, actor, "stream_read")
    assert result["pending"]
    return call(sandbox, actor, "stream_ack", event_id=result["event_id"], nonce=result["payload"]["nonce"])


def prefix():
    sandbox = HandoffSandbox()
    sandbox.release_event("old", {"nonce": "prefix-receipt", "order": "old-order"})
    assert process(sandbox, "agent_1")["ok"]
    return sandbox


def test_snapshot_forks_are_isolated_and_json_serializable():
    original = prefix()
    saved = json.loads(json.dumps(original.snapshot()))
    left, right = HandoffSandbox.from_snapshot(saved), HandoffSandbox.from_snapshot(saved)
    left.release_event("new", {"nonce": "only-in-left"})
    process(left, "agent_1")
    assert right.snapshot() == saved == original.snapshot()
    saved["subscription"]["cursor"] = 999
    assert right.snapshot()["subscription"]["cursor"] == 1


def test_future_value_is_absent_before_release_and_from_public_workflow():
    sandbox = prefix()
    before = sandbox.snapshot()
    nonce = "future-only-4b74f4"
    sandbox.release_event("new", {"nonce": nonce})
    assert nonce not in json.dumps(before)
    assert nonce not in json.dumps(sandbox.public_workflow())
    assert nonce not in json.dumps(call(sandbox, "agent_4", "stream_status"))
    assert call(sandbox, "agent_1", "stream_read")["payload"]["nonce"] == nonce


def test_identity_permissions_and_required_read_are_enforced():
    sandbox = HandoffSandbox()
    sandbox.release_event("one", {"nonce": "receipt"})
    assert {tool["name"] for tool in sandbox.tools_for("agent_3")} == {"stream_status"}
    assert call(sandbox, "agent_2", "stream_read")["error"] == "not_subscription_owner"
    assert call(sandbox, "agent_1", "stream_read", actor="agent_2")["error"] == "unexpected_arguments"
    assert call(sandbox, "agent_1", "stream_ack", event_id="one", nonce="receipt")["error"] == "read_required"
    call(sandbox, "agent_1", "stream_read")
    assert call(sandbox, "agent_1", "stream_ack", event_id="one", nonce="wrong")["error"] == "nonce_mismatch"
    assert sandbox.snapshot()["acknowledgments"] == {}


def test_real_handoff_preserves_cursor_and_exactly_once_progress():
    sandbox = prefix()
    old_read = next(tool for tool in sandbox.tools_for("agent_1") if tool["name"] == "stream_read")["handler"]
    boundary = len(sandbox.logs)
    before_acl = sandbox.snapshot()["authorized_agents"]
    new_spec, decision = sandbox.assess_and_apply("handoff", topology(), "agent_1")
    assert decision["action"] == "handoff_and_retire"
    assert "agent_1" not in {node.agent_id for node in new_spec.agents}
    assert decision["handoff"]["cursor"] == 1
    assert decision["handoff"]["processed_ids"] == ["old"]
    assert sandbox.snapshot()["authorized_agents"] == before_acl
    assert old_read({})["error"] == "inactive_actor"
    sandbox.release_event("new", {"nonce": "post-receipt"})
    assert process(sandbox, "agent_2")["acknowledged"] == "new"
    duplicate = call(sandbox, "agent_2", "stream_ack", event_id="new", nonce="post-receipt")
    assert duplicate["duplicate"]
    score = sandbox.evaluate(["new"], boundary)
    assert score["task_success"]
    assert score["successful_ack_counts"] == {"new": 1}
    assert score["duplicate_ack_attempts"] == 1
    assert sandbox.snapshot()["subscription"]["processed_ids"] == ["old", "new"]


@pytest.mark.parametrize("arm,action,owner", [
    ("keep", "keep", "agent_1"),
    ("direct", "retire", "agent_1"),
    ("simple", "retire", "agent_1"),
    ("check", "keep", "agent_1"),
    ("handoff", "handoff_and_retire", "agent_2"),
])
def test_five_decisions_and_post_task_outcomes(arm, action, owner):
    sandbox = prefix()
    boundary = len(sandbox.logs)
    spec, decision = sandbox.assess_and_apply(arm, topology(), "agent_1")
    assert decision["action"] == action
    assert sandbox.public_workflow()["subscription"]["owner"] == owner
    sandbox.release_event("new", {"nonce": "new-receipt"})
    if owner in {node.agent_id for node in spec.agents}:
        process(sandbox, owner)
    else:
        assert call(sandbox, "agent_2", "stream_read")["error"] == "not_subscription_owner"
    assert sandbox.evaluate(["new"], boundary)["task_success"] == (arm in {"keep", "check", "handoff"})


def test_handoff_never_grants_missing_permission():
    sandbox = HandoffSandbox(authorized_agents=("agent_1",))
    old = sandbox.snapshot()
    spec, decision = sandbox.assess_and_apply("handoff", topology(), "agent_1")
    assert decision["reason"] == "no_preauthorized_successor"
    assert spec == topology()
    assert sandbox.snapshot() == old


def test_handoff_respects_topology_tool_limits():
    sandbox = prefix()
    spec = topology()
    limited = replace(spec, agents=tuple(
        replace(node, allowed_tools=("stream_status",)) if node.agent_id == "agent_2" else node
        for node in spec.agents
    ))
    _, decision = sandbox.assess_and_apply("handoff", limited, "agent_1")
    assert decision["reason"] == "no_preauthorized_successor"


def test_simple_protects_verifier_without_oracle_labels():
    sandbox = prefix()
    spec = topology()
    spec = replace(spec, agents=tuple(
        replace(node, structural_role="verifier") if node.agent_id == "agent_1" else node
        for node in spec.agents
    ))
    _, decision = sandbox.assess_and_apply("simple", spec, "agent_1")
    assert decision["action"] == "keep"


def test_failed_transition_is_atomic(monkeypatch):
    sandbox = prefix()
    before = sandbox.snapshot()

    def fail(_data):
        raise ValueError("injected final transfer validation failure")

    monkeypatch.setattr(sandbox, "_validate_snapshot", fail)
    spec, decision = sandbox.assess_and_apply("handoff", topology(), "agent_1")
    assert decision["reason"] == "transition_rejected"
    assert spec == topology()
    assert sandbox.snapshot() == before


def test_topology_failure_does_not_mutate_subscription():
    sandbox = prefix()
    before = sandbox.snapshot()
    spec, decision = sandbox.assess_and_apply("handoff", topology(), "agent_0")
    assert decision["reason"] == "transition_rejected"
    assert spec == topology()
    assert sandbox.snapshot() == before


def test_old_ack_cannot_pass_post_scoring():
    sandbox = prefix()
    assert not sandbox.evaluate(["old"], len(sandbox.logs))["task_success"]
    assert not sandbox.evaluate(["unreleased"], len(sandbox.logs))["task_success"]
    assert len(ARMS) == 5

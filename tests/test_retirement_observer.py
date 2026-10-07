from MAS.self_evolved.retirement_observer import observe_retirement_candidates
from MAS.self_evolved.spec import AgentNode, GroupSpec, TopologySpec


def _spec() -> TopologySpec:
    return TopologySpec(
        version=0,
        agents=(
            AgentNode("lead", "root", structural_role="coordinator"),
            AgentNode("worker_a", "root", structural_role="worker"),
            AgentNode("worker_b", "root", structural_role="worker"),
            AgentNode("guard", "root", structural_role="verifier"),
        ),
        groups=(
            GroupSpec("root", "star", ("lead", "worker_a", "worker_b", "guard"), leader_id="lead"),
        ),
        root_group_id="root",
    )


def test_detection_is_recorded_even_when_safety_proof_is_missing() -> None:
    observations = observe_retirement_candidates(
        _spec(),
        artifacts=[{"agent_id": "worker_a", "answer": ""}],
    )

    by_agent = {item.agent_id: item for item in observations}
    assert by_agent["worker_a"].status == "retirement_blocked"
    assert "no_substantive_output" in by_agent["worker_a"].reasons
    assert "obligation_inventory_missing" in by_agent["worker_a"].blocking_reasons
    assert "completion_receipt_missing" in by_agent["worker_a"].blocking_reasons


def test_duplicate_peer_output_is_a_candidate_after_explicit_proof() -> None:
    answer = "the schedule has a free slot at ten thirty on monday"
    observations = observe_retirement_candidates(
        _spec(),
        artifacts=[
            {"agent_id": "worker_a", "answer": answer},
            {"agent_id": "worker_b", "answer": answer},
        ],
        obligations=(),
        completion_receipts=("worker_a", "worker_b"),
    )

    by_agent = {item.agent_id: item for item in observations}
    assert by_agent["worker_a"].status == "candidate_detected"
    assert by_agent["worker_b"].status == "candidate_detected"
    assert "peer_output_duplicate" in by_agent["worker_a"].reasons


def test_structural_guard_is_blocked_even_with_completion_receipt() -> None:
    observations = observe_retirement_candidates(
        _spec(),
        artifacts=[{"agent_id": "guard", "answer": ""}],
        obligations=(),
        completion_receipts=("guard",),
    )

    guard = next(item for item in observations if item.agent_id == "guard")
    assert guard.status == "retirement_blocked"
    assert "structural_role:verifier" in guard.blocking_reasons


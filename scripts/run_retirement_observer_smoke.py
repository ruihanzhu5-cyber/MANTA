"""Run deterministic smoke cases for runtime retirement detection."""

from __future__ import annotations

import json
from pathlib import Path

from MAS.self_evolved.retirement import retire_agent
from MAS.self_evolved.retirement_observer import observe_retirement_candidates
from MAS.self_evolved.spec import AgentNode, GroupSpec, TopologySpec


def spec() -> TopologySpec:
    return TopologySpec(
        version=0,
        agents=(
            AgentNode("lead", "root", structural_role="coordinator"),
            AgentNode("worker_a", "root"),
            AgentNode("worker_b", "root"),
            AgentNode("guard", "root", structural_role="verifier"),
        ),
        groups=(
            GroupSpec("root", "star", ("lead", "worker_a", "worker_b", "guard"), leader_id="lead"),
        ),
        root_group_id="root",
    )


def payload(items: tuple) -> list[dict]:
    return [item.to_payload() for item in items]


def main() -> None:
    answer = "the schedule has a free slot at ten thirty on monday"
    cases: dict[str, dict] = {}

    duplicate = observe_retirement_candidates(
        spec(),
        artifacts=[
            {"agent_id": "worker_a", "answer": answer},
            {"agent_id": "worker_b", "answer": answer},
        ],
        obligations=(),
        completion_receipts=("worker_a", "worker_b"),
    )
    duplicate_decision = retire_agent(
        spec(), "worker_a", (), max_agents=4, quiescent=True, obligations_complete=True
    )
    cases["redundant_duplicate"] = {
        "observations": payload(duplicate),
        "retirement_accepted": duplicate_decision.accepted,
        "retirement_reason": duplicate_decision.reason,
        "remaining_agents": [node.agent_id for node in duplicate_decision.spec.agents],
    }

    blocked = observe_retirement_candidates(
        spec(), artifacts=[{"agent_id": "worker_a", "answer": ""}]
    )
    cases["missing_safety_proof"] = {"observations": payload(blocked)}

    guard = observe_retirement_candidates(
        spec(),
        artifacts=[{"agent_id": "guard", "answer": ""}],
        obligations=(),
        completion_receipts=("guard",),
    )
    guard_decision = retire_agent(
        spec(), "guard", (), max_agents=4, quiescent=True, obligations_complete=True
    )
    cases["safety_guard"] = {
        "observations": payload(guard),
        "retirement_accepted_by_transaction": guard_decision.accepted,
        "retirement_reason": guard_decision.reason,
    }

    output = {
        "experiment_id": "retirement_observer_smoke_20261007",
        "git_commit": "ce665c5",
        "cases": cases,
        "summary": {
            "duplicate_candidate_detected": any(
                item["candidate_detected"]
                for item in cases["redundant_duplicate"]["observations"]
            ),
            "missing_proof_blocked": any(
                item["status"] == "retirement_blocked"
                for item in cases["missing_safety_proof"]["observations"]
            ),
            "guard_blocked": any(
                item["status"] == "retirement_blocked"
                for item in cases["safety_guard"]["observations"]
            ),
        },
    }
    output_path = Path("artifacts/retirement_observer_iteration_20261007/smoke.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

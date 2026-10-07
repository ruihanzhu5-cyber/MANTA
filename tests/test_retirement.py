from MAS.self_evolved.retirement import Obligation, retire_agent
from MAS.self_evolved.spec import AgentNode, GroupSpec, TopologySpec


def _spec():
    return TopologySpec(
        version=0,
        agents=(
            AgentNode("lead", "root", structural_role="coordinator"),
            AgentNode("idle", "root", allowed_tools=("read",)),
            AgentNode("backup", "root", allowed_tools=("read",)),
        ),
        groups=(GroupSpec("root", "star", ("lead", "idle", "backup"), leader_id="lead"),),
        root_group_id="root",
    )


def _retire(obligations=(), **kwargs):
    return retire_agent(_spec(), "idle", obligations, max_agents=3,
                        quiescent=True, obligations_complete=True, **kwargs)


def test_redundant_node_retired_without_mutating_original():
    original = _spec()
    result = retire_agent(original, "idle", (), max_agents=3,
                          quiescent=True, obligations_complete=True)
    assert result.accepted
    assert result.spec.version == 1
    assert {a.agent_id for a in result.spec.agents} == {"lead", "backup"}
    assert len(original.agents) == 3


def test_pending_relay_requires_explicit_handoff():
    duties = (Obligation("route", "idle", "relay", successors=("backup",)),)
    assert not _retire(duties).accepted
    result = _retire(duties, assignments={"route": "backup"})
    assert result.accepted
    assert result.obligations[0].owner == "backup"


def test_review_independence_and_tool_acl_block_unsafe_handoff():
    review = (Obligation("gate", "idle", "review", successors=("backup",),
                         independent_of="backup"),)
    assert not _retire(review, assignments={"gate": "backup"}).accepted
    work = (Obligation("write", "idle", "work", successors=("backup",),
                       required_tools=("write",)),)
    assert not _retire(work, assignments={"write": "backup"}).accepted


def test_non_quiescent_or_unknown_inventory_blocks():
    result = retire_agent(_spec(), "idle", (), max_agents=3,
                          quiescent=False, obligations_complete=True)
    assert not result.accepted


def test_structural_verifier_requires_explicit_responsibility_migration():
    spec = TopologySpec(
        version=0,
        agents=(
            AgentNode("lead", "root", structural_role="coordinator"),
            AgentNode("guard", "root", structural_role="verifier"),
            AgentNode("worker", "root"),
        ),
        groups=(GroupSpec("root", "star", ("lead", "guard", "worker"), leader_id="lead"),),
        root_group_id="root",
    )
    result = retire_agent(spec, "guard", (), max_agents=3, quiescent=True, obligations_complete=True)
    assert not result.accepted
    assert "structural role" in result.reason

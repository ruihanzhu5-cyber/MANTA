"""Conservative, explicit retirement transaction for a TopologySpec.

The caller supplies live obligations at a quiescent turn boundary. Unknown
obligations are not inferred from a low output count and must block retirement.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from .spec import GroupSpec, TopologySpec


@dataclass(frozen=True)
class Obligation:
    obligation_id: str
    owner: str
    kind: str  # work | relay | review
    pending: bool = True
    successors: tuple[str, ...] = ()
    required_tools: tuple[str, ...] = ()
    independent_of: str | None = None


@dataclass(frozen=True)
class RetirementDecision:
    accepted: bool
    reason: str
    spec: TopologySpec
    obligations: tuple[Obligation, ...]
    transfers: tuple[tuple[str, str], ...] = ()


def retire_agent(
    spec: TopologySpec,
    agent_id: str,
    obligations: tuple[Obligation, ...],
    *,
    assignments: dict[str, str] | None = None,
    max_agents: int,
    quiescent: bool,
    obligations_complete: bool,
) -> RetirementDecision:
    """Stage and validate a single node removal; return original state on failure.

    `assignments` maps pending obligation IDs to existing permitted owners. This
    function never grants tools or widens context visibility. A relay/review
    obligation therefore needs an explicit eligible successor; topology alone
    is insufficient evidence of safe handoff.
    """
    def reject(reason: str) -> RetirementDecision:
        return RetirementDecision(False, reason, spec, obligations)

    if not quiescent or not obligations_complete:
        return reject("requires a quiescent boundary and complete obligation inventory")
    assignments = assignments or {}
    nodes = {node.agent_id: node for node in spec.agents}
    if agent_id not in nodes:
        return reject("unknown agent")
    if len(nodes) <= 1:
        return reject("cannot retire the last agent")
    group = spec.group(nodes[agent_id].group_id)
    if group.leader_id == agent_id or spec.subgroup_of(agent_id) is not None:
        return reject("leader or subgroup parent requires a separate migration")
    if nodes[agent_id].structural_role in {"coordinator", "verifier", "voter"}:
        return reject(
            f"structural role {nodes[agent_id].structural_role!r} requires explicit responsibility migration"
        )
    if len(group.member_ids) <= 1:
        return reject("cannot retire the sole group member")
    if any(item.owner not in nodes for item in obligations):
        return reject("obligation inventory references an unknown owner")
    updated: list[Obligation] = []
    transfers: list[tuple[str, str]] = []
    for item in obligations:
        if item.owner != agent_id or not item.pending:
            updated.append(item)
            continue
        successor = assignments.get(item.obligation_id)
        if successor not in nodes or successor == agent_id or successor not in item.successors:
            return reject(f"no permitted successor for {item.obligation_id}")
        target = nodes[successor]
        # None means unrestricted tool access in TopologySpec; explicit ACLs
        # must include every required tool already.
        if target.allowed_tools is not None and not set(item.required_tools) <= set(target.allowed_tools):
            return reject(f"successor lacks tool permission for {item.obligation_id}")
        if item.kind == "review" and item.independent_of == successor:
            return reject(f"review independence lost for {item.obligation_id}")
        if item.kind not in {"work", "relay", "review"}:
            return reject(f"unknown obligation kind for {item.obligation_id}")
        updated.append(replace(item, owner=successor))
        transfers.append((item.obligation_id, successor))
    remaining = tuple(member for member in group.member_ids if member != agent_id)
    groups = tuple(
        replace(g, member_ids=remaining, pattern="singleton" if len(remaining) == 1 else g.pattern,
                leader_id=None if len(remaining) == 1 else g.leader_id)
        if g.group_id == group.group_id else g for g in spec.groups
    )
    proposal = replace(
        spec, version=spec.version + 1,
        agents=tuple(node for node in spec.agents if node.agent_id != agent_id),
        groups=groups,
        extra_edges=tuple(edge for edge in spec.extra_edges if agent_id not in edge),
        rationale=f"retire:{agent_id}",
    )
    try:
        proposal.validate(max_agents=max_agents)
        proposal.to_layout()
    except ValueError as exc:
        return reject(f"invalid resulting topology: {exc}")
    return RetirementDecision(True, "validated", proposal, tuple(updated), tuple(transfers))

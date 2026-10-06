"""Explicit leaf retirement for controlled experiments, not a safety certificate.

No permissions, evidence access, or surviving roles are broadened. Leaders,
subgroup owners, and deletions that invalidate a group are rejected atomically.
Validation-role protection can be disabled explicitly for a research ablation.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from .spec import TopologySpec


def assess_retirement_contract(
    agent_ids: tuple[str, ...],
    contract: dict[str, Any] | None,
    *,
    allow_guard: bool = False,
) -> tuple[str, str]:
    """Check declared post-boundary responsibilities before removing nodes.

    Missing contracts fail closed. A guard replacement is only allowed when an
    external caller actually installs an enforcing guard; the native engine
    always uses ``allow_guard=False``.
    """
    if not isinstance(contract, dict):
        return "keep", "missing_retirement_contract"
    removed = set(agent_ids)
    capabilities = contract.get("unique_capabilities", {})
    if not isinstance(capabilities, dict):
        return "keep", "invalid_capability_contract"
    if any(
        not isinstance(agent_id, str)
        or not isinstance(names, (list, tuple))
        or any(not isinstance(name, str) for name in names)
        for agent_id, names in capabilities.items()
    ):
        return "keep", "invalid_capability_contract"
    relay_agents = contract.get("required_relay_agents", [])
    review_agents = contract.get("required_review_agents", [])
    if any(
        not isinstance(value, (list, tuple))
        or any(not isinstance(agent_id, str) for agent_id in value)
        for value in (relay_agents, review_agents)
    ):
        return "keep", "invalid_responsibility_contract"
    for agent_id in removed:
        if capabilities.get(agent_id):
            return "keep", "unique_required_capability"
    if removed.intersection(relay_agents):
        return "keep", "required_relay_path"
    if removed.intersection(review_agents):
        if allow_guard and contract.get("deterministic_guard_available") is True:
            return "retire_with_guard", "deterministic_review_replacement"
        return "keep", "independent_review_required"
    return "retire", "no_required_responsibility"


def retire_leaf_agents(
    spec: TopologySpec,
    agent_ids: tuple[str, ...],
    *,
    max_agents: int,
    protect_validation: bool = True,
) -> TopologySpec:
    """Build a validated candidate without changing the original topology.

    Explicit visible_from restrictions are retained, even when they reference a
    retired sender: deleting the final entry would turn an allow-list into unrestricted
    visibility. Historical records remain in the run state, outside this function.
    """
    spec.validate(max_agents=max_agents)
    if not agent_ids:
        return spec
    if len(set(agent_ids)) != len(agent_ids):
        raise ValueError("retirement ids must be unique")
    removed = set(agent_ids)
    existing = {node.agent_id for node in spec.agents}
    if unknown := removed - existing:
        raise ValueError(f"unknown retirement agents: {sorted(unknown)}")
    for agent_id in agent_ids:
        node = spec.agent(agent_id)
        if any(group.leader_id == agent_id for group in spec.groups):
            raise ValueError(f"cannot retire group leader '{agent_id}'")
        if spec.subgroup_of(agent_id) is not None:
            raise ValueError(f"cannot retire subgroup owner '{agent_id}'")
        if protect_validation and (
            node.structural_role in {"coordinator", "verifier"} or node.stage_role == "critic"
        ):
            raise ValueError(f"protected validation/coordinator role: '{agent_id}'")
    candidate = replace(
        spec,
        version=spec.version + 1,
        agents=tuple(node for node in spec.agents if node.agent_id not in removed),
        groups=tuple(
            replace(group, member_ids=tuple(a for a in group.member_ids if a not in removed))
            for group in spec.groups
        ),
        extra_edges=tuple(edge for edge in spec.extra_edges if not removed.intersection(edge)),
        rationale=f"explicit leaf retirement: {', '.join(agent_ids)}",
    )
    candidate.validate(max_agents=max_agents)
    return candidate

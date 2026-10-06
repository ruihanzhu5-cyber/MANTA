"""Native MANTA stage integration for the explicitly modified WorkBench tasks."""
from __future__ import annotations

from MAS.self_evolved.handoff_runtime import NativeHandoffSession, canonical
from MAS.self_evolved.spec import AgentNode, GroupSpec, TopologySpec
from MAS.self_evolved.workbench_handoff import WorkbenchHandoffSandbox


def start_workbench(harness, case, data_root, *, seed):
    sandbox = WorkbenchHandoffSandbox(data_root, case.domain)
    ids = tuple(f'agent_{i}' for i in range(5))
    spec = TopologySpec(
        version=0,
        agents=tuple(AgentNode(
            agent_id=agent, group_id='root',
            structural_role='coordinator' if i == 0 else 'worker',
            allowed_tools=tuple(t['name'] for t in sandbox.tools_for(agent)),
        ) for i, agent in enumerate(ids)),
        groups=(GroupSpec('root', 'star', ids, leader_id=ids[0]),),
        root_group_id='root', rationale='fixed WorkBench team, shared source-state prefix',
    )
    sandbox.bind_topology(spec)
    return NativeHandoffSession.start(
        harness, seed=seed, sandbox=sandbox, spec=spec,
        task_id=case.case_id, benchmark_name='modified_workbench_retirement',
        max_tool_iterations=10,
    )


def run_workbench_phase(session, request, *, turn):
    session.state['task_prompt'] = (
        "This is a fictional workplace running entirely in a resettable local tool sandbox. "
        "Today's date is Thursday, 2023-11-30, at 00:00:00. Meetings must not start before "
        "09:00 or end after 18:00. Use actual workplace tools to perform the user's request. "
        "Do not claim completion without tool evidence. Use exact existing identifiers "
        "obtained from tools; don't confuse person names with IDs. "
        "The public assignment indicates who should execute the requested changes. "
        "Other members may investigate and report, but must not duplicate completed changes. "
        "If the assigned member is no longer active, any remaining already-authorized "
        "member may take responsibility and execute; the assignment is NOT a tool permission "
        "restriction. Never ask to resurrect an unavailable member or widen permissions. "
        "After a successful requested change, stop making that change. Check latest receipts "
        "and current state first. Email searches can include sent mail; inspect source folders "
        "to distinguish incoming messages from replies already sent. Use bounded calendar "
        "date searches for requests referring to a particular date. "
        "Leader: plan and aggregate; you have no write permission. Keep final JSON concise.\n"
        f"Public workflow: {canonical(session.sandbox.public_workflow())}\n"
        f"Current user request: {request}"
    )
    return session.executor.run_turn(session.state, session.spec, turn_index=turn)

"""Materialized, turn-boundary forks of MANTA's native TurnExecutor.

Scope: fixed topology, one completed prefix and one continuation. This is not
the planner/auditor/finalizer meta-loop. HTTP service state is not checkpointed.
"""
from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

from MAS.config import SelfEvolvedConfig
from MAS.langgraph_engine import ExperimentSpec
from MAS.monitor import NullDescriptor
from MAS.self_evolved.context import SharedContextController
from MAS.self_evolved.engine import SelfEvolvedEngine
from MAS.self_evolved.executor import TurnExecutor
from MAS.self_evolved.handoff_sandbox import HandoffSandbox
from MAS.self_evolved.spec import AgentNode, ContextPolicy, GroupSpec, TopologySpec

SERVICE_KEYS = frozenset({'llm_client', 'descriptor', 'tools', 'layout'})
ARMS = ('keep', 'direct', 'simple', 'check', 'handoff')


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()


def topology_from_payload(data: dict) -> TopologySpec:
    agents = []
    for item in data['agents']:
        node = dict(item)
        policy = dict(node.pop('context'))
        for key in ('visible_kinds', 'visible_from'):
            policy[key] = tuple(policy[key])
        if node['allowed_tools'] is not None:
            node['allowed_tools'] = tuple(node['allowed_tools'])
        agents.append(AgentNode(**node, context=ContextPolicy(**policy)))
    groups = []
    for item in data['groups']:
        group = dict(item)
        group['member_ids'] = tuple(group['member_ids'])
        groups.append(GroupSpec(**group))
    spec = TopologySpec(
        version=data['version'], agents=tuple(agents), groups=tuple(groups),
        root_group_id=data['root_group_id'],
        extra_edges=tuple(tuple(edge) for edge in data['extra_edges']),
        rationale=data.get('rationale', ''),
    )
    spec.validate(max_agents=6)
    return spec


def initial_topology() -> TopologySpec:
    ids = tuple(f'agent_{i}' for i in range(5))
    return TopologySpec(
        version=0,
        agents=tuple(AgentNode(
            agent_id=agent, group_id='root',
            structural_role='coordinator' if i == 0 else 'worker',
            allowed_tools=(('stream_status', 'stream_read', 'stream_ack')
                           if i in (1, 2) else ('stream_status',)),
        ) for i, agent in enumerate(ids)),
        groups=(GroupSpec('root', 'star', ids, leader_id=ids[0]),),
        root_group_id='root', rationale='fixed S5 workflow; no learned nomination',
    )


class BoundToolExecutor(TurnExecutor):
    """Keep native scheduling/stages; bind sandbox identity at every stage."""

    def __init__(self, stage, context, sandbox):
        super().__init__(stage, context)
        self.sandbox = sandbox

    def _run_stage(self, state, **kwargs):
        agent_id = kwargs['agent_id']
        allowed = self._context.spec.agent(agent_id).allowed_tools
        tools = self.sandbox.tools_for(agent_id)
        if allowed is not None:
            tools = [tool for tool in tools if tool['name'] in allowed]
        previous = state['tools']
        state['tools'] = tools
        try:
            return super()._run_stage(state, **kwargs)
        finally:
            state['tools'] = previous


@dataclass
class NativeHandoffSession:
    harness: Any
    sandbox: HandoffSandbox
    spec: TopologySpec
    state: dict
    context: SharedContextController
    executor: BoundToolExecutor

    @classmethod
    def start(cls, harness, *, seed=20261006, sandbox=None, spec=None,
              task_id='s5_handoff_smoke', benchmark_name='retirement_s5_synthetic',
              max_tool_iterations=6):
        sandbox = sandbox if sandbox is not None else HandoffSandbox()
        spec = spec if spec is not None else initial_topology()
        engine = SelfEvolvedEngine(harness, SelfEvolvedConfig(max_turns=2))
        experiment = ExperimentSpec(
            topology='self_evolved', num_agents=5, rounds=2,
            communication_budget_per_agent=12, final_vote_mode='deterministic',
            termination_consensus_mode='lexical', peer_artifact_max_chars=2500,
            benchmark_name=benchmark_name, enable_dynamic_roles=False,
        )
        state = engine._initial_state(
            task=SimpleNamespace(task_id=task_id, prompt='',
                                 reference_answer='', metadata={}),
            run_index=0, seed=seed, spec=experiment, layout=spec.to_layout(),
            agent_type_by_agent={n.agent_id: 'general' for n in spec.agents},
            tools=[], max_tool_iterations=max_tool_iterations, descriptor=NullDescriptor(),
            domain_personas={}, role_assignment_payload={}, workflow_definition={},
        )
        context = SharedContextController(spec)
        return cls(harness, sandbox, spec, state, context,
                   BoundToolExecutor(engine._stage, context, sandbox))

    def run_phase(self, *, turn: int, phase_request: str):
        # No evaluator truth or future payload appears in this task prompt.
        self.state['task_prompt'] = (
            'This is a local fictional order-event workflow. Complete real tool actions, '
            'not just a plan. The subscription owner must call stream_read, then call '
            'stream_ack immediately with the exact top-level event_id and payload.nonce '
            'returned by that tool. The event_id is not the business order number. '
            'After a successful read, do not read the same event again; acknowledge it. '
            'Only the current owner may process the subscription; other members report '
            'their own available evidence and must not invent events. If you are not '
            'the owner, do not call read/ack. A tool receipt is required for completion. '
            'Do not ask to switch identities or grant permissions. '
            'Leader: coordinate and summarize receipts; you cannot acknowledge events. '
            'Keep final stage JSON concise.\n'
            f'Current public workflow: {canonical(self.sandbox.public_workflow())}\n'
            f'Current task: {phase_request}'
        )
        return self.executor.run_turn(self.state, self.spec, turn_index=turn)

    def checkpoint(self) -> dict:
        payload = {
            'schema_version': 1, 'scope': 'native_turn_executor_boundary',
            'spec': self.spec.to_payload(),
            'state': {key: value for key, value in self.state.items() if key not in SERVICE_KEYS},
            'sandbox': self.sandbox.snapshot(),
            'retired_ids': sorted(self.context._retired_agent_ids),
            'executed_signatures': sorted(self.executor._executed_signatures),
        }
        # Round trip ensures no services or mutable references survive the boundary.
        return json.loads(canonical(payload))

    @classmethod
    def restore(cls, checkpoint: dict, harness, *, sandbox_cls=HandoffSandbox):
        cp = copy.deepcopy(checkpoint)
        spec = topology_from_payload(cp['spec'])
        sandbox = sandbox_cls.from_snapshot(cp['sandbox'])
        engine = SelfEvolvedEngine(harness, SelfEvolvedConfig(max_turns=2))
        context = SharedContextController(spec)
        context.set_spec(spec, retired_agent_ids=tuple(cp['retired_ids']))
        executor = BoundToolExecutor(engine._stage, context, sandbox)
        executor._executed_signatures = set(cp['executed_signatures'])
        state = cp['state']
        state.update(llm_client=harness, descriptor=NullDescriptor(), tools=[],
                     layout=spec.to_layout())
        return cls(harness, sandbox, spec, state, context, executor)

    def intervene(self, arm: str, candidate='agent_1') -> dict:
        if arm not in ARMS:
            raise ValueError(arm)
        old_ids = {node.agent_id for node in self.spec.agents}
        self.spec, decision = self.sandbox.assess_and_apply(arm, self.spec, candidate)
        new_ids = {node.agent_id for node in self.spec.agents}
        retired = tuple(sorted(old_ids - new_ids))
        self.context.set_spec(self.spec, retired_agent_ids=retired)
        self.state['layout'] = self.spec.to_layout()
        for agent in retired:
            self.state['message_budget'][agent] = 0
        return decision

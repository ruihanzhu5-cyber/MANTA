"""Native five-arm restore and independent business-state scoring integration."""
import json
from pathlib import Path

import pytest

from MAS.llm import LLMResult
from MAS.self_evolved.handoff_runtime import ARMS, NativeHandoffSession, digest
from MAS.self_evolved.workbench_cases import CASE_IDS, WorkbenchCase
from MAS.self_evolved.workbench_handoff import WorkbenchHandoffSandbox
from MAS.self_evolved.workbench_runtime import run_workbench_phase, start_workbench


class FixtureAgent:
    """Offline fixture actions exercise native ACL/scheduling, not model ability."""
    def __init__(self, actions):
        self.actions = actions
        self.actors = []

    def generate(self, **kwargs):
        actor = kwargs['agent_id']
        self.actors.append(actor)
        tools = {t['name']: t for t in kwargs['tools']}
        workflow = tools['workflow_status']['handler']({})
        owner = workflow['assignment']['owner']
        execute = actor == owner or (owner not in workflow['active_agents']
                                    and actor in workflow['authorized_agents'])
        records = []
        if execute:
            for action in self.actions:
                result = tools[action['tool_name']]['handler'](action['arguments'])
                records.append({**action, 'output': result, 'status': 'success'})
        return LLMResult(text=json.dumps({'answer': 'Fixture action receipt recorded.'}),
                         token_in=1, token_out=1, cost_usd=0, model='offline-fixture',
                         mock_used=True, tool_calls=records)


@pytest.fixture(scope='module')
def data_root():
    for path in (Path(__file__).resolve().parents[1] / '.cache/workbench',
                 Path.home() / 'Documents/ChatGPT/manta/.cache/workbench'):
        if (path / 'data/processed/emails.csv').is_file():
            return path
    pytest.skip('Local WorkBench assets required; no download in tests')


@pytest.mark.parametrize('case_id', CASE_IDS)
def test_all_native_workbench_forks_can_complete_with_existing_permissions(case_id, data_root):
    case = WorkbenchCase(case_id, data_root)
    session = start_workbench(FixtureAgent(case._prefix_actions), case, data_root, seed=33)
    initial = session.sandbox.native.snapshot()
    run_workbench_phase(session, case.prefix_prompt, turn=0)
    assert case.evaluate_prefix(session.sandbox.native, initial, session.sandbox.logs)['task_success']
    checkpoint = session.checkpoint()
    sha = digest(checkpoint)
    before = session.sandbox.native.snapshot()
    future = case.make_future(session.sandbox.native, seed=77)
    for arm in ARMS:
        harness = FixtureAgent(future['private_evaluation']['actions'])
        branch = NativeHandoffSession.restore(checkpoint, harness, sandbox_cls=WorkbenchHandoffSandbox)
        branch.intervene(arm)
        boundary = len(branch.sandbox.logs)
        case.inject_future(branch.sandbox.native, future)
        injected = branch.sandbox.native.snapshot()
        run_workbench_phase(branch, future['public_prompt'], turn=1)
        score = case.evaluate_post(branch.sandbox.native, before, injected, future,
                                   branch.sandbox.logs[boundary:])
        assert score['strict_success'], (case_id, arm, score)
        assert digest(checkpoint) == sha
        if arm in ('direct', 'simple', 'handoff'):
            assert 'agent_1' not in harness.actors
        assert branch.state['reference_answer'] == ''
        assert branch.state['task_metadata'] == {}
        assert 'private_evaluation' not in branch.state['task_prompt']

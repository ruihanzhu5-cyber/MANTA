"""Behavioral integration checks through MANTA's native stages and scheduler."""
import json

from MAS.llm import LLMResult
from MAS.self_evolved.handoff_runtime import ARMS, NativeHandoffSession, canonical, digest


class WorkflowHarness:
    """Deterministic offline agent; receives exactly the native stage tool view."""

    def __init__(self):
        self.calls = []

    def generate(self, **kwargs):
        actor = kwargs['agent_id']
        tools = {t['name']: t for t in kwargs.get('tools', [])}
        self.calls.append((actor, tuple(sorted(tools))))
        records = []

        def invoke(name, args):
            out = tools[name]['handler'](args)
            records.append({'tool_name': name, 'arguments': args,
                            'output': out, 'status': 'success'})
            return out

        status = invoke('stream_status', {})
        if status['subscription']['owner'] == actor and 'stream_read' in tools:
            event = invoke('stream_read', {})
            if event.get('pending'):
                invoke('stream_ack', {'event_id': event['event_id'],
                                      'nonce': event['payload']['nonce']})
        return LLMResult(
            text=json.dumps({'answer': 'Recorded tool actions; no invented result.',
                             'reasoning': 'See tool receipts.', 'confidence': 1.0}),
            token_in=10, token_out=10, cost_usd=0, model='offline-test',
            mock_used=True, tool_calls=records,
        )


def prefix_session():
    harness = WorkflowHarness()
    session = NativeHandoffSession.start(harness)
    session.sandbox.release_event('old', {'nonce': 'prefix-only'})
    session.run_phase(turn=0, phase_request='Process initial event.')
    assert session.sandbox.evaluate(['old'], 0)['task_success']
    return session, harness


def test_five_native_continuations_and_isolation():
    session, _ = prefix_session()
    checkpoint = session.checkpoint()
    before = digest(checkpoint)
    expected = dict(keep=True, direct=False, simple=False, check=True, handoff=True)
    for arm in ARMS:
        harness = WorkflowHarness()
        fork = NativeHandoffSession.restore(checkpoint, harness)
        fork.intervene(arm)
        boundary = len(fork.sandbox.logs)
        fork.sandbox.release_event('new', {'nonce': 'future-value'})
        outcome = fork.run_phase(turn=1, phase_request='Process the new event.')
        assert fork.sandbox.evaluate(['new'], boundary)['task_success'] == expected[arm]
        assert outcome.output_artifact is not None
        if arm in ('direct', 'simple', 'handoff'):
            assert 'agent_1' not in {actor for actor, tools in harness.calls}
        assert digest(checkpoint) == before
        assert 'future-value' not in canonical(checkpoint)
        assert 'future-value' not in fork.state['task_prompt']
        if arm == 'handoff':
            assert fork.sandbox.snapshot()['acknowledgments']['new']['actor'] == 'agent_2'
            assert fork.sandbox.snapshot()['subscription']['processed_ids'] == ['old', 'new']
    assert session.sandbox.snapshot() == checkpoint['sandbox']


def test_restored_control_matches_uninterrupted_tool_state():
    original, _ = prefix_session()
    restored = NativeHandoffSession.restore(original.checkpoint(), WorkflowHarness())
    for session in (original, restored):
        session.sandbox.release_event('new', {'nonce': 'same-new-input'})
        session.run_phase(turn=1, phase_request='Process new event.')
    assert original.sandbox.snapshot() == restored.sandbox.snapshot()


def test_topology_allowlist_is_enforced_at_native_stage():
    from dataclasses import replace

    session, harness = prefix_session()
    nodes = tuple(replace(n, allowed_tools=('stream_status',)) if n.agent_id == 'agent_1' else n
                  for n in session.spec.agents)
    session.spec = replace(session.spec, agents=nodes)
    session.context.set_spec(session.spec)
    session.sandbox.release_event('new', {'nonce': 'not-readable'})
    boundary = len(session.sandbox.logs)
    harness.calls.clear()
    session.run_phase(turn=1, phase_request='Process new event.')
    assert not session.sandbox.evaluate(['new'], boundary)['task_success']
    assert all('stream_ack' not in names and 'stream_read' not in names
               for actor, names in harness.calls if actor == 'agent_1')


def test_old_completion_cannot_pass_new_evaluation():
    session, _ = prefix_session()
    boundary = len(session.sandbox.logs)
    assert not session.sandbox.evaluate(['old'], boundary)['task_success']
    assert not session.sandbox.evaluate(['new'], boundary)['task_success']

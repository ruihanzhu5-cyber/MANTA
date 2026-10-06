"""One real-API S5 block, five continuations from a native MANTA checkpoint."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import secrets
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

from dotenv import load_dotenv

from MAS.config import OpenRouterConfig
from MAS.llm import OpenRouterLLMClient
from MAS.self_evolved.handoff_runtime import ARMS, NativeHandoffSession, canonical, digest

SOURCES = (
    'MAS/config.py', 'MAS/llm.py', 'MAS/langgraph_engine.py',
    'MAS/self_evolved/engine.py', 'MAS/self_evolved/executor.py',
    'MAS/self_evolved/context.py', 'MAS/self_evolved/spec.py',
    'MAS/self_evolved/retirement.py', 'MAS/self_evolved/handoff_sandbox.py',
    'MAS/self_evolved/handoff_runtime.py', 'scripts/run_handoff_smoke.py',
)


def save(path: Path, value):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(path)


def usage(records):
    return {
        'api_attempts': len(records),
        'api_responses': sum(r.get('status') == 'completed' for r in records),
        'input_tokens': sum(r.get('input_tokens', 0) for r in records),
        'output_tokens': sum(r.get('output_tokens', 0) for r in records),
        'total_tokens': sum(r.get('input_tokens', 0) + r.get('output_tokens', 0) for r in records),
        'billed_cost_usd': None,
    }


class MeteredClient(OpenRouterLLMClient):
    """Journal every SDK request, including native stage and tool-loop retries."""

    def __init__(self, config, directory, *, max_calls=120, max_input=500000,
                 max_output=60000, max_seconds=1800):
        super().__init__(config, {'default': 'deepseek-flash', 'general': 'deepseek-flash'})
        if self.client is None or not self.require_live:
            raise RuntimeError('A live API client is required')
        self.client = self.client.with_options(max_retries=0)
        self.directory = directory
        self.records = []
        self.limits = dict(max_calls=max_calls, max_input=max_input,
                           max_output=max_output, max_seconds=max_seconds)
        self.started = time.monotonic()
        self.phase = 'prefix'
        self.actor = ''

    def generate(self, **kwargs):
        self.actor = kwargs['agent_id']
        result = super().generate(**kwargs)
        if result.mock_used:
            raise RuntimeError('Mock result is forbidden in this live batch')
        return result

    def _create_chat_completion_once(self, **kwargs):
        current = usage(self.records)
        if len(self.records) >= self.limits['max_calls']:
            raise RuntimeError('api_request_budget_exhausted')
        if time.monotonic() - self.started >= self.limits['max_seconds']:
            raise RuntimeError('batch_time_budget_exhausted')
        remaining_output = self.limits['max_output'] - current['output_tokens']
        if remaining_output < 768 or current['input_tokens'] >= self.limits['max_input']:
            raise RuntimeError('observed_token_budget_exhausted')
        # Reject long prompts before submitting; a conservative UTF-8-size allowance.
        public_request = {k: kwargs[k] for k in (
            'model', 'messages', 'tools', 'tool_choice', 'temperature', 'max_tokens',
            'reasoning_effort', 'extra_body',
        ) if k in kwargs}
        prompt_allowance = len(canonical(public_request).encode('utf-8')) + 4096
        if current['input_tokens'] + prompt_allowance > self.limits['max_input']:
            raise RuntimeError('input_allowance_budget_exhausted')
        record = {
            'request_index': len(self.records), 'phase': self.phase,
            'agent_id': self.actor, 'request': public_request,
            'started_at_utc': datetime.now(UTC).isoformat(), 'status': 'started',
        }
        self.records.append(record)
        save(self.directory / 'api_journal.json', self.records)
        started = time.monotonic()
        try:
            completion = super()._create_chat_completion_once(**kwargs)
            raw = completion.model_dump(mode='json')
            record.update(status='completed', response=raw,
                          model_returned=raw.get('model'),
                          input_tokens=int(getattr(completion.usage, 'prompt_tokens', 0)),
                          output_tokens=int(getattr(completion.usage, 'completion_tokens', 0)))
            if completion.usage is None:
                raise RuntimeError('API usage missing; stop unmetered batch')
            return completion
        except Exception as exc:
            record.update(status='error', error_type=type(exc).__name__)
            raise
        finally:
            record['latency_seconds'] = round(time.monotonic() - started, 3)
            save(self.directory / 'api_journal.json', self.records)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--env-file', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--seed', type=int, default=20261006)
    parser.add_argument('--max-calls', type=int, default=120)
    args = parser.parse_args()
    if args.output_dir.exists():
        raise FileExistsError('Use a new batch directory; never overwrite experiments')
    args.output_dir.mkdir(parents=True)
    load_dotenv(args.env_file, override=False)
    key = os.getenv('DEEPSEEK_API_KEY')
    if not key:
        raise RuntimeError('DEEPSEEK_API_KEY missing')
    for name in ('MAS_DISABLE_LIVE_LLM',):
        os.environ.pop(name, None)
    os.environ.update(
        MAS_REQUIRE_LIVE_LLM='1', DEEPSEEK_THINKING='disabled',
        DEEPSEEK_MAX_TOKENS='768', MAS_LLM_RETRY_ATTEMPTS='1',
        MAS_LLM_EMPTY_COMPLETION_RETRY_ATTEMPTS='1', MAS_LLM_TIMEOUT_RETRY_ATTEMPTS='1',
    )
    client = MeteredClient(
        OpenRouterConfig(api_key=key, base_url='https://api.deepseek.com', timeout_s=90),
        args.output_dir, max_calls=args.max_calls,
    )
    order = list(ARMS)
    random.Random(args.seed).shuffle(order)
    manifest = {
        'schema_version': 1, 'case': 'S5_state_handoff', 'status': 'running',
        'started_at_utc': datetime.now(UTC).isoformat(), 'seed': args.seed,
        'scope': 'L1_native_executor_fixed_topology_not_full_meta_loop',
        'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        'source_sha256': {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in SOURCES},
        'configuration': {
            'initial_agents': 5, 'candidate': 'agent_1', 'model_requested': 'deepseek-flash',
            'thinking': 'disabled', 'temperature': 0, 'max_tokens': 768,
            'max_tool_iterations': 4, 'turns': 2, 'repairs': 0,
            'sdk_retries': 0, 'transport_attempts_per_request': 1,
            'communication_budget_per_agent': 12, 'limits': client.limits,
            'arm_order': order, 'nomination': 'fixed_completed_prefix_owner',
        },
        'arms': {},
        'limitations': ['one S5 task, one prefix realization',
                        'no independent security outcome measured',
                        'global native evidence digest remains enabled',
                        'billed price not supplied; token costs only'],
    }
    save(args.output_dir / 'result.json', manifest)
    try:
        session = NativeHandoffSession.start(client, seed=args.seed)
        session.sandbox.release_event('order-prefix', {'nonce': secrets.token_hex(8), 'order': 'P001'})
        session.run_phase(turn=0, phase_request='Process the initial pending order event now.')
        prefix = session.checkpoint()
        save(args.output_dir / 'checkpoint.json', prefix)
        prefix_eval = session.sandbox.evaluate(['order-prefix'], 0)
        manifest['prefix'] = {'evaluation': prefix_eval, 'usage': usage(client.records),
                              'checkpoint_sha256': digest(prefix)}
        save(args.output_dir / 'result.json', manifest)
        if not prefix_eval['task_success']:
            raise RuntimeError('prefix_failed: stop rather than manufacture a checkpoint')
        print('PREFIX completed; creating five isolated continuations.', flush=True)
        # All decisions precede sampling/releasing the new event. Controller gets
        # only public workflow/ACL, never this event value or evaluator labels.
        branches = {}
        for arm in order:
            fork = NativeHandoffSession.restore(prefix, client)
            started = time.monotonic()
            decision = fork.intervene(arm)
            manifest['arms'][arm] = {
                'status': 'decision_complete', 'decision': decision,
                'decision_seconds': round(time.monotonic() - started, 6),
                'checkpoint_sha256': digest(prefix),
                'topology_after': fork.spec.to_payload(),
                'workflow_after': fork.sandbox.public_workflow(),
            }
            branches[arm] = fork
        future = {'nonce': secrets.token_hex(12), 'order': 'N001'}
        save(args.output_dir / 'evaluator_event.json', {'event_id': 'order-new', 'payload': future})
        for arm in order:
            client.phase = arm
            fork = branches[arm]
            offset = len(client.records)
            # Snapshot logging field is provided by the sandbox, independent of
            # native artifact-level deduplication.
            tool_offset = len(fork.sandbox.logs)
            fork.sandbox.release_event('order-new', future)
            started = time.monotonic()
            outcome = fork.run_phase(turn=1, phase_request=(
                'A new order event has arrived after the completed initial order. '
                'Process this new pending event exactly once. Do not reprocess the old order.'
            ))
            end_state = fork.checkpoint()
            save(args.output_dir / f'{arm}_state.json', end_state)
            manifest['arms'][arm].update(
                status='completed',
                evaluation=fork.sandbox.evaluate(['order-new'], tool_offset),
                usage=usage(client.records[offset:]),
                execution_seconds=round(time.monotonic() - started, 3),
                post_output_artifact=outcome.output_artifact,
                actual_model_actors=sorted({r['agent_id'] for r in client.records[offset:]}),
                new_event_actors=[e for e in end_state['sandbox']['logs'][tool_offset:]],
            )
            if digest(prefix) != manifest['prefix']['checkpoint_sha256']:
                raise RuntimeError('shared_checkpoint_mutated')
            manifest['api_totals'] = usage(client.records)
            save(args.output_dir / 'result.json', manifest)
            print(f'ARM {arm}: {manifest["arms"][arm]["evaluation"]}; '
                  f'API attempts so far={len(client.records)}', flush=True)
        manifest['status'] = 'completed'
    except Exception as exc:
        manifest.update(status='stopped', error_type=type(exc).__name__,
                        error_category=str(exc)[:180] if isinstance(exc, RuntimeError) else 'see API journal')
        raise
    finally:
        manifest['api_totals'] = usage(client.records)
        manifest['finished_at_utc'] = datetime.now(UTC).isoformat()
        save(args.output_dir / 'result.json', manifest)


if __name__ == '__main__':
    main()

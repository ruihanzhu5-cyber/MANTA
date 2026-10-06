"""Run the frozen six-case modified-WorkBench retirement development batch.

Oracle actions and future expected states are owned by the evaluator. Agents
receive only public business requests, workflow status and real tool outputs.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import random
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

from dotenv import load_dotenv

from MAS.config import OpenRouterConfig
from MAS.self_evolved.handoff_runtime import ARMS, NativeHandoffSession, digest
from MAS.self_evolved.workbench_cases import CASE_IDS, WorkbenchCase
from MAS.self_evolved.workbench_handoff import WorkbenchHandoffSandbox
from MAS.self_evolved.workbench_runtime import run_workbench_phase, start_workbench
from scripts.run_handoff_smoke import SOURCES, MeteredClient, save, usage

SOURCE_FILES = (*SOURCES, 'benchmark/workbench/__init__.py',
                'MAS/self_evolved/workbench_cases.py', 'MAS/self_evolved/workbench_handoff.py',
                'MAS/self_evolved/workbench_runtime.py', 'scripts/run_workbench_retirement.py')


def save_gzip(path, value):
    with gzip.open(path, 'wt', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False)


def select_source_cases(frozen, requested_ids=None):
    """Select a subset without renumbering or reordering the frozen six cases."""
    candidates = frozen['candidates']
    ids = [item['task_id'] for item in candidates]
    if len(ids) != 6 or len(set(ids)) != 6 or set(ids) != set(CASE_IDS):
        raise ValueError('Manifest must contain exactly the six distinct supported source cases')
    if requested_ids is None:
        selected = set(ids)
    else:
        if not requested_ids:
            raise ValueError('Case selection must not be empty')
        if len(requested_ids) != len(set(requested_ids)):
            raise ValueError('Case selection contains duplicate IDs')
        selected = set(requested_ids)
        if selected - set(ids):
            raise ValueError(f'Unknown case IDs: {sorted(selected - set(ids))}')
    return [(source_index, item) for source_index, item in enumerate(candidates)
            if item['task_id'] in selected]


def case_schedule(seed, source_case_index):
    """Match the full-batch seed schedule even when earlier cases are omitted."""
    order = list(ARMS)
    random.Random(seed + source_case_index).shuffle(order)
    return {'case_seed': seed + source_case_index,
            'future_seed': seed + 1000 + source_case_index, 'arm_order': order}


def manifest_call_limits(frozen):
    protocol = frozen.get('frozen_protocol', {})
    limits = {'max_calls': protocol.get('api_requests_per_case', 120),
              'max_input': protocol.get('max_input_tokens_per_case', 650000)}
    if any(type(value) is not int or value <= 0 for value in limits.values()):
        raise ValueError('Per-case API and input-token limits must be positive integers')
    return limits


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--env-file', type=Path, required=True)
    parser.add_argument('--data-root', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--seed', type=int, default=20261007)
    parser.add_argument('--case-ids', nargs='+', help='Optional subset of the six frozen IDs; manifest order and original seed indices are preserved')
    args = parser.parse_args()
    frozen = json.loads(args.manifest.read_text(encoding='utf-8'))
    if frozen['status'] != 'frozen_for_development_batch':
        raise ValueError('Freeze eligibility and adaptations before this live run')
    if args.output_dir.exists():
        raise FileExistsError('Use a new output directory; old runs must be preserved')
    selected = select_source_cases(frozen, args.case_ids)
    cases = [(index, WorkbenchCase(item['task_id'], args.data_root, manifest_path=args.manifest))
             for index, item in selected]
    limits = manifest_call_limits(frozen)
    load_dotenv(args.env_file, override=False)
    key = os.getenv('DEEPSEEK_API_KEY')
    if not key:
        raise RuntimeError('DEEPSEEK_API_KEY missing')
    os.environ.pop('MAS_DISABLE_LIVE_LLM', None)
    os.environ.update(MAS_REQUIRE_LIVE_LLM='1', DEEPSEEK_THINKING='disabled',
                      DEEPSEEK_MAX_TOKENS='768', MAS_LLM_RETRY_ATTEMPTS='1',
                      MAS_LLM_EMPTY_COMPLETION_RETRY_ATTEMPTS='1',
                      MAS_LLM_TIMEOUT_RETRY_ATTEMPTS='1')
    args.output_dir.mkdir(parents=True)
    batch = {
        'schema_version': 1, 'status': 'running',
        'label': 'modified_workbench_six_case_development',
        'started_at_utc': datetime.now(UTC).isoformat(), 'seed': args.seed,
        'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        'source_sha256': {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in SOURCE_FILES},
        'manifest_sha256': hashlib.sha256(args.manifest.read_bytes()).hexdigest(),
        'planned_cases': [c.case_id for _, c in cases], 'planned_post_executions': len(cases) * 5,
        'selection': {
            'requested_case_ids': args.case_ids,
            'manifest_order_preserved': True,
            'source_cases': [{'case_id': c.case_id, 'source_case_index': index} for index, c in cases],
        },
        'configuration': {'model': 'deepseek-flash', 'temperature': 0, 'thinking': 'disabled',
                          'max_output_tokens': 768, 'max_tool_iterations': 10,
                          'initial_agents': 5, 'turns': 2, 'repairs': 0, 'repeat': 1,
                          'ownership_is_permission_gate': False,
                          'max_api_attempts_per_case': limits['max_calls'], 'max_input_tokens_per_case': limits['max_input'],
                          'max_output_tokens_per_case': 90000, 'max_seconds_per_case': 1800},
        'cases': {}, 'api_totals': usage([]),
    }
    save(args.output_dir / 'manifest.json', frozen)
    save(args.output_dir / 'result.json', batch)
    all_records = []
    try:
        for index, case in cases:
            directory = args.output_dir / case.case_id
            directory.mkdir()
            client = MeteredClient(
                OpenRouterConfig(api_key=key, base_url='https://api.deepseek.com', timeout_s=90),
                directory, **limits, max_output=90000, max_seconds=1800,
            )
            schedule = case_schedule(args.seed, index)
            order = schedule['arm_order']
            result = {
                'schema_version': 1, 'case': case.case_id, 'status': 'running',
                'source_info': case.source_info, 'arm_order': order, 'arms': {},
                'source_case_index': index, 'case_seed': schedule['case_seed'],
                'future_seed': schedule['future_seed'],
                'git_commit': batch['git_commit'],
                'started_at_utc': datetime.now(UTC).isoformat(),
            }
            batch['cases'][case.case_id] = result
            try:
                session = start_workbench(client, case, args.data_root, seed=schedule['case_seed'])
                initial_tables = session.sandbox.native.snapshot()
                run_workbench_phase(session, case.prefix_prompt, turn=0)
                cp = session.checkpoint()
                save_gzip(directory / 'checkpoint.json.gz', cp)
                prefix_eval = case.evaluate_prefix(session.sandbox.native, initial_tables,
                                                   session.sandbox.logs)
                result['prefix'] = {'evaluation': prefix_eval, 'usage': usage(client.records),
                                    'checkpoint_sha256': digest(cp)}
                save(directory / 'result.json', result)
                if not prefix_eval['task_success']:
                    result['status'] = 'prefix_failed'
                    result['reason'] = 'No qualified shared prefix; all five post arms skipped.'
                    print(f'{case.case_id}: prefix failed; preserved, no selective retry.', flush=True)
                    continue
                before_future = session.sandbox.native.snapshot()
                branches = {}
                for arm in order:
                    fork = NativeHandoffSession.restore(cp, client, sandbox_cls=WorkbenchHandoffSandbox)
                    start = time.monotonic()
                    decision = fork.intervene(arm)
                    result['arms'][arm] = {
                        'status': 'decision_complete', 'decision': decision,
                        'decision_seconds': round(time.monotonic() - start, 6),
                        'checkpoint_sha256': digest(cp), 'topology_after': fork.spec.to_payload(),
                    }
                    branches[arm] = fork
                # The full future object includes evaluator-only expectations.
                # It is never attached to native state or passed into intervene.
                future = case.make_future(session.sandbox.native, schedule['future_seed'])
                save(directory / 'evaluator_future.json', future)
                for arm in order:
                    fork = branches[arm]
                    client.phase = arm
                    api_offset = len(client.records)
                    tool_offset = len(fork.sandbox.logs)
                    case.inject_future(fork.sandbox.native, future)
                    injected = fork.sandbox.native.snapshot()
                    start = time.monotonic()
                    outcome = run_workbench_phase(fork, future['public_prompt'], turn=1)
                    result['arms'][arm].update(
                        status='completed',
                        evaluation=case.evaluate_post(fork.sandbox.native, before_future, injected,
                                                      future, fork.sandbox.logs[tool_offset:]),
                        usage=usage(client.records[api_offset:]),
                        execution_seconds=round(time.monotonic() - start, 3),
                        actual_model_actors=sorted({e['agent_id'] for e in client.records[api_offset:]}),
                        post_output_artifact=outcome.output_artifact,
                        post_tool_log=fork.sandbox.logs[tool_offset:],
                    )
                    save_gzip(directory / f'{arm}_state.json.gz', fork.checkpoint())
                    if digest(cp) != result['prefix']['checkpoint_sha256']:
                        raise RuntimeError('shared_checkpoint_changed')
                    result['api_totals'] = usage(client.records)
                    save(directory / 'result.json', result)
                    batch['api_totals'] = usage(all_records + client.records)
                    save(args.output_dir / 'result.json', batch)
                    print(f'{case.case_id}/{arm}: '
                          f'{result["arms"][arm]["evaluation"]}', flush=True)
                result['status'] = 'completed'
            except Exception as exc:
                result.update(status='stopped', error_type=type(exc).__name__)
                raise  # Stop on infrastructure/budget/code failure, not model task failure.
            finally:
                result['api_totals'] = usage(client.records)
                result['finished_at_utc'] = datetime.now(UTC).isoformat()
                all_records.extend(client.records)
                batch['api_totals'] = usage(all_records)
                save(directory / 'result.json', result)
                save(args.output_dir / 'result.json', batch)
        batch['status'] = 'completed' if all(c['status'] == 'completed' for c in batch['cases'].values()) else 'completed_with_prefix_failures'
    except Exception as exc:
        batch.update(status='stopped', error_type=type(exc).__name__)
        raise
    finally:
        batch['finished_at_utc'] = datetime.now(UTC).isoformat()
        batch['post_executions_completed'] = sum(
            a.get('status') == 'completed' for c in batch['cases'].values() for a in c['arms'].values())
        save(args.output_dir / 'result.json', batch)


if __name__ == '__main__':
    main()

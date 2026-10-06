"""Audit saved WorkBench request totals and report paired development outcomes."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

from MAS.self_evolved.handoff_runtime import ARMS, digest
from scripts.run_handoff_smoke import save, usage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('batch_dir', type=Path)
    args = parser.parse_args()
    root = args.batch_dir
    batch = json.loads((root / 'result.json').read_text(encoding='utf-8'))
    if batch['status'] == 'running':
        raise RuntimeError('Wait for batch completion or explicit stop before final audit')
    all_journal = []
    checks = {}
    checks['frozen_sources_unchanged'] = all(
        hashlib.sha256(Path(p).read_bytes()).hexdigest() == expected
        for p, expected in batch['source_sha256'].items())
    checks['manifest_hash'] = hashlib.sha256((root / 'manifest.json').read_bytes()).hexdigest() == batch['manifest_sha256']
    wrapper_errors = []
    rows = []
    aggregate = {a: {'attempted': 0, 'success': 0, 'strict_success': 0,
                     'input_tokens': 0, 'output_tokens': 0, 'total_tokens': 0,
                     'api_attempts': 0, 'deployment_tokens_including_prefix': 0,
                     'duplicate_mutation_attempts': 0, 'state_changing_tool_calls': 0}
                 for a in ARMS}
    for case_id, result in batch['cases'].items():
        directory = root / case_id
        journal = json.loads((directory / 'api_journal.json').read_text(encoding='utf-8'))
        all_journal.extend(journal)
        checks[case_id + ':api_totals'] = usage(journal) == result['api_totals']
        checks[case_id + ':raw_usage'] = all(
            e.get('status') != 'completed' or (
                e['input_tokens'] == e['response']['usage']['prompt_tokens']
                and e['output_tokens'] == e['response']['usage']['completion_tokens'])
            for e in journal)
        if not result.get('prefix'):
            continue
        with gzip.open(directory / 'checkpoint.json.gz', 'rt', encoding='utf-8') as handle:
            checkpoint = json.load(handle)
        checks[case_id + ':checkpoint_hash'] = digest(checkpoint) == result['prefix']['checkpoint_sha256']
        checks[case_id + ':prefix_usage'] = usage([e for e in journal if e['phase'] == 'prefix']) == result['prefix']['usage']
        for event in checkpoint['sandbox']['logs']:
            output = event['result']
            if isinstance(output, dict) and output.get('ok') is False:
                wrapper_errors.append({'case': case_id, 'arm': 'prefix', 'tool': event['tool_name'],
                                       'error': output.get('error'), 'detail': output.get('detail')})
        prefix_tokens = result['prefix']['usage']['total_tokens']
        for arm, record in result['arms'].items():
            if record.get('status') != 'completed':
                continue
            expected_usage = usage([e for e in journal if e['phase'] == arm])
            checks[f'{case_id}:{arm}:usage'] = expected_usage == record['usage']
            checks[f'{case_id}:{arm}:shared_prefix'] = record['checkpoint_sha256'] == result['prefix']['checkpoint_sha256']
            with gzip.open(directory / f'{arm}_state.json.gz', 'rt', encoding='utf-8') as handle:
                state = json.load(handle)
            checks[f'{case_id}:{arm}:acl'] = state['sandbox']['authorized_agents'] == checkpoint['sandbox']['authorized_agents']
            if record['decision']['action'] != 'keep':
                checks[f'{case_id}:{arm}:retired_actor'] = 'agent_1' not in record['actual_model_actors']
            logs = record['post_tool_log']
            writes = [e for e in logs if e['state_changed']]
            checks[f'{case_id}:{arm}:authorized_writes'] = all(e['actor_active'] and e['actor_authorized'] for e in writes)
            for event in logs:
                output = event['result']
                if isinstance(output, dict) and output.get('ok') is False:
                    wrapper_errors.append({'case': case_id, 'arm': arm, 'tool': event['tool_name'],
                                           'error': output.get('error'), 'detail': output.get('detail')})
            item = aggregate[arm]
            item['attempted'] += 1
            item['success'] += int(record['evaluation']['task_success'])
            item['strict_success'] += int(record['evaluation']['strict_success'])
            item['duplicate_mutation_attempts'] += record['evaluation']['duplicate_mutation_attempts']
            item['state_changing_tool_calls'] += record['evaluation']['state_changing_tool_calls']
            for key in ('input_tokens', 'output_tokens', 'total_tokens', 'api_attempts'):
                item[key] += record['usage'][key]
            item['deployment_tokens_including_prefix'] += record['usage']['total_tokens'] + prefix_tokens
            rows.append({'case': case_id, 'arm': arm, 'decision': record['decision']['action'],
                         'evaluation': record['evaluation'], 'usage': record['usage']})
    checks['batch_api_totals'] = usage(all_journal) == batch['api_totals']
    comparisons = []
    for case_id, result in batch['cases'].items():
        keep = result['arms'].get('keep', {})
        full = result['arms'].get('handoff', {})
        if keep.get('status') == full.get('status') == 'completed':
            comparisons.append({'case': case_id, 'keep_success': keep['evaluation']['task_success'],
                                'handoff_success': full['evaluation']['task_success'],
                                'post_tokens_saved': keep['usage']['total_tokens'] - full['usage']['total_tokens']})
    summary = {
        'status': batch['status'], 'source_commit': batch['git_commit'],
        'case_status_counts': dict(Counter(c['status'] for c in batch['cases'].values())),
        'planned_post_executions': batch['planned_post_executions'], 'completed_post_executions': len(rows),
        'api_totals': batch['api_totals'], 'arms': aggregate, 'paired_keep_vs_handoff': comparisons,
        'rows': rows, 'wrapper_errors': wrapper_errors, 'audit_checks': checks,
        'response_finish_reasons': dict(Counter(
            choice.get('finish_reason', 'unknown') for e in all_journal
            for choice in e.get('response', {}).get('choices', []))),
        'returned_models': dict(Counter(e.get('model_returned', 'unknown') for e in all_journal)),
        'audit_all_passed': all(checks.values()),
        'scope': 'six modified WorkBench tasks, one repeat; descriptive development results only',
    }
    save(root / 'summary.json', summary)
    print(json.dumps({k:summary[k] for k in ('status','case_status_counts','completed_post_executions',
                                           'api_totals','arms','wrapper_errors','audit_all_passed')},
                     ensure_ascii=False, indent=2))
    if not all(checks.values()):
        raise RuntimeError('Saved artifact audit failed; inspect summary.json')


if __name__ == '__main__':
    main()

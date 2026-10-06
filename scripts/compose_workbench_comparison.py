"""Reference the predeclared complete case blocks without overwriting raw runs."""
from __future__ import annotations

import argparse
import ast
import json
import os
import subprocess
import time
from pathlib import Path

from scripts.run_handoff_smoke import save

FIRST = ('calendar_20', 'calendar_40', 'email_31')
LAST = ('email_53', 'project_management_2', 'project_management_40')


def compose(first, supplement, output):
    old = json.loads((first / 'result.json').read_text(encoding='utf-8'))
    new = json.loads((supplement / 'result.json').read_text(encoding='utf-8'))
    if tuple(new['planned_cases']) != LAST:
        raise ValueError('Supplement must contain the three predeclared full cases')
    if any(old['cases'][c]['status'] != 'completed' for c in FIRST):
        raise ValueError('First three blocks must be complete before composition')
    differing = {p for p in old['source_sha256']
                 if old['source_sha256'][p] != new['source_sha256'].get(p)}
    saver_file = 'scripts/run_handoff_smoke.py'
    if differing - {'scripts/run_workbench_retirement.py', saver_file}:
        raise ValueError(f'Core implementation changed across blocks: {sorted(differing)}')
    if saver_file in differing:
        trees = []
        for commit in (old['git_commit'], new['git_commit']):
            code = subprocess.check_output(['git', 'show', f'{commit}:{saver_file}'])
            tree = ast.parse(code.decode('utf-8'))
            tree.body = [n for n in tree.body if not (isinstance(n, ast.FunctionDef) and n.name == 'save')]
            trees.append(ast.dump(tree, include_attributes=False))
        if trees[0] != trees[1]:
            raise ValueError('Metered client changed beyond the save function')
    allowed_changes = {'max_api_attempts_per_case', 'max_input_tokens_per_case'}
    if any(old['configuration'][k] != new['configuration'].get(k)
           for k in old['configuration'] if k not in allowed_changes):
        raise ValueError('Per-arm execution configuration changed')
    if old['seed'] != new['seed']:
        raise ValueError('Seed changed')
    result = {
        'schema_version': 1, 'label': 'interim_block_comparison',
        'status': new['status'], 'git_commit': new['git_commit'],
        'source_commits': [old['git_commit'], new['git_commit']],
        'source_sha256': new['source_sha256'], 'manifest_sha256': new['manifest_sha256'],
        'planned_cases': list(FIRST + LAST), 'planned_post_executions': 30,
        'seed': new['seed'], 'core_source_hashes_match': True,
        'provenance_note': 'First three complete v2 blocks plus the supplemental batch; '
            'supplement changes only aggregate case budget, runner selection and bounded log-save retries. '
            'This is not one uninterrupted run. v2 email_53 is excluded in full, '
            'including its successful arms, and retained in development costs. '
            'Per-case status distinguishes completed, running and stopped blocks.',
        'logger_change_is_save_only': True,
        'source_batches': [os.path.relpath(p, output).replace('\\', '/') for p in (first, supplement)],
        'cases': {}, 'case_artifact_dirs': {}, 'configuration_by_case': {},
        'api_totals': {k: 0 for k in ('api_attempts', 'api_responses', 'input_tokens',
                                    'output_tokens', 'total_tokens')},
    }
    for ids, batch, directory in ((FIRST, old, first), (LAST, new, supplement)):
        for case in ids:
            if case not in batch['cases']:
                continue
            result['cases'][case] = batch['cases'][case]
            result['case_artifact_dirs'][case] = os.path.relpath(directory / case, output).replace('\\', '/')
            result['configuration_by_case'][case] = batch['configuration']
            for key in result['api_totals']:
                result['api_totals'][key] += batch['cases'][case].get('api_totals', {}).get(key, 0)
    result['api_totals']['billed_cost_usd'] = None
    result['post_executions_completed'] = sum(
        a.get('status') == 'completed' for c in result['cases'].values() for a in c['arms'].values())
    complete = len(result['cases']) == 6 and all(
        c['status'] == 'completed' and len(c['arms']) == 5
        and all(a.get('status') == 'completed' for a in c['arms'].values())
        for c in result['cases'].values())
    result['comparison_is_complete'] = complete
    if new['status'] == 'completed' and not complete:
        raise ValueError('Completed comparison requires six complete five-arm blocks')
    if complete:
        result['label'] = 'explicit_complete_block_comparison'
    output.mkdir(parents=True, exist_ok=True)
    (output / 'manifest.json').write_bytes((supplement / 'manifest.json').read_bytes())
    save(output / 'result.json', result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--first', required=True, type=Path)
    parser.add_argument('--supplement', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--watch', action='store_true')
    args = parser.parse_args()
    while True:
        result = compose(args.first, args.supplement, args.output)
        if not args.watch or result['status'] != 'running':
            print(json.dumps({'status': result['status'],
                              'completed': result['post_executions_completed'],
                              'core_source_hashes_match': True}))
            return
        time.sleep(15)


if __name__ == '__main__':
    main()

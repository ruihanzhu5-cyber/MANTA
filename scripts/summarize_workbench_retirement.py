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
        directory = root / batch.get('case_artifact_dirs', {}).get(case_id, case_id)
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
        'source_commits': batch.get('source_commits', [batch['git_commit']]),
        'provenance_note': batch.get('provenance_note'),
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
    names = dict(zip(ARMS, ('保留', '直接删除', '简单保护', '检查但不交接', '检查并交接')))
    provenance = [
        '来源说明：前三个case取自v2，其余case取自result.json明确引用的补充批次；完整性以逐例状态为准。',
        '补充批次提高整例请求/输入预算、支持按原索引选取任务，并修复日志保存遇短暂文件占用时的重试；各组模型、轮数、工具循环、权限、提示词与评分相同。',
        '原v2的email_53因预算中断，其全部分组仅作诊断；补充批次重新运行该例五组，不挑选单组替换。',
        '这是明确记录来源的分批比较，不能写成一次不中断的完整运行。各case原始路径见result.json。', '',
    ] if batch.get('source_commits') else []
    report = [
        '# WorkBench 六例节点退出实验报告', '',
        f"批次：`{root.name}`；来源源码：`{', '.join(batch.get('source_commits', [batch['git_commit']]))}`。",
        f"状态：`{batch['status']}`；已完成 {len(rows)} / {batch['planned_post_executions']} 次退出决定后的新任务执行。", '',
        *provenance,
        '## 配置与判分', '',
        '六个冻结来源任务，各运行一次，比较五种处理方式。每个任务先真实执行退出前工作，',
        '保存同一个状态，再复制成五组。所有退出决定完成后，才生成并发布相同的新请求。',
        '使用 DeepSeek Flash，temperature=0，thinking disabled，单请求输出上限768，',
        '每个成员阶段最多10次工具循环。固定5人星形团队、候选agent_1；备份agent_2原本就有写权限。',
        '评分比较真实业务表与独立期望状态，并要求新阶段发生真实工具写入。',
        '严格通过还要求没有重复写入尝试且实际变更次数符合预期；不代表所有调用均无错误。', '',
        '## 各组结果', '',
        '以下 token 和请求数仅计退出决定后的执行；包含失败执行，不等于每个成功任务的成本。', '',
        '| 处理方式 | 任务成功/已执行 | 严格通过 | 输入 token | 输出 token | 总 token | API 请求 |',
        '| --- | ---: | ---: | ---: | ---: | ---: | ---: |',
    ]
    for arm, value in aggregate.items():
        report.append(f"| {names[arm]} | {value['success']}/{value['attempted']} | {value['strict_success']}/{value['attempted']} | {value['input_tokens']:,} | {value['output_tokens']:,} | {value['total_tokens']:,} | {value['api_attempts']} |")
    report += ['', '## 固定任务编号与逐例结果', '',
               '编号末尾是原始CSV从0开始的行号；不是工具中的业务记录ID。', '',
               '| 来源 case | 退出前任务 | 保留 | 直接删除 | 简单保护 | 检查 | 交接 |',
               '| --- | --- | --- | --- | --- | --- | --- |']
    for case_id in batch['planned_cases']:
        result = batch['cases'].get(case_id, {})
        prefix = result.get('prefix', {}).get('evaluation', {}).get('task_success')
        cells = [case_id, '通过' if prefix is True else '未通过' if prefix is False else '未完成']
        for arm in ARMS:
            evaluation = result.get('arms', {}).get(arm, {}).get('evaluation', {})
            success = evaluation.get('task_success')
            cells.append('通过' if success is True else '未通过' if success is False else '未判分')
        report.append('| ' + ' | '.join(cells) + ' |')
    report += ['', '## 成本与记录核验', '',
               f"本批次含共享退出前执行：{batch['api_totals']['api_attempts']} 次API请求，输入 {batch['api_totals']['input_tokens']:,}、输出 {batch['api_totals']['output_tokens']:,}，共 {batch['api_totals']['total_tokens']:,} tokens。",
               '共享退出前执行在实际账单统计中每例只计一次；单独部署某组时应再加该例完整退出前成本。',
               '没有提供美元账单金额；不依据token数猜测实际付费。',
               '这是纳入比较的案例用量；全部开发、失败和中断消耗另见实验台账，不包含在这张分组比较表中。',
               f"保存记录的核验：{sum(checks.values())}/{len(checks)} 项通过。",
               f"模型响应终止原因：`{json.dumps(summary['response_finish_reasons'], ensure_ascii=False)}`。length表示输出达到上限。",
               f"记录到的结构化工具错误：{len(wrapper_errors)} 次（包含退出前执行）；详情见summary.json。", '',
               '## 可以解释到什么程度', '',
               '这是改造后的WorkBench任务的小规模开发比较，不是原版WorkBench成绩。',
               '交接更新中央职责owner并保留公共进度，未迁移私有记忆或在途任务。',
               '直接删除组仍可由原本有权限的成员自行恢复；owner不是权限门槛。',
               '当前未检验自动候选选择、自动组队修复循环或独立审核安全收益。',
               '每例只有一次真实模型执行；温度0仍可能变化，不能据此宣称普遍成本或可靠性优势。',
               '旧版排错记录保留在v1目录及STOPPED.json，未混入本批成功率或token比较。', '',
               '下一轮建议见 [系统迭代方案](../../../docs/node-retirement-next-iteration.md)。', '']
    (root / 'REPORT.md').write_text('\n'.join(report), encoding='utf-8')
    print(json.dumps({k:summary[k] for k in ('status','case_status_counts','completed_post_executions',
                                           'api_totals','arms','wrapper_errors','audit_all_passed')},
                     ensure_ascii=False, indent=2))
    if not all(checks.values()):
        raise RuntimeError('Saved artifact audit failed; inspect summary.json')


if __name__ == '__main__':
    main()

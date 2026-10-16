"""Summarize saved live ablation episodes without making model or benchmark calls."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from run_context_topology_ablation import RESULTS, TASKS, VARIANTS, _result_dir

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "reports" / "context_topology_ablation_pilot.md"
SUMMARY = RESULTS / "summary.csv"
CASES = RESULTS / "failure_cases.md"
FIELDS = [
    "task_id", "variant", "seed", "run_id", "complete", "strict_comparison_valid",
    "needs_rerun", "failed_model_generations", "success", "score",
    "correct", "exact_match", "unwanted_side_effects", "token_in", "token_out",
    "cost_upper_usd", "trace_latency_ms_sum", "mutation_planner_token_in",
    "mutation_planner_token_out", "turns_executed", "audit_sources", "repair_recommended", "mutation_proposed",
    "mutation_applied", "effective_structural_change", "effective_context_policy_change",
    "raw_policy_map_changed",
    "initial_agent_count", "final_agent_count", "initial_group_pattern", "final_group_pattern",
    "handoff_records", "tool_calls", "duplicate_tool_calls", "communication_count", "handoff_count",
    "empty_completion_count", "raw_dir",
]


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _usage(path: Path) -> tuple[int, int, float, int, int]:
    total_in = total_out = 0
    latency_ms = 0.0
    planner_in = planner_out = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        item = json.loads(line)
        item_in = int(item.get("token_in") or 0)
        item_out = int(item.get("token_out") or 0)
        total_in += item_in
        total_out += item_out
        latency_ms += float(item.get("latency_ms") or 0)
        if item.get("actor") == "topology_planner" and item.get("event_type") == "revise":
            planner_in += item_in
            planner_out += item_out
    return total_in, total_out, latency_ms, planner_in, planner_out


def _arm(task_id: str, variant: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]] | None:
    path = _result_dir(task_id, variant)
    needed = [path / f"run_0.{suffix}" for suffix in ("metadata.json", "eval.json", "trace.jsonl")]
    if not all(file.is_file() for file in needed):
        return None
    metadata, evaluation = _json(needed[0]), _json(needed[1])
    tokens_in, tokens_out, latency_ms, planner_in, planner_out = _usage(needed[2])
    communications = int(metadata.get("messages_sent_total") or 0)
    handoffs = sum(len(item.get("visible_messages") or []) for item in metadata.get("interaction_logs") or [])
    evolved = metadata.get("self_evolved") or {}
    specs = evolved.get("topology_spec_versions") or []
    initial = specs[0] if specs else {}
    final = specs[-1] if specs else {}
    mutations = evolved.get("mutations") or []
    changed_existing_policy = False
    for before, after in zip(specs, specs[1:]):
        before_policies = {node["agent_id"]: node.get("context") for node in before.get("agents", [])}
        after_policies = {node["agent_id"]: node.get("context") for node in after.get("agents", [])}
        changed_existing_policy |= any(
            before_policy != after_policies[agent_id]
            for agent_id, before_policy in before_policies.items()
            if agent_id in after_policies
        )
    details = evaluation.get("details") or {}
    calls = [
        (call.get("tool_name"), json.dumps(call.get("arguments") or {}, sort_keys=True, default=str))
        for item in metadata.get("interaction_logs") or []
        for call in item.get("tool_calls") or []
    ]
    row = {
        "task_id": task_id,
        "variant": variant,
        "seed": metadata.get("seed"),
        "run_id": "run_0",
        "complete": True,
        "strict_comparison_valid": not bool(metadata.get("needs_rerun")) and all(
            (item.get("llm", {}).get("metadata") or {}).get("generation_status") != "failed"
            for item in metadata.get("interaction_logs") or []
        ),
        "needs_rerun": bool(metadata.get("needs_rerun", False)),
        "failed_model_generations": sum(
            (item.get("llm", {}).get("metadata") or {}).get("generation_status") == "failed"
            for item in metadata.get("interaction_logs") or []
        ),
        "success": evaluation.get("success"),
        "score": evaluation.get("score"),
        "correct": details.get("correct"),
        "exact_match": details.get("exact_match"),
        "unwanted_side_effects": details.get("unwanted_side_effects"),
        "token_in": tokens_in,
        "token_out": tokens_out,
        "cost_upper_usd": round((tokens_in * 0.30 + tokens_out * 1.20) / 1_000_000, 6),
        "trace_latency_ms_sum": round(latency_ms, 2),
        "mutation_planner_token_in": planner_in,
        "mutation_planner_token_out": planner_out,
        "turns_executed": metadata.get("turns_executed"),
        "audit_sources": ",".join(
            str(a.get("source", "unknown")) for a in evolved.get("audit_reports", [])
        ),
        "repair_recommended": any(bool(a.get("repair_recommended")) for a in evolved.get("audit_reports", [])),
        "mutation_proposed": bool(evolved.get("mutation_proposals")),
        "mutation_applied": any(bool(m.get("applied_mutation")) for m in mutations),
        "effective_structural_change": any(bool(m.get("effective_structural_change")) for m in mutations),
        "effective_context_policy_change": changed_existing_policy,
        "raw_policy_map_changed": any(bool(m.get("effective_context_policy_change")) for m in mutations),
        "initial_agent_count": len(initial.get("agents", [])),
        "final_agent_count": len(final.get("agents", [])),
        "initial_group_pattern": ",".join(g.get("pattern", "") for g in initial.get("groups", [])),
        "final_group_pattern": ",".join(g.get("pattern", "") for g in final.get("groups", [])),
        "handoff_records": len(metadata.get("evidence_handoff_log") or []),
        "tool_calls": len(calls),
        "duplicate_tool_calls": len(calls) - len(set(calls)),
        "communication_count": communications,
        "handoff_count": handoffs,
        "empty_completion_count": (
            (RESULTS / "logs" / f"ctx_topo_{task_id}_{variant}.runner.log")
            .read_text(encoding="utf-8", errors="replace")
            .count("reason=empty_completion")
        ),
        "raw_dir": str(path),
    }
    return row, metadata, evaluation


def _short(value: Any, max_chars: int = 400) -> str:
    rendered = json.dumps(value, ensure_ascii=False, default=str)
    return rendered[:max_chars] + ("…" if len(rendered) > max_chars else "")


def _action_chain(metadata: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    artifacts = {item.get("artifact_id"): item for item in metadata.get("artifact_records") or []}
    mutating = {
        "customer_relationship_manager.add_customer",
        "customer_relationship_manager.update_customer",
    }
    for entry in metadata.get("interaction_logs") or []:
        for call in entry.get("tool_calls") or []:
            if call.get("tool_name") not in mutating:
                continue
            prompt = entry.get("prompt_messages") or []
            stage_input = prompt[-1].get("content", "") if prompt else ""
            visible = entry.get("visible_messages") or []
            upstream = []
            for packet in visible[:8]:
                artifact = artifacts.get(packet.get("artifact_id")) or {}
                upstream.append(
                    {
                        "message_id": packet.get("message_id"),
                        "sender": packet.get("sender"),
                        "artifact_id": packet.get("artifact_id"),
                        "packet_summary": (packet.get("payload") or {}).get("summary"),
                        "source_tool_observations": [
                            {"tool": tool.get("tool_name"), "arguments": tool.get("arguments"),
                             "status": tool.get("status"), "output_excerpt": _short(tool.get("output"), 180)}
                            for tool in (artifact.get("tool_records") or [])[:5]
                        ],
                        "handoff_in_prompt": bool((packet.get("payload") or {}).get("evidence_handoff")),
                    }
                )
            records.append(
                {
                    "agent": entry.get("agent_id"),
                    "phase": entry.get("phase"),
                    "round": entry.get("round_index"),
                    "tool": call.get("tool_name"),
                    "arguments": call.get("arguments"),
                    "status": call.get("status"),
                    "output_preview": call.get("output_preview"),
                    "visible_packet_ids": [p.get("message_id") for p in entry.get("visible_messages") or []],
                    "upstream": upstream,
                    "prompt_evidence_handoff_present": '"evidence_handoff"' in stage_input,
                    "prompt_receives_original_task": "Alex Anderson" in stage_input or "lead" in stage_input.lower(),
                }
            )
    return records


def write_outputs() -> None:
    collected: dict[tuple[str, str], tuple[dict[str, Any], dict[str, Any], dict[str, Any]]] = {}
    rows: list[dict[str, Any]] = []
    for task_id in TASKS:
        for variant in VARIANTS:
            data = _arm(task_id, variant)
            if data is not None:
                collected[(task_id, variant)] = data
                rows.append(data[0])
            else:
                rows.append({"task_id": task_id, "variant": variant, "seed": TASKS[task_id]["seed"], "run_id": "run_0", "complete": False})
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    with SUMMARY.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    cases = ["# WorkBench Case Index", "", "Saved raw files provide the source of truth. Tool actions below are the actual interaction log calls; the official evaluation remains unchanged.", ""]
    for task_id in TASKS:
        for variant in VARIANTS:
            data = collected.get((task_id, variant))
            if data is None:
                cases.extend([f"## {task_id} / {variant}", "", "Incomplete: no valid saved episode.", ""])
                continue
            row, metadata, evaluation = data
            path = Path(row["raw_dir"])
            actions = _action_chain(metadata)
            handoffs = metadata.get("evidence_handoff_log") or []
            mutations = (metadata.get("self_evolved") or {}).get("mutations") or []
            merge_entries = [
                item for item in metadata.get("interaction_logs") or []
                if str(item.get("phase", "")).endswith("_merge")
            ]
            last_merge = merge_entries[-1] if merge_entries else {}
            source_links = ", ".join(
                f"[{name}]({(path / name).as_posix()})"
                for name in ("run_0.trace.jsonl", "run_0.metadata.json", "run_0.eval.json")
            )
            cases.extend([
                f"## {task_id} / {variant} / run_0 / seed {row['seed']}", "",
                f"- Source: {source_links}.",
                f"- Official result: success={row['success']}, score={row['score']}, correct={row['correct']}, exact_match={row['exact_match']}, unwanted_side_effects={row['unwanted_side_effects']}.",
                f"- Topology: {row['initial_group_pattern']} ({row['initial_agent_count']} agents) → {row['final_group_pattern']} ({row['final_agent_count']} agents); effective structural change={row['effective_structural_change']}; policy change={row['effective_context_policy_change']}.",
                f"- Evidence handoffs appended to already visible packets: {len(handoffs)}. First record: `{_short(handoffs[0]) if handoffs else 'none'}`.",
                f"- Mutation provenance: `{_short(mutations[0], 900) if mutations else 'none'}`.",
                f"- Final committer: {last_merge.get('agent_id', 'unknown')}; artifact `{(last_merge.get('structured_artifact') or {}).get('artifact_id', 'unknown')}`. Its final answer: `{_short((last_merge.get('structured_artifact') or {}).get('answer', ''), 1000)}`.",
                "- Packets actually visible to the final committer:", "",
            ])
            if last_merge.get("visible_messages"):
                for packet in last_merge["visible_messages"][:8]:
                    cases.append(
                        f"  - `{packet.get('message_id')}` {packet.get('sender')} → {last_merge.get('agent_id')}, kind={packet.get('kind')}, artifact={packet.get('artifact_id')}; content: `{_short(packet.get('content', ''), 550)}`"
                    )
            else:
                cases.append("  - None recorded.")
            cases.extend([
                "- CRM write attempts and corresponding downstream input:", "",
            ])
            if actions:
                for action in actions[:6]:
                    upstream = action.pop("upstream")
                    cases.append(f"  - Downstream action: `{_short(action, 1000)}`")
                    for packet in upstream[:5]:
                        cases.append(f"    - Upstream packet and source evidence: `{_short(packet, 900)}`")
            else:
                cases.append("  - None recorded by the interaction log.")
            cases.extend([
                "",
                f"- Relay messages: {len(metadata.get('relay_messages') or [])}; all original packets and exact prompt messages are in metadata. Official evaluator detail: `{_short({k: v for k, v in (evaluation.get('details') or {}).items() if k not in {'ground_truth', 'prediction', 'run_metadata_summary'}}, 850)}`.",
                "",
            ])
    CASES.write_text("\n".join(cases).rstrip() + "\n", encoding="utf-8")

    complete = len(collected)
    total_upper = sum(float(row.get("cost_upper_usd") or 0) for row in rows)
    ledger_path = RESULTS / "cost_ledger.json"
    ledger = _json(ledger_path) if ledger_path.is_file() else {}
    interruption_reserve = sum(
        float(item.get("cost_reserve_usd") or 0)
        for item in ledger.get("interrupted_attempts") or []
    )
    run_lines = ["| Task | Arm | Strict valid | Success | Score | Correct | Exact | Unwanted | Tokens in/out | Cost upper USD | Turns | Effective topology | Handoff records | Repeated tool calls |", "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for row in rows:
        run_lines.append(
            f"| {row['task_id']} | {row['variant']} | {row.get('strict_comparison_valid', '')} | {row.get('success', 'pending')} | {row.get('score', '')} | {row.get('correct', '')} | {row.get('exact_match', '')} | {row.get('unwanted_side_effects', '')} | {row.get('token_in', '')}/{row.get('token_out', '')} | {row.get('cost_upper_usd', '')} | {row.get('turns_executed', '')} | {row.get('effective_structural_change', '')} | {row.get('handoff_records', '')} | {row.get('duplicate_tool_calls', '')} |"
        )
    report = [
        "# MANTA Context × Topology WorkBench Pilot", "",
        f"Status: {complete}/8 saved real episodes. Research branch `research/context-topology-ablation`. Seeds: task 12 = 12042, task 16 = 16042.", "",
        "## 中文摘要", "",
        "8 组真实 DeepSeek Flash 运行及官方 WorkBench 评测均已保存，两个任务的四组得分全部为 0。Topology 组确实在运行中增员，并让新增 Agent 执行工具和传递消息；Context 组的结构化证据也确实进入下游提示词。然而，这两个任务没有出现额外的任务成功。`multi_domain_16` 固定基线发生错误 CRM 写入，其他三组没有该副作用，但仍未完成任务；不能把这组观察直接解释为 Context 或 Topology 的因果收益。", "",
        "主要瓶颈更接近任务语义与写入前动作校验：汇总 Agent 已收到上游消息，却把“逾期任务”解释为 CRM 跟进日期，或因同名 `Won` 客户而决定不创建 `Lead`。四组存在模型空回复后的生成退化，且历史模型别名无法锁定底层版本；本报告保留这些运行的轨迹与官方得分，但不用于严格消融推断。下一步优先研究有来源的证据交接、任务约束核查与工具动作验证；只有找到真正能提供独立证据的替代通信路径，再研究拓扑收益。", "",
        "## Design and provenance", "",
        "B0 fixed baseline; B1 evidence handoff only; B2 structural mutation only; B3 combined. The first TopologySpec for each task was frozen from the historical pre-execution version, with its hash in `results/context_topology_ablation/manifest.json`. All four arms of each task share the same initial agent set, pattern, context policy, task, seed, DeepSeek Flash route, WorkBench sandbox, and official evaluator. The historical planner call is a shared preparation artifact and incurred no new API charge in this pilot. All arms have up to two turns and one audit-triggered repair opportunity. Fixed arms use KEEP_TOPOLOGY when repair is warranted. Dynamic arms exclude proposed `set_context_policy` operations so structural changes and handoff are separate factors.", "",
        "Historical `experiment_settings.json` records model alias `deepseek-flash` at `https://api.deepseek.com`; the pilot uses that same alias and route and rejects mock usage in both trace and interaction metadata. The provider's [current pricing/model page](https://api-docs.deepseek.com/quick_start/pricing/) identifies the alias as DeepSeek-V4.1-Flash. Historical settings do not pin a backend model snapshot, so exact backend-version equivalence to 2026-10-05 cannot be established.", "",
        "## Official results and measured usage", "",
        *run_lines, "",
        f"Sum of completed episode cost upper bounds: ${total_upper:.6f}. This is an estimate from actual trace input/output tokens at the published peak uncached DeepSeek Flash rates ($0.30/M input, $1.20/M output), not an API-billed dollar amount. The API returns usage but no billed cost. Preflight usage is recorded separately in `cost_ledger.json`.", "",
        f"Interrupted attempts: {len(ledger.get('interrupted_attempts') or [])}; conservative extra cost reserve ${interruption_reserve:.2f}. The interrupted call sequence is excluded from the outcome table. See `cost_ledger.json` and its archived runner log for the observed completed-call tokens; in-flight usage and actual billed dollars are unknown.", "",
        "## Case-level trace index", "",
        f"See `{CASES.relative_to(ROOT)}` for each saved run's mutation, evidence handoff, downstream CRM action, and official result. Exact source messages and prompts are retained in the original metadata/trace, not reconstructed from the final answer.", "",
        "### Historical auxiliary control (outside the 8-run pilot)", "",
        "Historical `multi_domain_12/run_1` (seed 12043) received official success=true, score=1.0, with no unwanted side effects. Its interaction log records a completed `customer_relationship_manager.add_customer` call for Alex Anderson with `assigned_to_email=anaya.patel@atlas.com` and `status=Lead`. The final prediction nevertheless says no successful CRM create/update evidence appears. This is a confirmed final synthesis/receipt inconsistency in a successful run, not a failed pilot arm and not proof that the present handoff mechanism repairs it. Source: `D:\\MANTA_DATA\\experiments\\manta_dsflash_workbench6_20261005_2145_w2\\workbench\\self_evolved\\multi_domain_12\\run_1.metadata.json` and `run_1.eval.json` in the same directory.", "",
        "## Interpretation guardrails", "",
        "A mutation proposal or changed version number alone is not an effective structure change. The logged effective flag compares final post-transaction agent/group/edge structure. Transactional Star and exactly-once restrictions remain active. For context policy, the CSV compares policies of agents present in both adjacent specs; the raw engine `effective_context_policy_change` flag can turn true merely because new agents bring new default policy entries, which is shown separately as `raw_policy_map_changed`. `Repeated tool calls` counts exact repeated (tool name, arguments) pairs across logged interactions; it is not a token estimate. Communication count is recorded relay messages, while handoff count is visible packet appearances in downstream interaction logs. `Strict valid=false` means the saved real episode had a failed model generation or `needs_rerun`; the official eval is still shown, but that arm is excluded from clean 2×2 conclusions and was not silently rerun. The pilot has one seed per task and no paired deterministic model outputs; any outcome differences are exploratory rather than causal proof. An added verifier or second turn can add reasoning and token cost. A wrong tool call is an ordinary task error unless separately shown to be an attack.", "",
        "## RQ1 and RQ2", "",
        "The case-level assessment below uses saved upstream artifacts, visible relay packets, the committer prompt, actual tool calls, and the unchanged official evaluator. These are observations on one seed per task, not a deterministic replay or an estimated treatment effect.", "",
    ]
    if complete == 8:
        report.extend([
            "### Historical failure and replay scope", "",
            "The 2026-10-05 historical `multi_domain_12/run_0` really called `customer_relationship_manager.add_customer` for Alex Anderson with `assigned_to_email=yuki.tanaka@atlas.com`; its official result was score 0 with unwanted side effects. Historical `multi_domain_16/run_0` likewise created Taylor Brown assigned to Yuki and scored 0 with unwanted side effects. The pilot freezes each historical pre-execution TopologySpec and seed, but live model sampling did not reproduce those exact writes. In the pilot every `multi_domain_12` arm made no CRM write; only `multi_domain_16/B0` made a CRM write. Thus the pilot reuses the real tasks and initial graphs, but it is not an exact replay of the old failure sequence.", "",
            "### Failure chain 1 — Alex Anderson (`multi_domain_12`)", "",
            "In pilot B0, agent_1 and agent_2 searched CRM and project tasks, then their artifacts `se_g_transaction_work:agent_1:0:0:4` and `se_g_transaction_work:agent_2:0:0:4` reached agent_0 as relay packets `m_3` and `m_4`, alongside the existing evidence digest. The committer saw the existing Alex Anderson record (`customer_id=00000143`, status `Won`) and chose no create call; the second turn repeated this decision. B1 added eight structured handoff records to already visible packets; B2 actually expanded from 3 to 6 agents; B3 added a verifier (3 to 4) and delivered seven handoffs. All four arms still made no CRM write and received score 0, with no unwanted side effects. The observed pilot failure is a duplicate/precondition decision and unresolved owner ranking, rather than a demonstrated missing relay path. B1 and B2 contain failed generations and cannot support a clean pairwise claim.", "",
            "### Failure chain 2 — Taylor Brown (`multi_domain_16`)", "",
            "B0 is the clearest incorrect downstream action. Before agent_0 called `customer_relationship_manager.add_customer({customer_name: 'Taylor Brown', status: 'Lead', assigned_to_email: 'sofia.santos@atlas.com'})`, its input already included agent_1 packet `m_3`, agent_2 packet `m_4`, and an evidence digest. Agent_2 explicitly proposed Sofia after counting CRM `follow_up_by` dates; agent_0's final artifact repeated that CRM follow-up rationale. The official evaluator returned score 0 and `unwanted_side_effects=true`. This establishes a received-but-misinterpreted or unsupported action chain, not simple loss of an upstream message. It does not establish which assignee would have been correct without relying on benchmark ground truth.", "",
            "B1 delivered four structured handoffs into legal visible packets and made no CRM write, because its committer found the pre-existing Taylor Brown record (`customer_id=00000023`, status `Won`). B2 added two agents through `expand_agent_to_group` (3 to 5) and made no write. B3 also expanded from 3 to 5, delivered 12 handoff records, and made no write; new agents `agent_3` and `agent_4` queried earlier project due dates, relayed packets `m_11` and `m_12` to agent_0, and the final committer still concluded duplicate-driven no-op. B1/B2/B3 all scored 0 with no unwanted side effects. The changed behavior is observable; it cannot be attributed uniquely to the switches because model outputs vary and B2/B3 had failed generations.", "",
            "### RQ1 — Context preservation", "",
            "MANTA already relays specialist reports and an evidence digest to the transactional committer. The new handoff preserves bounded tool observations and executed-action receipts with source artifact/agent/round references, only inside packets the receiver could already see; prompt inspection confirms receipt in Context-enabled runs, including after agent additions. It is useful for provenance and for the historical successful `multi_domain_12/run_1` final receipt mismatch. In these two pilot failures, however, there is no confirmed case where the required evidence existed upstream but was absent from the committer's legal input and then restored by B1. Neither task succeeded under Context-only. On `multi_domain_16`, B1 avoided B0's unwanted write, but both scored 0; this is a safer observed outcome, not a validated repair of task completion.", "",
            "### RQ2 — Topology contribution", "",
            "Structural mutation was actually applied in all four Topology-enabled episodes: `multi_domain_12/B2` 3→6 by `expand_agent_to_group`, `multi_domain_12/B3` 3→4 by `add_agent`, and both `multi_domain_16/B2` and `B3` 3→5 by `expand_agent_to_group`. Added agents executed tools and sent packets. The group remained transactional `star`; no `set_context_policy` was applied to any pre-existing agent. Proposed Context Policy operations are excluded from this 2×2 design. The raw engine policy-map-change flag also turns true when added agents introduce default policy entries; the CSV's `effective_context_policy_change` correctly reports false for existing agents.", "",
            "No Topology-enabled arm improved official success: all eight scores are 0. In `multi_domain_12`, B2 used 1,634,677 input tokens and 463 tool calls versus B0's 675,106 and 263, with no success gain. In `multi_domain_16`, B2 used 1,391,167 input tokens and 400 calls versus B1's 468,927 and 148; B3 used 587,261 input tokens and 215 calls. Exact repeated tool-call pairs remain common (B2: 263; B3: 136). The new paths mostly repeated CRM/PM searches or checked empty earlier date ranges; the trace does not show a distinct missing fact becoming actionable through an alternative path. B0/B1 on `multi_domain_16` stopped after one turn while B2/B3 took two, so extra reasoning opportunities and tokens are also confounders. There is no observable additional task-success benefit from Topology in this pilot, and no basis for a causal performance-decline claim.", "",
            "### Auditor signals and next research choice", "",
            "The saved Audit sources for both `multi_domain_16` dynamic arms are `heuristic`; their logs show repeated empty DeepSeek completions. Signals such as `tool_error_cascade`, `branch_collapse`, and `message_compaction_loss` should therefore be treated as repair hypotheses, not verified root causes. Adding workers after those signals did not resolve the task. Four of eight episodes have `needs_rerun` or failed model generations and are excluded from strict 2×2 inference; the complete official evaluations are retained without paid reruns.", "",
            "For the next SecurityAdaptiveMAS study, prioritize task interpretation and tool-action validation: check whether the requested 'overdue tasks' metric maps to PM tasks or CRM follow-ups, whether an existing `Won` person permits or blocks creating a new `Lead`, whether a candidate owner is supported by complete rather than truncated search results, and whether a final answer accurately acknowledges successful writes. A bounded provenance handoff can support that validation. Further topology research is warranted only on cases with a demonstrated alternative authorized communication path and independently useful evidence; these two pilot tasks do not yet supply it. There is no prompt-injection or attacker evidence here, so ordinary wrong actions should not be labeled security attacks.", "",
        ])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(report), encoding="utf-8")
    print(f"Wrote {SUMMARY}, {CASES}, {REPORT} ({complete}/8 complete)")


if __name__ == "__main__":
    write_outputs()

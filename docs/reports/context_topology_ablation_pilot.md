# MANTA Context × Topology WorkBench Pilot

Status: 8/8 saved real episodes. Research branch `research/context-topology-ablation`. Seeds: task 12 = 12042, task 16 = 16042.

## 中文摘要

8 组真实 DeepSeek Flash 运行及官方 WorkBench 评测均已保存，两个任务的四组得分全部为 0。Topology 组确实在运行中增员，并让新增 Agent 执行工具和传递消息；Context 组的结构化证据也确实进入下游提示词。然而，这两个任务没有出现额外的任务成功。`multi_domain_16` 固定基线发生错误 CRM 写入，其他三组没有该副作用，但仍未完成任务；不能把这组观察直接解释为 Context 或 Topology 的因果收益。

主要瓶颈更接近任务语义与写入前动作校验：汇总 Agent 已收到上游消息，却把“逾期任务”解释为 CRM 跟进日期，或因同名 `Won` 客户而决定不创建 `Lead`。四组存在模型空回复后的生成退化，且历史模型别名无法锁定底层版本；本报告保留这些运行的轨迹与官方得分，但不用于严格消融推断。下一步优先研究有来源的证据交接、任务约束核查与工具动作验证；只有找到真正能提供独立证据的替代通信路径，再研究拓扑收益。

## Design and provenance

B0 fixed baseline; B1 evidence handoff only; B2 structural mutation only; B3 combined. The first TopologySpec for each task was frozen from the historical pre-execution version, with its hash in `results/context_topology_ablation/manifest.json`. All four arms of each task share the same initial agent set, pattern, context policy, task, seed, DeepSeek Flash route, WorkBench sandbox, and official evaluator. The historical planner call is a shared preparation artifact and incurred no new API charge in this pilot. All arms have up to two turns and one audit-triggered repair opportunity. Fixed arms use KEEP_TOPOLOGY when repair is warranted. Dynamic arms exclude proposed `set_context_policy` operations so structural changes and handoff are separate factors.

Historical `experiment_settings.json` records model alias `deepseek-flash` at `https://api.deepseek.com`; the pilot uses that same alias and route and rejects mock usage in both trace and interaction metadata. The provider's [current pricing/model page](https://api-docs.deepseek.com/quick_start/pricing/) identifies the alias as DeepSeek-V4.1-Flash. Historical settings do not pin a backend model snapshot, so exact backend-version equivalence to 2026-10-05 cannot be established.

## Official results and measured usage

| Task | Arm | Strict valid | Success | Score | Correct | Exact | Unwanted | Tokens in/out | Cost upper USD | Turns | Effective topology | Handoff records | Repeated tool calls |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| multi_domain_12 | B0_fixed | True | False | 0.0 | False | False | False | 675106/104264 | 0.327649 | 2 | False | 0 | 152 |
| multi_domain_12 | B1_context | False | False | 0.0 | False | False | False | 650536/93794 | 0.307714 | 2 | False | 8 | 124 |
| multi_domain_12 | B2_topology | False | False | 0.0 | False | False | False | 1634677/190533 | 0.719043 | 2 | True | 0 | 282 |
| multi_domain_12 | B3_combination | True | False | 0.0 | False | False | False | 1374131/126918 | 0.564541 | 2 | True | 7 | 148 |
| multi_domain_16 | B0_fixed | True | False | 0.0 | False | False | True | 1696073/124733 | 0.658501 | 1 | False | 0 | 164 |
| multi_domain_16 | B1_context | True | False | 0.0 | False | False | False | 468927/71420 | 0.226382 | 1 | False | 4 | 74 |
| multi_domain_16 | B2_topology | False | False | 0.0 | False | False | False | 1391167/168707 | 0.619799 | 2 | True | 0 | 263 |
| multi_domain_16 | B3_combination | False | False | 0.0 | False | False | False | 587261/112736 | 0.311462 | 2 | True | 12 | 136 |

Sum of completed episode cost upper bounds: $3.735091. This is an estimate from actual trace input/output tokens at the published peak uncached DeepSeek Flash rates ($0.30/M input, $1.20/M output), not an API-billed dollar amount. The API returns usage but no billed cost. Preflight usage is recorded separately in `cost_ledger.json`.

Interrupted attempts: 1; conservative extra cost reserve $2.00. The interrupted call sequence is excluded from the outcome table. See `cost_ledger.json` and its archived runner log for the observed completed-call tokens; in-flight usage and actual billed dollars are unknown.

## Case-level trace index

See `results\context_topology_ablation\failure_cases.md` for each saved run's mutation, evidence handoff, downstream CRM action, and official result. Exact source messages and prompts are retained in the original metadata/trace, not reconstructed from the final answer.

### Historical auxiliary control (outside the 8-run pilot)

Historical `multi_domain_12/run_1` (seed 12043) received official success=true, score=1.0, with no unwanted side effects. Its interaction log records a completed `customer_relationship_manager.add_customer` call for Alex Anderson with `assigned_to_email=anaya.patel@atlas.com` and `status=Lead`. The final prediction nevertheless says no successful CRM create/update evidence appears. This is a confirmed final synthesis/receipt inconsistency in a successful run, not a failed pilot arm and not proof that the present handoff mechanism repairs it. Source: `D:\MANTA_DATA\experiments\manta_dsflash_workbench6_20261005_2145_w2\workbench\self_evolved\multi_domain_12\run_1.metadata.json` and `run_1.eval.json` in the same directory.

## Interpretation guardrails

A mutation proposal or changed version number alone is not an effective structure change. The logged effective flag compares final post-transaction agent/group/edge structure. Transactional Star and exactly-once restrictions remain active. For context policy, the CSV compares policies of agents present in both adjacent specs; the raw engine `effective_context_policy_change` flag can turn true merely because new agents bring new default policy entries, which is shown separately as `raw_policy_map_changed`. `Repeated tool calls` counts exact repeated (tool name, arguments) pairs across logged interactions; it is not a token estimate. Communication count is recorded relay messages, while handoff count is visible packet appearances in downstream interaction logs. `Strict valid=false` means the saved real episode had a failed model generation or `needs_rerun`; the official eval is still shown, but that arm is excluded from clean 2×2 conclusions and was not silently rerun. The pilot has one seed per task and no paired deterministic model outputs; any outcome differences are exploratory rather than causal proof. An added verifier or second turn can add reasoning and token cost. A wrong tool call is an ordinary task error unless separately shown to be an attack.

## RQ1 and RQ2

The case-level assessment below uses saved upstream artifacts, visible relay packets, the committer prompt, actual tool calls, and the unchanged official evaluator. These are observations on one seed per task, not a deterministic replay or an estimated treatment effect.

### Historical failure and replay scope

The 2026-10-05 historical `multi_domain_12/run_0` really called `customer_relationship_manager.add_customer` for Alex Anderson with `assigned_to_email=yuki.tanaka@atlas.com`; its official result was score 0 with unwanted side effects. Historical `multi_domain_16/run_0` likewise created Taylor Brown assigned to Yuki and scored 0 with unwanted side effects. The pilot freezes each historical pre-execution TopologySpec and seed, but live model sampling did not reproduce those exact writes. In the pilot every `multi_domain_12` arm made no CRM write; only `multi_domain_16/B0` made a CRM write. Thus the pilot reuses the real tasks and initial graphs, but it is not an exact replay of the old failure sequence.

### Failure chain 1 — Alex Anderson (`multi_domain_12`)

In pilot B0, agent_1 and agent_2 searched CRM and project tasks, then their artifacts `se_g_transaction_work:agent_1:0:0:4` and `se_g_transaction_work:agent_2:0:0:4` reached agent_0 as relay packets `m_3` and `m_4`, alongside the existing evidence digest. The committer saw the existing Alex Anderson record (`customer_id=00000143`, status `Won`) and chose no create call; the second turn repeated this decision. B1 added eight structured handoff records to already visible packets; B2 actually expanded from 3 to 6 agents; B3 added a verifier (3 to 4) and delivered seven handoffs. All four arms still made no CRM write and received score 0, with no unwanted side effects. The observed pilot failure is a duplicate/precondition decision and unresolved owner ranking, rather than a demonstrated missing relay path. B1 and B2 contain failed generations and cannot support a clean pairwise claim.

### Failure chain 2 — Taylor Brown (`multi_domain_16`)

B0 is the clearest incorrect downstream action. Before agent_0 called `customer_relationship_manager.add_customer({customer_name: 'Taylor Brown', status: 'Lead', assigned_to_email: 'sofia.santos@atlas.com'})`, its input already included agent_1 packet `m_3`, agent_2 packet `m_4`, and an evidence digest. Agent_2 explicitly proposed Sofia after counting CRM `follow_up_by` dates; agent_0's final artifact repeated that CRM follow-up rationale. The official evaluator returned score 0 and `unwanted_side_effects=true`. This establishes a received-but-misinterpreted or unsupported action chain, not simple loss of an upstream message. It does not establish which assignee would have been correct without relying on benchmark ground truth.

B1 delivered four structured handoffs into legal visible packets and made no CRM write, because its committer found the pre-existing Taylor Brown record (`customer_id=00000023`, status `Won`). B2 added two agents through `expand_agent_to_group` (3 to 5) and made no write. B3 also expanded from 3 to 5, delivered 12 handoff records, and made no write; new agents `agent_3` and `agent_4` queried earlier project due dates, relayed packets `m_11` and `m_12` to agent_0, and the final committer still concluded duplicate-driven no-op. B1/B2/B3 all scored 0 with no unwanted side effects. The changed behavior is observable; it cannot be attributed uniquely to the switches because model outputs vary and B2/B3 had failed generations.

### RQ1 — Context preservation

MANTA already relays specialist reports and an evidence digest to the transactional committer. The new handoff preserves bounded tool observations and executed-action receipts with source artifact/agent/round references, only inside packets the receiver could already see; prompt inspection confirms receipt in Context-enabled runs, including after agent additions. It is useful for provenance and for the historical successful `multi_domain_12/run_1` final receipt mismatch. In these two pilot failures, however, there is no confirmed case where the required evidence existed upstream but was absent from the committer's legal input and then restored by B1. Neither task succeeded under Context-only. On `multi_domain_16`, B1 avoided B0's unwanted write, but both scored 0; this is a safer observed outcome, not a validated repair of task completion.

### RQ2 — Topology contribution

Structural mutation was actually applied in all four Topology-enabled episodes: `multi_domain_12/B2` 3→6 by `expand_agent_to_group`, `multi_domain_12/B3` 3→4 by `add_agent`, and both `multi_domain_16/B2` and `B3` 3→5 by `expand_agent_to_group`. Added agents executed tools and sent packets. The group remained transactional `star`; no `set_context_policy` was applied to any pre-existing agent. Proposed Context Policy operations are excluded from this 2×2 design. The raw engine policy-map-change flag also turns true when added agents introduce default policy entries; the CSV's `effective_context_policy_change` correctly reports false for existing agents.

No Topology-enabled arm improved official success: all eight scores are 0. In `multi_domain_12`, B2 used 1,634,677 input tokens and 463 tool calls versus B0's 675,106 and 263, with no success gain. In `multi_domain_16`, B2 used 1,391,167 input tokens and 400 calls versus B1's 468,927 and 148; B3 used 587,261 input tokens and 215 calls. Exact repeated tool-call pairs remain common (B2: 263; B3: 136). The new paths mostly repeated CRM/PM searches or checked empty earlier date ranges; the trace does not show a distinct missing fact becoming actionable through an alternative path. B0/B1 on `multi_domain_16` stopped after one turn while B2/B3 took two, so extra reasoning opportunities and tokens are also confounders. There is no observable additional task-success benefit from Topology in this pilot, and no basis for a causal performance-decline claim.

### Auditor signals and next research choice

The saved Audit sources for both `multi_domain_16` dynamic arms are `heuristic`; their logs show repeated empty DeepSeek completions. Signals such as `tool_error_cascade`, `branch_collapse`, and `message_compaction_loss` should therefore be treated as repair hypotheses, not verified root causes. Adding workers after those signals did not resolve the task. Four of eight episodes have `needs_rerun` or failed model generations and are excluded from strict 2×2 inference; the complete official evaluations are retained without paid reruns.

For the next SecurityAdaptiveMAS study, prioritize task interpretation and tool-action validation: check whether the requested 'overdue tasks' metric maps to PM tasks or CRM follow-ups, whether an existing `Won` person permits or blocks creating a new `Lead`, whether a candidate owner is supported by complete rather than truncated search results, and whether a final answer accurately acknowledges successful writes. A bounded provenance handoff can support that validation. Further topology research is warranted only on cases with a demonstrated alternative authorized communication path and independently useful evidence; these two pilot tasks do not yet supply it. There is no prompt-injection or attacker evidence here, so ordinary wrong actions should not be labeled security attacks.

# MANTA 实验台账

更新：2026-10-06（北京时间）。本台账按原始 `artifacts`、结果 JSON 和配置记录；未完成的运行不推断最终分数。以后新实验请追加条目，保留失败和修订历史。路径相对仓库根目录，节点退役结果使用绝对路径。**状态是本次盘点时的磁盘证据状态，不等同于仍在运行的进程状态。**

## 版本与共同条件

- 当前主工作区 HEAD：`98afc28ac47cd0645cbdc77b53aa35a113615476`。`git status --short` 显示 `MAS/config.py`、`MAS/llm.py`、PlanCraft、CLI 和测试等未提交改动，以及新脚本和本说明文件；这些改动没有被本次盘点修改。历史运行时的完整 dirty tree 快照未找到，不能将当前 HEAD 当作每次运行的精确源码版本。
- DeepSeek 组使用 `config/manta_deepseek_flash.toml` 及各 worker 配置：`https://api.deepseek.com`、请求模型 `deepseek-flash`，MANTA `self_evolved`，种子 42，目标每任务 3 次。`deepseek-flash` 是服务端别名；原始结果未证明服务端权重版本恒定。详细结构参数见配置和各目录 `experiment_settings.json`。
- `*.eval.json` 数量是落盘评估记录数量，**不是成功数量**。并行 worker 结果复制到正式目录时会重复计数，不应跨目录相加。成本除有明确记录者外均为**未核实**。

## DeepSeek Flash 历史

| ID / 日期 | 假设、数据和配置差异 | 本次盘点可核实的状态、指标 | 证据及不能得出的结论 |
| --- | --- | --- | --- |
| `manta_dsflash_4bench_20261005_1800`，10-05 | 原定 BrowseComp、WorkBench、PlanCraft、MATH-500 各 30 任务×3 次；顺序在线更新 skill；检验替换 backbone 后的 MANTA 表现。 | 仅 19 个 `*.eval.json`；说明文件记录其中 8 次受 Windows 非 ASCII 输出编码影响失败，运行停止。 | `artifacts/full_experiment/<ID>/`、`artifacts/monitor/<ID>/status.json`、`DEEPSEEK_FLASH_REPRODUCTION.md`。不能纳入正式得分，也不能从 19 次推断四基准性能。运行时源码有未提交修订，精确 diff 未封存。费用未核实。 |
| `manta_dsflash_4bench_utf8_20261005_2030`，10-05 至 10-06 | UTF-8 修正后重启，原定四基准，后来 PlanCraft 取消；整合并行分片，目标仅 BrowseComp、WorkBench、MATH-500 共 270 次。 | 正式目录现有 91 个 `*.eval.json`；监控 `status.json` 最后写为 `failed`（BrowseComp exit 1）；MATH 目录有 `PARALLEL_PROVENANCE.json`。尚未见完整三基准正式汇总。 | `artifacts/full_experiment/<ID>/`、`artifacts/monitor/<ID>/status.json`。91 条可能包含复制结果，不能宣称 270 次已正式完成或得出三基准总分。费用未核实。 |
| `manta_dsflash_math6_20261005_2100_w0`…`w5`，10-05 | MATH-500，6×5 任务×3 次；各 worker 独立 skill，`skill_update_batch_size=0`，检验并行方法变体。 | 6 个 worker 各 15 条 eval、各 5 个 scored task；`benchmark_summary.json` 分数依次 1、1、1、1、1、0.8，失败/缺失均 0。按 30 任务等权，均值 0.9667。 | `artifacts/full_experiment/<ID>/math500/benchmark_summary.json`；正式目录 `math500/PARALLEL_PROVENANCE.json`。不是顺序在线自演化协议的精确复现，也不是论文 Gemma 对照。费用未核实。 |
| `manta_dsflash_parallel3_20261005_2120_w0`…`w5`，10-05 | BrowseComp 与 WorkBench，原方案还包含 PlanCraft；6×5 任务×3 次，独立 skill、禁跨任务更新。PlanCraft 后取消并通过 gate 设 `expected_runs=0`。 | w0、w1、w3、w4、w5 各 30 条 eval，并各有 BrowseComp/WorkBench 的 5 任务汇总；w2 仅 23 条 eval、无完整 benchmark summary。已完整五个 BrowseComp 分片的分数依次 .8、.7333、1、.8、.6667；WorkBench 依次 1、1、.1333、1、1。 | `artifacts/full_experiment/<ID>/`、对应 `artifacts/monitor/<ID>/status.json`、`external_parallel_gate.json`。w2 尚缺完整汇总，不能将上述五片均值当成 30 任务总分；PlanCraft 没有可据此报告的评估结果。费用未核实。 |
| `manta_dsflash_workbench6_20261005_2145_w0`…`w5`，10-05 | 独立 WorkBench 6×5 任务×3 次，拟合并回 parallel3 原 worker；部分 worker 因 SciPy 导入内存不足重试，并设 OpenBLAS 单线程。 | 各 15 条 eval、5 个 scored task，benchmark 分数依次 1、1、.2667、.1333、1、1，失败/缺失均 0；30 任务等权均值 .7333。 | `artifacts/full_experiment/<ID>/workbench/benchmark_summary.json`、`DEEPSEEK_FLASH_REPRODUCTION.md`。合并及正式总分须另核对 provenance；不要与 parallel3 中同一任务重复统计。费用未核实。 |
| PlanCraft 取消，10-05 23:17 | 用户在任何 PlanCraft 评估产出前将其移出目标；各 BrowseComp/WorkBench worker 的 PlanCraft gate 预期次数为 0。 | 取消，不是零分。 | `DEEPSEEK_FLASH_REPRODUCTION.md`、`artifacts/full_experiment/manta_dsflash_parallel3_20261005_2120_w*/plancraft/external_parallel_gate.json`。不能作为模型在 PlanCraft 上失败或成功的证据。 |
| `20261005T083623Z`、`20261005T083649Z` 与 `artifacts/smoke/offline_config_smoke`，10-05 | 早期准备/离线冒烟。 | 目录存在；前两者无 eval。 | `artifacts/full_experiment/<ID>/`、`artifacts/smoke/offline_config_smoke/`。目前缺明确启动命令、任务定义与 API 调用记录，不能推断模型结果或费用。 |

## 节点退役实验（独立分支）

分支 `research/node-retirement`，提交 `166f305b1a1a0a17890ffb083b6a5398419586bb`，PR [#1](https://github.com/ruihanzhu5-cyber/MANTA/pull/1)。结果根目录：`C:\Users\larei\.codex\worktrees\node-retirement\manta\results\node_retirement`。各原始 JSON 的 `git_commit` 为启动时分支基底 `643e2601fb8ad12ba9ed185640c0ac928868b22e`，当时实验文件未提交；最终 v2/v3 另存执行源 SHA-256。全部为 `deepseek-flash` 官方 API、thinking disabled、每 arm 一次模型实现；使用确定性可重置的 MANTA 派生沙箱，不是原生引擎 benchmark，也无可靠美元费用。

| 文件 / 日期 10-06 | 假设、修订与状态 | 结果/token 及边界 |
| --- | --- | --- |
| `smoke_redundant.json` | 冗余节点两 arm 调用路径冒烟；7 次 live API calls。 | 用于确认调用可执行，不作总体准确率。 |
| `pilot_three_cases.json` | 初版三个案例探索，保留失败；38 次调用。 | 修订前证据，不与后版合并。 |
| `pilot_v2_relay_review.json` | 修订 relay/review 输入；25 次调用。 | 探索修订，不作为最终选定案例结果。 |
| `final_pilot_v2.json` | 四案例共同协议，49 次调用；前三个可用案例中的冗余、relay 和 review 由此选取。 | 冗余：keep/直接退役均正确，post-boundary tokens 146→121；relay：keep 找到标签、直接退役漏掉，263→212；review：各 arm 均拒绝发送，720→595。review 未触发未授权操作，不能宣称安全收益。 |
| `unique_capability_v3.json` | 修复 v2 中提示词假称工具证据的问题，改为可审计的候选节点专属沙箱工具记录；13 次调用。 | keep 找到代码、直接退役漏掉，post-boundary tokens 688→661。v2 policy 即使保留节点也曾失败；单次样本不能证明普遍收益。 |

上述调用数和选定结果详见 `results/node_retirement/README.md` 与各 JSON。post-boundary tokens 仅含边界后 prompt+completion，非整场或计费总量；不得把节点退役案例与 DeepSeek 基准分数拼成一项试验。

## 原生 handoff 后续实验（2026-10-06，同一研究线的独立工作树）

来源工作树为 `C:\Users\larei\.codex\worktrees\retirement-handoff\manta`，分支 `codex/retirement-handoff`。以下按其原始 `results/node_retirement_handoff/EXPERIMENT_LEDGER.md`、S5 结果及 `workbench6_20261006_v1/STOPPED.json` 续记；不与上述四案例沙箱 pilot 或 DeepSeek 基准分数合并。共同模型为 DeepSeek Flash 官方 API、thinking disabled；未取得可信的美元账单。

| ID / 版本 | 检验与配置 | 实际状态和指标 | 证据、解释边界 |
| --- | --- | --- | --- |
| `s5_smoke_20261006_v1`，源码 `453bd78a397cb542b7fe4baab29094166e1a1af4` | 合法订阅交接能否让旧 owner 退役、新 owner 处理事件；合成 S5、一共享前缀、拟五 arm，5 个 native star agents，temperature 0，thinking disabled，单 stage 4 次工具迭代。 | 前缀将业务订单号 `P001` 错当 `event_id`，ack 失败，资格检查中止；post arm **0**。9 个请求，输入 23,416、输出 2,575、合计 25,991 tokens。 | `results/node_retirement_handoff/s5_smoke_20261006_v1/` 与独立台账。不能视作退役 arm 失败或效果证据。 |
| `s5_smoke_20261006_v2`，源码 `0cdbd0d`（完整 SHA/hash 在 manifest） | 修正 ID 语义及工具错误反馈，迭代预算改为每 stage 6 次；同一合成 S5、共享真实前缀，五个预定 arm 各续跑一次。 | 完成五 arm。Keep/CheckOnly/CheckHandoff 完成新事件；Direct/SimpleProtect 未完成。CheckHandoff 转移 owner 至 agent_2 并退役 agent_1。51 个请求（含一次物理共享前缀），输入 156,059、输出 18,066、合计 174,125 tokens；post tokens Keep 33,592，CheckHandoff 31,746，差 1,846（5.50%）。 | `results/node_retirement_handoff/s5_smoke_20261006_v2/` 与独立台账。单个配对 block，未测试完整自动 meta-loop 或安全收益，不能给跨任务置信结论。两版开发调用合计 60 请求、200,116 tokens，不是 v2 单独费用。 |
| `workbench6_20261006_v1`，源码 `607c97206ecd8bd6dcb6dd093159b51a6e72879c` | 冻结 WorkBench 六例：`calendar_20`、`calendar_40`、`email_31`、`email_53`、`project_management_2`、`project_management_40`；原拟各 1 次×5 arm，检验原生 handoff。 | 两个 calendar 案例五 arm 均成功；随后 `email_31` 暴露原生邮件日期 string/Timestamp 混排及实验包装器 numpy 数组序列化缺陷，批次中断。219 次 API 尝试、218 次响应，已观测输入 931,867、输出 66,601、合计 **998,468 tokens 下界**；另 1 个中断请求用量未知。 | `results/node_retirement_handoff/workbench6_20261006_v1/STOPPED.json`、原始结果及 console log。calendar 仅探索性；邮件失败和开销受实现缺陷混杂，**不得**当作退役机制效果；不与修复后的版本混合。 |
| `workbench6_20261006_v2`，源码 `a9d35b9` | 修复日期排序和数组序列化，六例与五组、模型和评分保持冻结。 | 19/30 个 continuation 完成；前三例五组全成功，`email_53` 四组完成，Simple 触及整例 120 请求预算；两例 project 未开始。398 请求/响应，1,912,819 tokens。 | `results/node_retirement_handoff/workbench6_20261006_v2/`、独立台账。`email_53` 未成完整五组，不能把四组诊断结果混入最终比较。 |
| `workbench3_20261006_v3`，源码 `52e0369` | 对后三例提高整例预算，保留原任务索引及每组设置。 | Windows 日志保存文件占用中断；`email_53` 三组完成，Direct 未评分，其余未开始。87 请求/响应、431,291 tokens；`.tmp` 中 87 响应及用量已核验并恢复。 | `results/node_retirement_handoff/workbench3_20261006_v3/RECOVERY.json`、原始及恢复 journal。属于持久化中断，不能当成模型或退出机制失败；诊断结果不进入最终比较。 |
| `workbench3_20261006_v4`，源码 `d7a5fe6` | 仅对日志保存加有限重试，后三例完整重跑。 | 后三例 15/15 任务与严格成功；334 请求/响应、1,621,168 tokens。 | `results/node_retirement_handoff/workbench3_20261006_v4/`。仅与 v2 前三完整例按预定完整 block 规则合并。 |
| `workbench6_20261006_comparison`，2026-10-06，来源 `a9d35b914255d970d5c2bb0b3344dfc6d936158f` + `d7a5fe6083f354a98ee25d8f6ec21bb46b2a2a75` | v2 前三例＋v4 后三例；六例各五组，退出前共享真实执行，之后独立续跑；DeepSeek Flash、temperature 0、thinking disabled、每请求输出上限 768、每成员阶段最多 10 工具循环。 | **30/30 完成；五组各 6/6 任务及严格成功。** Post tokens：Keep 557,572；Direct 420,802；SimpleProtect 429,674；CheckOnly 583,188；CheckHandoff 407,683。交接比 Keep 低 26.88%，比 Direct 低 3.12%，但六例中四例更贵。含六个共享前缀：612 请求、2,920,880 tokens；165/165 记录一致性核验通过。 | `results/node_retirement_handoff/workbench6_20261006_comparison/REPORT.md`、`result.json`、`development_accounting.json`。这是改造后的 WorkBench 小样本，不是原版 benchmark；五组成功相同，未证明额外成功率或普遍成本优势。未提供美元账单。 |

本研究线最终源码提交 `9bfae607508f6ab44f4b4358ce2f5bd7ee29f79c`，用户 fork 的[草稿 PR #2](https://github.com/ruihanzhu5-cyber/MANTA/pull/2)。WorkBench v1–v4 开发总量 **1,038 请求、1,037 完整响应、已知 4,963,746 tokens**；连同 S5 两版为 **1,098 请求、1,097 完整响应、已知 5,163,862 tokens**，另有 v1 一个中断请求用量未知。此开发总量已包含最终比较，不能重复相加；不含更早基线复现。相关离线检查分 68＋14＋2 项通过。`docs/node-retirement-next-iteration.md` 的可见性隔离、真实待办交接及一组成对变体 10 次执行均为**建议，尚未运行**。

## 尚缺证据与续记规则

1. 保存每次运行时的提交加 dirty diff 或源码 hash；当前主分支未提交改动不能回填成历史快照。
2. 核对 parallel3 w2 的剩余记录、所有 worker 的最终进程/状态、正式三基准合并 provenance 和完整汇总。现有监控状态可能陈旧；仅从文件数无法确认进程是否仍活动。
3. 如需费用，需可信的 API 账单或逐调用 usage 汇总；不要用请求次数推估美元费用。
4. 新实验追加 ID、北京时间、git 提交及 dirty 状态/源码 hash、模型/API 及返回模型元数据、任务集合与实际样本数、相对前版差异、假设、落盘状态、原始指标、usage/费用、原始证据路径、解释限制；失败、取消、恢复、冒烟单独保留。

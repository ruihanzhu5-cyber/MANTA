# AppWorld Context Chain：下一轮最小实验建议（Phase B）

## 先说结论

这 12 条 Clean 轨迹官方成功为 0/12，因此下一轮不能把任何安全方法的任务成功提升写成已证实收益。先做执行有效性对照，再做交接表示对照。当前状态：

```text
READY_FOR_PAID_RUN=NO
```

原因是本轮没有针对 Phase B 新实验的明确费用额度，而且已有 Clean 结果没有先建立可完成的功能基线。历史实验预算不自动视为本轮授权。本 Phase A/B1 没有发起付费请求。

## 两个推荐 Case

### 1. `6c2c621_1`：Simple Note → Markdown

选择理由：这是唯一同时满足“下游 Artifact 的 `evidence_summary` 为空”和“工具层可观察到任务字段不足”的优先 Case。现有轨迹里的搜索结果有标题、标签和时间字段形状，但没有观察到正文被读出；Native 还在创建目录后以 `transaction_committed` 停止。因此第一步是确认单 Agent 是否能走通“读正文 → 创建文件 → 写文件”的合法 API 路径。

先做的有效性对照：同任务、同 AppWorld、同工具、同预算，加入一个 Single-Agent 功能对照和原生 MANTA 对照。若 Single-Agent 也无法读正文或写文件，交接视图实验不能解释失败。

### 2. `6171bbc_1`：Spotify Playlist

选择理由：这是重复读取和动态增员最清楚的 Case。MANTA Native 第二轮确实增加了 `agent_3`；它的 22 个唯一参数根中有 16 个没有和第一轮重叠，但最终仍没有具体播放列表结果。它适合核对“可追溯证据是否减少重复读取”，但只有在执行有效性先通过后，才能讨论任务效用。

## 三个交接臂

所有臂必须使用同一个模型、任务、Agent 数、工具集合、预算、官方评分器和世界初始化方式；只改变合法 Agent 看到的交接视图：

1. **`NATIVE_PACKET`**：当前 MANTA 的结构化 JSON 外壳加自然语言字段。
2. **`SUMMARY_ONLY`**：只保留当前摘要和必要身份字段，不增加结论。
3. **`EVIDENCE_REFERENCED`**：保留原摘要，并添加当前接收者按 ContextPolicy 本来可见的 Artifact ID、Tool Event ID、限定来源和必要字段路径。不能添加 Ground Truth、评分器隐藏状态、额外账号权限或新的工具。

离线可行性已经完成：90 个真实 Relay→接收者组合中，`EVIDENCE_REFERENCED` 能提供 895 个来源引用和 169 个任务字段引用；这只是表示层可解析性，不是性能结果。

## 执行顺序和护栏

### 第 0 步：功能有效性

- 对 `6c2c621_1` 先跑 Single-Agent 与原生 MANTA 的最小对照。
- 保持 `temperature=0`、thinking disabled、同 DeepSeek Flash、`runs_per_task=1`、相同工具和官方 Judge。
- 必须看到真实的正文读取和目标文件写入，再进入三臂交接对照。
- 如果功能对照仍失败，把问题记录为 API 路径/任务执行问题，不把它写成 Context Chain 收益。

### 第 1 步：`1 task × 3 arms`

优先用已经通过功能有效性检查的 Case。三臂各 1 次，独立世界目录，保留完整 Prompt/Relay/Artifact/Tool Event 记录。只允许在 Prompt 组装前替换交接视图；不能改 Planner、Auditor、拓扑、官方数据或 Judge。

### 第 2 步：`2 tasks × 3 arms`

只有第 1 步三臂都完成模型调用、工具调用和官方评测，且没有超出批准费用时，才扩到第二个推荐 Case。IPI 另开固定低信任入口、目标和安全 Oracle；Clean 轨迹只用来选择入口和干预窗口，不能当作 IPI 传播证据。

## CLI 和费用状态

当前基线驱动的真实运行入口是：

```powershell
python main.py run --config <frozen-config.toml> --benchmark appworld `
  --task-ids <task_id> --runs-per-task 1 --system-label <arm>
```

基线批处理脚本只有在显式提供费用上限时才会发起模型请求：

```powershell
python scripts/research/run_appworld_baselines.py --approved-cap-usd <new-approved-cap>
```

本轮没有执行上面两个命令。三臂交接需要一个独立的实验驱动，把视图替换限制在合法 Relay→Prompt 位置；在该驱动完成前不能把现有基线命令冒充成三臂实验。费用上限必须是本轮新批准的数值，不能默认沿用历史额度。建议保留一个小的预留金额，遇到超时、异常返回或账单不确定时停止新增任务。

## 与 MANTA 和 MAPLE-Guard 的关系

这项实验审计的是 MANTA 的 Context/Memory 交接链和任务执行有效性。`NATIVE_PACKET` 是 MANTA 原生条件；`SUMMARY_ONLY` 与 `EVIDENCE_REFERENCED` 是本轮为审计构造的离线交接视图，不是现成外部论文 Baseline。MAPLE-Guard 只能作为相关的安全/证据组织工作背景，不能把这里自造的三臂写成 MAPLE-Guard 的实验结果。

## Checkpoint 和 IPI 限制

当前没有可信的 AppWorld 完整 Checkpoint 恢复，因此不能声称做了“同 Checkpoint 反事实续跑”。如果 Phase B 进入真实运行，只能用独立重置世界做匹配条件实验，并在结果中说明差异。IPI 结果必须分开报告 raw payload reach、语义采纳、Memory reuse 和真实有害操作；本轮 12 条 Clean 轨迹不支持其中任何一项。

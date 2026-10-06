# 节点退出实验（第一版）

此分支增加一个显式、默认关闭的节点删除干预，用于研究“删除看似冗余的
agent 是否影响后续质量与安全”。它不是自动贡献评分器，也不是安全性证明。
不把删除操作开放给 Topology Planner；候选节点由实验配置指定。

## 配置与运行

复制你已经跑通的实验配置，在 `[self_evolved]` 段设置：

```toml
initial_planner_mode = "fixed"
max_turns = 2
retirement_after_turn = 1
retirement_agent_ids = ["agent_2"]
retirement_protect_validation = true
playbook_read = false
skill_update_batch_size = 0
```

保留原配置中的模型、benchmark、工具和 `[mas]` 参数；`[mas]` 中选择
`topology = "self_evolved"`，并给足初始节点，例如 `number_of_agents = 3`。
使用固定初始化便于明确节点身份；任务初始化模式也支持，但可能没有所指定的节点，
届时请求会被记录为 rejected。非检索工具任务已有最多 3 个初始节点的限制。

删除组配置和对照组配置保存为两个文件。对照组仅把候选改为空列表：

```toml
retirement_agent_ids = []
```

分别用现有 CLI 运行，下面以 `math500` 为例：

```bash
python main.py run --config config/retirement-control.toml --benchmark math500 --topology self_evolved --task-limit 1 --runs-per-task 1
python main.py run --config config/retirement-delete.toml --benchmark math500 --topology self_evolved --task-limit 1 --runs-per-task 1
```

两组使用相同任务、seed、模型、初始拓扑、communication budget、工具环境与独立的
输出目录。若后续轮次需要继续通信，应给足通信预算；现有预算在 turn 间不会重置。
真实工具环境必须分别复位；相同 seed 并不保证远程 LLM 采样一致。
本版提供相同控制流程的两个独立运行，尚未实现从同一个执行 checkpoint 分叉回放。

## 干预语义

- `retirement_after_turn = 0`：原始 MANTA 控制流程，默认不删除。
- 正数 N：执行 N 个 turn，在边界删除指定节点，再执行一个后续 turn 后定稿。
  所有实验组均关闭 planner repair，并使用相同固定 horizon；自然停止决定另存为
  `natural_decision`。因此成本应与上述空列表对照比较，而非把额外 turn 归因于删除。
- N 必须小于 `max_turns`。检索任务沿用最多 2 turn 的限制，因此仅支持 N=1。
- 成功执行状态变更工具后，原有 transaction guard 优先停止，记录 skipped，
  不为实验强制重放副作用。实际轮数可能因此不足，需要单独统计。
- 请求原子执行：任何一个节点不合法，整批请求都不删除；后续仍跑原拓扑，记录 rejected。

## 当前约束和历史数据

仅删除不拥有子组且不是 group leader 的节点；禁止产生空 group 或只剩一个成员的
debate/voting group，不自动改组模式、迁移任务、赋予权限或增加证据可见性。
默认保护结构角色为 verifier/coordinator 或 stage role 为 critic 的节点。
`retirement_protect_validation = false` 可用于删除验证节点的明确消融；leader、
子组所有者和结构合法性检查仍保留。

删除后 group membership、extra edges、layout、后续执行顺序和 context spec 同步更新，
被删节点的消息预算归零。历史 artifacts、消息、证据 ledger、工具日志、persona 和
累计计数保留用于分析。旧消息保持原样，但已退出节点发出的 packet 不再通过
`visible_packets` 作为活跃消息读取；否则未知 sender 可能被误当成不受限制的 meta sender。
证据 ledger 仍按现有 digest 可见性规则读取，因此部分历史贡献仍能支持后续任务。
显式 `visible_from` 引用保留，避免删掉最后一个限制条目后意外放宽访问。

这些约束不检查安全职责是否完备、未完成任务是否交接、隐含桥接作用，
也没有 shadow 验证或自动恢复。下一阶段需要通过带权限规则的工具 stub、
必要验证事件和依赖标注，建立这些约束的可测定义。

## 结果读取

现有 run metadata 增加 `self_evolved.retirement_experiment`：

- `events`：control/applied/rejected/skipped，候选、拒绝理由、删除前后完整 spec 与
  layout、保留记录数、边界操作延迟。零 token 的 `retirement_boundary` trace event
  也记录同一事件，不产生额外 LLM 调用。
- `turn_metrics`：turn 编号、拓扑版本、活跃节点、执行及 audit 的输入/输出 token、
  输出 artifact ID、未解决问题、预期成员数。
- `self_evolved.topology_spec_versions`：成功删除后追加新版本。
- 原有 audit reports、termination history、artifact records、tool records 与 trace
  用于检查后续失败。整次运行的 token 成本应按完整 trace 统计，包含规划、定稿等成本；
  turn metrics 只包含该 turn 执行、descriptor 与 audit 的事件。

最终答案沿用 MANTA 的跨 turn 候选选择，可能选中删除前的答案。
因此不能仅凭最终成功率认定删除后稳定；还需查看后续 turn 的输出 artifact 和 audit，
用 benchmark 的正式评估接口判断质量。未授权执行、遗漏验证和依赖失败指标尚未实现。

## 验证

```bash
pytest tests/test_self_evolved_retirement.py tests/test_self_evolved_spec.py tests/test_self_evolved_context.py tests/test_self_evolved_engine_smoke.py tests/test_mas_config.py
```

测试使用离线 mock，不消耗模型 token；验证结构删除、原子拒绝、角色保护、权限不放宽、
已退节点停止执行、对照 horizon、配置加载及已提交副作用优先停止。
真实 benchmark 成本、正确率和安全效果需另外实验。

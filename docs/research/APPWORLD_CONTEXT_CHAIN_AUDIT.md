# MANTA × AppWorld Context / Memory 交接链审计（Phase A）

## 范围和读入结果

本审计从基线 `a12bc00daf04b7dd5316f06b68b0b13724584be8` 新建分支完成。只读了已经提交的 12 条 Clean 轨迹：原生 Static Star 6 条和 MANTA Native 6 条；没有重跑任务、启动 Docker 或发起新的 LLM API 请求。

离线命令和结果：

```powershell
python scripts/research/audit_appworld_context_chain.py --offline
# read_runs=12, official_success=0/12
python scripts/research/compare_handoff_views_offline.py --offline
# runs_read=12, rows=270
python -m pytest -q tests/research/test_context_chain_audit.py
# 3 passed, exit code 0
```

机器可读结果在被 Git 忽略的 `artifacts/appworld_context_chain/`：

- `all_12_cases.csv`：每条轨迹一行，含工具调用、交接、终止、Token 和重复候选统计。
- `event_index.json`：脱敏的 Tool Event、Artifact、Relay、真实 Prompt 可见包、Ledger 和 Digest 索引。
- `handoff_variants.csv`：三种离线交接视图的逐 Relay/接收者比较。
- `offline_validation.txt`：`runs_read=12`、`official_success=0/12`、`schema_checks=PASS`。

所有 12 条轨迹的 `metadata`、`trace`、`trajectory`、`eval`、`result` 文件都能解析。报告没有写入原始参数、原始工具返回、完整 Prompt 或账号内容。阶段 Token 只引用日志里已经记录的模型事件；不能把工具循环期间累计的 Token 当成一条 Prompt 的精确 Token，也没有用字符数伪造节省量。

## 真实代码调用链

### Tool Output → MANTA 工具记录

`benchmark/appworld/tool_bridge.py:120-171` 的 `AppWorldBridge.tools().invoke` 先校验参数，再调用 `world.execute` 的桥接 RPC（`133`），保留原生输出哈希和字段形状（`150-152`），记录 `appworld_tool_events`（`139-160`），最后把可解析的 dict/list 直接返回给模型（`163-171`）。因此 `appworld_tool_events` 是适配器事件；MANTA 的 `tool_records_log` 是另一条日志流，在 Native 轨迹中会把同一次调用再记录一次。审计脚本按节点记录和空节点副本去重后再统计，避免把日志重复当成 Agent 重复工作。

### Prompt 和阶段内部工具循环

`MAS/langgraph_engine.py:2249-2397` 的 `_execute_agent_stage` 组装 Prompt、调用模型、必要时追加一次工具重试，并把每个工具调用写进 Artifact 和工具日志。`2493-2538` 把完整 `prompt_messages`、`visible_messages`、`prior_artifact`、结构化 Artifact 和 Token 记入 `interaction_logs` 与 trace。

`MAS/langgraph_engine.py:4481-4642` 的 `_build_agent_prompt` 实际包含：任务消息、`prior_artifact`、`visible_packets`、可用工具，以及文字说明 `Stage context follows as JSON`。这不是“纯 JSON”与“纯自然语言”的两个原生条件，而是结构化 JSON 外壳加自然语言字段的单一原生方式。审计按每个真实 stage log 解析 `visible_packets`，再和 `message_views.visible_message_ids` 对齐。

### Artifact → Relay

`MAS/artifacts.py:99-164` 的 `build_artifact` 会把模型 JSON 解析成 `summary`、`answer`、`critique`、`revision_request`、`confidence`、`unresolved_issues`、`evidence_summary`，解析失败则标为 `fallback`。`167-190` 的 `packet_payload_from_artifact` 只把这些 Artifact 字段放进 Relay payload；`source_artifact_ids` 和 `tool_records` 不会随 Relay 一起传给接收者。

`MAS/self_evolved/executor.py:793-858` 分别生成 `task_package`、`orchestrator_feedback` 和 `specialist_report`。发送成功不等于接收者看见；接收情况以真实 Prompt 中解析出的包 ID 为准。

### Context Policy 和 Evidence Ledger

`MAS/self_evolved/context.py:45-93` 根据接收者、kind、轮次、发送者权限和 `latest_only` 选择可见 Relay。`97-136` 把 Artifact 的 claim/evidence 写入共享 Ledger；`143-190` 生成受范围限制的 `evidence_digest`。代码明确写明 Digest 是 Prompt-only（`152-155`），不会写入 `state["messages"]`，所以它不应被误报成 Relay 丢失。

### 终止、拓扑和长期 Skill

`MAS/self_evolved/engine.py:480-545` 在成功状态变更后把终止原因设为 `transaction_committed`，并抑制后续轮次；相同决策签名则设为 `no_meaningful_change`。这两个原因分别记录为行动控制和停滞控制，不能混成同一个交接缺口。

`MAS/self_evolved/engine.py:949-1055` 记录 mutation proposal、应用的 ops 和新增 Agent。12 条轨迹的实验快照都显示 `skill_update_batch_size=0`、`default_packet_max_chars=0`；因此本轮没有在线写长期 Topology Skill，不能把同 Episode 的 Relay/Ledger 当作跨任务 Memory。

`MAS/artifacts.py:332-356` 的 `compute_consensus` 只按规范化答案 Signature 计数。`MAS/self_evolved/executor.py:862-878` 的组输出也先按 Signature 计票。源码没有看到“不同来源独立性”校验，这是一个 **PLAUSIBLE 源码候选缺口**；Clean 轨迹中的相同结论不能因此被称为攻击造成的虚假共识。

## 12 条轨迹总览

| 项目 | Static Star（6 条） | MANTA Native（6 条） |
| --- | ---: | ---: |
| 官方成功 | 0/6 | 0/6 |
| 读到的原生 Tool Event | 594 | 689 |
| 去掉日志副本后的工具记录 | 595 | 690 |
| Artifact 数 | 42 | 39 |
| Relay 数 | 48 | 42 |
| 实际模型 Prompt 交互数 | 42 | 39 |
| 出现 Evidence Digest 的 Prompt 数 | 0 | 9 |
| 记录的 Ledger 条数 | 0 | 39 |
| 候选重复读取（REPEAT_POSSIBLE） | 205 | 332 |
| 分页/参数变体（PAGINATION_OR_VARIANT） | 319 | 289 |
| 状态变化后的再次核对（VERIFY_AGAIN） | 13 | 2 |

这些是审计标记，不是“浪费率”。`REPEAT_POSSIBLE` 只表示同工具、同归一化参数哈希、中间没有已知成功写操作；跨 Agent 的同一读取仍可能是独立核对。分页、排序、查询条件或账户变化被单列为 `PAGINATION_OR_VARIANT`。不能根据这些计数直接归因于图结构或 Memory 设计。

MANTA Native 有 3 次可观察的 `APPLY_MUTATION`，每次都是给 `g_transaction` 增加一个 `critic/verifier` Agent；这说明日志里存在有效拓扑 op，但“新增 Agent 带来任务收益”仍是 **UNKNOWN**。Static Star 没有 mutation。所有 12 条官方评分仍为 0。

## Case ① `6c2c621_1`：Simple Note → Markdown

**结论：交接完全丢失任务证据为 NOT_SUPPORTED；已观察到的是工具路径/终止控制问题，外加 Artifact 证据字段变空。**

### MANTA Native 的逐跳记录

| 跳 | 证据 |
| --- | --- |
| Tool Event | Worker 的 `simple_note__search_notes` 事件 `native:5`、`native:7`、`native:11` 等返回的字段形状主要是 `title`、`tags`、`created_at`、`updated_at`；`file_system__show_directory` 返回目录条目形状；没有观察到笔记正文 `body/content` 被取出。所有这些事件 `execution_error=false`，但 `task_completed=false`。 |
| Producer Artifact | Planner `se_g_transaction_plan:agent_0:0:0:3` 为 `status=ok`，`evidence_summary` 有 4 条；Worker `se_g_transaction_work:agent_1:0:0:4` 和 Critic `se_g_transaction_work:agent_2:0:0:4` 都是 `status=fallback`、`evidence_summary=0`。两者均保留 Planner Artifact ID 作为 `source_artifact_ids`。 |
| Relay | `m_1`（Planner→Worker）和 `m_2`（Planner→Critic）都是 `task_package`；Worker/ Critic 回传 `m_3`、`m_4`，kind 为 `specialist_report`。Payload 只有 Artifact 摘要字段，没有 `tool_records` 或原始 Tool Event 引用。 |
| Receiver Prompt | Aggregator 的真实 Prompt 可见 `digest_agent_0_r0_3`、`m_3`、`m_4`，并带 Planner 的 `prior_artifact`；对应 `message_views` 记录也是这三个 ID。Digest 实际来自 Ledger 的 3 个条目，且是 Prompt-only。 |
| Later action | Aggregator 继续调用 `simple_note__search_notes`、`file_system__directory_exists`，随后调用 `file_system__create_directory`（`native:41`）；没有看到写 Markdown 文件的 Tool Event。 |
| Verifier | 官方 `success=false`、`appworld_task_completed=false`；终止原因为 `self_evolved:transaction_committed`。 |

这里有一个真实、可复核的信息缺口：Worker/Critic 的 Artifact 没有 `evidence_summary`，Relay 也没有 Tool Event 引用；但接收者仍通过 Planner 的 `prior_artifact` 和 Digest 得到了部分摘要。因此“Relay 丢失 = 下游完全没有证据”不成立。更强的观察是：原始工具调用没有拿到正文/文件写入所需字段，且创建目录触发了 `transaction_committed`，后者阻断了继续写文件。**终止控制失配与交接信息丢失必须分开。**

Static Star 的同一 Case 也没有出现跨 Agent 完全证据消失：`specialist_worker:agent_1:0:0:0` 有 5 条 evidence，`agent_2` 为 0；第二轮继续查找并最终在 `no_meaningful_change` 停止。两种配置都没有证明“已有完整工具事实在 Relay 后不可用”；更像是查询结果没有覆盖正文、模型没有走到文件写入 API，以及 Native 的状态变更提前停机。

## Case ② `6171bbc_1`：Spotify Playlist

**结论：重复读取和新增 Agent 都是 OBSERVED；“新增 Agent 提供独立证据”只有 PARTIAL/PLAUSIBLE，最终阻塞是没有产生具体播放列表结果，而不是已证明的交接丢失。**

### 逐轮和逐 Agent

- Static Star 6 个阶段性 Artifact 共 127 个工具记录，`spotify__show_album_library`、`spotify__search_songs`、`spotify__show_album` 等调用在不同 Agent 和轮次间重复；同名调用中有大量参数哈希不同的 `PAGINATION_OR_VARIANT`，不能只凭工具名算重复。
- MANTA Native 第一轮 3 个 Agent；第二轮的 mutation 记录明确是 `APPLY_MUTATION`、新增 `agent_3`、1 个 `add_agent` op。新 Agent 的 `record:228`–`record:252` 共 25 条调用、22 个唯一参数根；与第一轮所有参数根重叠 6 个，新增 16 个。新增部分包括 `spotify__show_album`、`spotify__show_album_privates`、`spotify__search_songs` 等，说明它不是完全复制第一轮，但仍重复读取 album/playlist library。
- `m_7` 是 Planner→新增 Critic 的 `orchestrator_feedback`，Critic 的真实 Prompt 只看到 `m_7`，没有 prior Artifact 或 Evidence Digest；它随后独立查询。Aggregator 的最后 Prompt 看到 `digest_agent_0_r1_8`、`m_8`、`m_9`、`m_10`。

### 阻塞和 verifier

两种配置的第二轮终止说明都明确写成“只有计划/login 步骤，没有具体 playlist 结果”，并以 `no_meaningful_change` 停止。MANTA Native 的新 Critic 有 16 个相对第一轮的新参数根，这是独立检索的可观察证据；但最终 Artifact 仍是 `fallback`，没有创建播放列表的 Tool Event。因而可确认的是“重复工作 + 新 Agent 仍未形成执行结果”，不能倒推成 Context Chain 已经丢失了某个具体播放列表字段。

## Case ③ `530b157_1`：Phone → Venmo → SMS

**结论：这是行动状态和任务完成边界案例，不是 IPI 成功案例。**

### Native 执行

| 跳 | 证据 |
| --- | --- |
| Context | Aggregator 的真实 Prompt 可见 `digest_agent_0_r0_3`、`m_3`、`m_4`，并带 Planner `prior_artifact`。 |
| Actions | `venmo__create_transaction` 的原生事件 `native:59` 和 `phone__send_text_message` 的 `native:60` 均 `execution_error=false`，顺序是先交易、后短信；都由 Aggregator Agent 的 committer stage 发起。 |
| Verifier | `native:59` 已标记 `task_completed=true`；控制器随后把终止原因写成 `self_evolved:transaction_committed`，没有再开下一轮。官方评测仍 `success=false`。 |

这证明一次状态变更成功不等于整个任务已经完成。它不证明 Prompt Injection 传播，也不证明 Memory 复用攻击。Clean 轨迹不能被当作 IPI 攻击证据。

### Static Star 对照

Static Star 的 `native:12`/`native:14` 和 `native:15`/`native:17` 分别形成两次交易/短信调用，均无工具错误；这是真实副作用重复的观察，但不是交接丢失的直接证明。其最终终止是 `orchestrator_no_discussion:no_meaningful_change`，不是 Native 的 `transaction_committed`。

## Phase B1：离线交接视图

在相同真实 Artifact 上生成了三个只读视图：

1. `NATIVE_PACKET`：当前结构化 JSON 外壳加自然语言字段。
2. `SUMMARY_ONLY`：只保留摘要和身份字段。
3. `EVIDENCE_REFERENCED`：在原有摘要/证据列表之外，添加已有 Artifact ID、已有 Tool Event ID 和字段路径；没有添加评分器隐藏状态或 Ground Truth。

结果（90 个真实 Relay→接收者组合，每种视图各 90 行）：

| 视图 | 真实可见 Prompt 数 | 可追溯 Tool Event 引用 | 任务字段引用覆盖 |
| --- | ---: | ---: | ---: |
| `NATIVE_PACKET` | 90 | 0 | 0 |
| `SUMMARY_ONLY` | 90 | 0 | 0 |
| `EVIDENCE_REFERENCED` | 90 | 895 | 169 |

这个结果只说明“来源引用可以在离线表示层加入并被解析”，不说明性能收益。三种视图的任务成功、ASR、真实执行 Token、攻击拦截率都标为 `NOT_MEASURED`。真正执行还需要固定任务、Agent、工具、预算、官方评分器和合法交接位置。

## 当前判据

本轮最终科研判据是：**没有找到足够证据证明“原始工具证据已经取得，但经过跨 Agent 交接后，适当的接收者实际再也无法使用它”。** 找到的是：

- Case 6c 的正文/文件写入证据从工具层就没有形成，随后创建目录触发提前停机；
- Case 6171 的重复读取和部分独立检索，但没有具体播放列表执行；
- Case 530 的成功状态变更和完整任务完成不是同一件事，Static Star 还有重复副作用。

因此 Context Chain 的“信息缺口”可以标为 **OBSERVED（Artifact 没有 Tool Event 引用，部分 Worker/Critic evidence 为空）**；“该缺口造成官方任务失败”只能标 **UNKNOWN**；“已证明跨 Agent 交接导致任务必要证据不可用”应标 **NOT_SUPPORTED**。本轮 Clean 轨迹也不能支持 IPI 传播、ASR 或安全收益结论。

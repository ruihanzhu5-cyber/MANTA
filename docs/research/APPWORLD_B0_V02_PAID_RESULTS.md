# AppWorld B0 v0.2 Paid Clean Results

## 一句话结论

本轮产生了 **3 个官方 Clean 成功**，全部来自 `SINGLE_AGENT_LH`；
`MANTA_NATIVE` 产生了 0 个官方成功。Native 的 5 条有效 Episode 都有真实的
Worker → Coordinator Relay，并且 Coordinator 的下游可见消息列表包含这些 Relay，
但没有一条同时满足官方成功。因此 `B1_GO=false`，本轮不启动 B1/B2。

## 运行范围

冻结顺序没有改变：`6c2c621_1`、`530b157_1`、`6171bbc_1`、`50e1ac9_1`、
`0d8a4ee_1`。每个任务各运行一次 `SINGLE_AGENT_LH` 和一次 `MANTA_NATIVE`，共
10 条有效评分 Episode。另有 2 条工程前置失败尝试：一条是旧 Native 初始化
`NameError`，一条是缺少 `50e1ac9` 的公开 Spotify 映射；两条都保留在本地账本，
不计入 10 条有效评分分母。

| Task | SINGLE_AGENT_LH | MANTA_NATIVE | LH 阶段 | Native Worker→Coordinator | Native 下游收到 Relay |
|---|---:|---:|---:|---:|---:|
| `6c2c621_1` | False | False | 3 | 2 | 2 |
| `530b157_1` | **True** | False | 3 | 2 | 2 |
| `6171bbc_1` | **True** | False | 3 | 4 | 4 |
| `50e1ac9_1` | False | False | 3 | 2 | 2 |
| `0d8a4ee_1` | **True** | False | 3 | 5 | 5 |

### 关键计数

| 指标 | 有效 10 条合计 | SINGLE_AGENT_LH | MANTA_NATIVE |
|---|---:|---:|---:|
| 官方成功 | 3 / 10 | 3 / 5 | 0 / 5 |
| 输入 Token | 9,978,470 | 3,075,030 | 6,903,440 |
| 输出 Token | 144,088 | 49,721 | 94,367 |
| LLM 请求数（工具循环 + 强制收尾） | 419 | 144 | 275 |
| 外层 `generate` 调用数 | 70 | 15 | 55 |
| AppWorld 工具事件 | 1,003 | 347 | 656 |
| 工具错误事件 | 58 | 16 | 42 |
| 保守费用上界 | `$3.1664` | `$0.9822` | `$2.1843` |

实际总账本上界（含两条工程失败尝试）：`$3.1672 / $4.00`。没有飞行中请求，
没有轮换 Key。实际供应商账单可能与本地保守估算不同；本地账本没有把预留额当作
真实费用。

## 任务动作核对

- `6c2c621_1` LH 调用了 `simple_note__show_note` 44 次和
  `file_system__create_file` 13 次；Native 调用了 `simple_note__search_notes`，
  但没有 `show_note` 或 `create_file`。
- `530b157_1` LH 完成了 `venmo__create_transaction` 和
  `phone__send_text_message`，官方成功；Native 也调用了这两个写操作各 1 次，
  但官方评分仍为 False。
- `6171bbc_1` LH 调用了 `spotify__create_playlist` 和
  `spotify__add_song_to_playlist`，官方成功；Native 没有完成对应写入。
- `50e1ac9_1` 是查询任务，两种 Arm 都没有官方成功；没有把“查询调用多”当作
  已完成任务。
- `0d8a4ee_1` LH 调用了 `phone__send_text_message` 2 次并官方成功；Native 没有
  发出短信写操作，官方失败。

## 并发和停止

- 第一批 2 条独立 Episode 并发运行。
- 隔离检查通过后，第二批用并发 4；最后一个任务的两条 Arm 并发运行。
- 单个 Episode 内部调度顺序没有改。
- 费用护栏触发过一次未启动的预算停止记录，但后续已在确认无模型请求的适配器
  错误修正账本后继续；没有偷偷追加额度。

## B1 判定

`B1_GO=false`。虽然 5 条 Native 有合法 Relay 且 Coordinator 的下游 Prompt 可见
对应消息，但 Native 官方成功数为 0。LH 的 3 个成功只能说明任务在新的长程单 Agent
路径下可完成，不能替代 Native 成功，也不能据此启动 B1/B2。

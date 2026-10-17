# AppWorld B0 v0.2 Case Failure Analysis

只使用公开工具事件、运行元数据和官方 `world.evaluate()` 结果。官方统计只提供
`difficulty`、`num_tests` 和 `success`；没有公开具体失败断言的地方标记为
`EVALUATOR_DETAIL_UNKNOWN`，不猜测隐藏测试内容。

| Task / Arm | 官方结果 | 主要标签 | 事件证据 |
|---|---:|---|---|
| `6c2c621_1` / LH | False | `OFFICIAL_STATE_MISMATCH`, `EARLY_STOP` | `show_note` 44 次、`create_file` 13 次，5 个工具错误；3 阶段均有调用，最终仍 `task_completed=false`，官方 `success=false`。 |
| `6c2c621_1` / Native | False | `MODEL_DID_NOT_READ_REQUIRED_EVIDENCE`, `OFFICIAL_STATE_MISMATCH` | 有效重跑中 `show_note` 和 `create_file` 都为 0，工具事件 47；官方评分有效但失败。 |
| `530b157_1` / LH | True | 无失败 | Venmo 交易 2 次、短信发送 1 次；官方 `success=true`、`task_completed=true`。有 1 个工具错误，但没有阻止完成。 |
| `530b157_1` / Native | False | `EVALUATOR_DETAIL_UNKNOWN` | `task_completed=true`，交易和短信各 1 次，官方评分有效但 `success=false`；公开评分没有给出具体失败断言。 |
| `6171bbc_1` / LH | True | 无失败 | 创建播放列表 1 次、添加歌曲 8 次；官方 `success=true`、`task_completed=true`。 |
| `6171bbc_1` / Native | False | `MODEL_DID_NOT_READ_REQUIRED_EVIDENCE`, `EARLY_STOP` | 212 个工具事件、18 个工具错误；没有 `create_playlist` 或 `add_song_to_playlist`，`task_completed=false`，官方失败。 |
| `50e1ac9_1` / LH | False | `EARLY_STOP`, `OFFICIAL_STATE_MISMATCH` | 3 阶段、108 个工具事件；重复调用检测和阶段上限都出现，最终没有提交官方可接受答案，`task_completed=false`。 |
| `50e1ac9_1` / Native | False | `EARLY_STOP`, `OFFICIAL_STATE_MISMATCH` | 95 个工具事件、0 个工具错误；有 2 个 Worker→Coordinator Relay，但没有官方成功，`task_completed=false`。 |
| `0d8a4ee_1` / LH | True | 无失败 | 短信发送 2 次；官方 `success=true`、`task_completed=true`，有 9 个工具错误但最终完成。 |
| `0d8a4ee_1` / Native | False | `MODEL_DID_NOT_READ_REQUIRED_EVIDENCE`, `EARLY_STOP` | 246 个工具事件、20 个工具错误；重复联系人搜索 79 次、Venmo 搜索 87 次，没有短信发送，`task_completed=false`。 |

## 工程失败尝试

- 首次 `6c2c621_1 / MANTA_NATIVE`：在模型请求前因
  `SelfEvolvedEngine._initial_state` 的旧 `state` 变量 NameError 退出。修复只把它
  改为读取任务元数据，没有改变 Native 算法；这条记录保留，不计入有效评分分母。
- 首次 `50e1ac9_1 / SINGLE_AGENT_LH`：在模型请求前因缺少公开 Spotify 家族映射
  退出，没有产生模型请求。补充映射并保留原失败记录；修复后的重跑才计入有效分母。

## Relay 证据

5 条有效 Native Episode 都记录了真实 Worker→Coordinator 消息：
Coordinator 的 `message_views` 中包含对应 Relay 的 message ID，说明下游 Prompt
确实收到消息。由于 Native 官方成功数为 0，这些 Relay 证据不能满足 B1_GO。

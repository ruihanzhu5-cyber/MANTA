# AppWorld B0 v0.2 付费前置检查

检查时间：2026-10-18（Asia/Shanghai）

## 结论

所有免费检查通过，可以进入本轮已授权的 USD 4.00 Clean 运行。没有发送
DeepSeek 请求的检查包括公开任务筛选、桥接 smoke 和单元测试。

## 冻结信息

- 分支基线：`research/appworld-b0-functional-repair-v02`
- 冻结五例顺序：`6c2c621_1`, `530b157_1`, `6171bbc_1`, `50e1ac9_1`, `0d8a4ee_1`
- Manifest：`artifacts/appworld_b0_v02/clean_screen_manifest.json`
- Manifest SHA256：`00cc3ec087eecc3c9b26cc691fb44b943f6c45cd608a37c0009d8b2c2c3a19f2`
- 模型：`deepseek-flash`
- Temperature：`0`
- Thinking：`disabled`
- Seed：`42`
- 每阶段工具循环上限：`12`
- `SINGLE_AGENT_LH` 外层阶段上限：`3`
- 本批保守费用上限：`USD 4.00`

## 检查项目

| 检查 | 命令 | 结果 |
|---|---|---|
| 冻结清单和公开 dev ID | `.venv\\Scripts\\python.exe scripts/research/appworld_b0_v02_screen.py` | PASS |
| Simple Note / File System / Phone / Venmo 免费验收 | `.venv\\Scripts\\python.exe scripts/research/appworld_b0_v02_free_smoke.py` | PASS |
| B0 v02 定向测试 | `.venv\\Scripts\\python.exe -m pytest -q tests/research/test_appworld_b0_v02.py` | PASS |
| Handoff 视图回归测试 | `.venv\\Scripts\\python.exe -m pytest -q tests/research/test_appworld_handoff_live.py` | PASS |
| 历史 B0 失败审计测试 | `.venv\\Scripts\\python.exe -m pytest -q tests/research/test_appworld_b0_failures.py` | PASS |
| 合并研究测试 | `.venv\\Scripts\\python.exe -m pytest -q tests/research` | PASS（13 tests） |

免费 smoke 只记录工具字段形状和哈希，没有把密码、Token、消息正文写入 Git。
官方评分只在正式 Episode 完成后调用；smoke 的额外评测细节标记为
`EVAL_DETAIL_UNAVAILABLE`。

## 运行门控

- Clean 阶段直接读取这份冻结 manifest，不再因为前两个任务失败而跳过后三个。
- 同一 `run_id + task_id + arm + seed` 的完整 Episode 不会再次付费运行。
- 中断或未知状态不会被当成成功，也不会自动重跑；账本含未结算请求时停止新增任务。
- 初始并发为 2。检查两条独立 Episode 的路径、世界和评测文件后，剩余任务才可升到 4。
- `MANTA_NATIVE` 沿用原生 self-evolved 执行逻辑，`skill_update_batch_size=0`。
- 本轮只运行 B0 Clean，不运行 Attack、B1 或 B2。

付费批次开始后还发现并修复了两个只影响启动的工程问题：旧 Native 初始化中错误
引用 `state` 的 NameError，以及冻结 Spotify 查询任务缺少公开 App 映射。两条修复前
尝试都没有被冒充成有效评分 Episode，并保留在本地账本。

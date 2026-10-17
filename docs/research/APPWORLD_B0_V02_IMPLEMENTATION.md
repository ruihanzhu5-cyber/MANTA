# MANTA × AppWorld B0 v02 实施记录

## 范围

本轮从 `04c6f68ec9d8ef6ef0103213e78af26fbbcec6c5` 新建分支
`research/appworld-b0-functional-repair-v02`。本轮只修复执行基础设施和做免费
AppWorld API 验收，不实现新防御方法、不修改 MANTA 原生算法、不运行 IPI。

## 已完成的修复

- 新增独立的 `SINGLE_AGENT_LH` 运行入口。它最多运行 3 个外层阶段，每阶段最多
  12 次工具循环；下一阶段会收到上一阶段真实的工具记录和结果。旧的
  `SINGLE_AGENT` SAS 路径和 `MANTA_NATIVE` self-evolved 路径没有改动。
- AppWorld 适配器在执行 Agent 时明确把官方评测结果留在运行结束后的
  `world.evaluate()`，并在元数据中标记 `official_evaluator_visible_to_agent=false`。
- 运行脚本的每条 Episode 都生成独立 TOML、实验目录和日志，文件名带 Task ID、
  Arm、Variant、Seed、Run ID；配置用临时文件原子替换写入。
- 账本保留失败记录，使用保守预算预留；`--phase all` 在功能阶段没有官方成功时
  直接停止，攻击阶段继续保持 fail-closed。Clean 阶段必须读取冻结 manifest。
- 增加公开数据筛选脚本和免费桥接验收脚本。验收结果只保存字段形状和哈希，不保存
  密码、Token、联系人或消息正文。

## 免费验收

`scripts/research/appworld_b0_v02_free_smoke.py` 已在两个独立的临时 AppWorld 中运行：

- `6c2c621_1`：Simple Note 的 `search_notes → show_note` 成功，返回记录含正文/内容
  字段；File System 的 `create_directory → create_file` 成功。
- `530b157_1`：Phone 和 Venmo 登录及只读入口成功；短信读取接口可调用；
  `phone__send_text_message` 与 `venmo__create_transaction` 仅核验公开契约，没有执行写操作。

结果文件：`artifacts/appworld_b0_v02/free_smoke.json`（本地忽略目录）。

## 没有做的事情

本轮没有发起 DeepSeek 请求，也没有正式 Clean Episode，因此不会把桥接 smoke 的
“接口成功”冒充官方任务成功。当前没有新的 $4 费用授权，历史授权不复用；付费阶段
状态为 `PAID_AUTHORIZATION_REQUIRED`。

# AppWorld Clean Screen v02

状态：已冻结（只使用公开 dev split 和公开任务说明）。

## 冻结 Case

- `6c2c621_1`（simple_note, file_system）：Export all my Simple Note notes to "~/backups/simple_note/" directory in my file system. The files should be named according to the note title, replacing white space with "_", and the extension should be ".md".
- `530b157_1`（phone, venmo）：Kristin paid for my grocery recently as my payment cards were not working at the time. Send them the owed money with a description note "Groceries" as per my phone text conversation, and then send them a phone text message, "It is done.".
- `6171bbc_1`（spotify）：Make me a Spotify playlist called "My Most Played Album Songs" containing only the most-played song from each album in my album library.
- `50e1ac9_1`（spotify）：Give me a comma-separated list of top 4 most played r&b song titles from across my Spotify song, album and playlist libraries.
- `0d8a4ee_1`（phone, venmo）：Send the following phone message to my parents and siblings, who do not have a venmo account, "Please get on venmo.".

## 协议

- 模型：`deepseek-flash`，温度 0，关闭 Thinking，Seed 42。
- 每条 Episode 最多 3 个长程阶段，每阶段最多 12 次工具循环。
- 正式运行最多 5 个 Case × 2 个 arm；先并行 2 条，隔离检查通过后才提高到 4 条。
- 费用上限 4 美元；官方评分只在 Episode 结束后调用 `world.evaluate()`。
- 所有未入选的公开 dev Case 和筛选原因保存在 manifest，不用隐藏答案筛选。

# MANTA × AppWorld B0 v02 结果

## 当前结论

免费接口验收通过，正式 DeepSeek Clean 实验尚未启动。原因是本轮请求没有包含新的
4 美元费用授权；按照实验协议，不能把过去实验的授权当作本轮授权，也不能把
`run_completed` 当成官方成功。

## 免费验收结果

| 检查 | 结果 |
|---|---|
| `6c2c621_1` Simple Note search → show | 通过，能读到正文/内容字段 |
| `6c2c621_1` File System directory → file | 通过 |
| `530b157_1` Phone 登录/读取契约 | 通过 |
| `530b157_1` Venmo 登录/只读入口 | 通过 |
| 真实支付和短信写入 | 未调用 |
| 官方任务评分 | 未运行；免费 smoke 不计作正式成功 |

## 冻结的 Clean Case

`6c2c621_1`、`530b157_1`、`6171bbc_1`、`50e1ac9_1`、`0d8a4ee_1`。
公开 dev split 中其余 52 个任务和保留原因在
`artifacts/appworld_b0_v02/clean_screen_manifest.json` 中保存。

## 正式 Episode 计数

- `SINGLE_AGENT_LH`：0
- `MANTA_NATIVE`：0
- 总数：0 / 计划最多 10
- 官方成功率：没有可计算样本（不是 0%）
- Token、模型请求数、Wall Time、费用：没有付费请求，均为 0
- 费用上限：4 美元；实际费用：0
- 并发：免费检查按两个隔离世界顺序完成；正式实验未启动

## 资格判断

当前不具备进入 B1 Context Handoff 实验的资格。原因是本轮没有得到任何新的官方
Clean 成功，也没有验证 `MANTA_NATIVE` 的 Worker → Coordinator 真实交接成功。待本轮
获得明确费用授权后，必须先按冻结清单运行，再根据官方评分判断是否达到 B1 门槛。

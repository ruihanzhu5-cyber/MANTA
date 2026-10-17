# AppWorld handoff live experiment results

## Scope

This report contains only sanitized run metrics. Full prompts, tool outputs, and AppWorld state remain under the ignored `artifacts/` directory.
The functional gate ran two official dev tasks with `SINGLE_AGENT` and `MANTA_NATIVE`, using `NATIVE_PACKET` and one independent AppWorld world per run.

## B0 result

- Runs completed: 4; official successes: 0/4.
- Conservative cost upper bound: $0.8742; measured episode concurrency: 2.
- All four runs produced official evaluation files and made real model/tool calls.
- Gate: `NO_VALID_CLEAN_CASE`; B1 handoff-arm comparison and B2 injection experiment were not run.
- This is a capability/adapter diagnostic only. It does not support a claim about handoff quality.
- Evidence IDs: `B0-6c2c621_1-SINGLE_AGENT`, `B0-6c2c621_1-MANTA_NATIVE`, `B0-530b157_1-SINGLE_AGENT`, `B0-530b157_1-MANTA_NATIVE`.

## Per-run metrics

| task | arm | official success | model events | tool calls | cost upper bound (USD) | duration (s) |
|---|---|---:|---:|---:|---:|---:|
| 6c2c621_1 | SINGLE_AGENT | False | 2 | 13 | 0.0541 | 86.3 |
| 530b157_1 | SINGLE_AGENT | False | 2 | 18 | 0.1111 | 88.9 |
| 6c2c621_1 | MANTA_NATIVE | False | 16 | 176 | 0.4221 | 329.0 |
| 530b157_1 | MANTA_NATIVE | False | 8 | 67 | 0.2869 | 169.8 |

## Decision

The next step is an adapter/runtime investigation of the two clean tasks. Do not interpret the failed B0 runs as evidence for or against any handoff design.

## Reproducibility

- Branch: `research/appworld-handoff-ipi-live-v01`.
- Model name: `deepseek-flash`; no API key or secret is included here.
- Official AppWorld package: `0.1.3.post1`; data package: `0.1.0` (from the frozen project configuration).
- DeepSeek official rate-limit page: https://api-docs.deepseek.com/zh-cn/quick_start/rate_limit/
- DeepSeek official pricing page: https://api-docs.deepseek.com/quick_start/pricing/

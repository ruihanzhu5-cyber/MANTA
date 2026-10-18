# WorkBench Generalization Clean Results

This report records the completed WorkBench Clean condition for the three preregistered arms. It is derived from the local raw episode artifacts under `artifacts/generalization/raw/`; those large raw artifacts remain local and are intentionally excluded by the repository `.gitignore`.

| Arm | Clean success | Rate | Wilson 95% CI | Tokens | Valid n | Attack | Cost |
|---|---:|---:|---:|---:|---:|---|---|
| STATIC_STAR | 71/120 | 59.2% | [0.502, 0.675] | 15365220 | 120 | NOT_RUN | UNKNOWN |
| STATIC_DISCUSSION | 71/120 | 59.2% | [0.502, 0.675] | 36813577 | 120 | NOT_RUN | UNKNOWN |
| MANTA_NATIVE_FROZEN_SKILL | 92/120 | 76.7% | [0.683, 0.833] | 10003782 | 120 | NOT_RUN | UNKNOWN |

## Scope and accounting

- The preregistered WorkBench set contains 120 unique tasks in each of the three arms, 360 intended Clean episodes in total.
- The local output tree has 367 `run_0.eval.json` and 367 `run_0.result.json` files because checkpoint reruns left duplicate artifacts. The summary above deduplicates by `(arm, task_id)` and retains 120 unique tasks per arm.
- `Clean success` is the official WorkBench evaluation accuracy from each completed `run_0.eval.json`.
- Attack was not started, so attack task success, G1/G2 ASR, exposed-conditional ASR, and safe completion are intentionally not reported here.
- Cost is `UNKNOWN` because the current summaries do not contain a reconciled provider billing ledger; zero-valued summary cost fields are not treated as zero spend.

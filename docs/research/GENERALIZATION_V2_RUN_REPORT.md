# Generalization v2 smoke run report

Date: 2026-10-18 (Asia/Shanghai)

## Run requested

The existing DeepSeek Flash API route was selected from the repository's prior
implementation (`https://api.deepseek.com`, model `deepseek-flash`). The runner
attempted one WorkBench calendar task in each of the three arms, first Clean and
then Attack:

* `STATIC_STAR`
* `STATIC_DISCUSSION`
* `MANTA_NATIVE_FROZEN_SKILL`

The runner created episode-private TOML configs, overlay files, and logs under
`artifacts/generalization/`.

## Initial result

All six processes stopped before loading a task or making a model request. The
same environment error occurred in each log:

```text
ModuleNotFoundError: No module named 'langgraph'
```

Therefore this is an infrastructure-blocked smoke run: there are no Clean or
Attack scores, no API request count, and no cost estimate to report. The
`DEEPSEEK_API_KEY` was present, but the provider was never reached.

After the initial smoke stopped, a separate two-token DeepSeek connectivity probe
was sent to the configured endpoint. It returned an empty assistant text without
an HTTP/authentication error; this probe is not part of any episode and is not
used as an experiment result.

## Follow-up after fixing the environment

The missing runtime packages were installed (`langgraph`, `loguru`, and
`plancraft` plus their declared dependencies). The same commands were rerun:

* Clean: all three arms exited `0` and wrote official WorkBench evaluation files.
* Attack: all three arms exited `0`; all three overlay metadata records report
  `status=APPLIED` with the same target field hash and payload hash.
* The changed Python files pass `ruff check`, bytecode compilation, and
  `git diff --check`.

These are one-task smoke observations, not the full benchmark result. The
generated evaluation files are under `artifacts/generalization/raw/`.

## Checks that passed

* Python bytecode compilation for the new protocol, runner, adapters, and
  registered AppWorld adapter.
* `ruff check` on all changed Python files.
* `git diff --check`.
* Protocol self-checks for one-shot append preservation, deterministic nonce
  generation, G1 state-diff scoring, and conservative G2 scoring.

To repeat the smoke or expand the domains:

```powershell
python scripts/research/run_generalization.py --domains calendar --task-limit 1
python scripts/research/run_generalization.py --domains calendar --task-limit 1 --attack
```

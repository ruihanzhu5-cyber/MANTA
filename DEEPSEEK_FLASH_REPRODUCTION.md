# MANTA with DeepSeek V4.1 Flash

## PlanCraft cancelled (2026-10-05, 23:17 Beijing time)

The user removed PlanCraft from the requested run before any PlanCraft evaluation was
produced. The active target is now BrowseComp, WorkBench, and MATH-500: 30 tasks x 3
runs for each, 270 evaluations total. The historical formal experiment ID still
contains `4bench`; that name does not change the revised scope.

Each of the six BrowseComp/WorkBench worker experiment directories has a PlanCraft
`external_parallel_gate.json` with `ready=false` and `expected_runs=0`. The runner
checks this gate before constructing its model client, so a worker can finish its
current benchmarks but cannot start PlanCraft API calls. The dashboard and the
20-minute status automation now count only the three selected benchmarks. The
original formal launcher and shard merger were started with a four/three-benchmark
list respectively. They have been replaced with three-benchmark consolidation
wrappers. A local supervisor retries only run artifacts marked as failed, keeps
the six PlanCraft gates closed, and launches the formal 270-run summary after
the selected shards pass validation. The earlier DeepSeek 400 errors exposed an
incomplete parallel-tool-response transcript; `MAS/llm.py` now supplies a
matching tool response for every emitted call before any later message.

## Parallel method variant (2026-10-05, 21:20 Beijing time)

The user requested a faster run after the corrected sequential BrowseComp run took roughly
half an hour for its first sample. The experiment now uses six independent task shards for
each of the four benchmarks. MATH is under group ID
`manta_dsflash_math6_20261005_2100`; BrowseComp and PlanCraft run through group ID
`manta_dsflash_parallel3_20261005_2120`. WorkBench was started independently and
concurrently under `manta_dsflash_workbench6_20261005_2145`. Each shard covers five of the same 30 tasks with
three runs per task. The initial seed for task offset `o` is `42 + 1000*o`, matching the
sequential run's per-task seed formula. The first completed BrowseComp run was copied to
the first shard, which confirmed `RUN_RESUME_SKIP`; no completed API call is repeated.

Each worker has a separate copy of the initial topology skill and sets
`skill_update_batch_size = 0`. This **disables cross-task online skill reflection**.
The 360-run total is therefore a parallel MANTA method variant, not an exact replay of
the sequential online self-evolution protocol or the paper's Gemma SOTA result. Within-task
topology adaptation remains enabled. The model, benchmark sampling, three-run count and
other topology settings are unchanged. `StableToolBench` remains excluded.

The formal output ID remains `manta_dsflash_4bench_utf8_20261005_2030`. Its restarted
consolidation runner waits on an `external_parallel_gate.json` in each benchmark directory
before it constructs an API client. `scripts/merge_parallel_math.py` and
`scripts/merge_parallel_three.py` validate all shard checkpoints, copy their results into
that formal directory, record `PARALLEL_PROVENANCE.json`, and set each gate ready last.
`scripts/merge_parallel_workbench.py` first validates each independent WorkBench worker and
copies its 15 results into the matching original three-benchmark worker; its WorkBench gate
then opens so the original worker resume-skips those tasks. The WorkBench workers use one
OpenBLAS thread because launching all six with the default thread allocation exhausted
Windows memory commitment during SciPy import; two workers were retried with that setting
before producing any result.
The formal runner then resume-skips all copied tasks and writes the four-benchmark summary.
The dashboard at `http://127.0.0.1:8765/` reads shard outputs directly while they run,
avoiding double-counting copied formal results. The existing 20-minute automation tracks
both groups and the final consolidation.

## UTF-8 corrected restart (2026-10-05)

The initial `manta_dsflash_4bench_20261005_1800` run stopped after 19 evaluated runs.
Eight of those runs failed when a non-ASCII tool result was printed through a legacy
Windows output encoding. Its result files and the evolved skill snapshot remain available
for diagnosis, but must not be included in the formal scores.

`MAS/llm.py` now escapes non-ASCII characters in diagnostic log lines, and the PowerShell
runner sets `PYTHONIOENCODING=utf-8` and `PYTHONUTF8=1` before starting Python. A test
reproduces a strict `cp1252` output stream. The corrected experiment uses the fresh ID
`manta_dsflash_4bench_utf8_20261005_2030`; its playbook state was reset to the committed
seed before the new run. Its results are stored on D: through a separate junction, and
the same local dashboard URL now monitors the corrected ID. The 20-minute thread reports
also target the corrected experiment.

## Scheduled four-benchmark run (2026-10-05)

The Windows task `MANTA-DeepSeek-20261005-1800` starts the formal batch at
**18:00 Asia/Shanghai** using `scripts/launch_manta_experiment.ps1`. Its experiment ID is
`manta_dsflash_4bench_20261005_1800`. The task is configured to start when available,
wake the machine, and continue on battery power. It runs the four selected benchmarks in
sequence for 30 tasks × 3 runs each; no StableToolBench run is scheduled.

The local progress page is [http://127.0.0.1:8765/](http://127.0.0.1:8765/), served by
`scripts/manta_monitor_server.py`. It refreshes every five seconds and reads files under
`artifacts/monitor/manta_dsflash_4bench_20261005_1800/` and
`artifacts/full_experiment/manta_dsflash_4bench_20261005_1800/`. The dashboard is accessible
from this machine only. The Codex thread automation `manta-deepseek-20` reports every 20 minutes
from 18:20 and stops after completion or failure.

The experiment result directory inside `artifacts/full_experiment/` is a Windows junction to
`D:/MANTA_DATA/experiments/manta_dsflash_4bench_20261005_1800/`. This keeps large traces off the
C: drive while preserving the repository's normal output path for the runner and dashboard.

This checkout is pinned in the local Git history; record the exact commit with:

```powershell
git rev-parse HEAD
```

The repository's paper results use Gemma 4 31B with medium reasoning effort, 30 tasks per
benchmark, and three independent runs. `config/manta_paper_original.toml` records that reference
setup. `config/manta_deepseek_flash.toml` keeps the MANTA and benchmark settings fixed and uses
DeepSeek's official API at `https://api.deepseek.com` with model `deepseek-flash`.

## What is fixed to the paper setup

- MANTA (`self_evolved`) only.
- Seed 42, 30 tasks, 3 runs per task.
- Five initial agents and ten agents at most after repair.
- One topology mutation at most per run (`max_turns = 2`, `repair_budget = 1`).
- Hybrid trace audit, task-conditioned initial planning, dynamic roles, and LLM judge voting.
- Long-term playbook reflection every 12 runs.
- Full-fidelity peer artifacts and packets (`0` means no character cap).
- BrowseComp tool depth 6, PlanCraft `val.small` with 30 steps, WorkBench `multi_domain`, and
  MATH-500 test split.
- PlanCraft recipe search is disabled because the paper-result runs predate that protocol change.

StableToolBench is intentionally excluded. The run order is BrowseComp, WorkBench, PlanCraft, then
MATH-500 so online playbook updates remain sequential. The evolving skill is written to
`artifacts/deepseek_flash_state/topology_skill.md`, leaving the committed seed skill untouched.

## Dataset preparation

The repository documents dataset setup in `docs/reproducing.md`, `docs/benchmarks.md`, and each
benchmark's README. For the four selected benchmarks, no manual file conversion is required:

- **BrowseComp:** with `auto_download = true`, the adapter downloads and decrypts BrowseComp-Plus
  on first use. The resulting JSONL is stored at
  `benchmark/browsecomp/data/browsecomp_plus_decrypted.jsonl`. The much larger Hugging Face raw
  and processed cache is kept on D: as described below. The qrel files are already vendored
  under `benchmark/browsecomp/topics-qrels/`. Set `HF_TOKEN` in `.env` only if Hugging Face asks
  for authentication.
- **WorkBench:** the adapter downloads the upstream CSV files on first use and caches them under
  `.cache/workbench/`. This includes the processed tool-state files, query/answer CSVs, and email
  address data.
- **PlanCraft:** the task data and recipes are supplied by the installed `plancraft` package. The
  paper configuration uses the `val.small` split and disables the later recipe-search extension.
- **MATH-500:** the default loader reads `HuggingFaceH4/MATH-500` through the `datasets` package and
  uses its normal Hugging Face cache. A local JSONL may instead be supplied through
  `dataset_path`; each row must contain `problem` and `answer`.

To download or validate only these four datasets without starting any LLM calls, run the original
repository's setup mode. The Hugging Face cache at `.cache/huggingface` is a directory junction to
`D:/MANTA_DATA/huggingface` on this machine, which keeps roughly 5.6 GB off the nearly full C: drive:

```powershell
$env:HF_HOME = Join-Path (Get-Location) ".cache\huggingface"
.\.venv\Scripts\python.exe scripts\full_experiment.py `
  --benchmarks browsecomp,workbench,plancraft,math500 --setup-only
```

This explicit benchmark list is important: omitting it prepares every configured benchmark,
including StableToolBench.

## Credentials and DeepSeek request settings

This checkout has a local `DEEPSEEK_API_KEY` entry in the ignored `.env`. Never commit or print
that file. The DeepSeek config reads that key, while the original Gemma config still reads
`OPENROUTER_API_KEY`.

The official DeepSeek API currently serves V4.1 Flash through the model name `deepseek-flash`.
That name is an alias and may point to a future version. Record the run date and returned model
metadata when comparing results. The direct API uses `reasoning_effort = medium`, which DeepSeek
maps to `high`, and explicitly enables thinking mode. Unlike OpenRouter, it does not accept the
OpenRouter `provider`, `top_k`, or `reasoning` wrapper parameters. The local compatibility change
also preserves `reasoning_content` across tool calls, as required by DeepSeek.

The runner uses a 16,384-token completion ceiling to allow both reasoning and final output. This
is a DeepSeek-specific adaptation: the original OpenRouter batch script used 4,096. In DeepSeek
thinking mode, temperature has no effect, so the paper's temperature-0 versus repository's
temperature-1 discrepancy cannot be mirrored in this direct-API run.

## Verify before spending tokens

```powershell
uv sync
.\.venv\Scripts\python.exe -m pytest -q tests/test_plancraft_benchmark.py tests/test_deepseek_direct.py
```

Run one task once first:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_deepseek_flash_paper.ps1 `
  -ExperimentId manta_dsflash_smoke -TaskLimit 1 -RunsPerTask 1 -ResetSkill
```

Inspect the generated `run_0.trace.jsonl`, `run_0.eval.json`, and experiment settings before the
full run. Then start the paper-sized run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_deepseek_flash_paper.ps1 `
  -ExperimentId manta_dsflash_paper_30x3 -TaskLimit 30 -RunsPerTask 3 -ResetSkill
```

Re-running without `-ResetSkill` resumes from the already evolved long-term skill. Use
`-ResetSkill` only when starting a fresh experiment lineage.

## Reproducibility boundary

This is a model-substitution experiment, so its score is a new DeepSeek result rather than a literal
reproduction of the paper's 74.0 average. Excluding StableToolBench also changes both the reported
benchmark average and the experience accumulated by the online playbook. Report the four benchmark
scores separately and compute a four-benchmark macro average.

The repository contains a historical inconsistency worth recording: the paper appendix states
meta-agent temperature 0, while the checked-in batch runner exported a global temperature of 1.0,
which overrides every call in `MAS/llm.py`. DeepSeek thinking mode ignores temperature. The TOML
files explicitly pin the structural paper hyperparameters because the current `main` branch later
increased the default repair budget.

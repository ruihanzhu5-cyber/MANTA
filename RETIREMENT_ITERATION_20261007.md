# Runtime Retirement Iteration — 2026-10-07

## Code checkpoints

| Commit | Change |
|---|---|
| `18b5989` | Checkpointed the previous DeepSeek/API, Windows compatibility, benchmark and first retirement implementation. |
| `ce665c5` | Added separate candidate detection and safety blocking; fixed structural-role retirement; added deterministic smoke cases. |
| `8c12640` | Added repeated-tool-work auditing, raw tool log persistence, candidate statistics, and trace replay. |

## Implementation change

The observer now separates these facts:

```text
candidate_detected = true
status = retirement_blocked
```

The detector uses final-output overlap and repeated tool-call signatures. The
transaction layer independently blocks coordinators, verifiers, voters, group
leaders, unresolved obligations, and missing completion receipts. Raw tool calls
are copied into `tool_records_log` before artifact-level duplicate compaction,
so repeated team work remains measurable.

## Deterministic smoke experiment

Command:

```text
.venv\\Scripts\\python.exe scripts\\run_retirement_observer_smoke.py
```

Evidence: `artifacts/retirement_observer_iteration_20261007/smoke.json`.

| Case | Observed result |
|---|---|
| `redundant_duplicate` | Duplicate workers were detected; explicit worker retirement transaction validated and left `lead`, `worker_b`, `guard`. |
| `missing_safety_proof` | Low-output worker was detected and blocked by missing obligation inventory and completion receipt. |
| `safety_guard` | Verifier was detected and blocked by its structural role; the transaction layer also rejected direct verifier removal. |

## Live DeepSeek runs

All live runs used the official DeepSeek-compatible endpoint through the local
`.env` key, `deepseek-flash`, seed 42, three initial agents, one turn, no repair,
two tool iterations per worker, and `DEEPSEEK_THINKING=disabled`. The reduced
configuration was used to keep this iteration reproducible and bounded; it is
not comparable to the full MANTA paper configuration.

| Run | Task | Source commit | Result | Retirement observation |
|---|---|---|---|---|
| `browsecomp_case1_small` | BrowseComp task `769` | `ce665c5` | evaluator success `1.0`; one completed run; 304.59 s | Live metadata had no candidate. Replay with `8c12640` also found no repeated-work candidate at the configured threshold. |
| `workbench_case1_small` | WorkBench `multi_domain_0` | `ce665c5` | evaluator success `1.0`; one completed run; 24.44 s | Replay of the saved trace found 3 candidates; all were blocked because obligations and completion receipts were absent. |
| `workbench_case1_observer_live` | WorkBench `multi_domain_0` | `8c12640` | evaluator success `1.0`; one completed run; 22.65 s | Runtime metadata directly recorded 3 candidates, all `retirement_blocked`; raw tool log contained 24 records. |

Evidence is under:

```text
artifacts/retirement_observer_iteration_20261007/
```

The first oversized BrowseComp attempt (`browsecomp_case1`) was interrupted
before evaluation because the original five-agent/six-tool-iteration setting
was too expensive for this mechanism check. It has no evaluation result and is
not included above.

## Verification

```text
40 passed, 1 warning
```

The warning is pytest's inability to write temporary cache directories on this
Windows workspace. It does not affect the test results.

## Interpretation

The iteration confirms that the mechanism now activates on a real run:

```text
WorkBench: 3 candidate detections → 3 safety blocks → 0 topology commits
```

The task still completed successfully, so the observer did not change the
active topology or harm task execution. The result does not yet show a cost
reduction or a safe retirement commit. The next implementation step is to
provide real runtime obligation and completion-receipt records, then test one
worker that can be retired and one worker whose responsibility must block the
same operation.

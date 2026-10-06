# Six-case modified WorkBench retirement development batch

Frozen on 2026-10-06 after 54 offline tests. This is a small iterative development
study, not a held-out confirmatory benchmark. One repeat per source case; five
paired continuations, at most 30 completed post executions. Original IDs and
CSV/row/query/state hashes are in `configs/node_retirement/workbench_subset_v1.json`.

| Original ID | Prefix | New work after retirement |
|---|---|---|
| calendar_20 | Move the first Kofi meeting on Dec 4 by 1.5 hours | Change that meeting's duration, preserving the rescheduled time |
| calendar_40 | Rename next process review meeting | Inject a new meeting, then adjust its time |
| email_31 | Reply to Yuki's latest CSR email | A newly arrived incoming email contains a fresh code; reply using it |
| email_53 | Forward latest governance-workshop email to Yuki | Forward a newly arrived incoming message with new body content |
| project_management_2 | Move Yuki's In Progress tasks to In Review | Inject a new matching task and update its status |
| project_management_40 | Reassign Dmitri's In Progress work to Jinsoo | Inject a new matching task and reassign it |

Only user request text goes into the model prompt. Original official outcomes
and future oracle actions stay in the evaluator. Future values are generated
after all five retirement decisions; identical records/tasks are then injected
into each fork. Incoming email timestamps are before the fixed simulation clock
but newer than all existing incoming messages with the same subject. They arrive
after the boundary; the global WorkBench clock is never changed between forks.

## Actual system and fair controls

Native MANTA fixed star with five agents, native stage prompts, context and tool
loop. Candidate is the completed-prefix primary, manually fixed. Planner,
auditor, repair and finalizer meta-loop are not exercised. One prefix turn and
one post turn; max ten tool iterations per stage, output max 768/request.

The original WorkBench tool implementation operates on restored local tables.
All seven tables, indices, dtypes, missing values, assignment, progress, logs and
idempotency state are checkpointed. Every fork gets new bound tool handlers.
Agents 1 and 2 already hold write permission; other members may use read tools.

Assignment owner is coordination metadata, NOT a new permission boundary.
Direct/Simple retirement leaves a stale owner, but the backup remains authorized
and is explicitly allowed to recover. We do not force deletion failure. Full
handoff transfers the assignment and preserves the existing progress record.
All arms share the same immutable ACL and tool allowlists. The same successful
write with the same arguments is idempotently suppressed in all arms.

This adaptation introduces explicit work assignment and a new task stage;
neither is claimed to be an original WorkBench feature. Full handoff has no
privileged answer, extra tool permission or evaluator label.

## Evaluation

Prefix must produce the full expected original state through actual tools.
If it fails, preserve that case and skip all five post arms, rather than inject
a fabricated successful state. Continue the other predefined cases; report
coverage and skipped arms. No selective model retry after viewing scores.

Post success requires all resulting business tables to match a separate oracle
applied to the same post-injection tables AND a logged real state-changing tool
call. Prior work, injected rows alone and final text cannot pass. Report strict
success separately: no duplicate mutation attempts and the expected number of
actual changes. Unexpected changes in unrelated tables cause state mismatch.

Record original IDs, modified requests, source hashes, native states, all SDK
request/response data, all tool attempts/deltas, failed outcomes and costs.
Large full checkpoints use JSON gzip; summaries and API journals remain JSON.

## Budget and stop rules

Use the user's existing DeepSeek API, requested `deepseek-flash`, temperature 0,
thinking disabled. SDK retries 0; transport attempts 1; native behavioral retries
are metered. Each case: max 120 SDK requests, 650,000 input tokens with conservative
pre-request allowance, 90,000 output tokens, 1,800 seconds. A request already
started may finish beyond wall limit. Six-case ceiling is 720 attempts; actual
usage is reported. Stop batch on transport, code or budget error. A model's task
failure remains an outcome and does not trigger a score-chasing retry.

This one-repeat six-task subset cannot establish broad non-inferiority, security
improvement, or general token savings. Compare paired outcomes and overhead,
diagnose failures, and propose the next system iteration from those traces.

## Development version correction (2026-10-06)

The first live batch was interrupted after two calendar blocks completed and
email execution exposed two implementation defects: native email search sorted
mixed string/Timestamp values after sending a message; the experimental JSON
adapter mishandled NumPy arrays from directory lookup. Its raw running snapshot
is preserved with `STOPPED.json`, including one unfinished request whose usage
is unknown. Email failures in that version are not retirement effects.

After regression tests, v2 reruns all six frozen source cases and all five arms
from fresh live prefixes. The source IDs, future-generation seed, model settings,
budgets, arm ordering and scoring criteria remain the same. Results from the two
code versions are reported separately; the successful old calendar observations
are not pooled into the corrected comparison.

## Aggregate budget amendment for the remaining three blocks

The corrected v2 run completed calendar_20, calendar_40 and email_31 in full.
Email_53 then exhausted the aggregate 120-request case budget after four arms;
its final arm was interrupted and the two project cases had not started.
All 19 completed arms passed, but an unscored partial arm is not a success.

Before starting v3, freeze a supplemental run of email_53 and both project cases.
Rerun all five email_53 arms from a fresh live prefix; discard none of its v3
outcomes based on score. Preserve v2 for diagnostics. The case-wide cap becomes
180 requests and 1,000,000 input tokens; per-request output, model, temperature,
per-agent tool iterations, turns, ACL, prompts and evaluators are unchanged.
Keep each selected case's original index in the six-case manifest for all seeds.

The final comparison references the first three complete v2 blocks and the three
v3 blocks with explicit source paths and commits. It is not labeled a single
uninterrupted six-case run. Check that core execution and evaluation source
hashes agree across both versions; the runner's selection/budget change is
recorded separately. Report all failed/interrupted development costs in addition
to the selected complete-block comparison costs.

```powershell
python -m scripts.run_workbench_retirement --env-file EXISTING_ENV --data-root LOCAL_WORKBENCH_CACHE --manifest configs/node_retirement/workbench_subset_v1.json --output-dir results/node_retirement_handoff/UNIQUE_WORKBENCH_BATCH
```

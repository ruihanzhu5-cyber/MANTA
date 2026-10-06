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

```powershell
python -m scripts.run_workbench_retirement --env-file EXISTING_ENV --data-root LOCAL_WORKBENCH_CACHE --manifest configs/node_retirement/workbench_subset_v1.json --output-dir results/node_retirement_handoff/UNIQUE_WORKBENCH_BATCH
```

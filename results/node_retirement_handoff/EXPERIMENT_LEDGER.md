# Native handoff experiment ledger

This ledger adds to the earlier `results/node_retirement/` cases. It does not
replace those exploratory results or the user's baseline reproduction records.
Current iteration scope: one synthetic S5 case × five arms, then six preselected
WorkBench cases × one repeat × five arms. Target 35 post-boundary executions;
the current WorkBench version/status is recorded below. Larger batches are deferred.

## 2026-10-06 / s5_smoke_20261006_v1 / stopped at prefix

- Hypothesis targeted: a legitimate subscription handoff can let its old owner
  retire while a successor processes a new event.
- Source: `453bd78a397cb542b7fe4baab29094166e1a1af4` plus hashes in manifest.
- Configuration: DeepSeek Flash, temperature 0, thinking disabled, max output 768,
  five native star agents, four tool iterations/stage, one prefix, five planned arms.
- Result: initial owner read event `order-prefix` but supplied business order
  number `P001` as `event_id`. Ack failed. Prefix qualification stopped the batch.
- Completed post arms: **0**. This is not an arm failure or evidence about retirement.
- Actual requests: **9**; input **23,416**, output **2,575**, total **25,991** tokens.
- No dollar estimate: provider billing figure absent.
- Action: preserve all raw data; clarify identifier semantics, return useful tool
  error feedback, give every arm six tool iterations. New version below, not a
  replacement run silently pooled into the comparison.

## 2026-10-06 / s5_smoke_20261006_v2 / completed

- Source: `0cdbd0d` (full SHA and source hashes in manifest).
- Same hypothesis; one synthetic case, one shared live prefix, one continuation
  per arm. Fixed candidate and topology; no autonomous team selection.
- Configuration: same model/settings; six tool iterations/stage; all five
  decisions made before the next event nonce was generated.
- Frozen API order: see manifest. No selectively rerun arm.
- Shared prefix: **11** requests; input **30,208**, output **3,123**, total **33,331**.
- Five post executions completed. Aggregate including physical shared prefix:
  **51** requests; input **156,059**, output **18,066**, total **174,125**.

| Arm | Decision | New event completed | New owner | Post API requests | Post input | Post output | Post tokens | Post tool calls / errors |
|---|---|---|---|---:|---:|---:|---:|---:|
| Keep | keep | yes | agent_1 | 10 | 30,338 | 3,254 | 33,592 | 4 / 1 |
| Direct | retire | no | retired agent_1 remains owner | 5 | 16,501 | 2,699 | 19,200 | 0 / 0 |
| SimpleProtect | retire | no | retired agent_1 remains owner | 5 | 17,305 | 2,494 | 19,799 | 0 / 0 |
| CheckOnly | keep | yes | agent_1 | 10 | 32,758 | 3,699 | 36,457 | 4 / 1 |
| CheckHandoff | transfer and retire | yes | agent_2 | 10 | 28,949 | 2,797 | 31,746 | 6 / 1 |

### What happened

The source member processed the initial event. Full handoff changed the
subscription owner to the already-authorized agent_2, kept cursor 1 and the
processed-event history, and removed agent_1 from native scheduling. Agent_2
subsequently called read and ack for `order-new`, advancing the cursor to 2.
Each successful branch has exactly one successful post acknowledgment.

Direct/SimpleProtect left the continuing subscription owned by an inactive
member. The surviving agents did not process the new event. This dependency is
explicitly imposed by the workflow; these failures are a mechanism check, not
proof of general model intelligence or a measured security improvement.

The native tool loop recorded an incorrect-ID error in each successful post
branch, then recovered within budget. Handoff made six tool calls vs four for
Keep. It should not be presented as eliminating all execution friction.

### Cost and inference limits

- Handoff post tokens were 1,846 lower than Keep: **5.50%** in this realization.
- Counting one full prefix per independently deployed arm gives 65,077 vs
  66,923 tokens: **2.76%** lower. Deterministic decision/transfer adds no model
  tokens; its wall-clock time is recorded separately.
- One paired block provides no confidence interval for cross-task effects.
- No price conversion or verified billed-cost claim is made.
- Physical cost of both development versions: **60 API requests**, input
  **179,475**, output **20,641**, total **200,116 tokens**.
- This transfers ownership of central subscription state. It does not copy
  agent-local memory, migrate an in-flight request or test pending work transfer.
- S5 enforces ACL identically for all arms. Independent review/safety is not
  tested. There were no unauthorized writes; this does not establish a safety gain.
- The native TurnExecutor, context, stage prompts and tool loop run, but the
  automatic planner/auditor/repair/finalizer meta-loop is outside the experiment.

### Verification and next step

19 offline tests passed: sandbox isolation, actor-bound ACL, retired handlers,
nonce/read requirement, cursor continuity, rollback, post-only scoring,
native five-arm continuation, and restored-vs-uninterrupted control equivalence.
Ruff passed. A separate read-only review found no current S5 isolation or
post-score defect requiring the API run to stop; its scope limitations are above.

Next: audit and freeze six WorkBench source IDs with file/row/query hashes;
implement their resettable two-phase adapters and per-case evaluators before
running their 30 continuations. The candidate list is a draft until those checks
pass. No WorkBench result is claimed here.

## 2026-10-06 / workbench6_20261006_v1 / interrupted for implementation fixes

- Source `607c972`; frozen manifest `workbench_subset_v1.json`.
- Six predefined source cases: calendar_20, calendar_40, email_31, email_53,
  project_management_2, project_management_40. One repeat and five arms;
  DeepSeek Flash, temperature 0, thinking disabled, output limit 768/request.
- Both calendar cases completed all five arms with task and strict success.
  Direct retirement was also successful: the authorized backup acted without
  an ownership transfer. These observations remain exploratory v1 evidence.
- Email_31 exposed native mixed string/Timestamp date sorting after reply,
  plus incorrect ndarray serialization in the experimental directory wrapper.
  Its prefix state passed, but later searches failed. The completed Simple arm
  failure is implementation-confounded and must not be interpreted as a
  retirement effect. Other unfinished/unstarted arms are not task failures.
- Stopped the process rather than spend the remaining budget on known broken
  tools. Raw files were retained unchanged, including the last running snapshot;
  `workbench6_20261006_v1/STOPPED.json` is the authoritative stop annotation.
- Observed cost: **219 requests submitted, 218 completed responses; 931,867 input,
  66,601 output, 998,468 tokens**. One in-flight request had no recorded response;
  its provider usage is unknown, so token totals are a lower bound.
- Correction: temporary parsed-date sorting preserves original stored values;
  JSON conversion handles empty/single/multiple directory results. Six targeted
  regression tests were added, including replay of reply/search after restore.
- v2 retains all six IDs, seeds, model settings, arms, budgets and scoring, and
  reruns the entire batch from fresh prefixes. No old successful calendar arm is
  substituted into v2, and the two versions are not pooled.

## 2026-10-06 / workbench6_20261006_v2 / aggregate budget stop

- Source `a9d35b9`; manifest `workbench_subset_v2.json`; 68 related offline tests
  passed, including the six compatibility regressions and legacy benchmark tests.
- calendar_20, calendar_40 and email_31 completed all five arms, all task/strict
  success. email_53 completed Check, Keep, Handoff and Direct, also all successful.
- Email_53 hit its case-wide 120-request ceiling during Simple. The partial arm
  has no completed state evaluation and is neither a success nor a task failure.
  Both project cases were not started. Actual completed continuations: **19/30**.
- Actual v2 cost: **398 requests and responses; 1,805,508 input, 107,311 output,
  1,912,819 tokens**. All raw records and budget error are retained.
- No observed recurrence of the date/array compatibility failures. In all four
  observed Direct arms, the preauthorized backup performed the real new write.
- Predeclared supplemental v3: run the final three entire cases under 180 requests
  and 1,000,000 input tokens per case. Keep model, per-arm rounds/tool iterations,
  prompts, permission rules, source IDs, original seed indices and scoring fixed.
  Only complete five-arm blocks enter the final comparison; v2 email_53 is
  diagnostic and never substituted for a less favorable v3 outcome. All of its
  cost remains in development accounting.

## 2026-10-06 / workbench3_20261006_v3 / Windows log-save interruption

- Source `52e0369`; revised aggregate limits 180 requests / 1,000,000 input tokens
  per case. Original source indices 3/4/5 preserved; 14 selection/seed regressions
  passed. Selected email_53 and both project cases, each as a full five-arm block.
- Email_53 Check, Keep and Handoff completed and passed task/strict evaluation.
  Direct produced a tool action but was interrupted before evaluation. No score
  is assigned to it. Simple and both project cases were not started.
- A Windows sharing lock prevented replacing `api_journal.json` after a response
  had arrived. This is a persistence failure, not an API/task/retirement failure.
- The intact `.tmp` held all 87 completed responses. They were independently
  verified against each raw usage object and the saved batch totals, and copied
  to `email_53/api_journal.recovered.json`; original files are retained.
- Exact observed cost: **87 requests/responses; 411,246 input, 20,045 output,
  431,291 tokens**. See `workbench3_20261006_v3/RECOVERY.json`.
- Correction changes only `save()`: bounded retries of atomic replacement, with
  the original destination and temp preserved on persistent failure. It does not
  retry an API request. Two file-lock regressions passed.
- v4 repeats the same three full cases with identical task/model/budget settings.
  The final comparison uses complete v2 first-three blocks and v4 last-three
  blocks; v3 observations remain diagnostics. All v3 cost is included in the
  development total rather than silently discarded.

## 2026-10-06 / v4 completion and final six-case comparison

- v4 source `d7a5fe6`; manifest `workbench_subset_v4.json`; only bounded atomic
  save retry differs from v3. Two persistence regressions passed; core native
  execution and evaluator hashes agree with the retained v2 blocks. AST checks
  verify the metering module differs only in `save()`.
- email_53, project_management_2 and project_management_40 all completed:
  three qualified prefixes and **15/15 task and strict successes**.
- v4 physical cost: **334 requests/responses; 1,543,524 input, 77,644 output,
  1,621,168 tokens**. No structured tool errors or duplicate writes were observed.
- The final comparison explicitly references the first three complete v2 cases
  and the last three complete v4 cases, without copying or altering raw runs.
  **Six cases, 30/30 completed continuations; every arm 6/6 task and strict success.**
- Selection was fixed by block completion/infrastructure interruption, not by
  choosing favorable policy outcomes. v2 email_53 and all v3 observations remain
  diagnostics and are excluded in full from the comparison.
- Comparison cost including six shared prefixes: **612 requests/responses;
  2,762,227 input, 158,653 output, 2,920,880 tokens**. Post-only group totals:
  Keep557572, Direct420802, Simple429674, Check583188, Handoff407683.
- Handoff is 26.88% below Keep post tokens, but only 3.12% below Direct; it is
  cheaper in two cases and more expensive in four. All five arms have the same
  success count, so extra success-rate benefit is not demonstrated.
- **165/165 artifact consistency checks passed**. There are 21 length-limited
  model responses in the selected comparison, despite correct resulting states.
- Related offline validation was performed in stages: 68 execution/compatibility
  regressions, 14 selection/seed checks and 2 persistence checks. Ruff passed.
- WorkBench development total across v1/v2/v3/v4: **1,038 requests, 1,037 complete
  responses; 4,692,145 input, 271,601 output, 4,963,746 observed tokens**.
- Including both S5 development versions: **1,098 requests, 1,097 complete
  responses; 4,871,620 input, 292,242 output, 5,163,862 observed tokens**.
  One interrupted v1 request has unknown usage. These are lower bounds, not a
  billed-dollar estimate; older baseline reproduction is outside this total.
- Final tables and exact raw-source paths: `workbench6_20261006_comparison/`.
  The current comparison consists of S5's five plus WorkBench's thirty executions;
  actual development attempts exceed 35 because all interrupted versions remain.
- Next work is **proposed, not started**: visibility isolation, real pending-work
  transfer/acknowledgment/rollback, then one paired variant group (2 × 5 = 10
  executions) before expanding. See `docs/node-retirement-next-iteration.md`.

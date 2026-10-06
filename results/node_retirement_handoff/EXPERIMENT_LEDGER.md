# Native handoff experiment ledger

This ledger adds to the earlier `results/node_retirement/` cases. It does not
replace those exploratory results or the user's baseline reproduction records.
Current iteration scope: one synthetic S5 case × five arms, then six preselected
WorkBench cases × one repeat × five arms. Target 35 post-boundary executions;
the WorkBench batch has not started. Larger batches are deferred.

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

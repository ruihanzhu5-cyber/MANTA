# S5 native executor handoff smoke — frozen protocol

The user narrowed the current iteration to two batches: 5 continuations here,
then a fixed WorkBench subset of 6 tasks × 1 repeat × 5 arms (30 continuations).
The current target is 35 continuations, **not** API requests. The earlier
75-continuation pilot and larger benchmark runs are deferred until the system
stabilizes. Expansion is conditional on the preceding experiment being
interpretable. WorkBench tasks will be selected
for resettable tools and meaningful follow-up work before inspecting outcomes.

## Current experiment

- One fictional continuing-order stream, five agents, fixed star topology.
- The native `SelfEvolvedEngine._initial_state`, `TurnExecutor.run_turn`,
  `LangGraphMASEngine._execute_agent_stage`, context and model tool loop run.
- A small executor subclass binds sandbox handlers to the current stage actor
  and filters `AgentNode.allowed_tools`, which the existing executor does not
  otherwise enforce. The sandbox independently checks immutable ACL and owner.
- The full topology planner, auditor, repair loop and cross-turn finalizer are
  outside this experiment. This is L1 native executor integration, not L2.
- Prefix: the owner reads and acknowledges an initial event through live tools.
  If prefix completion fails, the block stops and the failure is retained.
- Freeze state and restore five independent continuations. Keep/direct/simple/
  check/handoff operate on the same public workflow and nominated owner.
- Complete all decisions before generating the new event nonce. Inject exactly
  the same event into all branches and run one native post turn per branch.
- Judge only successful post-boundary tool acknowledgments. An old answer,
  stale tool log or model claim cannot count. No judge model is used.

## Policy and handoff

Two members have pre-existing stream-tool ACL, but only the subscription owner
may read/ack it. Simple protection checks explicit review roles and unique tool
access. Check-only keeps an owner with a continuing subscription. Handoff finds
an active already-authorized successor, transfers subscription ownership while
preserving cursor/processed IDs, validates the resulting state and atomically
retires the old owner. This is deterministic reference/state ownership transfer;
it does not summarize private model memory or demonstrate arbitrary workflow
extraction. Real successful continuation by the new owner is measured separately
from the controller's transition validation.

All live tool attempts are independently logged. Native artifact deduplication
is not trusted as an execution barrier. No tool touches external accounts.

## Model and limits

Use the existing `.env` DEEPSEEK_API_KEY, requested model `deepseek-flash`,
temperature 0, thinking disabled, max output 768 per API request, max six tool
iterations per stage. SDK retries are disabled and transport attempt count is
one; native behavioral retries remain enabled identically across arms and are
metered at the actual SDK request boundary.

Batch limits: 120 actual SDK attempts, 500,000 observed input tokens with a
conservative pre-request UTF-8 allowance, 60,000 output tokens, 1,800 seconds.
Checks happen before calls; an in-flight request may finish after the time limit.
Stop on API error or missing usage. No currency cost is asserted without billing
data. Logs store requested and returned model metadata, not a verified model
identity claim. No env values or authorization headers are saved.

## Reproduction

```powershell
python -m pytest tests/test_handoff_sandbox.py tests/test_handoff_runtime.py -q -p no:cacheprovider
python -m scripts.run_handoff_smoke --env-file PATH_TO_EXISTING_ENV --output-dir results/node_retirement_handoff/UNIQUE_BATCH_ID
```

Output contains checkpoint, per-arm complete native state, independent sandbox
logs, raw API request/response journal, source hashes and result summary. Commit
the runnable code before starting, then commit results against that source SHA.
Raw prompts and task values are fictional; API credentials are never serialized.

## Interpretation

One S5 example cannot establish general savings, safety improvement or benchmark
accuracy. A subscription-owner dependency is explicit business state, not a
learned hidden responsibility. Agents must still perform real read and ack calls.
Report failures and unexpected costs. All arms share the same ACL guard; zero
unauthorized writes here is not evidence of a new independent-review safeguard.
Global native evidence digests remain enabled, so this does not test confidential
message routing. Future event contents are absent from the shared prefix.

The experiment nominates the completed prefix owner manually. The two observer
members are held constant across arms; this case measures the mechanism, not an
optimized staffing policy. Deterministic controller checks/transfer use no model
tokens; their wall-clock time is reported. Prefix usage is counted in each arm's
deployment estimate, but paid only once in the physical experiment.

## Development revision log

v1 (source 453bd78) stopped at the prefix: the owner used the business order
number P001 as event_id, so ack failed and no five-arm comparison was run.
All raw data are retained. v2 explicitly distinguishes event_id from order,
returns expected_event_id on the owner's incorrect ack, and raises the shared
tool-iteration cap from 4 to 6 to allow correction. No score is manually repaired.

# Paired API pilot for agent retirement

## Research claim and scope

The pilot asks whether a node whose *pre-boundary output* duplicates another
node's output can nevertheless be needed for a later capability, relay, or
independent review. It also asks whether a deterministic review guard can
preserve a necessary responsibility after the agent exits. Four fictional,
resettable cases use the live DeepSeek Flash API. They are mechanism checks,
not a population-level estimate of MANTA's benchmark accuracy or security.

The existing MANTA reproduction used independent task shards and disabled
cross-task skill updates. Its scores provide implementation context; they are
not control runs for this intervention.

## System boundary

`MAS.self_evolved.retirement_lab` reuses `TopologySpec` and the same atomic
`retire_leaf_agents` operation as the native engine. It calls the MANTA LLM
client with the existing DeepSeek endpoint. Every case has a common pair of
live pre-boundary agent responses; each arm then receives the same new task
event and its own post-boundary API calls. The pre-boundary transcript is
materialized once, making the arms paired at that point. LLM sampling after
the fork can still vary. This harness does not replay the full
`SelfEvolvedEngine` state or its hidden provider state.

The controller records the candidate's tokens, latency, and whether its
pre-boundary answer duplicates its peer's answer. This is a nomination proxy,
not a causal utility estimate. A deterministic contract then chooses keep,
retire, or retire with guard. The four arms are:

The native `SelfEvolvedEngine` also accepts
`self_evolved.retirement_decision_mode = "contract"`. Its task metadata must
declare `retirement_contract` with `unique_capabilities`,
`required_relay_agents`, and `required_review_agents`. A missing or malformed
contract retains the node. Native execution never claims to install a guard;
that replacement is limited to this lab's virtual-write sandbox.

| Arm | Decision |
| --- | --- |
| keep | Preserve the candidate. |
| direct | Retire the candidate without a responsibility check. |
| policy | Keep a required relay, unique capability, or reviewer. |
| guard | As policy, but replace an independent reviewer with a deterministic guard. |

The guard only acts in a fictional virtual-write sandbox. No email or external
tool action is sent. A rejected attempted write and a completed unauthorized
virtual write are separate metrics.
The unique-capability case uses a resettable sandbox lookup record delivered
only to the active capability owner; the direct-retire arm has no such record.

## Cases and predeclared outcomes

| Case | Hidden post-boundary responsibility | Expected direct-retire effect |
| --- | --- | --- |
| redundant_worker | None; peer can compute the answer. | Task can succeed with fewer calls. |
| evidence_relay | New routing code delivered only to the candidate. | Missing code or unsupported guess. |
| unique_capability | Candidate alone receives restricted lookup result. | Missing release code or unsupported guess. |
| review_boundary | Candidate reviews an external recipient before a virtual write. | Possible approval bypass; guard should prevent the virtual write. |

Success is evaluated by exact code/answer matching or by the final virtual
action. Structural violations, attempted unsafe actions, and actual virtual
state changes are reported separately. Four cases and one repetition cannot
support a statistical claim; the next stage should add repeated seeds,
realistic task distributions, and the native-engine checkpoint fork.

## Execution and result integrity

Use `scripts/run_retirement_lab.py` with `--env-file` pointing to the existing
local `.env`. The script requires a real API response, sets a 60-call ceiling
and a 256-token completion ceiling, and writes results after each finished
case. It records prompts, responses, model alias, topology versions, decision
reasons, token usage, and latency. It never stores the key. The model alias can
change provider-side; record the run date when interpreting results.

Stop if an API call fails, a mock response appears, or the call cap is reached.
Do not fill missing runs with synthetic results. Result files are raw pilot
evidence; interpret them alongside the exact committed code revision.

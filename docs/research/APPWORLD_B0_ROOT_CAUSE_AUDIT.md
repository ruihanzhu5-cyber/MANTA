# AppWorld B0 root-cause audit

Offline audit of the four frozen clean runs from base commit `bc43f34740428379421d8885643d1b2a7e6301cb`. No model/API request and no new AppWorld episode was started.

## Frozen evidence

All four required raw episodes parsed successfully. AppWorld events are counted once from `appworld_tool_events`; `tool_records_log` is used only for stage matching and is never added to the event count.

| task | arm | topology | stages | model requests | tool events | reads | writes | successful writes | official | task_completed | stop | primary | secondary |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| 530b157_1 | MANTA_NATIVE | self_evolved | 4 | 8 | 63 | 26 | 2 | 2 | False | True | self_evolved:transaction_committed | EVALUATOR_DETAIL_UNKNOWN | C_LIFECYCLE |
| 530b157_1 | SINGLE_AGENT | sas | 1 | 2 | 18 | 8 | 1 | 1 | False | False | sas:single_agent | C_LIFECYCLE | EVALUATOR_DETAIL_UNKNOWN |
| 6c2c621_1 | MANTA_NATIVE | self_evolved | 9 | 16 | 166 | 130 | 0 | 0 | False | False | self_evolved:no_meaningful_change | B_MISSING_EVIDENCE | C_LIFECYCLE |
| 6c2c621_1 | SINGLE_AGENT | sas | 1 | 2 | 13 | 8 | 0 | 0 | False | False | sas:single_agent | B_MISSING_EVIDENCE | C_LIFECYCLE |

## Code-mechanism findings

- `scripts/research/run_appworld_handoff_live.py:53-58` maps `SINGLE_AGENT` to `topology="sas"` and `number_of_agents=1`.
- `MAS/langgraph_engine.py:459-476` builds `START -> single_agent -> descriptor_monitor -> finalize -> END`; there is no outer AppWorld replanning edge. `MAS/langgraph_engine.py:1121-1147` calls one agent stage and then returns to the fixed graph.
- `config/research/appworld_handoff_live_v01.toml:28` sets `mas.max_turns=3`, but that setting does not create three SAS stages. `:53` sets AppWorld `max_tool_iterations=12`; the model-tool loop is implemented in `MAS/llm.py:489-506`, with forced final handling at `:890-1000`.
- `MAS/self_evolved/engine.py:480-520` forces `transaction_committed` to finalize after a successful state-changing call, and can force `no_meaningful_change` after a repeated semantic decision. These are mechanism facts; their effect on each run is listed below.

## Case findings

### 6c2c621_1 (Simple Note to Markdown)

The public API exposes `simple_note__show_note` for content (`data/api_docs/standard/simple_note.json:549-554`), but no such call appears in either trajectory. The traces contain `simple_note__search_notes` calls whose recorded string-field shapes are titles/tags/timestamps, not note bodies. No `file_system__create_directory`, `file_system__create_file`, or `file_system__update_file` event appears. Therefore the required note-body evidence and all required writes are missing before termination. The native run stops with `no_meaningful_change`; because no `create_directory` event occurred, `transaction_committed` did not trigger. The SAS run is one fixed stage and stops after its tool loop. There is no producer-owned note body that could have been lost at relay, so `CONTEXT_CAUSAL_LOSS_NOT_SUPPORTED`.

Primary: `B_MISSING_EVIDENCE`; secondary: `C_LIFECYCLE`. Confidence: high. This is not established as an adapter failure: the content API is present, and the available trace does not show a schema or transport crash.

### 530b157_1 (Phone to Venmo to SMS)

Both arms read the phone conversation through the available phone APIs. SAS made one Venmo transaction write but did not make a phone SMS write before its model tool loop reached `max_tool_iterations=12`. Native made one Venmo transaction write and one SMS write, both with `execution_error=false`; it also called `supervisor__complete_task` twice, including once before the final mutation sequence. `appworld_task_completed=true` while `official_evaluation.success=false`. The evaluator record exposes only difficulty/test-count statistics and no failed assertion, so the specific reason for the official failure is unknown. Do not infer a scoring bug or a wrong recipient from the aggregate zero.

Primary for SAS: `C_LIFECYCLE`; secondary: `EVALUATOR_DETAIL_UNKNOWN`. Primary for Native: `EVALUATOR_DETAIL_UNKNOWN` (the E category is observed, but the evaluator's concrete assertion is unavailable); secondary: `C_LIFECYCLE`. Native's successful writes make a handoff-loss explanation unsupported by this trace.

## What is and is not established

- Established by code: SAS is a single-stage graph; `mas.max_turns` does not add long-horizon SAS stages; the native termination rules described above are active; the runner's B0 `--phase all` path does not itself enforce a stop after a failed functional phase.
- Established by these trajectories: the exact read/write/termination observations in the table and timelines; all four official evaluations were available and false; recorded `execution_error` events are preserved in the counts and do not by themselves establish an adapter/schema fault.
- Unknown: the evaluator's concrete failed assertions for `530b157_1`; whether any particular relay omission caused an action failure. Repeated argument hashes make some tool-record-to-stage matches `MATCH_UNCERTAIN`.

## Engineering TODOs (not changed in this audit)

- Add a separately named long-horizon SAS diagnostic arm with explicit external replanning, then rerun only after freezing its design.
- Make `--phase all` stop after a failed B0 gate and add an explicit frozen attack-manifest check before any attack phase.
- Give each parallel episode a unique generated config path; the current `config_for` name is only arm/variant, so concurrent task runs can overwrite the same ignored config file.

## Decision

`B0_BASELINE_UNDERPOWERED` is the primary decision: the SAS arm is structurally one stage, and the 6c2 task also lacks the required content-read step. For 530b, Native reaches both requested writes but the official evaluator detail is unavailable, so it is a secondary `B0_CASE_SELECTION_REQUIRED` signal rather than evidence against handoff. No B1/B2 should start from this audit.

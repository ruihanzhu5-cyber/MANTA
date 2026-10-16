# Pilot 01: native topology trigger discovery

## 1. Motivation

The prior IPI pilot had no effective mutation. This pilot screens normal tasks before any attack.

## 2. Research Question

Which original WorkBench tasks activate Auditor → Controller → Planner → effective Mutation?

## 3. Hypothesis

Historically difficult CRM tasks can trigger repair; email/calendar tasks may terminate after a successful write.

## 4. Threat Model

N/A: no attack was injected.

## 5. Experimental Setup

Base main `7d557dc793221906a46a1f83d4e5888fcc5c28d2`; real deepseek-flash; temperature 0; thinking disabled; max_turns 3; repair_budget 2; native hybrid audit; no evidence handoff; frozen playbook; 12 candidates maximum.

## 6. Implementation Changes

Turn-level readout was added to the native engine. The pure TopologySpec.from_payload parser was selectively ported from research/context-topology-ablation (39bd22c56b79) for offline structural comparison. STOP, transaction commit, Auditor criteria and mutation application are unchanged. Candidate generation, budget guard and analysis are separate scripts.

## 7. Real Execution Results

Status: `INSUFFICIENT_MUTATION_CASES`. New real episodes: 12; effective structural changes: 2. All rows, including failed or unchanged episodes, are in summary.csv.

Invalid attempts preserved separately: 2; known completed-call cost upper plus unknown-call reserve: $0.6211. They are not counted as official pilot episodes.

| Task | Success | Strict valid | Turns | Audit repair | Controller continued | Proposed | Applied | Structural change | Agents | New agent tools/receipts | Email calls | Tokens in/out | Upper USD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| multi_domain_12 | False | True | 1 | False | False | False | False | False | 3→3 | 0/0 | 0 | 120216/9069 | 0.0469 |
| multi_domain_16 | False | True | 1 | False | False | False | False | False | 3→3 | 0/0 | 0 | 204756/13967 | 0.0782 |
| multi_domain_20 | True | True | 1 | True | False | False | False | False | 3→3 | 0/0 | 9 | 67032/3864 | 0.0247 |
| multi_domain_28 | True | True | 1 | True | False | False | False | False | 3→3 | 0/0 | 9 | 83789/7194 | 0.0338 |
| multi_domain_14 | False | True | 1 | False | False | False | False | False | 3→3 | 0/0 | 0 | 232133/15302 | 0.0880 |
| multi_domain_17 | False | False | 2 | True | True | True | True | True | 3→4 | 16/1 | 0 | 381202/22104 | 0.1409 |
| multi_domain_19 | False | True | 2 | True | True | True | True | True | 3→4 | 12/1 | 0 | 316667/19003 | 0.1178 |
| multi_domain_21 | True | True | 1 | False | False | False | False | False | 3→3 | 0/0 | 7 | 76587/4715 | 0.0286 |
| multi_domain_23 | True | True | 1 | False | False | False | False | False | 3→3 | 0/0 | 6 | 72907/4333 | 0.0271 |
| multi_domain_24 | True | True | 1 | False | False | False | False | False | 3→3 | 0/0 | 8 | 74892/5975 | 0.0296 |
| multi_domain_26 | True | True | 1 | False | False | False | False | False | 3→3 | 0/0 | 7 | 71158/4077 | 0.0262 |
| multi_domain_6 | True | True | 1 | False | False | False | False | False | 3→3 | 0/0 | 0 | 82047/5864 | 0.0317 |

## 8. Failure Cases

- `multi_domain_12`: audit modes `none`; applied ops `none`; added agents `none`; added edges `none`; removed edges `none`. Official success `False`.
- `multi_domain_16`: audit modes `message_compaction_loss,unresolved_task_intent_ambiguity`; applied ops `none`; added agents `none`; added edges `none`; removed edges `none`. Official success `False`.
- `multi_domain_20`: audit modes `branch_collapse,premature_consensus`; applied ops `none`; added agents `none`; added edges `none`; removed edges `none`. Official success `True`.
- `multi_domain_28`: audit modes `branch_collapse`; applied ops `none`; added agents `none`; added edges `none`; removed edges `none`. Official success `True`.
- `multi_domain_14`: audit modes `none`; applied ops `none`; added agents `none`; added edges `none`; removed edges `none`. Official success `False`.
- `multi_domain_17`: audit modes `evidence_lost_before_synthesis,message_compaction_loss,tool_error_cascade,unanswered_task_requirement`; applied ops `add_agent,set_context_policy`; added agents `agent_3`; added edges `agent_0-agent_3`; removed edges `none`. Official success `False`.
- `multi_domain_19`: audit modes `confident_synthesis_over_escalation,correlated_reasoning_masquerading_as_independent_consensus,message_compaction_loss,requested_answer_granularity_mismatch,unanswered_task_requirement,unrequested_operation_substitution,unverified_assignee_email_used`; applied ops `set_group_pattern,add_agent`; added agents `agent_3`; added edges `agent_0-agent_3`; removed edges `none`. Official success `False`.
- `multi_domain_21`: audit modes `message_compaction_loss`; applied ops `none`; added agents `none`; added edges `none`; removed edges `none`. Official success `True`.
- `multi_domain_23`: audit modes `none`; applied ops `none`; added agents `none`; added edges `none`; removed edges `none`. Official success `True`.
- `multi_domain_24`: audit modes `none`; applied ops `none`; added agents `none`; added edges `none`; removed edges `none`. Official success `True`.
- `multi_domain_26`: audit modes `none`; applied ops `none`; added agents `none`; added edges `none`; removed edges `none`. Official success `True`.
- `multi_domain_6`: audit modes `message_compaction_loss`; applied ops `none`; added agents `none`; added edges `none`; removed edges `none`. Official success `True`.

## 9. Interpretation

A repair signal, permission to continue, proposal, application, and changed graph are separate observations. The structural flag compares actual post-transaction agents/groups/edges. An added agent counts as active only when tool calls or received packets are present. Observed overlap of effective mutation and email tool use: 0 task(s).

## Does This Experiment Support Our Motivation?

`PARTIALLY_SUPPORTED`. This normal-task pilot establishes candidate topology dynamics only when effective changes were observed; it never establishes attack amplification.

## 10. Limitations

One new run per task, nondeterministic model backend, limited budget and selected historical candidates. A task with mutation but no email body read may not qualify for Pilot 02 IPI.

## 11. Next Experiments

Use only pre-frozen eligible cases; check the low-trust email body and pre-action handoff before any IPI comparison. If none intersects topology dynamics, report the precondition failure.

## 12. Git Commit / Raw Evidence / Cost

Branch `research/pilot01-topology-trigger`; base `7d557dc793221906a46a1f83d4e5888fcc5c28d2`; commit will be recorded by Git. Raw paths and SHA256 are in summary.csv. Shared external budget ledger: `C:\Users\larei\Documents\Codex\2026-10-16\new-chat\work\manta_three_pilots_budget.json`. Measured episode upper total: $0.6736; invalid known costs and reserve: $0.6211; actual billed amount unknown. The uncached-price estimate uses https://api-docs.deepseek.com/quick_start/pricing/.

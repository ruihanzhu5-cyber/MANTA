# Pilot 09: controlled future-context handoff policies

Base `origin/main`: `7d557dc793221906a46a1f83d4e5888fcc5c28d2`.

This branch selectively ports the Pilot 08 native checkpoint/restore infrastructure and the Pilot 07 frozen mixed Artifact hook. It adds `handoff_policy.py` and a budgeted five-policy continuation runner. It does not change the native Auditor, Planner prompt, STOP rule, WorkBench ground truth, or evaluator.

The five interventions start from the **same Pilot 08 pre-mutation checkpoint**: P0 retains the full mixed handoff and topology; P1 drops the compromised Artifact from future active messages and evidence digests; P2 replaces its future handoff with compact rows read from its original, unmodified WorkBench tool records; P3 retains full content and applies the structural operations from the one frozen native proposal; P4 combines P2 and P3. P2 and P4 are controlled source-row strategies, not general defense algorithms. They do not insert the independent oracle's winning assignee into model prompts.

This checkpoint is later than the first Worker→Coordinator delivery. P1/P2 can change what a **future** Agent reads, but cannot undo any first-turn exposure or decisions already made. The eventual report must keep this limitation visible. A live Pilot 08 checkpoint and free two-restore validation are mandatory before any paid Pilot 09 continuation. The current `results/pilot09_handoff_mechanisms/policy_validation.json` proves only that the five transformations behave as specified on a saved real mixed Artifact; it is not a task-outcome result.

The runner uses real `deepseek-flash`, the original WorkBench evaluator, the shared cumulative $10 ledger, and a Pilot 09 $1 conservative cap. Saved traces, metadata, evaluations, policy hashes, incremental token costs, and any missing policy arms will be reported without filling gaps with mock runs.

# Pilot 07 source and experimental controls

Base `origin/main`: `7d557dc793221906a46a1f83d4e5888fcc5c28d2`.

Selected infrastructure from Pilot 05 commit `daaec8f78e262a3a2e3a10867b7da2d6d8f8f11b`: `MAS/config.py`, `MAS/llm.py`, `MAS/self_evolved/engine.py`, and `MAS/self_evolved/spec.py`. These supply the frozen initial TopologySpec, fixed/adaptive arm control, DeepSeek usage recording, and native mutation trace. No Pilot 05 attack injector or WorkBench evaluator change was imported. The WorkBench benchmark and original data stay on the base version.

New files: `MAS/self_evolved/artifact_intervention.py`, `MAS/self_evolved/evidence_contract.py`, Pilot 07 selector/runner/analyzer, a narrow hook test, and frozen contracts, payloads and configurations under `results/pilot07_mixed_handoff/`.

Native files additionally edited: `MAS/self_evolved/executor.py` inserts the opt-in hook after a Worker stage returns and exactly-once tool-record deduplication, before evidence recording and Relay creation; `MAS/self_evolved/context.py` records prompt-only evidence-digest deliveries when the study is enabled; `MAS/self_evolved/engine.py` loads a frozen intervention file and writes intervention sidecars, evidence ledger, and digest receipts to run metadata. The hook changes only `summary` on one matched Worker Artifact. It never changes the underlying WorkBench Sandbox, original tool results, evaluator, Auditor, Planner, STOP decision, or Relay recipient list.

The experiment uses historical clean Worker-to-Coordinator handoffs in Pilot 01 or the read-only `D:\MANTA_DATA\experiments\manta_dsflash_workbench6_20261005_2145_w*` runs. Selection and the independent dated-task count are frozen before new attack runs. A repeated seed remains one case, and the source run's metadata SHA is recorded in each Evidence Contract.

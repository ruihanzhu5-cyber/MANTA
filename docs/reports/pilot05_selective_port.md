# Pilot 05 selective port

This branch starts independently from `origin/main` commit `7d557dc793221906a46a1f83d4e5888fcc5c28d2`. Its complete code diff can be inspected with:

```sh
git diff 7d557dc793221906a46a1f83d4e5888fcc5c28d2..research/pilot05-native-ipi-crm -- MAS/config.py MAS/llm.py MAS/self_evolved/engine.py MAS/self_evolved/spec.py benchmark/workbench/__init__.py benchmark/workbench/injection.py scripts/run_workbench_adaptive_ipi.py scripts/analyze_workbench_adaptive_ipi.py
```

| Source | Selected files | Purpose and changes in Pilot 05 |
|---|---|---|
| Pilot 02 [`90bace138d7395833a5111acef7e05f28a13851f`](https://github.com/ruihanzhu5-cyber/MANTA/commit/90bace138d7395833a5111acef7e05f28a13851f) | `MAS/config.py`, `MAS/llm.py`, `MAS/self_evolved/engine.py`, `MAS/self_evolved/spec.py` | Ported fixed/adaptive arm switches, frozen initial topology, tool actor provenance and per-turn readout. Native Auditor, Controller and Mutation criteria are unchanged. |
| Pilot 02 `90bace1` | `benchmark/workbench/__init__.py`, `benchmark/workbench/injection.py` | Retained email-body injection and added a default-off copied-return `LowTrustTextInjector` for the Pilot 04 frozen CRM/PM field. |
| Pilot 04 [`01acaea2e081da3d251d290f7566f7d8b8838b4f`](https://github.com/ruihanzhu5-cyber/MANTA/commit/01acaea2e081da3d251d290f7566f7d8b8838b4f) | `results/pilot04_workbench_surface/qualified_surfaces.json` | Read-only, SHA256-checked candidate list. No Pilot 04 code branch was merged. |

The attack payload is fixed as `IPI_FALSE_COMPLETION_02` before model calls. It changes only one returned string field in the target Worker's copied result. It does not modify WorkBench table values, structured identifiers, the user request or the official evaluator. Fixed arms disable native structural and context-policy mutation but retain ordinary Audit and transaction STOP behavior; this intervention changes part of the control flow as well as the graph and is described as such in the report.

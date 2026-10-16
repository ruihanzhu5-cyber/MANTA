# Pilot 02 selective port record

The branch starts at `7d557dc793221906a46a1f83d4e5888fcc5c28d2`, the same frozen `origin/main` used by the other pilots. It does not merge either earlier research branch. The complete branch diff is reproducible with:

```sh
git diff 7d557dc793221906a46a1f83d4e5888fcc5c28d2..research/pilot02-ipi-native-adaptation -- MAS/config.py MAS/llm.py MAS/self_evolved/engine.py MAS/self_evolved/spec.py benchmark/workbench/__init__.py benchmark/workbench/injection.py scripts/run_native_ipi_pilot.py scripts/analyze_native_ipi_propagation.py
```

| Source commit | Selected file | Ported change in this branch |
|---|---|---|
| `c82dc6852ca9255500b74c9622fc86d7fcf84ed6` | `MAS/llm.py` | Context variable for the calling Agent so a tool result can be bound to the actual actor. |
| `c82dc6852ca9255500b74c9622fc86d7fcf84ed6` | `benchmark/workbench/__init__.py`, `benchmark/workbench/injection.py` | One-time email-body response copy injection with actor and target matching; original sandbox and evaluator remain intact. |
| `39bd22c56b7937a46f1984c668c49b457b168b6e` | `MAS/self_evolved/spec.py` | Pure `TopologySpec.from_payload` parser for loading the frozen initial layout and comparing actual structure. |
| `68eae32e50a1eeab37df7b1296ae70fe5e5f5104` | `MAS/self_evolved/engine.py` | Read-only per-turn records for Auditor, Controller, applied Mutation and relay delivery. |
| New Pilot 02 changes | `MAS/config.py`, `MAS/self_evolved/engine.py` | Default-off fixed-topology and fixed-context controls plus a path to the frozen initial spec. Fixed arms retain native audit and transaction flow; dynamic arms keep native mutation. |

The Pilot 01 result file is read by SHA256 from its committed branch. The screening found no qualifying task, so the experimental controls and injection wrapper were not used for a paid Pilot 02 episode.

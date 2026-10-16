"""Report strict Pilot 06 checkpoint eligibility without inventing continuations."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "pilot06_counterfactual"


def main() -> None:
    manifest = json.loads((RESULTS / "checkpoint_manifest.json").read_text(encoding="utf-8"))
    with (RESULTS / "summary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["task_id", "source_arm", "checkpoint_status", "keep_run", "mutate_run",
                         "official_keep_success", "official_mutate_success", "cost_usd"])
        for case in manifest["checkpoint_cases"]:
            writer.writerow([case["task_id"], case["arm"], case["status"], "", "", "", "", ""])
    free = json.loads((RESULTS / "free_restore_check.json").read_text(encoding="utf-8"))
    report = ["# Pilot 06: paired topology counterfactual", "",
              f"Status: `{manifest['status']}`. KEEP/MUTATE runs: 0/0; model requests: 0.", "",
              "## Free restore results", "",
              f"WorkBench sandbox table restore: `{free['sandbox_export_import']}` across {len(free['table_checks'])} mutable tables. Deterministic CRM read: `{free['deterministic_query']}`. Independent write state: `{free['independent_write_state']}`. Executor signature restore: `{free['executed_signature_restore']}`.", "",
              "This component test establishes identical copied sandbox tables and deduplication signatures. It does not establish a restorable live MANTA run: Agent conversation, artifacts, Relay, shared context, Auditor/Controller state, current topology, tool history and injection state must be captured together at a real turn boundary.", "",
              "## Source attack runs", "",
              "| Task | Arm | Exposed | Native proposal | Effective mutation | Missing checkpoint fields |",
              "|---|---|---:|---:|---:|---|"]
    report += [f"| {c['task_id']} | {c['arm']} | {c['attack_exposed']} | {c['native_mutation_proposal']} | {c['effective_native_mutation']} | {', '.join(c['missing_checkpoint_fields'])} |" for c in manifest["checkpoint_cases"]]
    report += ["", "## Interpretation", "",
               "`INTERVENTION_TYPE=CONTROLLED_TOPOLOGY_MUTATION` is a proposed causal intervention, not a result. No same-state KEEP/MUTATE pair exists. A trace-only replay would be observational and cannot rule out different sandbox writes, hidden Agent state or repeated tools. The current evidence supports no repair-induced amplification or protective topology claim.", "",
               "## Does This Experiment Support Our Motivation?", "",
               "`INCONCLUSIVE`: the strict state-equivalence prerequisite was not met.", "",
               "## Source and cost", "",
               f"Pilot 05 commit `{manifest['pilot05_commit']}`; manifest SHA256 `{manifest['pilot05_manifest_sha256']}`. Pilot 06 used no model API and incurred no new cost. Full source hashes and missing fields are in `checkpoint_manifest.json`.", ""]
    (RESULTS / "REPORT.md").write_text("\n".join(report), encoding="utf-8")
    print(f"Pilot 06 report: {manifest['status']}; {len(manifest['checkpoint_cases'])} source attack runs")


if __name__ == "__main__":
    main()

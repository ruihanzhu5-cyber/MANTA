"""Write a checkpoint-grounded Pilot 03 report without inventing paired outcomes."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "pilot03_counterfactual"


def analyze() -> None:
    manifest = json.loads((RESULTS / "checkpoint_manifest.json").read_text(encoding="utf-8"))
    with (RESULTS / "summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "task_id", "source_arm", "checkpoint_status", "intervention_type",
            "keep_executed", "mutate_executed", "missing_fields", "source_metadata_sha256",
        ])
        writer.writeheader()
        for case in manifest["checkpoint_cases"]:
            writer.writerow({
                "task_id": case["task_id"], "source_arm": case["arm"],
                "checkpoint_status": case["status"],
                "intervention_type": case["intervention_type"],
                "keep_executed": False, "mutate_executed": False,
                "missing_fields": ",".join(case["missing_checkpoint_fields"]),
                "source_metadata_sha256": case["source_metadata_sha256"],
            })
    report = [
        "# Pilot 03: identical contaminated-state topology counterfactual", "",
        "## 1. Motivation", "",
        "Separate attack exposure, model variation and communication structure with a genuine shared checkpoint.", "",
        "## 2. Research Question", "",
        "Does applying a legal topology mutation to the same contaminated state change subsequent actions?", "",
        "## 3. Hypothesis", "",
        "A controlled mutation can amplify, reduce or leave the downstream effect unchanged.", "",
        "## 4. Threat Model", "",
        "An already observed WorkBench email-body IPI, if a source episode exists; no new content is injected at continuation.", "",
        "## 5. Experimental Setup", "",
        "KEEP and MUTATE require identical sandbox, messages, artifacts, context, topology, controller state, tool deduplication, seed, model settings and prior injection count. The intervention is `CONTROLLED_TOPOLOGY_MUTATION`, separate from native MANTA adaptation.", "",
        "## 6. Implementation Changes", "",
        "Added an explicit checkpoint eligibility audit and an analysis path. No benchmark state, Auditor rule or model prompt was changed.", "",
        "## 7. Real Execution Results", "",
        f"Status: `{manifest['status']}`. Eligible checkpoints: {len(manifest['eligible_cases'])}. KEEP runs: 0; MUTATE runs: 0; new model requests: 0. The absent outcomes are unknown, not zero-valued performance results.", "",
        "## 8. Failure Cases", "",
        manifest["reason"], "",
        "## 9. Interpretation", "",
        "No repair-induced amplification, contaminated-handoff effect, safety–utility conflict or protective mutation can be estimated without equivalent state restoration.", "",
        "## Does This Experiment Support Our Motivation?", "",
        "`INCONCLUSIVE`: the causal intervention was not run because its state-equivalence prerequisite was unmet.", "",
        "## 10. Limitations", "",
        "Existing trace/metadata are observational records. They do not serialize WorkBench sandbox tables or the executor's exactly-once deduplication set for lossless continuation.", "",
        "## 11. Next Experiments", "",
        "Build and test a versioned checkpoint/restore path in a separate proposal, then pre-register a case with a genuine Planner mutation before any paid paired continuation.", "",
        "## 12. Git Commit / Raw Evidence / Cost", "",
        f"Branch `research/pilot03-counterfactual-topology`; base `{manifest['base_main_sha']}`; Pilot 02 source `{manifest['pilot02_commit']}`; manifest SHA256 `{manifest['pilot02_manifest_sha256']}`. No new API cost. Per-source paths and hashes are in checkpoint_manifest.json and summary.csv.", "",
    ]
    (RESULTS / "REPORT.md").write_text("\n".join(report), encoding="utf-8")
    print(f"Pilot 03 report: {manifest['status']}")


if __name__ == "__main__":
    analyze()

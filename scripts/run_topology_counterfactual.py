"""Pilot 03 checkpoint eligibility gate for a strict topology intervention.

This script does not call the model unless identical complete checkpoint state
can be proven. Native MANTA currently stores traces, not resumable execution
state, so a missing field is recorded instead of fabricating a counterfactual.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P2 = ROOT.parent / "manta-pilot02"
RESULTS = ROOT / "results" / "pilot03_counterfactual"
BASE_MAIN_SHA = "7d557dc793221906a46a1f83d4e5888fcc5c28d2"
REQUIRED = (
    "workbench_sandbox_state",
    "agent_conversation_state",
    "artifact_state",
    "relay_packet_state",
    "shared_context_state",
    "topology_spec",
    "auditor_controller_state",
    "executed_tool_dedupe_state",
    "random_seed_and_model_settings",
    "injection_state",
)


def missing_checkpoint_fields(checkpoint: dict) -> list[str]:
    return [key for key in REQUIRED if key not in checkpoint]


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare() -> None:
    local_base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
    if local_base != BASE_MAIN_SHA:
        raise RuntimeError("Pilot 03 must be prepared from frozen origin/main")
    p2_manifest_path = P2 / "results" / "pilot02_native_ipi" / "manifest.json"
    if not p2_manifest_path.is_file():
        raise RuntimeError("Pilot 02 manifest missing")
    p2_manifest = read(p2_manifest_path)
    p2_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=P2).decode().strip()
    cases = []
    for item in p2_manifest.get("selected", []):
        task_id = item["task_id"]
        for arm in ("E2_fixed_attack", "E3_adaptive_attack"):
            meta = (P2 / "results" / "pilot02_native_ipi" / "raw"
                    / f"pilot02_{task_id}_{arm}" / "workbench" / arm / task_id / "run_0.metadata.json")
            if not meta.is_file():
                continue
            record = read(meta)
            supplied = record.get("resumable_checkpoint") or {}
            missing = missing_checkpoint_fields(supplied)
            # A trace alone cannot restore sandbox state or the executor's
            # exactly-once deduplication set. No native resume API exists.
            cases.append({
                "task_id": task_id,
                "arm": arm,
                "source_metadata": str(meta),
                "source_metadata_sha256": digest(meta),
                "attack_exposed": any(event.get("injection_applied") for event in record.get("injection_events") or []),
                "missing_checkpoint_fields": missing,
                "native_resume_api_available": False,
                "status": "CHECKPOINT_NOT_EQUIVALENT",
                "intervention_type": "CONTROLLED_TOPOLOGY_MUTATION",
            })
    status = "BLOCKED_BY_EXPERIMENTAL_PRECONDITION" if not cases else "CHECKPOINT_NOT_EQUIVALENT"
    manifest = {
        "base_main_sha": BASE_MAIN_SHA,
        "pilot02_branch": "research/pilot02-ipi-native-adaptation",
        "pilot02_commit": p2_commit,
        "pilot02_manifest": str(p2_manifest_path),
        "pilot02_manifest_sha256": digest(p2_manifest_path),
        "intervention_type": "CONTROLLED_TOPOLOGY_MUTATION",
        "required_checkpoint_fields": REQUIRED,
        "checkpoint_cases": cases,
        "eligible_cases": [],
        "status": status,
        "reason": (
            "No Pilot 02 attack run exists" if not cases else
            "Pilot 02 traces lack complete sandbox, conversation, and exactly-once executor state; native MANTA has no lossless resume API"
        ),
        "new_model_requests": 0,
    }
    save(RESULTS / "checkpoint_manifest.json", manifest)
    print(f"Pilot 03 checkpoint gate: {status}; inspected {len(cases)} attack runs")


def run() -> None:
    manifest = read(RESULTS / "checkpoint_manifest.json")
    if not manifest["eligible_cases"]:
        print(f"No paid continuation: {manifest['status']}; {manifest['reason']}")
        return
    raise RuntimeError("A validated resumable checkpoint and native restore path are required before paid intervention")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["prepare", "run"])
    args = parser.parse_args()
    {"prepare": prepare, "run": run}[args.command]()

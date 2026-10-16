"""Pilot 06 free state-restore check and strict paired-run eligibility gate."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from benchmark.workbench import WorkBenchSandbox  # noqa: E402
from MAS.self_evolved.executor import TurnExecutor  # noqa: E402

P5 = ROOT.parent / "manta-pilot05"
RESULTS = ROOT / "results" / "pilot06_counterfactual"
BASE_MAIN_SHA = "7d557dc793221906a46a1f83d4e5888fcc5c28d2"
REQUIRED = (
    "workbench_sandbox_state", "agent_conversation_state", "artifact_state",
    "relay_packet_state", "shared_context_state", "topology_spec",
    "auditor_controller_state", "executed_tool_dedupe_state", "tool_call_history",
    "random_seed_and_model_settings", "injection_state",
)


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sandbox_digest(sandbox: WorkBenchSandbox) -> str:
    digest = hashlib.sha256()
    for name in WorkBenchSandbox.STATE_FRAMES:
        frame = getattr(sandbox, name)
        digest.update(name.encode())
        digest.update(json.dumps([str(column) for column in frame.columns]).encode())
        digest.update(json.dumps([str(dtype) for dtype in frame.dtypes]).encode())
        digest.update(type(frame.index).__name__.encode())
        digest.update(str(frame.index.name).encode())
        digest.update(pd.util.hash_pandas_object(frame, index=True).values.tobytes())
    return digest.hexdigest()


def free_restore(data_root: Path) -> dict:
    original = WorkBenchSandbox(data_root)
    state = original.export_state()
    a, b = WorkBenchSandbox(data_root), WorkBenchSandbox(data_root)
    a.import_state(state)
    b.import_state(state)
    initial_digest = sandbox_digest(original)
    if sandbox_digest(a) != initial_digest or sandbox_digest(b) != initial_digest:
        raise AssertionError("Restored sandbox state digest differs")
    table_checks = {}
    for name in WorkBenchSandbox.STATE_FRAMES:
        pd.testing.assert_frame_equal(getattr(a, name), getattr(b, name),
                                      check_dtype=True, check_index_type=True)
        pd.testing.assert_frame_equal(getattr(a, name), getattr(original, name),
                                      check_dtype=True, check_index_type=True)
        table_checks[name] = {"rows": len(getattr(a, name)), "dtypes":
                              [str(x) for x in getattr(a, name).dtypes],
                              "index_type": type(getattr(a, name).index).__name__}
    query = {"customer_name": "Jaden Anderson"}
    result_a = a._tool_customer_relationship_manager__search_customers(**query)
    result_b = b._tool_customer_relationship_manager__search_customers(**query)
    if [(x["customer_id"], x["status"], x["notes"]) for x in result_a] != [
            (x["customer_id"], x["status"], x["notes"]) for x in result_b]:
        raise AssertionError("Read-only CRM results differ after restore")
    customer_id = result_a[0]["customer_id"]
    original_status = result_a[0]["status"]
    a._tool_customer_relationship_manager__update_customer(
        customer_id=customer_id, field="status", new_value="Lead")
    if b._tool_customer_relationship_manager__search_customers(**query)[0]["status"] != original_status:
        raise AssertionError("Sandbox restore branches share mutable CRM state")
    write = {"tool_name": "customer_relationship_manager.update_customer",
             "arguments": {"customer_id": customer_id, "field": "status", "new_value": "Lead"}}
    executor = TurnExecutor(None, None)
    executor._dedupe_tool_records({"tool_records": [dict(write)]})
    signature_state = executor.export_state()
    for _ in range(2):
        restored = TurnExecutor(None, None)
        restored.import_state(signature_state)
        artifact = {"tool_records": [dict(write)]}
        restored._dedupe_tool_records(artifact)
        if artifact["tool_records"]:
            raise AssertionError("Previously executed write survived deduplication")
    return {"sandbox_export_import": "PASS", "initial_state_sha256": initial_digest,
            "table_checks": table_checks,
            "deterministic_query": "PASS", "independent_write_state": "PASS",
            "executed_signature_restore": "PASS",
            "scope": "Free component-level check. No Agent history, Auditor/Controller state, injection state or native resume was tested."}


def prepare() -> None:
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip() != BASE_MAIN_SHA:
        raise RuntimeError("Pilot 06 must start from frozen origin/main")
    p5_manifest_path = P5 / "results" / "pilot05_native_ipi" / "manifest.json"
    if not p5_manifest_path.is_file():
        raise RuntimeError("Pilot 05 manifest missing")
    p5 = read(p5_manifest_path)
    p5_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=P5).decode().strip()
    source_config = Path(p5["selected"][0]["source_config"]) if p5.get("selected") else None
    if source_config is None:
        raise RuntimeError("Pilot 05 had no frozen source task")
    import tomllib

    config = tomllib.loads(source_config.read_text(encoding="utf-8"))
    data_root = Path(config["workbench"]["data_dir"])
    free_check = free_restore(data_root)
    save(RESULTS / "free_restore_check.json", free_check)
    ledger = read(Path(p5["shared_budget_ledger"]))
    attack_runs = [x for x in ledger.get("episodes", []) if x.get("pilot") == "pilot05"
                   and x.get("arm") in {"E2_fixed_attack", "E3_adaptive_attack"}]
    cases = []
    for episode in attack_runs:
        meta_path = Path(episode["metadata_path"])
        if sha(meta_path) != episode["metadata_sha256"]:
            raise RuntimeError("Pilot 05 metadata hash mismatch")
        metadata = read(meta_path)
        controls = metadata.get("self_evolved", {}).get("turn_control_records") or []
        effective = any(bool(x.get("effective_structural_change")) for x in controls)
        proposed = any(x.get("mutation_proposal") for x in controls)
        exposed = any(x.get("injection_applied") for x in metadata.get("injection_events") or [])
        native_checkpoint = metadata.get("resumable_checkpoint") or {}
        missing = [name for name in REQUIRED if name not in native_checkpoint]
        case_status = ("NO_ATTACK_EXPOSURE" if not exposed else
                       "NO_NATIVE_MUTATION_CANDIDATE" if not proposed else
                       "CHECKPOINT_NOT_EQUIVALENT")
        cases.append({
            "task_id": episode["task_id"], "arm": episode["arm"],
            "source_metadata": str(meta_path), "source_metadata_sha256": sha(meta_path),
            "attack_exposed": exposed, "native_mutation_proposal": proposed,
            "effective_native_mutation": effective, "missing_checkpoint_fields": missing,
            "native_resume_api_available": False,
            "status": case_status,
        })
    has_candidate = any(c["attack_exposed"] and c["native_mutation_proposal"] for c in cases)
    manifest = {
        "base_main_sha": BASE_MAIN_SHA, "branch": "research/pilot06-state-paired-topology",
        "pilot05_commit": p5_commit, "pilot05_manifest": str(p5_manifest_path),
        "pilot05_manifest_sha256": sha(p5_manifest_path),
        "free_restore_check": str(RESULTS / "free_restore_check.json"),
        "free_restore_check_sha256": sha(RESULTS / "free_restore_check.json"),
        "required_checkpoint_fields": REQUIRED, "checkpoint_cases": cases,
        "eligible_cases": [], "intervention_type": "CONTROLLED_TOPOLOGY_MUTATION",
        "status": "CHECKPOINT_NOT_EQUIVALENT" if has_candidate else "BLOCKED_BY_EXPERIMENTAL_PRECONDITION",
        "reason": ("Component restore passes, but Pilot 05 did not save a full native execution checkpoint or expose a lossless resume API. Trace/metadata cannot reconstruct prior sandbox and exactly-once state."
                   if has_candidate else "No attack-exposed Pilot 05 run has a legal native Mutation proposal at an eligible turn boundary."),
        "new_model_requests": 0,
    }
    save(RESULTS / "checkpoint_manifest.json", manifest)
    print(f"Pilot 06 gate: {manifest['status']}; inspected {len(cases)} attack runs")


def run() -> None:
    manifest = read(RESULTS / "checkpoint_manifest.json")
    if not manifest["eligible_cases"]:
        print(f"No paid KEEP/MUTATE continuation: {manifest['status']}")
        return
    raise RuntimeError("Native lossless resume is required before paired continuation")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["prepare", "run"])
    command = parser.parse_args().command
    {"prepare": prepare, "run": run}[command]()

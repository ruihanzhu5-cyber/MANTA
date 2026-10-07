"""Monitor six MATH shards and safely attach their results to the formal run.

The gate is set to ready only after every task has a complete, clean checkpoint.
The original shard artifacts remain untouched for provenance and recovery.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def worker_snapshot(root: Path, worker: dict[str, Any]) -> dict[str, Any]:
    experiment_id = str(worker["experiment_id"])
    status_path = root / "artifacts" / "monitor" / experiment_id / "status.json"
    status = read_json(status_path) if status_path.exists() else {"state": "missing"}
    run_root = root / "artifacts" / "full_experiment" / experiment_id / "math500" / "self_evolved"
    evaluations = []
    for path in run_root.glob("*/run_*.eval.json"):
        try:
            evaluations.append(read_json(path))
        except (OSError, ValueError, json.JSONDecodeError):
            continue
    return {
        "experiment_id": experiment_id,
        "state": status.get("state", "missing"),
        "message": status.get("message", ""),
        "completed_runs": len(evaluations),
        "successful_runs": sum(bool(item.get("success")) for item in evaluations),
        "run_root": str(run_root),
    }


def validate_worker(root: Path, worker: dict[str, Any]) -> list[Path]:
    experiment_id = str(worker["experiment_id"])
    run_root = root / "artifacts" / "full_experiment" / experiment_id / "math500" / "self_evolved"
    expected_tasks = int(worker["task_limit"])
    expected_runs = int(worker["runs_per_task"])
    task_dirs = sorted(path for path in run_root.iterdir() if path.is_dir() and (path / "task_summary.json").exists())
    if len(task_dirs) != expected_tasks:
        raise RuntimeError(f"{experiment_id}: expected {expected_tasks} completed tasks, found {len(task_dirs)}")
    for task_dir in task_dirs:
        summary = read_json(task_dir / "task_summary.json")
        if summary.get("checkpoint_complete") is not True or summary.get("needs_rerun"):
            raise RuntimeError(f"{experiment_id}/{task_dir.name}: incomplete or needs rerun")
        if int(summary.get("completed_runs", -1)) != expected_runs or len(summary.get("runs", [])) != expected_runs:
            raise RuntimeError(f"{experiment_id}/{task_dir.name}: wrong run count")
        for index in range(expected_runs):
            for suffix in ("answer.txt", "metadata.json", "trace.jsonl", "eval.json"):
                path = task_dir / f"run_{index}.{suffix}"
                if not path.exists():
                    raise RuntimeError(f"Missing required artifact: {path}")
            metadata = read_json(task_dir / f"run_{index}.metadata.json")
            if (metadata.get("run_status", "completed") != "completed" or metadata.get("needs_rerun")
                    or metadata.get("fallback") or metadata.get("error") or metadata.get("failure_category")):
                raise RuntimeError(f"{experiment_id}/{task_dir.name}/run_{index}: invalid run metadata")
            evaluation = read_json(task_dir / f"run_{index}.eval.json")
            if str(evaluation.get("task_id")) != task_dir.name:
                raise RuntimeError(f"{experiment_id}/{task_dir.name}/run_{index}: task ID mismatch")
    return task_dirs


def complete_group(root: Path, manifest: dict[str, Any], group_dir: Path) -> None:
    formal_id = str(manifest["formal_experiment_id"])
    formal_benchmark = root / "artifacts" / "full_experiment" / formal_id / "math500"
    gate_path = formal_benchmark / "external_parallel_gate.json"
    gate = read_json(gate_path)
    if gate.get("group_id") != manifest["group_id"]:
        raise RuntimeError("Formal MATH gate belongs to another parallel group")
    destination = formal_benchmark / "self_evolved"
    sources = [(worker, validate_worker(root, worker)) for worker in manifest["workers"]]
    task_names = [path.name for _, paths in sources for path in paths]
    if len(task_names) != 30 or len(set(task_names)) != 30:
        raise RuntimeError(f"Expected 30 distinct MATH tasks, found {len(set(task_names))}")
    destination.mkdir(parents=True, exist_ok=True)
    for _, task_dirs in sources:
        for source in task_dirs:
            target = destination / source.name
            if target.exists():
                raise RuntimeError(f"Refusing to overwrite existing formal task: {target}")
            shutil.copytree(source, target)
    copied = list(destination.glob("*/run_*.eval.json"))
    if len(copied) != int(manifest["planned_runs"]):
        raise RuntimeError(f"Formal MATH copy count is {len(copied)}, expected {manifest['planned_runs']}")
    provenance = {
        "group_id": manifest["group_id"],
        "formal_experiment_id": formal_id,
        "method_note": manifest["method_note"],
        "skill_update_batch_size": manifest["skill_update_batch_size"],
        "workers": manifest["workers"],
        "merged_at_utc": datetime.now(UTC).isoformat(),
        "task_count": len(task_names),
        "run_count": len(copied),
    }
    write_json(formal_benchmark / "PARALLEL_PROVENANCE.json", provenance)
    gate["ready"] = True
    gate["error"] = None
    write_json(gate_path, gate)
    write_json(group_dir / "status.json", {"state": "completed", "completed_runs": len(copied), "planned_runs": len(copied), "workers": [worker_snapshot(root, w) for w in manifest["workers"]]})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--group-id", default="manta_dsflash_math6_20261005_2100")
    parser.add_argument("--interval", type=float, default=30)
    args = parser.parse_args()
    group_dir = ROOT / "artifacts" / "monitor" / args.group_id
    manifest = read_json(group_dir / "manifest.json")
    formal_benchmark = ROOT / "artifacts" / "full_experiment" / str(manifest["formal_experiment_id"]) / "math500"
    gate_path = formal_benchmark / "external_parallel_gate.json"
    try:
        while True:
            snapshots = [worker_snapshot(ROOT, worker) for worker in manifest["workers"]]
            completed = sum(item["completed_runs"] for item in snapshots)
            write_json(group_dir / "status.json", {
                "state": "running", "completed_runs": completed,
                "successful_runs": sum(item["successful_runs"] for item in snapshots),
                "planned_runs": manifest["planned_runs"], "workers": snapshots,
                "updated_at_utc": datetime.now(UTC).isoformat(),
            })
            failed = [item for item in snapshots if item["state"] == "failed"]
            if failed:
                raise RuntimeError("MATH worker failed: " + ", ".join(item["experiment_id"] for item in failed))
            if all(item["state"] == "completed" for item in snapshots):
                complete_group(ROOT, manifest, group_dir)
                print("MATH_PARALLEL_MERGED 90/90", flush=True)
                return 0
            time.sleep(args.interval)
    except Exception as exc:
        message = f"{type(exc).__name__}: {exc}"
        write_json(group_dir / "status.json", {"state": "failed", "error": message, "updated_at_utc": datetime.now(UTC).isoformat()})
        if gate_path.exists():
            gate = read_json(gate_path)
            gate["error"] = message
            write_json(gate_path, gate)
        print(message, file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

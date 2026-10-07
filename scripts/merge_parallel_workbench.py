"""Attach independent WorkBench shards to the waiting three-benchmark workers."""

from __future__ import annotations

import argparse
import shutil
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from merge_parallel_math import read_json, write_json
from merge_parallel_three import validate_task

ROOT = Path(__file__).resolve().parents[1]


def _worker_status(worker: dict[str, Any]) -> dict[str, Any]:
    worker_id = str(worker["experiment_id"])
    status_path = ROOT / "artifacts" / "monitor" / worker_id / "status.json"
    status = read_json(status_path) if status_path.exists() else {"state": "missing"}
    source = ROOT / "artifacts" / "full_experiment" / worker_id / "workbench" / "self_evolved"
    evaluations = list(source.glob("*/run_*.eval.json"))
    return {
        "experiment_id": worker_id,
        "target_experiment_id": worker["target_experiment_id"],
        "state": status.get("state", "missing"),
        "message": status.get("message", ""),
        "completed_runs": len(evaluations),
    }


def _merge_worker(manifest: dict[str, Any], worker: dict[str, Any]) -> None:
    source_id = str(worker["experiment_id"])
    target_id = str(worker["target_experiment_id"])
    source = ROOT / "artifacts" / "full_experiment" / source_id / "workbench" / "self_evolved"
    target_benchmark = ROOT / "artifacts" / "full_experiment" / target_id / "workbench"
    gate_path = target_benchmark / "external_parallel_gate.json"
    gate = read_json(gate_path)
    if gate.get("group_id") != manifest["group_id"] or gate.get("target_worker_id") != target_id:
        raise RuntimeError(f"WorkBench gate identity mismatch: {gate_path}")
    if gate.get("ready"):
        return
    task_dirs = sorted(path for path in source.iterdir() if path.is_dir() and (path / "task_summary.json").exists())
    if len(task_dirs) != int(worker["task_limit"]):
        raise RuntimeError(f"{source_id}: expected five complete tasks, found {len(task_dirs)}")
    for task_dir in task_dirs:
        validate_task(task_dir, int(worker["runs_per_task"]))
        for eval_path in task_dir.glob("run_*.eval.json"):
            evaluation = read_json(eval_path)
            if str(evaluation.get("task_id")) != task_dir.name:
                raise RuntimeError(f"WorkBench task ID mismatch: {eval_path}")
    destination = target_benchmark / "self_evolved"
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise RuntimeError(f"Refusing to overwrite existing WorkBench worker output: {destination}")
    for task_dir in task_dirs:
        shutil.copytree(task_dir, destination / task_dir.name)
    copied = list(destination.glob("*/run_*.eval.json"))
    if len(copied) != int(gate["expected_runs"]):
        raise RuntimeError(f"{target_id}: expected {gate['expected_runs']} WorkBench results, found {len(copied)}")
    write_json(target_benchmark / "PARALLEL_PROVENANCE.json", {
        "group_id": manifest["group_id"],
        "source_worker_id": source_id,
        "target_worker_id": target_id,
        "benchmark": "workbench",
        "skill_update_batch_size": 0,
        "run_count": len(copied),
        "method_note": manifest["method_note"],
        "merged_at_utc": datetime.now(UTC).isoformat(),
    })
    gate["ready"] = True
    gate["error"] = None
    write_json(gate_path, gate)
    print(f"WORKBENCH_SHARD_MERGED source={source_id} target={target_id} runs=15", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--group-id", default="manta_dsflash_workbench6_20261005_2145")
    parser.add_argument("--interval", type=float, default=30)
    args = parser.parse_args()
    group_dir = ROOT / "artifacts" / "monitor" / args.group_id
    manifest = read_json(group_dir / "manifest.json")
    merged: set[str] = set()
    try:
        while True:
            snapshots = [_worker_status(worker) for worker in manifest["workers"]]
            retryable_failures = []
            for worker, status in zip(manifest["workers"], snapshots, strict=True):
                if status["state"] == "failed":
                    retryable_failures.append(status["experiment_id"])
                    continue
                if status["state"] == "completed" and status["experiment_id"] not in merged:
                    _merge_worker(manifest, worker)
                    merged.add(status["experiment_id"])
            done = sum(item["completed_runs"] for item in snapshots)
            group_status = {
                "state": "completed" if len(merged) == len(snapshots) else (
                    "recovering" if retryable_failures else "running"
                ),
                "completed_runs": done,
                "planned_runs": manifest["planned_runs"],
                "merged_workers": sorted(merged),
                "retryable_failures": retryable_failures,
                "workers": snapshots,
                "updated_at_utc": datetime.now(UTC).isoformat(),
            }
            write_json(group_dir / "status.json", group_status)
            if group_status["state"] == "completed":
                return 0
            time.sleep(args.interval)
    except Exception as exc:
        message = f"{type(exc).__name__}: {exc}"
        write_json(group_dir / "status.json", {
            "state": "failed", "error": message,
            "updated_at_utc": datetime.now(UTC).isoformat(),
        })
        for worker in manifest["workers"]:
            gate_path = (ROOT / "artifacts" / "full_experiment" /
                         str(worker["target_experiment_id"]) / "workbench" /
                         "external_parallel_gate.json")
            if gate_path.exists():
                gate = read_json(gate_path)
                if not gate.get("ready"):
                    gate["error"] = message
                    write_json(gate_path, gate)
        print(message, file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

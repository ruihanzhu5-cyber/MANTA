"""Attach completed selected benchmark shards to one formal run."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from merge_parallel_math import read_json, write_json

ROOT = Path(__file__).resolve().parents[1]


def snapshot(worker: dict[str, Any]) -> dict[str, Any]:
    worker_id = str(worker["experiment_id"])
    status_path = ROOT / "artifacts" / "monitor" / worker_id / "status.json"
    status = read_json(status_path) if status_path.exists() else {"state": "missing"}
    counts: dict[str, int] = {}
    successes: dict[str, int] = {}
    for benchmark in ("browsecomp", "workbench", "plancraft"):
        run_root = ROOT / "artifacts" / "full_experiment" / worker_id / benchmark / "self_evolved"
        evaluations = []
        for path in run_root.glob("*/run_*.eval.json"):
            try:
                evaluations.append(read_json(path))
            except (OSError, ValueError, json.JSONDecodeError):
                continue
        counts[benchmark] = len(evaluations)
        successes[benchmark] = sum(bool(item.get("success")) for item in evaluations)
    return {"experiment_id": worker_id, "state": status.get("state", "missing"),
            "message": status.get("message", ""), "completed_runs": counts,
            "successful_runs": successes}


def validate_task(task_dir: Path, runs: int) -> None:
    summary = read_json(task_dir / "task_summary.json")
    if (summary.get("checkpoint_complete") is not True or summary.get("needs_rerun")
            or int(summary.get("completed_runs", -1)) != runs
            or len(summary.get("runs", [])) != runs):
        raise RuntimeError(f"Incomplete or invalid checkpoint: {task_dir}")
    for index in range(runs):
        for suffix in ("answer.txt", "metadata.json", "trace.jsonl", "eval.json"):
            path = task_dir / f"run_{index}.{suffix}"
            if not path.exists():
                raise RuntimeError(f"Missing artifact: {path}")
        metadata = read_json(task_dir / f"run_{index}.metadata.json")
        if (metadata.get("run_status", "completed") != "completed" or metadata.get("needs_rerun")
                or metadata.get("fallback") or metadata.get("error") or metadata.get("failure_category")):
            raise RuntimeError(f"Invalid run metadata: {task_dir}/run_{index}")


def merge_benchmark(manifest: dict[str, Any], benchmark: str) -> None:
    formal_id = str(manifest["formal_experiment_id"])
    formal_benchmark = ROOT / "artifacts" / "full_experiment" / formal_id / benchmark
    gate_path = formal_benchmark / "external_parallel_gate.json"
    gate = read_json(gate_path)
    if gate.get("group_id") != manifest["group_id"]:
        raise RuntimeError(f"Gate belongs to a different group: {gate_path}")
    destination = formal_benchmark / "self_evolved"
    sources = []
    for worker in manifest["workers"]:
        worker_id = str(worker["experiment_id"])
        run_root = ROOT / "artifacts" / "full_experiment" / worker_id / benchmark / "self_evolved"
        task_dirs = sorted(path for path in run_root.iterdir() if path.is_dir() and (path / "task_summary.json").exists())
        if len(task_dirs) != int(worker["task_limit"]):
            raise RuntimeError(f"{worker_id}/{benchmark}: wrong task count {len(task_dirs)}")
        for task_dir in task_dirs:
            validate_task(task_dir, int(worker["runs_per_task"]))
        sources.extend(task_dirs)
    if len(sources) != 30 or len({path.name for path in sources}) != 30:
        raise RuntimeError(f"{benchmark}: expected 30 distinct task IDs")

    destination.mkdir(parents=True, exist_ok=True)
    for source in sources:
        target = destination / source.name
        if target.exists():
            # The original formal BrowseComp run_0 was copied to worker 0 before
            # launch. It is the only permitted partial target. All other output
            # collisions are errors rather than silent overwrites.
            if benchmark != "browsecomp" or source.name != "769":
                raise RuntimeError(f"Refusing to overwrite existing task: {target}")
            for existing in target.iterdir():
                if existing.name == "task_summary.json":
                    continue
                counterpart = source / existing.name
                if not counterpart.is_file() or existing.read_bytes() != counterpart.read_bytes():
                    raise RuntimeError(f"Existing formal artifact differs from shard: {existing}")
            shutil.copytree(source, target, dirs_exist_ok=True)
        else:
            shutil.copytree(source, target)
    copied = list(destination.glob("*/run_*.eval.json"))
    if len(copied) != int(gate["expected_runs"]):
        raise RuntimeError(f"{benchmark}: expected {gate['expected_runs']} evaluations, found {len(copied)}")
    write_json(formal_benchmark / "PARALLEL_PROVENANCE.json", {
        "group_id": manifest["group_id"], "benchmark": benchmark,
        "formal_experiment_id": formal_id,
        "method_note": manifest["method_note"],
        "skill_update_batch_size": manifest["skill_update_batch_size"],
        "workers": manifest["workers"],
        "task_count": len(sources), "run_count": len(copied),
        "merged_at_utc": datetime.now(UTC).isoformat(),
    })
    gate["ready"] = True
    gate["error"] = None
    write_json(gate_path, gate)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--group-id", default="manta_dsflash_parallel3_20261005_2120")
    parser.add_argument("--interval", type=float, default=30)
    args = parser.parse_args()
    group_dir = ROOT / "artifacts" / "monitor" / args.group_id
    manifest = read_json(group_dir / "manifest.json")
    try:
        while True:
            workers = [snapshot(worker) for worker in manifest["workers"]]
            selected = tuple(manifest["benchmarks"])
            selected_completed = sum(
                item["completed_runs"][benchmark]
                for item in workers for benchmark in selected
            )
            write_json(group_dir / "status.json", {
                "state": "running", "workers": workers,
                "planned_runs": manifest["planned_runs"],
                "completed_runs": selected_completed,
                "updated_at_utc": datetime.now(UTC).isoformat(),
            })
            if all(
                item["completed_runs"][benchmark]
                == int(worker["task_limit"]) * int(worker["runs_per_task"])
                for item, worker in zip(workers, manifest["workers"])
                for benchmark in selected
            ):
                validation_error = None
                for benchmark in selected:
                    gate_path = (ROOT / "artifacts" / "full_experiment"
                                 / str(manifest["formal_experiment_id"]) / benchmark
                                 / "external_parallel_gate.json")
                    if read_json(gate_path).get("ready"):
                        continue
                    try:
                        merge_benchmark(manifest, benchmark)
                    except RuntimeError as exc:
                        validation_error = f"{benchmark}: {exc}"
                        break
                    print(f"PARALLEL_MERGED benchmark={benchmark} runs=90", flush=True)
                if validation_error:
                    write_json(group_dir / "status.json", {
                        "state": "recovering", "workers": workers,
                        "planned_runs": manifest["planned_runs"],
                        "completed_runs": selected_completed,
                        "validation_error": validation_error,
                        "updated_at_utc": datetime.now(UTC).isoformat(),
                    })
                    time.sleep(args.interval)
                    continue
                write_json(group_dir / "status.json", {
                    "state": "completed", "planned_runs": manifest["planned_runs"],
                    "completed_runs": manifest["planned_runs"], "workers": workers,
                    "updated_at_utc": datetime.now(UTC).isoformat(),
                })
                return 0
            time.sleep(args.interval)
    except Exception as exc:
        message = f"{type(exc).__name__}: {exc}"
        write_json(group_dir / "status.json", {"state": "failed", "error": message,
                                             "updated_at_utc": datetime.now(UTC).isoformat()})
        for benchmark in manifest["benchmarks"]:
            gate_path = (ROOT / "artifacts" / "full_experiment" /
                         str(manifest["formal_experiment_id"]) / benchmark /
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

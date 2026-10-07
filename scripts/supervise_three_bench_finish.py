"""Finish the user-approved three-benchmark run without starting PlanCraft."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

import psutil

ROOT = Path(__file__).resolve().parents[1]
MONITOR = ROOT / "artifacts" / "monitor"
OUTPUT = ROOT / "artifacts" / "full_experiment"
ORIGINAL_GROUP = "manta_dsflash_parallel3_20261005_2120"
WORKBENCH_GROUP = "manta_dsflash_workbench6_20261005_2145"
MATH_GROUP = "manta_dsflash_math6_20261005_2100"
FORMAL_ID = "manta_dsflash_4bench_utf8_20261005_2030"
STATE_PATH = MONITOR / "three_bench_supervisor_status.json"
MAX_RETRIES = 3


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def write_json(path: Path, value: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def status(experiment_id: str) -> dict:
    return read_json(MONITOR / experiment_id / "status.json")


def evaluations(experiment_id: str, benchmark: str) -> int:
    root = OUTPUT / experiment_id / benchmark / "self_evolved"
    return sum(1 for _ in root.glob("*/run_*.eval.json"))


def plan_craft_waiting(experiment_id: str) -> bool:
    log = MONITOR / experiment_id / "runner.log"
    try:
        with log.open("rb") as handle:
            handle.seek(0, 2)
            handle.seek(max(0, handle.tell() - 8192))
            tail = handle.read().decode("utf-8", errors="replace")
    except OSError:
        return False
    last_line = next((line for line in reversed(tail.splitlines()) if line.strip()), "")
    return ("EXTERNAL_BENCHMARK_WAIT" in last_line
            and "\\plancraft\\external_parallel_gate.json" in last_line)


def stop_parked_worker(experiment_id: str, index: int, process_id: int) -> None:
    proc = psutil.Process(process_id)
    command = " ".join(proc.cmdline()).lower()
    if "launch_parallel_three_worker.ps1" not in command or f"-index {index}" not in command:
        raise RuntimeError(f"Refusing to stop unexpected process {process_id}")
    if not plan_craft_waiting(experiment_id):
        raise RuntimeError(f"{experiment_id} has not reached the PlanCraft gate")
    if evaluations(experiment_id, "browsecomp") != 15 or evaluations(experiment_id, "workbench") != 15:
        raise RuntimeError(f"{experiment_id} has incomplete selected benchmarks")
    if evaluations(experiment_id, "plancraft"):
        raise RuntimeError(f"{experiment_id} unexpectedly started PlanCraft")
    descendants = proc.children(recursive=True)
    for child in reversed(descendants):
        try:
            child.terminate()
        except psutil.NoSuchProcess:
            pass
    gone, alive = psutil.wait_procs(descendants, timeout=5)
    for child in alive:
        child.kill()
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except psutil.TimeoutExpired:
        proc.kill()
    current = status(experiment_id)
    current["state"] = "resuming"
    current["message"] = "PlanCraft 已取消，按三项配置完成汇总"
    current["pid"] = None
    current["updated_at_utc"] = datetime.now(UTC).isoformat()
    write_json(MONITOR / experiment_id / "status.json", current)


def launch(script: str, index: int | None, experiment_id: str) -> int:
    powershell = shutil.which("pwsh")
    if not powershell:
        raise RuntimeError("pwsh is unavailable")
    command = [
        powershell, "-NoLogo", "-NoProfile", "-NonInteractive",
        "-ExecutionPolicy", "Bypass", "-File", str(ROOT / "scripts" / script),
    ]
    if index is not None:
        command += ["-Index", str(index)]
    monitor_dir = MONITOR / experiment_id
    monitor_dir.mkdir(parents=True, exist_ok=True)
    with (monitor_dir / "supervisor.stdout.log").open("ab") as stdout, (
        monitor_dir / "supervisor.stderr.log"
    ).open("ab") as stderr:
        child = subprocess.Popen(
            command,
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=stdout,
            stderr=stderr,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
    return child.pid


def run_once(memory: dict, dry_run: bool) -> tuple[dict, bool]:
    attempts: dict[str, int] = memory.setdefault("attempts", {})
    actions: list[str] = []

    # These independent shards must be valid before their results are copied
    # into the original workers. A failed run is retried in the same shard.
    for index in range(6):
        experiment_id = f"{WORKBENCH_GROUP}_w{index}"
        worker = status(experiment_id)
        if worker.get("state") == "failed" and attempts.get(experiment_id, 0) < MAX_RETRIES:
            actions.append(f"retry {experiment_id} with WorkBench only")
            if not dry_run:
                attempts[experiment_id] = attempts.get(experiment_id, 0) + 1
                launch("resume_workbench_worker.ps1", index, experiment_id)

    for index in range(6):
        experiment_id = f"{ORIGINAL_GROUP}_w{index}"
        worker = status(experiment_id)
        workbench_gate = read_json(OUTPUT / experiment_id / "workbench" / "external_parallel_gate.json")
        if not workbench_gate.get("ready"):
            continue
        parked = (worker.get("state") == "running" and plan_craft_waiting(experiment_id))
        failed = worker.get("state") == "failed"
        if not (parked or failed) or attempts.get(experiment_id, 0) >= MAX_RETRIES:
            continue
        if parked and (evaluations(experiment_id, "browsecomp") != 15
                       or evaluations(experiment_id, "workbench") != 15):
            continue
        actions.append(f"finish {experiment_id} with BrowseComp and WorkBench only")
        if not dry_run:
            if parked:
                stop_parked_worker(experiment_id, index, int(worker["pid"]))
            attempts[experiment_id] = attempts.get(experiment_id, 0) + 1
            launch("resume_three_bench_worker.ps1", index, experiment_id)

    groups_done = (
        status(ORIGINAL_GROUP).get("state") == "completed"
        and status(WORKBENCH_GROUP).get("state") == "completed"
        and status(MATH_GROUP).get("state") == "completed"
    )
    formal = status(FORMAL_ID)
    if groups_done and formal.get("state") == "failed" and attempts.get(FORMAL_ID, 0) < MAX_RETRIES:
        actions.append("restart formal consolidation for three benchmarks")
        if not dry_run:
            attempts[FORMAL_ID] = attempts.get(FORMAL_ID, 0) + 1
            launch("launch_three_bench_formal.ps1", None, FORMAL_ID)

    done = formal.get("state") == "completed" and groups_done
    if done and (evaluations(FORMAL_ID, "browsecomp") != 90
                 or evaluations(FORMAL_ID, "workbench") != 90
                 or evaluations(FORMAL_ID, "math500") != 90
                 or evaluations(FORMAL_ID, "plancraft") != 0):
        raise RuntimeError("Formal result counts do not match 90+90+90 and zero PlanCraft")
    memory["state"] = "completed" if done else "running"
    memory["last_actions"] = actions
    memory["updated_at_utc"] = datetime.now(UTC).isoformat()
    return memory, done


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=float, default=30)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    memory = read_json(STATE_PATH) or {"attempts": {}}
    while True:
        try:
            memory, done = run_once(memory, args.dry_run)
            if not args.dry_run:
                write_json(STATE_PATH, memory)
            if memory["last_actions"]:
                print("; ".join(memory["last_actions"]), flush=True)
            if done:
                print("Three-benchmark formal result completed", flush=True)
                return 0
        except Exception as exc:
            memory["last_error"] = f"{type(exc).__name__}: {exc}"
            memory["updated_at_utc"] = datetime.now(UTC).isoformat()
            if not args.dry_run:
                write_json(STATE_PATH, memory)
            print(memory["last_error"], flush=True)
        if args.once:
            return 0
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())

"""Sequential, budget-gated live AppWorld baseline driver.

No model call is made unless an explicit cap is supplied for this experiment.
Raw output and the ledger stay under ignored artifacts/. The six task IDs are
frozen in config/research/appworld_manta_v01.toml before any live attack run.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import threading
import time
import tomllib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config/research/appworld_manta_v01.toml"
OUT = ROOT / "artifacts/appworld_baselines"
LEDGER = OUT / "ledger.json"
ARMS = {"STATIC_STAR": "orchestrator_no_discussion", "MANTA_NATIVE": "self_evolved"}
ADAPTER_REVISION = "structured_tool_outputs_v2"
_LEDGER_LOCK = threading.Lock()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_ledger(cap: float, *, revise_cap: bool = False) -> dict[str, Any]:
    if LEDGER.exists():
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        # Early failed runs may have only log usage: run exceptions collapse the
        # trace to one error event. Count provider-reported DONE usage anyway.
        for row in ledger["episodes"]:
            log_path = Path(str(row.get("log_path", "")))
            if not log_path.is_file():
                continue
            usage = [(int(a), int(b)) for a, b in re.findall(
                r"\bDONE\b[^\n]*\btoken_in=(\d+)\s+token_out=(\d+)",
                log_path.read_text(encoding="utf-8", errors="replace")
            )]
            token_in = sum(a for a, _ in usage)
            token_out = sum(b for _, b in usage)
            row["token_in"] = max(int(row.get("token_in", 0)), token_in)
            row["token_out"] = max(int(row.get("token_out", 0)), token_out)
            estimate = (row["token_in"] * 0.30 + row["token_out"] * 1.20) / 1_000_000
            row["conservative_cost_usd"] = max(
                float(row.get("conservative_cost_usd", 0)), estimate)
            row["cost_upper_usd"] = max(float(row.get("cost_upper_usd", 0)), estimate)
            row["model_events"] = max(int(row.get("model_events", 0)), len(usage))
        old_cap = float(ledger["approved_cap_usd"])
        if abs(old_cap - cap) > 1e-9:
            if not revise_cap:
                raise ValueError("Existing ledger cap differs; use --revise-cap to record a change")
            if cap < spent_upper(ledger):
                raise ValueError("Revised cap is below already recorded upper-bound spend")
            ledger.setdefault("cap_revisions", []).append({
                "old_usd": old_cap, "new_usd": cap,
                "revised_utc": datetime.now(UTC).isoformat(),
            })
            ledger["approved_cap_usd"] = cap
        write_json(LEDGER, ledger)
        return ledger
    return {"approved_cap_usd": cap, "inflight": [], "episodes": []}


def spent_upper(ledger: dict[str, Any]) -> float:
    return sum(float(row["cost_upper_usd"]) for row in ledger["episodes"]) + sum(
        float(row["reserve_usd"]) for row in ledger["inflight"]
    )


def generated_config(arm: str, overlay_path: str = "", suffix: str = "") -> Path:
    content = CONFIG.read_text(encoding="utf-8")
    base_arm = arm.removesuffix("_ATTACK")
    if base_arm not in ARMS:
        raise ValueError(f"Unknown baseline arm: {arm}")
    for old, new in (
        ('topology = "self_evolved"', f'topology = "{ARMS[base_arm]}"'),
        ('arm = "MANTA_NATIVE"', f'arm = "{arm}"'),
        ('attack_overlay_path = ""', f'attack_overlay_path = {json.dumps(overlay_path)}'),
    ):
        if content.count(old) != 1:
            raise ValueError(f"Expected one frozen config anchor: {old}")
        content = content.replace(old, new, 1)
    path = OUT / "configs" / f"{arm}{suffix}.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def trace_summary(run_root: Path, log_path: Path) -> dict[str, Any]:
    log_text = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
    logged_usage = [(int(a), int(b)) for a, b in re.findall(
        r"\bDONE\b[^\n]*\btoken_in=(\d+)\s+token_out=(\d+)", log_text
    )]
    logged_in = sum(a for a, _ in logged_usage)
    logged_out = sum(b for _, b in logged_usage)
    metrics_files = list(run_root.rglob("run_0.trace_metrics.json"))
    eval_files = list(run_root.rglob("run_0.eval.json"))
    trace_files = list(run_root.rglob("run_0.trace.jsonl"))
    if len(metrics_files) != 1 or len(eval_files) != 1 or len(trace_files) != 1:
        return {"complete_artifacts": False, "token_in": logged_in,
                "token_out": logged_out, "model_events": len(logged_usage),
                "conservative_cost_usd": (logged_in * 0.30 + logged_out * 1.20) / 1_000_000}
    metrics = json.loads(metrics_files[0].read_text(encoding="utf-8"))
    evaluation = json.loads(eval_files[0].read_text(encoding="utf-8"))
    trace = [json.loads(line) for line in trace_files[0].read_text(encoding="utf-8").splitlines()
             if line.strip()]
    token_in = max(logged_in, sum(int(event.get("token_in") or 0) for event in trace))
    token_out = max(logged_out, sum(int(event.get("token_out") or 0) for event in trace))
    estimated = (token_in * 0.30 + token_out * 1.20) / 1_000_000
    observed_cost = float(metrics.get("metrics", {}).get("cost_total") or 0)
    return {
        "complete_artifacts": True,
        "official_score_available": bool(evaluation.get("details", {}).get("official_score_available")),
        "official_task_success": bool(evaluation.get("success")),
        "token_in": token_in,
        "token_out": token_out,
        "model_events": max(len(logged_usage), sum(
            bool(event.get("token_in") or event.get("token_out")) for event in trace)),
        "tool_calls": int(metrics.get("metrics", {}).get("tool_calls_total") or 0),
        "observed_cost_usd": observed_cost,
        "conservative_cost_usd": max(observed_cost, estimated),
        "trace_metrics_path": str(metrics_files[0]),
    }


def run_one(
    task_id: str, arm: str, ledger: dict[str, Any], *, reserve: float,
    max_seconds: int, overlay_path: str = "",
) -> dict[str, Any]:
    with _LEDGER_LOCK:
        prior = [row for row in ledger["episodes"] if row["task_id"] == task_id
                 and row["arm"] == arm]
    valid = [row for row in prior if row.get("return_code") == 0
             and row.get("adapter_revision") == ADAPTER_REVISION
             and row.get("complete_artifacts") and row.get("official_score_available")
             and row.get("model_events", 0) > 0 and row.get("tool_calls", 0) > 0]
    if valid:
        return valid[-1]
    with _LEDGER_LOCK:
        if spent_upper(ledger) + reserve > float(ledger["approved_cap_usd"]):
            raise RuntimeError("BUDGET_STOP: conservative reservation would exceed authorized cap")
        inflight = {"task_id": task_id, "arm": arm, "reserve_usd": reserve,
                    "started_utc": datetime.now(UTC).isoformat()}
        ledger["inflight"].append(inflight)
        write_json(LEDGER, ledger)
    config_path = generated_config(arm, overlay_path, f"_{task_id}_attempt{len(prior)+1}")
    attempt = len(prior) + 1
    experiment_id = f"appworld_{task_id}_{arm.lower()}_attempt{attempt}"
    run_root = OUT / "raw" / experiment_id
    log_path = OUT / "logs" / f"{experiment_id}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.pop("MAS_DISABLE_LIVE_LLM", None)
    env.update({
        "MAS_REQUIRE_LIVE_LLM": "1", "DEEPSEEK_THINKING": "disabled",
        "OPENROUTER_TEMPERATURE": "0", "DEEPSEEK_MAX_TOKENS": "2048",
        "MAS_OPENROUTER_TIMEOUT_S": "150", "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1",
    })
    command = [sys.executable, "main.py", "run", "--config", str(config_path),
               "--benchmark", "appworld", "--task-ids", task_id, "--runs-per-task", "1",
               "--seed", "42", "--output-dir", str(OUT / "raw"),
               "--output-layout", "hierarchical", "--experiment-id", experiment_id,
               "--system-label", arm]
    start = time.monotonic()
    return_code: int | None = None
    error = ""
    try:
        with log_path.open("w", encoding="utf-8") as log:
            completed = subprocess.run(command, cwd=ROOT, env=env, stdout=log,
                                       stderr=subprocess.STDOUT, timeout=max_seconds, check=False)
            return_code = completed.returncode
    except subprocess.TimeoutExpired:
        error = "TIME_LIMIT"
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    try:
        summary = trace_summary(run_root, log_path)
    except Exception as exc:
        summary = {"complete_artifacts": False,
                   "artifact_error": f"{type(exc).__name__}: {exc}"}
    cost_upper = max(reserve if not summary.get("complete_artifacts") else 0.0,
                     float(summary.get("conservative_cost_usd", 0)))
    episode = {"task_id": task_id, "arm": arm, "attempt": attempt,
               "adapter_revision": ADAPTER_REVISION,
               "return_code": return_code,
               "error": error, "duration_seconds": round(time.monotonic() - start, 2),
               "cost_upper_usd": cost_upper, "log_path": str(log_path), **summary}
    with _LEDGER_LOCK:
        if inflight in ledger["inflight"]:
            ledger["inflight"].remove(inflight)
        ledger["episodes"].append(episode)
        write_json(LEDGER, ledger)
    return episode


def run_batch(items: list[tuple[str, str]], ledger: dict[str, Any], *, reserve: float,
              max_seconds: int, workers: int, overlay_path: str = "") -> list[dict[str, Any]]:
    from concurrent.futures import ThreadPoolExecutor, as_completed
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {
            pool.submit(run_one, task_id, arm, ledger, reserve=reserve,
                        max_seconds=max_seconds, overlay_path=overlay_path): (task_id, arm)
            for task_id, arm in items
        }
        for future in as_completed(futures):
            task_id, arm = futures[future]
            try:
                row = future.result()
            except Exception as exc:
                row = {"task_id": task_id, "arm": arm, "error": f"{type(exc).__name__}: {exc}"}
            results.append(row)
            print(task_id, arm, row.get("official_task_success"), row.get("error"), flush=True)
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--approved-cap-usd", type=float)
    parser.add_argument("--revise-cap", action="store_true")
    parser.add_argument("--reserve-per-run-usd", type=float, default=1.0)
    parser.add_argument("--max-seconds-per-run", type=int, default=1800)
    parser.add_argument("--phase", choices=["clean", "attack"], default="clean")
    parser.add_argument("--attack-overlay-path", default="")
    parser.add_argument("--attack-task-ids", default="")
    parser.add_argument("--parallel-workers", type=int, default=4)
    args = parser.parse_args()
    if args.approved_cap_usd is None or args.approved_cap_usd <= 0:
        print("BLOCKED_PAID_AUTHORIZATION: supply the approved cap for this AppWorld round")
        return 2
    project_key = os.getenv("DEEPSEEK_API_KEY") or dotenv_values(ROOT / ".env").get("DEEPSEEK_API_KEY")
    if not project_key:
        print("BLOCKED_PAID_CREDENTIAL: set the authorized project DEEPSEEK_API_KEY")
        return 2
    os.environ["DEEPSEEK_API_KEY"] = str(project_key)
    config = tomllib.loads(CONFIG.read_text(encoding="utf-8"))
    ids = list(config["appworld"]["task_ids"])
    ledger = load_ledger(args.approved_cap_usd, revise_cap=args.revise_cap)
    if args.phase == "clean":
        first_batch = [(task_id, arm) for task_id in ids[:2] for arm in ARMS]
        run_batch(first_batch, ledger, reserve=args.reserve_per_run_usd,
                  max_seconds=args.max_seconds_per_run, workers=1)
        smoke = [next((row for row in reversed(ledger["episodes"])
                       if row["task_id"] == task_id and row["arm"] == arm), {})
                 for task_id in ids[:2] for arm in ARMS]
        if len(smoke) != 4 or not all(
            row.get("complete_artifacts") and row.get("official_score_available")
            and row.get("model_events", 0) > 0 and row.get("tool_calls", 0) > 0
            for row in smoke
        ):
            print("CLEAN_SMOKE_GATE_FAILED: inspect adapter; attack phase remains closed")
            return 3
        remaining = [(task_id, arm) for task_id in ids[2:] for arm in ARMS]
        run_batch(remaining, ledger, reserve=args.reserve_per_run_usd,
                  max_seconds=args.max_seconds_per_run, workers=args.parallel_workers)
    else:
        attack_ids = [item.strip() for item in args.attack_task_ids.split(",") if item.strip()]
        if not attack_ids or not args.attack_overlay_path:
            raise ValueError("Attack phase requires frozen task IDs and overlay file")
        if set(attack_ids).difference(ids):
            raise ValueError("Attack IDs must be in the frozen clean set")
        if not all(any(row["task_id"] == task_id and row["arm"] == arm
                       and row.get("official_score_available") for row in ledger["episodes"])
                   for task_id in attack_ids for arm in ARMS):
            raise RuntimeError("Clean official evaluations are required before attack arms")
        attack_items = [(task_id, base_arm + "_ATTACK")
                        for task_id in attack_ids for base_arm in ARMS]
        for row in run_batch(attack_items, ledger, reserve=args.reserve_per_run_usd,
                             max_seconds=args.max_seconds_per_run, workers=args.parallel_workers,
                             overlay_path=str(Path(args.attack_overlay_path).resolve())):
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

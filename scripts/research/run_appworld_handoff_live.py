"""Budgeted live DeepSeek Flash runner for the AppWorld handoff experiment."""

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
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config/research/appworld_handoff_live_v01.toml"
OUT = ROOT / "artifacts/appworld_handoff_live"
LEDGER = OUT / "ledger.json"
BASE_CONFIG = CONFIG.read_text(encoding="utf-8")
LOCK = threading.Lock()
VALID_VARIANTS = {"NATIVE_PACKET", "SUMMARY_ONLY", "EVIDENCE_REFERENCED"}


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def load_ledger(cap: float) -> dict[str, Any]:
    if LEDGER.exists():
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        if abs(float(ledger.get("approved_cap_usd", cap)) - cap) > 1e-9:
            raise RuntimeError("Existing live ledger cap differs; use a fresh artifact directory")
        return ledger
    return {"approved_cap_usd": cap, "inflight": [], "episodes": [],
            "created_utc": datetime.now(UTC).isoformat(), "model": "deepseek-flash"}


def spent_upper(ledger: dict[str, Any]) -> float:
    return sum(float(row.get("cost_upper_usd", 0)) for row in ledger.get("episodes", [])) + sum(
        float(row.get("reserve_usd", 0)) for row in ledger.get("inflight", [])
    )


def config_for(arm: str, variant: str) -> Path:
    topology = "sas" if arm == "SINGLE_AGENT" else "self_evolved"
    agents = "1" if arm == "SINGLE_AGENT" else "3"
    text = BASE_CONFIG.replace('topology = "self_evolved"', f'topology = "{topology}"', 1)
    text = text.replace("number_of_agents = 3", f"number_of_agents = {agents}", 1)
    text = text.replace('arm = "MANTA_NATIVE"', f'arm = "{arm}"', 1)
    text = text.replace('handoff_variant = "NATIVE_PACKET"', f'handoff_variant = "{variant}"', 1)
    path = OUT / "configs" / f"{arm}_{variant}.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _trace_summary(run_root: Path, log_path: Path) -> dict[str, Any]:
    text = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
    usage = [(int(a), int(b)) for a, b in re.findall(r"\bDONE\b[^\n]*\btoken_in=(\d+)\s+token_out=(\d+)", text)]
    metrics_files = list(run_root.rglob("run_0.trace_metrics.json"))
    eval_files = list(run_root.rglob("run_0.eval.json"))
    trace_files = list(run_root.rglob("run_0.trace.jsonl"))
    result: dict[str, Any] = {
        "complete_artifacts": len(metrics_files) == len(eval_files) == len(trace_files) == 1,
        "token_in": sum(a for a, _ in usage), "token_out": sum(b for _, b in usage),
        "model_events": len(usage),
    }
    if not result["complete_artifacts"]:
        result["official_score_available"] = False
        result["cost_upper_usd"] = 1.0
        return result
    metrics = json.loads(metrics_files[0].read_text(encoding="utf-8"))
    evaluation = json.loads(eval_files[0].read_text(encoding="utf-8"))
    trace = [json.loads(line) for line in trace_files[0].read_text(encoding="utf-8").splitlines() if line.strip()]
    token_in = max(result["token_in"], sum(int(event.get("token_in") or 0) for event in trace))
    token_out = max(result["token_out"], sum(int(event.get("token_out") or 0) for event in trace))
    estimated = (token_in * 0.30 + token_out * 1.20) / 1_000_000
    observed = float(metrics.get("metrics", {}).get("cost_total") or 0)
    result.update({
        "official_score_available": bool(evaluation.get("details", {}).get("official_score_available")),
        "official_task_success": bool(evaluation.get("success")),
        "token_in": token_in, "token_out": token_out,
        "model_events": max(len(usage), sum(bool(event.get("token_in") or event.get("token_out")) for event in trace)),
        "tool_calls": int(metrics.get("metrics", {}).get("tool_calls_total") or 0),
        "observed_cost_usd": observed, "cost_upper_usd": max(observed, estimated),
        "evaluation": evaluation,
    })
    return result


def run_one(task_id: str, arm: str, variant: str, ledger: dict[str, Any], *, reserve: float, max_seconds: int, dry_run: bool) -> dict[str, Any]:
    key = (task_id, arm, variant)
    prior = [row for row in ledger["episodes"] if (row.get("task_id"), row.get("arm"), row.get("variant")) == key]
    if prior and prior[-1].get("complete_artifacts"):
        return prior[-1]
    if dry_run:
        return {"task_id": task_id, "arm": arm, "variant": variant, "dry_run": True}
    with LOCK:
        if spent_upper(ledger) + reserve > float(ledger["approved_cap_usd"]):
            raise RuntimeError("BUDGET_STOP: conservative reservation would exceed cap")
        inflight = {"task_id": task_id, "arm": arm, "variant": variant, "reserve_usd": reserve,
                    "started_utc": datetime.now(UTC).isoformat()}
        ledger["inflight"].append(inflight); write_json(LEDGER, ledger)
    config = config_for(arm, variant)
    experiment_id = f"appworld_handoff_{task_id}_{arm.lower()}_{variant.lower()}"
    run_root = OUT / "raw" / experiment_id
    log_path = OUT / "logs" / f"{experiment_id}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy(); env.pop("MAS_DISABLE_LIVE_LLM", None)
    env.update({"MAS_REQUIRE_LIVE_LLM": "1", "DEEPSEEK_THINKING": "disabled",
                "OPENROUTER_TEMPERATURE": "0", "DEEPSEEK_MAX_TOKENS": "2048",
                "MAS_OPENROUTER_TIMEOUT_S": "150", "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"})
    command = [sys.executable, "main.py", "run", "--config", str(config), "--benchmark", "appworld",
               "--task-ids", task_id, "--runs-per-task", "1", "--seed", "42", "--output-dir", str(OUT / "raw"),
               "--output-layout", "hierarchical", "--experiment-id", experiment_id, "--system-label", arm]
    started = time.monotonic(); return_code = None; error = ""
    try:
        with log_path.open("w", encoding="utf-8") as log:
            return_code = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT,
                                         timeout=max_seconds, check=False).returncode
    except subprocess.TimeoutExpired:
        error = "TIME_LIMIT"
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    summary = _trace_summary(run_root, log_path)
    episode = {"task_id": task_id, "arm": arm, "variant": variant, "return_code": return_code,
               "error": error, "duration_seconds": round(time.monotonic() - started, 2), **summary}
    with LOCK:
        if inflight in ledger["inflight"]: ledger["inflight"].remove(inflight)
        ledger["episodes"].append(episode); write_json(LEDGER, ledger)
    print(f"{task_id} {arm} {variant} success={episode.get('official_task_success', False)}", flush=True)
    return episode


def run_batch(items: list[tuple[str, str, str]], ledger: dict[str, Any], *, workers: int, reserve: float, max_seconds: int, dry_run: bool) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {pool.submit(run_one, *item, ledger, reserve=reserve, max_seconds=max_seconds, dry_run=dry_run): item for item in items}
        for future in as_completed(futures):
            try: results.append(future.result())
            except Exception as exc: results.append({"item": futures[future], "error": f"{type(exc).__name__}: {exc}"})
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["functional", "clean", "attack", "all"], default="all")
    parser.add_argument("--approved-cap-usd", type=float, required=True)
    parser.add_argument("--parallel-episodes", type=int, default=None)
    parser.add_argument("--model-max-inflight", type=int, default=8)
    parser.add_argument("--max-seconds-per-run", type=int, default=1800)
    parser.add_argument("--task-ids", default="6c2c621_1,530b157_1")
    parser.add_argument("--arms", default="")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    key_present = bool(os.getenv("DEEPSEEK_API_KEY") or dotenv_values(ROOT / ".env").get("DEEPSEEK_API_KEY"))
    if not key_present and not args.dry_run:
        print("BLOCKED_PAID_AUTHORIZATION: existing DeepSeek key is not configured")
        return 2
    # The account-level Flash limit is 2500; this experiment deliberately uses
    # a small measured cap and never rotates keys.
    ledger = load_ledger(float(args.approved_cap_usd))
    ids = [item.strip() for item in args.task_ids.split(",") if item.strip()]
    requested_arms = [item.strip() for item in args.arms.split(",") if item.strip()]
    phases = [args.phase] if args.phase != "all" else ["functional", "clean", "attack"]
    for phase in phases:
        workers = args.parallel_episodes or (2 if phase == "functional" else 4)
        if phase == "functional":
            items = [(task_id, arm, "NATIVE_PACKET") for task_id in ids for arm in (requested_arms or ["SINGLE_AGENT", "MANTA_NATIVE"])]
        elif phase == "clean":
            items = [(ids[0], "MANTA_NATIVE", variant) for variant in sorted(VALID_VARIANTS)]
        else:
            # Attack execution is intentionally gated until a separate clean
            # manifest is written by the analysis step.
            print("NO_VALID_ATTACK_MANIFEST: run clean and review before attack")
            continue
        run_batch(items, ledger, workers=min(workers, max(1, args.model_max_inflight)), reserve=0.75,
                  max_seconds=args.max_seconds_per_run, dry_run=args.dry_run)
    write_json(LEDGER, ledger)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

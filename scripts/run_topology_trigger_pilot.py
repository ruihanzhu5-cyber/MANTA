"""Pilot 01: screen native WorkBench tasks for real MANTA topology mutations.

The historical files are read-only candidate evidence. Every listed pilot result
comes from a new DeepSeek call. The shared budget ledger lives outside worktrees.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK_ROOT = ROOT.parent
RESULTS = ROOT / "results" / "pilot01_topology_trigger"
ORIGINAL = Path(os.getenv("MANTA_ORIGINAL_REPO", r"C:\Users\larei\Documents\ChatGPT\manta"))
HISTORY = Path(os.getenv("MANTA_HISTORY_ROOT", r"D:\MANTA_DATA\experiments"))
LEDGER = Path(os.getenv("MANTA_PILOTS_BUDGET_LEDGER", str(WORK_ROOT / "manta_three_pilots_budget.json")))
BASE_MAIN_SHA = "7d557dc793221906a46a1f83d4e5888fcc5c28d2"
PRICE_SOURCE = "https://api-docs.deepseek.com/quick_start/pricing/"
TOTAL_CAP = 10.0
PILOT_CAP = 3.5
NEXT_RESERVE = 1.5
PRIORITY = [12, 16, 20, 28, 14, 17, 19, 21, 23, 24, 26, 6]


def save_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    temp.replace(path)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def upper_cost(token_in: int, token_out: int) -> float:
    return (token_in * 0.30 + token_out * 1.20) / 1_000_000


def history_candidates() -> list[dict]:
    candidates: dict[str, list[dict]] = {}
    pattern = "manta_dsflash_workbench6_20261005_2145_w*/workbench/self_evolved/*/run_*.metadata.json"
    for path in HISTORY.glob(pattern):
        try:
            metadata = json.loads(path.read_text(encoding="utf-8"))
            task_path = path.parent / "task.json"
            task = json.loads(task_path.read_text(encoding="utf-8"))
            task_id = str(task["task_id"])
            se = metadata.get("self_evolved") or {}
            versions = se.get("topology_spec_versions") or []
            audit = se.get("audit_reports") or []
            tool_calls = [
                call for interaction in metadata.get("interaction_logs") or []
                for call in interaction.get("tool_calls") or [] if isinstance(call, dict)
            ]
            email_reads = sum(
                str(call.get("tool_name") or call.get("name") or "").startswith("email.")
                for call in tool_calls
            )
            candidates.setdefault(task_id, []).append({
                "task_id": task_id,
                "task_prompt": task.get("prompt") or task.get("query") or "",
                "source_task": str(task_path),
                "source_task_sha256": sha256(task_path),
                "source_metadata": str(path),
                "source_metadata_sha256": sha256(path),
                "source_worker": int(re.search(r"_w(\d+)", str(path)).group(1)),
                "source_run": path.name.split(".")[0],
                "seed": int(metadata["seed"]),
                "historical_spec_versions": len(versions),
                "historical_repair_signals": sum(bool(r.get("repair_recommended")) for r in audit),
                "historical_email_calls": email_reads,
            })
        except (KeyError, ValueError, TypeError, OSError):
            continue
    selected = []
    for number in PRIORITY:
        task_id = f"multi_domain_{number}"
        runs = candidates.get(task_id, [])
        if not runs:
            continue
        selected.append(max(runs, key=lambda r: (
            r["historical_spec_versions"], r["historical_repair_signals"],
            r["historical_email_calls"], -r["seed"]
        )))
    return selected[:12]


def replace_one(content: str, pattern: str, replacement: str) -> str:
    updated, n = re.subn(pattern, replacement, content, count=1, flags=re.MULTILINE)
    if n != 1:
        raise RuntimeError(f"Expected one config match for {pattern}: {n}")
    return updated


def prepare() -> None:
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip() != BASE_MAIN_SHA:
        raise RuntimeError("Pilot 01 must be prepared from the frozen origin/main commit")
    tasks = history_candidates()
    if not tasks:
        raise RuntimeError("No historical WorkBench task records found")
    skill_source = ROOT / "config" / "topology_skill.md"
    skill_target = RESULTS / "frozen" / "topology_skill.md"
    skill_target.parent.mkdir(parents=True, exist_ok=True)
    skill_target.write_bytes(skill_source.read_bytes())
    for item in tasks:
        source = ORIGINAL / "config" / f"manta_deepseek_flash_workbench6_w{item['source_worker']}.toml"
        content = source.read_text(encoding="utf-8")
        content = replace_one(content, r'^output_dir = ".*"$', 'output_dir = "results/pilot01_topology_trigger/raw"')
        content = replace_one(content, r'^skill_path = ".*"$', f'skill_path = "{skill_target.as_posix()}"')
        if content.count("max_turns = 2") != 2:
            raise RuntimeError(f"Expected MAS and self_evolved max_turns in {source}")
        content = content.replace("max_turns = 2", "max_turns = 3")
        content = replace_one(content, r'^repair_budget = 1$', 'repair_budget = 2')
        content = replace_one(content, r'^\[workbench\]$', f'[workbench]\ndata_dir = "{(ORIGINAL / ".cache" / "workbench").as_posix()}"')
        config_path = RESULTS / "configs" / f"{item['task_id']}.toml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(content, encoding="utf-8")
        item["config"] = str(config_path)
        item["config_sha256"] = sha256(config_path)
        item["historical_config"] = str(source)
    manifest = {
        "base_main_sha": BASE_MAIN_SHA,
        "historical_source_branch": "research/context-topology-ablation",
        "historical_source_commit": "39bd22c56b7937a46f1984c668c49b457b168b6e",
        "model": "deepseek-flash",
        "temperature": 0,
        "thinking": "disabled",
        "max_turns": 3,
        "repair_budget": 2,
        "audit_mode": "hybrid",
        "evidence_handoff_enabled": False,
        "skill_update_batch_size": 0,
        "playbook_sha256": sha256(skill_target),
        "shared_budget_ledger": str(LEDGER),
        "price_source": PRICE_SOURCE,
        "candidate_rule": "12,16 first; email/calendar audit candidates next; then historical mutation candidates; max 12; no attack outcome used",
        "candidates": tasks,
    }
    save_json(RESULTS / "manifest.json", manifest)
    save_json(RESULTS / "historical_scan.json", tasks)
    print(f"Prepared {len(tasks)} offline candidates", flush=True)


def load_budget() -> dict:
    if LEDGER.exists():
        return json.loads(LEDGER.read_text(encoding="utf-8"))
    return {
        "cap_usd": TOTAL_CAP,
        "price_source": PRICE_SOURCE,
        "price_checked_date": "2026-10-16",
        "formula": "uncached peak: $0.30/M input + $1.20/M output",
        "actual_billed_usd": "unknown",
        "episodes": [],
        "inflight": [],
        "preflights": [],
        "invalid_attempts": [],
    }


def budget_spent(ledger: dict) -> float:
    return sum(float(x["cost_upper_usd"]) for x in ledger["episodes"] + ledger["preflights"]) + sum(
        float(x["reserve_usd"]) for x in ledger["inflight"]
    ) + sum(
        float(x["cost_upper_usd"]) + float(x.get("unknown_usage_reserve_usd", 0))
        for x in ledger.get("invalid_attempts", [])
    )


def result_dir(task_id: str) -> Path:
    experiment_id = f"pilot01_{task_id}"
    return RESULTS / "raw" / experiment_id / "workbench" / "P1_native" / task_id


def inspect(task_id: str, seed: int) -> dict:
    folder = result_dir(task_id)
    metadata_path = folder / "run_0.metadata.json"
    eval_path = folder / "run_0.eval.json"
    trace_path = folder / "run_0.trace.jsonl"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    evaluation = json.loads(eval_path.read_text(encoding="utf-8"))
    if metadata.get("error") or not (metadata.get("self_evolved") or {}).get("turn_control_records"):
        raise RuntimeError(f"Incomplete engine metadata for {task_id}: {metadata.get('error')}")
    if int(metadata["seed"]) != seed:
        raise RuntimeError(f"Seed mismatch for {task_id}")
    token_in = token_out = 0
    mock = False
    for line in trace_path.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        token_in += int(event.get("token_in") or 0)
        token_out += int(event.get("token_out") or 0)
        mock |= bool((event.get("payload") or {}).get("mock_used"))
    mock |= any(bool((x.get("llm") or {}).get("mock_used")) for x in metadata.get("interaction_logs") or [])
    if mock:
        raise RuntimeError(f"Mock observed in formal episode {task_id}")
    turns = (metadata.get("self_evolved") or {}).get("turn_control_records") or []
    return {
        "task_id": task_id,
        "seed": seed,
        "run_id": "run_0",
        "official_success": bool(evaluation.get("success")),
        "score": evaluation.get("score"),
        "unwanted_side_effects": (evaluation.get("details") or {}).get("unwanted_side_effects"),
        "needs_rerun": bool(metadata.get("needs_rerun")),
        "turns": len(turns),
        "audit_repair_recommended": any(bool(t.get("repair_recommended")) for t in turns),
        "controller_continued": any(not bool((t.get("termination_decision") or {}).get("should_stop", True)) for t in turns),
        "mutation_proposed": any(t.get("mutation_proposal") for t in turns),
        "mutation_applied": any(t.get("applied_mutation") for t in turns),
        "effective_structural_change": any(bool(t.get("effective_structural_change")) for t in turns),
        "effective_context_policy_change": any(bool(t.get("effective_context_policy_change")) for t in turns),
        "initial_agent_count": turns[0]["agent_count"] if turns else None,
        "final_agent_count": len((metadata.get("self_evolved") or {}).get("topology_spec_versions", [{}])[-1].get("agents", [])),
        "relay_generated": sum(len(t.get("relay_packets_generated") or []) for t in turns),
        "relay_receipts": sum(len(t.get("relay_packet_receipts") or []) for t in turns),
        "tool_calls": int(metadata.get("tool_calls_total") or 0),
        "token_in": token_in,
        "token_out": token_out,
        "cost_upper_usd": round(upper_cost(token_in, token_out), 6),
        "trace_path": str(trace_path),
        "trace_sha256": sha256(trace_path),
        "metadata_path": str(metadata_path),
        "metadata_sha256": sha256(metadata_path),
        "evaluation_path": str(eval_path),
        "evaluation_sha256": sha256(eval_path),
    }


def run() -> None:
    manifest = json.loads((RESULTS / "manifest.json").read_text(encoding="utf-8"))
    from dotenv import dotenv_values
    from openai import OpenAI

    secret = os.getenv("DEEPSEEK_API_KEY") or dotenv_values(ORIGINAL / ".env").get("DEEPSEEK_API_KEY")
    if not secret:
        raise RuntimeError("DEEPSEEK_API_KEY missing; no mock fallback")
    ledger = load_budget()
    if not any(x.get("pilot") == "pilot01" for x in ledger["preflights"]):
        if budget_spent(ledger) + 0.01 > TOTAL_CAP:
            raise RuntimeError("Shared budget exhausted before preflight")
        response = OpenAI(api_key=secret, base_url="https://api.deepseek.com", timeout=60).chat.completions.create(
            model="deepseek-flash", messages=[{"role": "user", "content": "Reply OK."}],
            temperature=0, max_tokens=8, extra_body={"thinking": {"type": "disabled"}},
        )
        usage = response.usage
        item = {"pilot": "pilot01", "token_in": int(usage.prompt_tokens or 0),
                "token_out": int(usage.completion_tokens or 0)}
        item["cost_upper_usd"] = upper_cost(item["token_in"], item["token_out"])
        ledger["preflights"].append(item)
        save_json(LEDGER, ledger)
    env = os.environ.copy()
    env["DEEPSEEK_API_KEY"] = secret
    env["MAS_REQUIRE_LIVE_LLM"] = "1"
    env["DEEPSEEK_THINKING"] = "disabled"
    env["OPENROUTER_TEMPERATURE"] = "0"
    env.pop("MAS_DISABLE_LIVE_LLM", None)
    for candidate in manifest["candidates"]:
        task_id = candidate["task_id"]
        if any(x.get("pilot") == "pilot01" and x.get("task_id") == task_id for x in ledger["episodes"]):
            continue
        pilot_spent = sum(float(x["cost_upper_usd"]) for x in ledger["episodes"] if x.get("pilot") == "pilot01")
        pilot_spent += sum(
            float(x["cost_upper_usd"]) + float(x.get("unknown_usage_reserve_usd", 0))
            for x in ledger.get("invalid_attempts", []) if x.get("pilot") == "pilot01"
        )
        if budget_spent(ledger) + NEXT_RESERVE > TOTAL_CAP or pilot_spent + NEXT_RESERVE > PILOT_CAP:
            print(f"Budget guard stopped before {task_id}", flush=True)
            break
        inflight = {"pilot": "pilot01", "task_id": task_id, "reserve_usd": NEXT_RESERVE,
                    "started_utc": datetime.now(UTC).isoformat()}
        ledger["inflight"].append(inflight)
        save_json(LEDGER, ledger)
        cmd = [sys.executable, "main.py", "run", "--config", candidate["config"],
               "--benchmark", "workbench", "--task-ids", task_id,
               "--runs-per-task", "1", "--seed", str(candidate["seed"]),
               "--output-dir", str(RESULTS / "raw"), "--output-layout", "hierarchical",
               "--experiment-id", f"pilot01_{task_id}", "--system-label", "P1_native"]
        log = RESULTS / "logs" / f"{task_id}.runner.log"
        log.parent.mkdir(parents=True, exist_ok=True)
        print(f"Starting real Pilot 01 {task_id}", flush=True)
        with log.open("w", encoding="utf-8") as handle:
            process = subprocess.run(cmd, cwd=ROOT, env=env, stdout=handle, stderr=subprocess.STDOUT)
        if process.returncode not in (0, 2):
            print(f"Episode stopped exit={process.returncode}; retained reserve and log {log}", flush=True)
            break
        try:
            result = inspect(task_id, candidate["seed"])
        except Exception as exc:
            print(f"Saved episode inspection failed: {exc}; retained reserve", flush=True)
            break
        result.update({"pilot": "pilot01", "pipeline_exit_code": process.returncode,
                       "runner_log": str(log), "runner_log_sha256": sha256(log)})
        ledger["inflight"].remove(inflight)
        ledger["episodes"].append(result)
        save_json(LEDGER, ledger)
        print(f"Finished {task_id}: mutation={result['effective_structural_change']} "
              f"score={result['score']} upper=${result['cost_upper_usd']:.4f}", flush=True)
        if sum(bool(x.get("effective_structural_change")) for x in ledger["episodes"] if x.get("pilot") == "pilot01") >= 3:
            break
    print("Pilot 01 run loop finished", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["prepare", "run"])
    args = parser.parse_args()
    {"prepare": prepare, "run": run}[args.command]()

"""Run frozen native WorkBench mixed-handoff arms with a shared cost guard."""

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
WORK = ROOT.parent
RESULTS = ROOT / "results/pilot07_mixed_handoff"
P1 = WORK / "manta-pilot01"
ORIGINAL = Path(r"C:\Users\larei\Documents\ChatGPT\manta")
LEDGER = WORK / "manta_three_pilots_budget.json"
BASE_MAIN_SHA = "7d557dc793221906a46a1f83d4e5888fcc5c28d2"
ARMS = {
    "A0_fixed_clean": (False, False),
    "A1_adaptive_clean": (True, False),
    "A2_fixed_mixed": (False, True),
    "A3_adaptive_mixed": (True, True),
}
PILOT_CAP = 4.5
ITERATION_CAP = 7.5
NEXT_RESERVE = 0.5


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n",
                         encoding="utf-8")
    temporary.replace(path)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def upper_cost(token_in: int, token_out: int) -> float:
    return (token_in * 0.30 + token_out * 1.20) / 1_000_000


def shared_guard(ledger: dict) -> float:
    return (
        sum(float(x.get("cost_upper_usd", 0)) for x in
            ledger.get("episodes", []) + ledger.get("preflights", []))
        + sum(float(x.get("cost_upper_usd", 0)) +
              float(x.get("unknown_usage_reserve_usd", 0))
              for x in ledger.get("invalid_attempts", []))
        + sum(float(x.get("reserve_usd", 0)) for x in ledger.get("inflight", []))
    )


def iteration_guard(ledger: dict) -> float:
    pilots = {"pilot07", "pilot08", "pilot09"}
    return (
        sum(float(x.get("cost_upper_usd", 0)) for x in
            ledger.get("episodes", []) + ledger.get("preflights", [])
            if x.get("pilot") in pilots)
        + sum(float(x.get("cost_upper_usd", 0)) +
              float(x.get("unknown_usage_reserve_usd", 0))
              for x in ledger.get("invalid_attempts", []) if x.get("pilot") in pilots)
        + sum(float(x.get("reserve_usd", 0)) for x in ledger.get("inflight", [])
              if x.get("pilot") in pilots)
    )


def pilot_guard(ledger: dict) -> float:
    return (
        sum(float(x.get("cost_upper_usd", 0)) for x in ledger.get("episodes", [])
            if x.get("pilot") == "pilot07")
        + sum(float(x.get("reserve_usd", 0)) for x in ledger.get("inflight", [])
              if x.get("pilot") == "pilot07")
    )


def replace_key(text: str, key: str, value: str) -> str:
    updated, count = re.subn(
        rf"(?m)^{re.escape(key)} = .*?$", lambda _: f"{key} = {value}", text, count=1
    )
    if count != 1:
        raise RuntimeError(f"Missing source config key {key}")
    return updated


def prepare() -> None:
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip() != BASE_MAIN_SHA:
        raise RuntimeError("Prepare Pilot 07 on frozen main before first commit")
    manifest_path = RESULTS / "manifest.json"
    manifest = load(manifest_path)
    cases_path = RESULTS / "selected_cases.json"
    contracts_path = RESULTS / "evidence_contracts.json"
    if file_hash(cases_path) != manifest["selected_cases_sha256"] or \
            file_hash(contracts_path) != manifest["evidence_contracts_sha256"]:
        raise RuntimeError("Frozen selected cases or Evidence Contracts changed")
    cases = load(cases_path)["selected"]
    skill_source = P1 / "results/pilot01_topology_trigger/frozen/topology_skill.md"
    skill_target = RESULTS / "frozen/topology_skill.md"
    skill_target.write_bytes(skill_source.read_bytes())
    template = (P1 / "results/pilot01_topology_trigger/configs/multi_domain_17.toml").read_text(
        encoding="utf-8")
    for case in cases:
        case["configs"] = {}
        for arm, (adaptive, mixed) in ARMS.items():
            text = replace_key(template, "output_dir", json.dumps(str(RESULTS / "raw")))
            text = replace_key(text, "skill_path", json.dumps(str(skill_target)))
            text = text.replace("[self_evolved]\n", "[self_evolved]\n"
                f"allow_topology_mutation = {str(adaptive).lower()}\n"
                f"allow_context_policy_mutation = {str(adaptive).lower()}\n"
                f"frozen_initial_spec_path = {json.dumps(case['frozen_spec_path'])}\n"
                + (f"artifact_intervention_path = {json.dumps(case['payload_path'])}\n"
                   if mixed else ""), 1)
            config_path = RESULTS / "configs" / case["task_id"] / f"{arm}.toml"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(text, encoding="utf-8")
            case["configs"][arm] = str(config_path)
    save(cases_path, {"selected": cases, "excluded": load(cases_path)["excluded"]})
    manifest.update({
        "selected_cases_sha256": file_hash(cases_path),
        "playbook_sha256": file_hash(skill_target),
        "model": "deepseek-flash", "temperature": 0, "thinking": "disabled",
        "max_turns": 3, "repair_budget": 2,
        "arms": ARMS, "shared_budget_ledger": str(LEDGER),
        "cost_guard": {"total_cap_usd": 10.0, "iteration_cap_usd": ITERATION_CAP,
                       "pilot07_cap_usd": PILOT_CAP, "next_request_reserve_usd": NEXT_RESERVE},
        "status": "FROZEN_READY",
    })
    save(manifest_path, manifest)
    print(f"Prepared {len(cases)} independent cases × {len(ARMS)} arms")


def output_folder(task_id: str, arm: str) -> Path:
    return RESULTS / "raw" / f"pilot07_{task_id}_{arm}" / "workbench" / arm / task_id


def inspect(case: dict, arm: str) -> dict:
    folder = output_folder(case["task_id"], arm)
    metadata_path = folder / "run_0.metadata.json"
    trace_path = folder / "run_0.trace.jsonl"
    eval_path = folder / "run_0.eval.json"
    metadata, evaluation = load(metadata_path), load(eval_path)
    if metadata.get("error") or int(metadata.get("seed", -1)) != case["seed"]:
        raise RuntimeError("Incomplete or seed-mismatched run")
    events = [json.loads(line) for line in trace_path.read_text(encoding="utf-8").splitlines()]
    if any((e.get("payload") or {}).get("mock_used") for e in events):
        raise RuntimeError("Mock trace cannot enter real results")
    token_in = sum(int(e.get("token_in") or 0) for e in events)
    token_out = sum(int(e.get("token_out") or 0) for e in events)
    interventions = metadata.get("artifact_intervention_events") or []
    applied = [x for x in interventions if x.get("applied")]
    if len(applied) > 1 or (not ARMS[arm][1] and interventions):
        raise RuntimeError("Unexpected intervention cardinality or clean-arm event")
    turns = (metadata.get("self_evolved") or {}).get("turn_control_records") or []
    effective = any(bool(x.get("effective_structural_change")) for x in turns)
    if not ARMS[arm][0] and effective:
        raise RuntimeError("Fixed arm mutated")
    initial = (metadata.get("self_evolved") or {}).get("topology_spec_versions", [None])[0]
    expected = load(Path(case["frozen_spec_path"]))["topology_spec"]
    if initial != expected:
        raise RuntimeError("Initial topology differs from frozen source")
    return {
        "pilot": "pilot07", "task_id": case["task_id"], "arm": arm,
        "seed": case["seed"], "run_id": "run_0", "status": "RECORDED",
        "intervention_applied": bool(applied),
        "intervention_events": interventions,
        "effective_structural_change": effective,
        "official_task_success": bool(evaluation.get("success")),
        "unwanted_side_effects": (evaluation.get("details") or {}).get("unwanted_side_effects"),
        "tool_calls": int(metadata.get("tool_calls_total") or 0),
        "token_in": token_in, "token_out": token_out,
        "cost_upper_usd": round(upper_cost(token_in, token_out), 6),
        "metadata_path": str(metadata_path), "metadata_sha256": file_hash(metadata_path),
        "trace_path": str(trace_path), "trace_sha256": file_hash(trace_path),
        "evaluation_path": str(eval_path), "evaluation_sha256": file_hash(eval_path),
    }


def run() -> None:
    from dotenv import dotenv_values

    manifest = load(RESULTS / "manifest.json")
    if manifest["status"] != "FROZEN_READY":
        raise RuntimeError("Pilot 07 is not frozen")
    cases = load(RESULTS / "selected_cases.json")["selected"]
    secret = os.getenv("DEEPSEEK_API_KEY") or dotenv_values(ORIGINAL / ".env").get("DEEPSEEK_API_KEY")
    if not secret:
        raise RuntimeError("DEEPSEEK_API_KEY missing; no mock fallback")
    env = os.environ.copy()
    env["DEEPSEEK_API_KEY"] = secret
    env["MAS_REQUIRE_LIVE_LLM"] = "1"
    env["DEEPSEEK_THINKING"] = "disabled"
    env["OPENROUTER_TEMPERATURE"] = "0"
    env.pop("MAS_DISABLE_LIVE_LLM", None)
    ledger = load(LEDGER)
    for case in cases:
        task_id = case["task_id"]
        for arm in ARMS:
            if any(x.get("pilot") == "pilot07" and x.get("task_id") == task_id and
                   x.get("arm") == arm for x in ledger.get("episodes", [])):
                continue
            if shared_guard(ledger) + NEXT_RESERVE > float(ledger["cap_usd"]) or \
                    iteration_guard(ledger) + NEXT_RESERVE > ITERATION_CAP or \
                    pilot_guard(ledger) + NEXT_RESERVE > PILOT_CAP:
                print(f"Budget guard stopped before {task_id}/{arm}", flush=True)
                return
            inflight = {"pilot": "pilot07", "task_id": task_id, "arm": arm,
                        "reserve_usd": NEXT_RESERVE, "started_utc": datetime.now(UTC).isoformat()}
            ledger.setdefault("inflight", []).append(inflight)
            save(LEDGER, ledger)
            command = [sys.executable, "main.py", "run", "--config", case["configs"][arm],
                       "--benchmark", "workbench", "--task-ids", task_id,
                       "--runs-per-task", "1", "--seed", str(case["seed"]),
                       "--output-dir", str(RESULTS / "raw"),
                       "--output-layout", "hierarchical",
                       "--experiment-id", f"pilot07_{task_id}_{arm}", "--system-label", arm]
            log = RESULTS / "logs" / f"{task_id}_{arm}.runner.log"
            log.parent.mkdir(parents=True, exist_ok=True)
            print(f"Starting real {task_id}/{arm}", flush=True)
            with log.open("w", encoding="utf-8") as handle:
                process = subprocess.run(command, cwd=ROOT, env=env,
                                         stdout=handle, stderr=subprocess.STDOUT)
            if process.returncode not in (0, 2):
                print(f"Runner failed exit={process.returncode}; reserve retained: {log}", flush=True)
                return
            try:
                episode = inspect(case, arm)
            except Exception as exc:
                print(f"Invalid saved run; reserve retained: {exc}", flush=True)
                return
            episode.update({"runner_log": str(log), "runner_log_sha256": file_hash(log),
                            "pipeline_exit_code": process.returncode})
            ledger["inflight"].remove(inflight)
            ledger.setdefault("episodes", []).append(episode)
            save(LEDGER, ledger)
            print(f"Finished {task_id}/{arm}: intervention={episode['intervention_applied']} "
                  f"mutation={episode['effective_structural_change']} "
                  f"upper=${episode['cost_upper_usd']:.4f}", flush=True)
        if task_id == cases[0]["task_id"]:
            first = [x for x in ledger["episodes"] if x.get("pilot") == "pilot07" and
                     x.get("task_id") == task_id and x.get("arm") in
                     {"A2_fixed_mixed", "A3_adaptive_mixed"}]
            if len(first) < 2 or not any(x.get("intervention_applied") for x in first):
                print("First four-arm pilot had no verified Artifact intervention; stopping", flush=True)
                return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["prepare", "run"])
    {"prepare": prepare, "run": run}[parser.parse_args().command]()

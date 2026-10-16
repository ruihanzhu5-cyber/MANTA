"""Pilot 05: native WorkBench CRM/PM IPI on Pilot 04 frozen surfaces."""

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
sys.path.insert(0, str(ROOT))
WORK_ROOT = ROOT.parent
P1 = WORK_ROOT / "manta-pilot01"
P4 = WORK_ROOT / "manta-pilot04"
RESULTS = ROOT / "results" / "pilot05_native_ipi"
LEDGER = Path(os.getenv("MANTA_PILOTS_BUDGET_LEDGER", str(WORK_ROOT / "manta_three_pilots_budget.json")))
ORIGINAL = Path(os.getenv("MANTA_ORIGINAL_REPO", r"C:\Users\larei\Documents\ChatGPT\manta"))
BASE_MAIN_SHA = "7d557dc793221906a46a1f83d4e5888fcc5c28d2"
PRICE_SOURCE = "https://api-docs.deepseek.com/quick_start/pricing/"
ARMS = {
    "E0_fixed_clean": (False, False),
    "E1_adaptive_clean": (True, False),
    "E2_fixed_attack": (False, True),
    "E3_adaptive_attack": (True, True),
}
TOTAL_CAP = 10.0
NEW_ITERATION_CAP = 4.0
PILOT_CAP = 3.0
NEXT_RESERVE = 0.5


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    temp.replace(path)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def upper_cost(token_in: int, token_out: int) -> float:
    return (token_in * 0.30 + token_out * 1.20) / 1_000_000


def replace_key(text: str, key: str, value: str, *, quoted: bool = False) -> str:
    rendered = f'{key} = "{value}"' if quoted else f"{key} = {value}"
    updated, count = re.subn(rf"(?m)^{re.escape(key)} = .*?$", lambda _: rendered, text, count=1)
    if count != 1:
        raise RuntimeError(f"Expected one {key} in source config")
    return updated


def write_config(item: dict, arm: str) -> Path:
    dynamic, attack = ARMS[arm]
    text = Path(item["source_config"]).read_text(encoding="utf-8")
    text = replace_key(text, "output_dir", (RESULTS / "raw").as_posix(), quoted=True)
    text = replace_key(text, "skill_path", (RESULTS / "frozen" / "topology_skill.md").as_posix(), quoted=True)
    text = text.replace("[self_evolved]\n", "[self_evolved]\n"
                        f'allow_topology_mutation = {str(dynamic).lower()}\n'
                        f'allow_context_policy_mutation = {str(dynamic).lower()}\n'
                        f'frozen_initial_spec_path = "{(RESULTS / "frozen" / (item["task_id"] + ".json")).as_posix()}"\n', 1)
    text = text.replace("[workbench]\n", "[workbench]\n"
                        f'ipi_enabled = {str(attack).lower()}\n'
                        'ipi_surface = "low_trust_text"\n'
                        f'ipi_target_tool_name = "{item["target_tool_name"]}"\n'
                        f'ipi_target_entity_id = "{item["target_entity_id"]}"\n'
                        f'ipi_target_text_field = "{item["target_text_field"]}"\n'
                        'ipi_payload_id = "IPI_FALSE_COMPLETION_02"\n'
                        f'ipi_target_agent_id = "{item["target_agent_id"]}"\n'
                        f'ipi_run_id = "{item["task_id"]}/{arm}/run_0"\n', 1)
    path = RESULTS / "configs" / item["task_id"] / f"{arm}.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def prepare_pilot05() -> None:
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip() != BASE_MAIN_SHA:
        raise RuntimeError("Pilot 05 must be prepared from frozen origin/main")
    p4_path = P4 / "results" / "pilot04_workbench_surface" / "qualified_surfaces.json"
    p4_manifest_path = P4 / "results" / "pilot04_workbench_surface" / "manifest.json"
    p4_manifest = read_json(p4_manifest_path)
    if sha256(p4_path) != p4_manifest["qualified_surfaces_sha256"]:
        raise RuntimeError("Pilot 04 qualified surface source hash changed")
    p4_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=P4).decode().strip()
    p1_path = P1 / "results" / "pilot01_topology_trigger" / "qualified_cases.json"
    p1_cases = {c["task_id"]: c for c in read_json(p1_path).get("cases") or []}
    source = read_json(p4_path)
    skill_source = P1 / "results" / "pilot01_topology_trigger" / "frozen" / "topology_skill.md"
    skill_target = RESULTS / "frozen" / "topology_skill.md"
    skill_target.parent.mkdir(parents=True, exist_ok=True)
    skill_target.write_bytes(skill_source.read_bytes())
    selected = []
    excluded = []
    for surface in source.get("selected_in_pre_registered_order") or []:
        task_id = surface["task_id"]
        case = p1_cases.get(task_id)
        if not case or not surface.get("eligible"):
            excluded.append({"task_id": task_id, "reason": "NOT_IN_FROZEN_P1_P4_INTERSECTION"})
            continue
        meta_path = Path(case["source_metadata"])
        if sha256(meta_path) != case["source_metadata_sha256"]:
            raise RuntimeError(f"Pilot 01 metadata changed: {task_id}")
        item = {
            "task_id": task_id, "task_prompt": case["prompt"], "seed": int(case["seed"]),
            "target_tool_name": surface["tool_name"],
            "target_entity_id": surface["entity_id"],
            "target_text_field": surface["text_field"],
            "target_agent_id": surface["source_agent"],
            "source_metadata": str(meta_path),
            "source_metadata_sha256": sha256(meta_path),
            "source_config": str(P1 / "results" / "pilot01_topology_trigger" / "configs" / f"{task_id}.toml"),
            "initial_spec_sha256": canonical_hash(case["initial_topology_spec"]),
            "pilot04_surface": surface,
        }
        frozen = {"task_id": task_id, "seed": item["seed"],
                  "topology_spec": case["initial_topology_spec"],
                  "topology_spec_sha256": item["initial_spec_sha256"],
                  "source_metadata": str(meta_path)}
        write_json(RESULTS / "frozen" / f"{task_id}.json", frozen)
        item["configs"] = {arm: str(write_config(item, arm)) for arm in ARMS}
        selected.append(item)
    from benchmark.workbench.injection import LOW_TRUST_PAYLOAD, LOW_TRUST_PAYLOAD_ID

    manifest = {
        "base_main_sha": BASE_MAIN_SHA,
        "pilot04_branch": "research/pilot04-workbench-text-surface",
        "pilot04_commit": p4_commit,
        "pilot04_qualified_sha256": sha256(p4_path),
        "pilot04_manifest_sha256": sha256(p4_manifest_path),
        "pilot01_commit": "68eae32e50a1eeab37df7b1296ae70fe5e5f5104",
        "pilot01_qualified_sha256": sha256(p1_path),
        "source_infrastructure": [
            {"commit": "90bace138d7395833a5111acef7e05f28a13851f", "files": ["MAS/config.py", "MAS/llm.py", "MAS/self_evolved/engine.py", "MAS/self_evolved/spec.py", "benchmark/workbench/__init__.py", "benchmark/workbench/injection.py"]},
            {"commit": p4_commit, "files": ["results/pilot04_workbench_surface/qualified_surfaces.json"]},
        ],
        "model": "deepseek-flash", "temperature": 0, "thinking": "disabled",
        "max_turns": 3, "repair_budget": 2,
        "payload_id": LOW_TRUST_PAYLOAD_ID,
        "payload_sha256": hashlib.sha256(LOW_TRUST_PAYLOAD.encode()).hexdigest(),
        "payload_text": LOW_TRUST_PAYLOAD,
        "arms": ARMS, "playbook_sha256": sha256(skill_target),
        "shared_budget_ledger": str(LEDGER), "price_source": PRICE_SOURCE,
        "selection_rule": "Pilot04 actual nonempty Worker low-trust text exposure + received Coordinator relay before first write and native mutation; clean success not required",
        "selected": selected, "excluded": excluded,
        "status": "READY" if selected else "BLOCKED_BY_EXPERIMENTAL_PRECONDITION",
    }
    write_json(RESULTS / "manifest.json", manifest)
    print(f"Prepared Pilot 05: selected={len(selected)}, excluded={len(excluded)}, status={manifest['status']}")


def shared_spent(ledger: dict) -> float:
    return (
        sum(float(x["cost_upper_usd"]) for x in ledger.get("episodes", []) + ledger.get("preflights", []))
        + sum(float(x.get("reserve_usd", 0)) for x in ledger.get("inflight", []))
        + sum(float(x.get("cost_upper_usd", 0)) + float(x.get("unknown_usage_reserve_usd", 0))
              for x in ledger.get("invalid_attempts", []))
    )


def iteration_spent(ledger: dict) -> float:
    paid = ledger.get("episodes", []) + ledger.get("preflights", [])
    invalid = ledger.get("invalid_attempts", [])
    inflight = ledger.get("inflight", [])
    return (sum(float(x.get("cost_upper_usd", 0)) for x in paid if x.get("pilot") in {"pilot05", "pilot06"})
            + sum(float(x.get("cost_upper_usd", 0)) + float(x.get("unknown_usage_reserve_usd", 0)) for x in invalid if x.get("pilot") in {"pilot05", "pilot06"})
            + sum(float(x.get("reserve_usd", 0)) for x in inflight if x.get("pilot") in {"pilot05", "pilot06"}))


def result_dir(task_id: str, arm: str) -> Path:
    return RESULTS / "raw" / f"pilot05_{task_id}_{arm}" / "workbench" / arm / task_id


def inspect(item: dict, arm: str) -> dict:
    folder = result_dir(item["task_id"], arm)
    meta_path = folder / "run_0.metadata.json"
    eval_path = folder / "run_0.eval.json"
    trace_path = folder / "run_0.trace.jsonl"
    metadata, evaluation = read_json(meta_path), read_json(eval_path)
    if metadata.get("error") or int(metadata.get("seed", -1)) != item["seed"]:
        raise RuntimeError(f"Incomplete or seed-mismatched run: {item['task_id']} {arm}")
    initial = metadata["self_evolved"]["topology_spec_versions"][0]
    if canonical_hash(initial) != item["initial_spec_sha256"]:
        raise RuntimeError(f"Frozen initial topology mismatch: {item['task_id']} {arm}")
    events = [json.loads(line) for line in trace_path.read_text(encoding="utf-8").splitlines()]
    if any((event.get("payload") or {}).get("mock_used") for event in events) or any(
        (log.get("llm") or {}).get("mock_used") for log in metadata.get("interaction_logs") or []
    ):
        raise RuntimeError("Mock result in real experiment")
    token_in = sum(int(e.get("token_in") or 0) for e in events)
    token_out = sum(int(e.get("token_out") or 0) for e in events)
    applied = [event for event in metadata.get("injection_events") or [] if event.get("injection_applied")]
    if len(applied) > 1 or (not ARMS[arm][1] and applied):
        raise RuntimeError("Injection cardinality or clean-arm violation")
    turns = metadata["self_evolved"].get("turn_control_records") or []
    effective = any(bool(t.get("effective_structural_change")) for t in turns)
    if not ARMS[arm][0] and effective:
        raise RuntimeError("Fixed arm had effective structural mutation")
    return {
        "pilot": "pilot05", "task_id": item["task_id"], "arm": arm, "seed": item["seed"],
        "official_task_success": bool(evaluation.get("success")), "score": evaluation.get("score"),
        "unwanted_side_effects": (evaluation.get("details") or {}).get("unwanted_side_effects"),
        "ground_truth": (evaluation.get("details") or {}).get("ground_truth"),
        "predicted_actions": (evaluation.get("details") or {}).get("prediction"),
        "needs_rerun": bool(metadata.get("needs_rerun")),
        "injection_applied": bool(applied), "injection_events": metadata.get("injection_events") or [],
        "attack_exposed": bool(applied),
        "target_tool_name": item["target_tool_name"],
        "target_entity_id": item["target_entity_id"],
        "target_text_field": item["target_text_field"],
        "effective_structural_change": effective,
        "agent_count": max(len(v.get("agents") or []) for v in metadata["self_evolved"].get("topology_spec_versions") or [{}]),
        "tool_calls": int(metadata.get("tool_calls_total") or 0),
        "token_in": token_in, "token_out": token_out,
        "cost_upper_usd": round(upper_cost(token_in, token_out), 6),
        "trace_path": str(trace_path), "trace_sha256": sha256(trace_path),
        "metadata_path": str(meta_path), "metadata_sha256": sha256(meta_path),
        "evaluation_path": str(eval_path), "evaluation_sha256": sha256(eval_path),
    }


def run() -> None:
    manifest = read_json(RESULTS / "manifest.json")
    if not manifest["selected"]:
        print("Pilot 02 blocked: no prequalified native IPI task; no paid request sent")
        return
    from dotenv import dotenv_values
    from openai import OpenAI

    secret = os.getenv("DEEPSEEK_API_KEY") or dotenv_values(ORIGINAL / ".env").get("DEEPSEEK_API_KEY")
    if not secret:
        raise RuntimeError("DEEPSEEK_API_KEY missing; no mock fallback")
    ledger = read_json(LEDGER)
    if not any(x.get("pilot") == "pilot05" for x in ledger.get("preflights", [])):
        if shared_spent(ledger) + 0.01 > TOTAL_CAP or iteration_spent(ledger) + 0.01 > NEW_ITERATION_CAP:
            raise RuntimeError("Shared budget exhausted")
        response = OpenAI(api_key=secret, base_url="https://api.deepseek.com", timeout=60).chat.completions.create(
            model="deepseek-flash", messages=[{"role": "user", "content": "Reply OK."}],
            temperature=0, max_tokens=8, extra_body={"thinking": {"type": "disabled"}},
        )
        usage = response.usage
        pre = {"pilot": "pilot05", "token_in": int(usage.prompt_tokens or 0),
               "token_out": int(usage.completion_tokens or 0)}
        pre["cost_upper_usd"] = upper_cost(pre["token_in"], pre["token_out"])
        ledger.setdefault("preflights", []).append(pre)
        write_json(LEDGER, ledger)
    env = os.environ.copy()
    env["DEEPSEEK_API_KEY"] = secret
    env["MAS_REQUIRE_LIVE_LLM"] = "1"
    env["DEEPSEEK_THINKING"] = "disabled"
    env["OPENROUTER_TEMPERATURE"] = "0"
    env.pop("MAS_DISABLE_LIVE_LLM", None)
    for item in manifest["selected"]:
        for arm in ARMS:
            task_id = item["task_id"]
            if any(x.get("pilot") == "pilot05" and x.get("task_id") == task_id and x.get("arm") == arm for x in ledger.get("episodes", [])):
                continue
            pilot_spent = sum(float(x["cost_upper_usd"]) for x in ledger.get("episodes", []) if x.get("pilot") == "pilot05")
            if (shared_spent(ledger) + NEXT_RESERVE > TOTAL_CAP or
                    iteration_spent(ledger) + NEXT_RESERVE > NEW_ITERATION_CAP or
                    pilot_spent + NEXT_RESERVE > PILOT_CAP):
                print(f"Budget guard stopped before {task_id} {arm}")
                return
            inflight = {"pilot": "pilot05", "task_id": task_id, "arm": arm,
                        "reserve_usd": NEXT_RESERVE, "started_utc": datetime.now(UTC).isoformat()}
            ledger.setdefault("inflight", []).append(inflight)
            write_json(LEDGER, ledger)
            command = [sys.executable, "main.py", "run", "--config", item["configs"][arm],
                       "--benchmark", "workbench", "--task-ids", task_id, "--runs-per-task", "1",
                       "--seed", str(item["seed"]), "--output-dir", str(RESULTS / "raw"),
                       "--output-layout", "hierarchical", "--experiment-id", f"pilot05_{task_id}_{arm}",
                       "--system-label", arm]
            log = RESULTS / "logs" / f"{task_id}_{arm}.runner.log"
            log.parent.mkdir(parents=True, exist_ok=True)
            print(f"Starting real Pilot 05 {task_id} {arm}", flush=True)
            with log.open("w", encoding="utf-8") as handle:
                process = subprocess.run(command, cwd=ROOT, env=env, stdout=handle, stderr=subprocess.STDOUT)
            if process.returncode not in (0, 2):
                print(f"Pipeline stopped exit={process.returncode}; reserve retained: {log}", flush=True)
                return
            try:
                episode = inspect(item, arm)
            except Exception as exc:
                print(f"Saved run invalid; reserve retained: {exc}", flush=True)
                return
            episode.update({"runner_log": str(log), "runner_log_sha256": sha256(log),
                            "pipeline_exit_code": process.returncode})
            ledger["inflight"].remove(inflight)
            ledger["episodes"].append(episode)
            write_json(LEDGER, ledger)
            print(f"Finished {task_id} {arm}: exposure={episode['injection_applied']} "
                  f"mutation={episode['effective_structural_change']} upper=${episode['cost_upper_usd']:.4f}", flush=True)
        attack_rows = [x for x in ledger.get("episodes", []) if x.get("pilot") == "pilot05"
                       and x.get("task_id") == task_id and x.get("arm") in {"E2_fixed_attack", "E3_adaptive_attack"}]
        if len(attack_rows) < 2 or not any(x.get("injection_applied") for x in attack_rows):
            print(f"First four-arm task has no verified injection; stopping before next task: {task_id}", flush=True)
            return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["prepare", "run"])
    args = parser.parse_args()
    {"prepare": prepare_pilot05, "run": run}[args.command]()

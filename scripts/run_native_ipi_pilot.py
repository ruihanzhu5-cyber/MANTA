"""Pilot 02: native adaptive WorkBench IPI comparison on Pilot 01 cases.

No paid calls are made unless a previously qualified mutation task also has a
verified pre-write Worker email-body read and downstream relay.
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
sys.path.insert(0, str(ROOT))
WORK_ROOT = ROOT.parent
P1 = WORK_ROOT / "manta-pilot01"
RESULTS = ROOT / "results" / "pilot02_native_ipi"
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
PILOT_CAP = 6.0
NEXT_RESERVE = 1.5


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


def worker_body_reads(metadata: dict) -> list[tuple[str, str, int]]:
    """Actual Worker read and legal relay, cross-checked with interaction logs."""
    relays = {
        (p.get("sender"), p.get("artifact_id")): p
        for p in metadata.get("relay_messages") or []
        if p.get("sender") != "agent_0" and "agent_0" in (p.get("recipients") or [])
    }
    result: list[tuple[str, str, int]] = []
    for artifact in metadata.get("artifact_records") or []:
        agent = str(artifact.get("agent_id") or "")
        relay = relays.get((agent, artifact.get("artifact_id")))
        if not relay:
            continue
        for call in artifact.get("tool_records") or []:
            name, output = call.get("tool_name"), call.get("output")
            ids = []
            if name == "email.search_emails" and isinstance(output, list):
                ids = [str(mail["email_id"]) for mail in output if isinstance(mail, dict)
                       and mail.get("email_id") and str(mail.get("body") or "").strip()]
            elif name == "email.get_email_information_by_id" and call.get("arguments", {}).get("field") == "body" and isinstance(output, dict) and str(output.get("body") or "").strip():
                ids = [str(call.get("arguments", {}).get("email_id") or "")]
            for email_id in ids:
                if email_id and email_id in str(relay.get("content") or ""):
                    result.append((email_id, agent, int(artifact.get("dispatch_id") or 0)))
    for log in metadata.get("interaction_logs") or []:
        agent = str(log.get("agent_id") or "")
        if not agent or agent == "agent_0":
            continue
        artifact = next((a for a in metadata.get("artifact_records") or []
                         if a.get("agent_id") == agent and a.get("dispatch_id") == log.get("dispatch_id")), None)
        if artifact is None or (agent, artifact.get("artifact_id")) not in relays:
            continue
        relay = relays[(agent, artifact.get("artifact_id"))]
        for call in log.get("tool_calls") or []:
            name = call.get("tool_name")
            preview = str(call.get("output_preview") or "")
            ids = []
            if name == "email.search_emails" and re.search(r'"body"\s*:\s*"[^" ]', preview):
                ids = re.findall(r'"email_id"\s*:\s*"([^"]+)"', preview)
            elif name == "email.get_email_information_by_id" and call.get("arguments", {}).get("field") == "body" and re.search(r'"body"\s*:\s*"[^" ]', preview):
                ids = [str(call.get("arguments", {}).get("email_id") or "")]
            for email_id in ids:
                if email_id and email_id in str(relay.get("content") or ""):
                    result.append((email_id, agent, int(log.get("dispatch_id") or 0)))
    return list(dict.fromkeys(result))


def eligible_target(case: dict, metadata: dict) -> tuple[str, str] | None:
    from benchmark.workbench import SIDE_EFFECT_TOOLS

    if not case.get("official_success") or not case.get("strict_valid"):
        return None
    write_dispatches = [
        int(log.get("dispatch_id") or 0)
        for log in metadata.get("interaction_logs") or []
        if any(call.get("tool_name") in SIDE_EFFECT_TOOLS for call in log.get("tool_calls") or [])
    ]
    if not write_dispatches:
        return None
    first_write = min(write_dispatches)
    for email_id, agent, dispatch in worker_body_reads(metadata):
        if dispatch < first_write:
            return email_id, agent
    return None


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
                        f'ipi_target_email_id = "{item["target_email_id"]}"\n'
                        f'ipi_target_agent_id = "{item["target_agent_id"]}"\n'
                        f'ipi_run_id = "{item["task_id"]}/{arm}/run_0"\n', 1)
    path = RESULTS / "configs" / item["task_id"] / f"{arm}.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def prepare() -> None:
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip() != BASE_MAIN_SHA:
        raise RuntimeError("Pilot 02 must be prepared from frozen origin/main")
    p1_cases = P1 / "results" / "pilot01_topology_trigger" / "qualified_cases.json"
    if not p1_cases.is_file():
        raise RuntimeError("Pilot 01 qualified_cases.json is missing")
    p1_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=P1).decode().strip()
    cases = read_json(p1_cases).get("cases") or []
    skill_source = P1 / "results" / "pilot01_topology_trigger" / "frozen" / "topology_skill.md"
    skill_target = RESULTS / "frozen" / "topology_skill.md"
    skill_target.parent.mkdir(parents=True, exist_ok=True)
    skill_target.write_bytes(skill_source.read_bytes())
    selected = []
    excluded = []
    for case in cases:
        task_id = case["task_id"]
        meta_path = Path(case["source_metadata"])
        if not meta_path.is_file() or sha256(meta_path) != case["source_metadata_sha256"]:
            raise RuntimeError(f"Pilot 01 source changed: {task_id}")
        metadata = read_json(meta_path)
        target = eligible_target(case, metadata)
        if target is None:
            excluded.append({"task_id": task_id, "reason": "no_successful_valid_prewrite_worker_email_body_handoff"})
            continue
        item = {"task_id": task_id, "task_prompt": case["prompt"], "seed": int(case["seed"]),
                "target_email_id": target[0], "target_agent_id": target[1],
                "source_metadata": str(meta_path), "source_metadata_sha256": sha256(meta_path),
                "source_config": str(P1 / "results" / "pilot01_topology_trigger" / "configs" / f"{task_id}.toml"),
                "initial_spec_sha256": canonical_hash(case["initial_topology_spec"])}
        frozen = {"task_id": task_id, "seed": item["seed"],
                  "topology_spec": case["initial_topology_spec"],
                  "topology_spec_sha256": item["initial_spec_sha256"],
                  "source_metadata": str(meta_path)}
        write_json(RESULTS / "frozen" / f"{task_id}.json", frozen)
        item["configs"] = {arm: str(write_config(item, arm)) for arm in ARMS}
        selected.append(item)
        if len(selected) == 3:
            break
    from benchmark.workbench.injection import PAYLOAD, PAYLOAD_ID

    manifest = {
        "base_main_sha": BASE_MAIN_SHA,
        "pilot01_branch": "research/pilot01-topology-trigger",
        "pilot01_commit": p1_commit,
        "qualified_cases_path": str(p1_cases),
        "qualified_cases_sha256": sha256(p1_cases),
        "source_infrastructure": [
            {"commit": "c82dc6852ca9255500b74c9622fc86d7fcf84ed6", "files": ["MAS/llm.py", "benchmark/workbench/__init__.py", "benchmark/workbench/injection.py"]},
            {"commit": "39bd22c56b7937a46f1984c668c49b457b168b6e", "files": ["MAS/self_evolved/spec.py#from_payload"]},
            {"commit": p1_commit, "files": ["MAS/self_evolved/engine.py#turn_control_records"]},
        ],
        "model": "deepseek-flash", "temperature": 0, "thinking": "disabled",
        "max_turns": 3, "repair_budget": 2, "payload_id": PAYLOAD_ID,
        "payload_sha256": hashlib.sha256(PAYLOAD.encode()).hexdigest(),
        "arms": ARMS, "playbook_sha256": sha256(skill_target),
        "shared_budget_ledger": str(LEDGER), "price_source": PRICE_SOURCE,
        "selection_rule": "Pilot01 real structural mutation + valid clean success + prewrite Worker email body read and actual Coordinator relay",
        "selected": selected, "excluded": excluded,
        "status": "READY" if selected else "BLOCKED_BY_EXPERIMENTAL_PRECONDITION",
    }
    write_json(RESULTS / "manifest.json", manifest)
    print(f"Prepared Pilot 02: selected={len(selected)}, excluded={len(excluded)}, status={manifest['status']}")


def shared_spent(ledger: dict) -> float:
    return (
        sum(float(x["cost_upper_usd"]) for x in ledger.get("episodes", []) + ledger.get("preflights", []))
        + sum(float(x.get("reserve_usd", 0)) for x in ledger.get("inflight", []))
        + sum(float(x.get("cost_upper_usd", 0)) + float(x.get("unknown_usage_reserve_usd", 0))
              for x in ledger.get("invalid_attempts", []))
    )


def result_dir(task_id: str, arm: str) -> Path:
    return RESULTS / "raw" / f"pilot02_{task_id}_{arm}" / "workbench" / arm / task_id


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
        "pilot": "pilot02", "task_id": item["task_id"], "arm": arm, "seed": item["seed"],
        "official_task_success": bool(evaluation.get("success")), "score": evaluation.get("score"),
        "unwanted_side_effects": (evaluation.get("details") or {}).get("unwanted_side_effects"),
        "ground_truth": (evaluation.get("details") or {}).get("ground_truth"),
        "predicted_actions": (evaluation.get("details") or {}).get("prediction"),
        "needs_rerun": bool(metadata.get("needs_rerun")),
        "injection_applied": bool(applied), "injection_events": metadata.get("injection_events") or [],
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
    if not any(x.get("pilot") == "pilot02" for x in ledger.get("preflights", [])):
        if shared_spent(ledger) + 0.01 > TOTAL_CAP:
            raise RuntimeError("Shared budget exhausted")
        response = OpenAI(api_key=secret, base_url="https://api.deepseek.com", timeout=60).chat.completions.create(
            model="deepseek-flash", messages=[{"role": "user", "content": "Reply OK."}],
            temperature=0, max_tokens=8, extra_body={"thinking": {"type": "disabled"}},
        )
        usage = response.usage
        pre = {"pilot": "pilot02", "token_in": int(usage.prompt_tokens or 0),
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
            if any(x.get("pilot") == "pilot02" and x.get("task_id") == task_id and x.get("arm") == arm for x in ledger.get("episodes", [])):
                continue
            pilot_spent = sum(float(x["cost_upper_usd"]) for x in ledger.get("episodes", []) if x.get("pilot") == "pilot02")
            if shared_spent(ledger) + NEXT_RESERVE > TOTAL_CAP or pilot_spent + NEXT_RESERVE > PILOT_CAP:
                print(f"Budget guard stopped before {task_id} {arm}")
                return
            inflight = {"pilot": "pilot02", "task_id": task_id, "arm": arm,
                        "reserve_usd": NEXT_RESERVE, "started_utc": datetime.now(UTC).isoformat()}
            ledger.setdefault("inflight", []).append(inflight)
            write_json(LEDGER, ledger)
            command = [sys.executable, "main.py", "run", "--config", item["configs"][arm],
                       "--benchmark", "workbench", "--task-ids", task_id, "--runs-per-task", "1",
                       "--seed", str(item["seed"]), "--output-dir", str(RESULTS / "raw"),
                       "--output-layout", "hierarchical", "--experiment-id", f"pilot02_{task_id}_{arm}",
                       "--system-label", arm]
            log = RESULTS / "logs" / f"{task_id}_{arm}.runner.log"
            log.parent.mkdir(parents=True, exist_ok=True)
            print(f"Starting real Pilot 02 {task_id} {arm}", flush=True)
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["prepare", "run"])
    args = parser.parse_args()
    {"prepare": prepare, "run": run}[args.command]()

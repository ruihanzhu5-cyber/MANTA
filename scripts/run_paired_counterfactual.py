"""Capture one live native proposal, then restore KEEP and MUTATE from it."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pickle
import re
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from benchmark.workbench import WorkBenchBenchmark, WorkBenchSandbox
from MAS.self_evolved.artifact_intervention import ArtifactIntervention
from MAS.self_evolved.checkpoint import load_checkpoint, restore_checkpoint
from MAS.self_evolved.context import SharedContextController
from MAS.self_evolved.executor import TurnExecutor

WORK = ROOT.parent
P07 = WORK / "manta-pilot07/results/pilot07_mixed_handoff"
RESULTS = ROOT / "results/pilot08_counterfactual"
LEDGER = WORK / "manta_three_pilots_budget.json"
ORIGINAL = Path(r"C:\Users\larei\Documents\ChatGPT\manta")
BASE_MAIN_SHA = "7d557dc793221906a46a1f83d4e5888fcc5c28d2"
RESERVE = 0.5
PILOT_CAP = 2.0
ITERATION_CAP = 7.5
ARMS = ("CAPTURE", "KEEP", "MUTATE")


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


def cost_upper(token_in: int, token_out: int) -> float:
    return (token_in * 0.30 + token_out * 1.20) / 1_000_000


def guard(ledger: dict) -> bool:
    episodes = ledger.get("episodes", []) + ledger.get("preflights", [])
    invalid = ledger.get("invalid_attempts", [])
    inflight = ledger.get("inflight", [])
    spent = (sum(float(x.get("cost_upper_usd", 0)) for x in episodes)
             + sum(float(x.get("cost_upper_usd", 0)) + float(x.get("unknown_usage_reserve_usd", 0))
                   for x in invalid)
             + sum(float(x.get("reserve_usd", 0)) for x in inflight))
    iteration = (sum(float(x.get("cost_upper_usd", 0)) for x in episodes
                     if x.get("pilot") in {"pilot07", "pilot08", "pilot09"})
                 + sum(float(x.get("cost_upper_usd", 0)) + float(x.get("unknown_usage_reserve_usd", 0))
                       for x in invalid if x.get("pilot") in {"pilot07", "pilot08", "pilot09"})
                 + sum(float(x.get("reserve_usd", 0)) for x in inflight
                       if x.get("pilot") in {"pilot07", "pilot08", "pilot09"}))
    pilot = (sum(float(x.get("cost_upper_usd", 0)) for x in episodes if x.get("pilot") == "pilot08")
             + sum(float(x.get("cost_upper_usd", 0)) + float(x.get("unknown_usage_reserve_usd", 0))
                   for x in invalid if x.get("pilot") == "pilot08")
             + sum(float(x.get("reserve_usd", 0)) for x in inflight if x.get("pilot") == "pilot08"))
    return spent + RESERVE <= float(ledger["cap_usd"]) and iteration + RESERVE <= ITERATION_CAP and pilot + RESERVE <= PILOT_CAP


def logged_usage(log: Path) -> tuple[int, int]:
    content = log.read_text(encoding="utf-8", errors="replace")
    rows = re.findall(r"\[llm\] DONE[^\n]*token_in=(\d+) token_out=(\d+)", content)
    return sum(int(row[0]) for row in rows), sum(int(row[1]) for row in rows)


def validate_live_checkpoint(task_id: str) -> bool:
    checkpoint = RESULTS / "checkpoints" / f"{task_id}.pkl.gz"
    payload = load_checkpoint(checkpoint)
    extra = payload["extra"]
    if extra["task_id"] != task_id or extra["native_proposal"].mutation is None:
        raise RuntimeError("Live checkpoint task or native proposal invalid")
    if not payload["attack_intervention_state"] or not payload["attack_intervention_state"]["applied"]:
        raise RuntimeError("Live checkpoint lacks consumed mixed Artifact")
    copies = []
    for _ in range(2):
        sb = WorkBenchSandbox(Path(r"C:\Users\larei\Documents\ChatGPT\manta\.cache\workbench"))
        bench = WorkBenchBenchmark.__new__(WorkBenchBenchmark)
        bench.tool_selection = "domains"
        tools = bench._build_tools(sb, ["crm", "project_management"])
        context = SharedContextController(extra["topo_spec"])
        executor = TurnExecutor(object(), context)
        hook = ArtifactIntervention.from_path(RESULTS / "frozen" / f"{task_id}.payload.json")
        state = restore_checkpoint(payload, tools=tools, sandbox=sb,
                                   llm_client=object(), descriptor=object(),
                                   intervention=hook, executor=executor)
        copies.append((sb, executor, hook, state))
    (left_sb, left_ex, left_hook, left_state), (right_sb, right_ex, right_hook, right_state) = copies
    keys = ("messages", "message_views", "artifacts", "evidence_ledger",
            "context_digest_deliveries", "tool_records_log", "interaction_logs",
            "context_state_versions", "termination_history", "agent_type_by_agent",
            "message_budget", "sent_counts")
    state_hashes = {
        key: hashlib.sha256(pickle.dumps(left_state.get(key), protocol=5)).hexdigest()
        for key in keys
    }
    if any(pickle.dumps(left_state.get(key), protocol=5) !=
           pickle.dumps(right_state.get(key), protocol=5) for key in keys):
        raise RuntimeError("Restored native logical states differ")
    if left_ex.export_state() != right_ex.export_state() or not left_hook.applied or not right_hook.applied:
        raise RuntimeError("Dedupe or consumed attack state differs")
    if not all(left_sb.export_state()["frames"][name].equals(right_sb.export_state()["frames"][name])
               for name in WorkBenchSandbox.STATE_FRAMES):
        raise RuntimeError("WorkBench sandbox copies differ before fork")
    query = {"assigned_to_email": "anaya.patel@atlas.com"}
    if left_sb.invoke("project_management.search_tasks", query) != right_sb.invoke(
            "project_management.search_tasks", query):
        raise RuntimeError("Normal-factory WorkBench query differs after restore")
    before_right = right_sb.crm_data.copy(deep=True)
    left_sb.crm_data.loc[0, "status"] = "Lost"
    if not right_sb.crm_data.equals(before_right):
        raise RuntimeError("Restored WorkBench sandboxes are not independent")
    proposal_payload = extra["native_proposal"].to_payload()
    mutation_bytes = json.dumps(proposal_payload["mutation"], sort_keys=True,
                                ensure_ascii=False).encode("utf-8")
    mutation_sha = hashlib.sha256(mutation_bytes).hexdigest()
    validation = {
        "status": "LIVE_BOUNDARY_TWO_RESTORE_PASSED",
        "task_id": task_id, "checkpoint_path": str(checkpoint),
        "checkpoint_sha256": payload["checkpoint_sha256"],
        "mutation_sha256": mutation_sha, "turn_index": extra["turn_index"],
        "logical_state_hashes": state_hashes,
        "two_independent_sandboxes": True,
        "existing_tool_dedupe_state_equal": True,
        "attack_intervention_consumed_in_both": True,
        "pre_fork_messages_artifacts_context_and_history_equal": True,
        "normal_factory_tool_query_equal": True,
        "strict_boundary_continuation_validated": False,
    }
    save(RESULTS / "restore_validation.json", validation)
    save(RESULTS / "restore_validation" / f"{task_id}.json", validation)
    save(RESULTS / "checkpoint_manifest.json", {
        "task_id": task_id, "checkpoint_path": str(checkpoint),
        "checkpoint_sha256": payload["checkpoint_sha256"],
        "boundary": "Auditor_and_Planner_completed_before_native_apply",
        "turn_index": extra["turn_index"], "seed": extra["seed"],
        "mutation_sha256": mutation_sha,
    })
    save(RESULTS / "checkpoint_manifests" / f"{task_id}.json",
         load(RESULTS / "checkpoint_manifest.json"))
    save(RESULTS / "frozen_mutations.json", {
        "task_id": task_id, "mutation_sha256": mutation_sha,
        "native_proposal": proposal_payload,
        "original_topology": extra["topo_spec"].to_payload(),
    })
    save(RESULTS / "frozen_mutations" / f"{task_id}.json",
         load(RESULTS / "frozen_mutations.json"))
    return True


def prepare(task_id: str) -> dict:
    selected = {x["task_id"]: x for x in load(P07 / "selected_cases.json")["selected"]}
    if task_id not in selected:
        raise ValueError("Task is absent from the frozen Pilot 07 selection")
    case = selected[task_id]
    frozen = RESULTS / "frozen"
    frozen.mkdir(parents=True, exist_ok=True)
    copies = {}
    for source, target in (
        (P07 / "frozen" / f"{task_id}.json", frozen / f"{task_id}.json"),
        (P07 / "payloads" / f"{task_id}.json", frozen / f"{task_id}.payload.json"),
        (P07 / "frozen/topology_skill.md", frozen / "topology_skill.md"),
    ):
        shutil.copy2(source, target)
        copies[str(target)] = {"source": str(source), "source_sha256": file_hash(source),
                               "local_sha256": file_hash(target)}
    source_config = Path(case["configs"]["A3_adaptive_mixed"])
    config_text = source_config.read_text(encoding="utf-8")
    for old, new in (
        (str(P07 / "raw"), str(RESULTS / "raw")),
        (str(P07 / "frozen" / f"{task_id}.json"), str(frozen / f"{task_id}.json")),
        (str(P07 / "payloads" / f"{task_id}.json"), str(frozen / f"{task_id}.payload.json")),
        (str(P07 / "frozen/topology_skill.md"), str(frozen / "topology_skill.md")),
    ):
        old, new = json.dumps(old)[1:-1], json.dumps(new)[1:-1]
        if old not in config_text:
            raise ValueError(f"Pilot 07 config lacks frozen path: {old}")
        config_text = config_text.replace(old, new)
    config = RESULTS / "configs" / f"{task_id}.toml"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(config_text, encoding="utf-8")
    manifest = {
        "base_main_sha": BASE_MAIN_SHA, "pilot07_source_case": task_id,
        "pilot07_source_manifest_sha256": file_hash(P07 / "manifest.json"),
        "pilot07_source_contracts_sha256": file_hash(P07 / "evidence_contracts.json"),
        "frozen_files": copies, "config": str(config), "config_sha256": file_hash(config),
        "seed": case["seed"], "model": "deepseek-flash", "temperature": 0,
        "thinking": "disabled", "max_turns": 3, "repair_budget": 2,
        "checkpoint_boundary": "after_native_proposal_before_apply",
        "price_rule": "uncached peak input $0.30/M output $1.20/M",
    }
    save(RESULTS / "manifest.json", manifest)
    save(RESULTS / "manifests" / f"{task_id}.json", manifest)
    return manifest


def run_one(task_id: str, arm: str, manifest: dict) -> bool:
    ledger = load(LEDGER)
    if any(x.get("pilot") == "pilot08" and x.get("task_id") == task_id
           and x.get("arm") == arm for x in ledger.get("episodes", [])):
        return True
    if not guard(ledger):
        print(f"Budget guard stopped Pilot 08 before {task_id}/{arm}", flush=True)
        return False
    secret = os.getenv("DEEPSEEK_API_KEY") or dotenv_values(ORIGINAL / ".env").get("DEEPSEEK_API_KEY")
    if not secret:
        raise RuntimeError("Missing real DeepSeek key; no mock fallback")
    checkpoint = RESULTS / "checkpoints" / f"{task_id}.pkl.gz"
    if arm == "CAPTURE" and checkpoint.exists():
        raise RuntimeError("Unrecorded pre-existing checkpoint; refusing a stale fork")
    if arm != "CAPTURE" and not checkpoint.exists():
        raise RuntimeError("KEEP/MUTATE require a saved native checkpoint")
    inflight = {"pilot": "pilot08", "task_id": task_id, "arm": arm,
                "reserve_usd": RESERVE, "started_utc": datetime.now(UTC).isoformat()}
    ledger.setdefault("inflight", []).append(inflight)
    save(LEDGER, ledger)
    env = os.environ.copy()
    env["DEEPSEEK_API_KEY"] = secret
    env["MAS_REQUIRE_LIVE_LLM"] = "1"
    env["DEEPSEEK_THINKING"] = "disabled"
    env["OPENROUTER_TEMPERATURE"] = "0"
    env.pop("MAS_DISABLE_LIVE_LLM", None)
    env.pop("MANTA_PILOT08_CAPTURE_CHECKPOINT", None)
    env.pop("MANTA_PILOT08_RESUME_CHECKPOINT", None)
    env.pop("MANTA_PILOT08_BRANCH", None)
    if arm == "CAPTURE":
        env["MANTA_PILOT08_CAPTURE_CHECKPOINT"] = str(checkpoint)
    else:
        env["MANTA_PILOT08_RESUME_CHECKPOINT"] = str(checkpoint)
        env["MANTA_PILOT08_BRANCH"] = arm
    experiment_id = f"pilot08_{task_id}_{arm}"
    command = [sys.executable, "main.py", "run", "--config", manifest["config"],
               "--benchmark", "workbench", "--task-ids", task_id,
               "--runs-per-task", "1", "--seed", str(manifest["seed"]),
               "--output-dir", str(RESULTS / "raw"), "--output-layout", "hierarchical",
               "--experiment-id", experiment_id, "--system-label", arm]
    log = RESULTS / "logs" / f"{task_id}_{arm}.runner.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    print(f"Starting real Pilot 08 {task_id}/{arm}", flush=True)
    with log.open("w", encoding="utf-8") as handle:
        process = subprocess.run(command, cwd=ROOT, env=env,
                                 stdout=handle, stderr=subprocess.STDOUT)
    folder = RESULTS / "raw" / experiment_id / "workbench" / arm / task_id
    meta_path = folder / "run_0.metadata.json"
    trace_path = folder / "run_0.trace.jsonl"
    eval_path = folder / "run_0.eval.json"
    token_in, token_out = logged_usage(log)
    outcome = {
        "pilot": "pilot08", "task_id": task_id, "arm": arm,
        "seed": manifest["seed"], "run_id": "run_0",
        "token_in": token_in, "token_out": token_out,
        "cost_upper_usd": round(cost_upper(token_in, token_out), 7),
        "runner_log": str(log), "runner_log_sha256": file_hash(log),
        "pipeline_exit_code": process.returncode,
        "checkpoint_path": str(checkpoint) if checkpoint.exists() else None,
        "checkpoint_sha256": file_hash(checkpoint) if checkpoint.exists() else None,
    }
    if process.returncode not in (0, 2):
        outcome["error"] = f"runner_exit_{process.returncode}"
    elif not all(p.exists() for p in (meta_path, trace_path, eval_path)):
        outcome["error"] = "missing_run_files"
    else:
        metadata = load(meta_path)
        evaluation = load(eval_path)
        outcome.update({
            "error": metadata.get("error") or "",
            "metadata_path": str(meta_path), "metadata_sha256": file_hash(meta_path),
            "trace_path": str(trace_path), "trace_sha256": file_hash(trace_path),
            "evaluation_path": str(eval_path), "evaluation_sha256": file_hash(eval_path),
            "official_task_success": bool(evaluation.get("success")),
            "unwanted_side_effects": (evaluation.get("details") or {}).get("unwanted_side_effects"),
            "intervention_applied": any(x.get("applied") for x in
                                        metadata.get("artifact_intervention_events") or []),
            "effective_structural_change": any(x.get("effective_structural_change") for x in
                                               (metadata.get("self_evolved") or {}).get("turn_control_records") or []),
        })
    ledger["inflight"].remove(inflight)
    if outcome["error"]:
        ledger.setdefault("invalid_attempts", []).append({
            **outcome, "reason": "pilot08_run_error",
            "unknown_usage_reserve_usd": 0.0 if token_in + token_out else RESERVE,
        })
        save(LEDGER, ledger)
        print(f"Pilot 08 run failed; raw and logged cost retained: {outcome['error']}", flush=True)
        return False
    ledger.setdefault("episodes", []).append(outcome)
    save(LEDGER, ledger)
    print(f"Finished Pilot 08 {task_id}/{arm}: checkpoint={bool(outcome['checkpoint_path'])} "
          f"mutation={outcome['effective_structural_change']} upper=${outcome['cost_upper_usd']:.4f}",
          flush=True)
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("task_id")
    args = parser.parse_args()
    manifest = prepare(args.task_id)
    for arm in ARMS:
        if not run_one(args.task_id, arm, manifest):
            return
        if arm == "CAPTURE" and not (RESULTS / "checkpoints" / f"{args.task_id}.pkl.gz").exists():
            print("No qualified native proposal after mixed Artifact; no paired continuation", flush=True)
            return
        if arm == "CAPTURE":
            validate_live_checkpoint(args.task_id)


if __name__ == "__main__":
    main()

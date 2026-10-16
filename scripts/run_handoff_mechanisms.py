"""Run five controlled future-context continuations from one Pilot 08 checkpoint."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent
P08 = WORK / "manta-pilot08/results/pilot08_counterfactual"
RESULTS = ROOT / "results/pilot09_handoff_mechanisms"
LEDGER = WORK / "manta_three_pilots_budget.json"
ORIGINAL = Path(r"C:\Users\larei\Documents\ChatGPT\manta")
BASE_MAIN_SHA = "7d557dc793221906a46a1f83d4e5888fcc5c28d2"
POLICIES = ("P0_FULL", "P1_DROP", "P2_EVIDENCE_ONLY", "P3_GRAPH_ONLY", "P4_JOINT")
RESERVE = 0.5


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


def budget_allows(ledger: dict) -> bool:
    episodes = ledger.get("episodes", []) + ledger.get("preflights", [])
    invalid = ledger.get("invalid_attempts", [])
    inflight = ledger.get("inflight", [])
    def spent_for(pilots: set[str] | None) -> float:
        def accept(entry: dict) -> bool:
            return pilots is None or entry.get("pilot") in pilots
        return (sum(float(x.get("cost_upper_usd", 0)) for x in episodes if accept(x))
                + sum(float(x.get("cost_upper_usd", 0)) +
                      float(x.get("unknown_usage_reserve_usd", 0))
                      for x in invalid if accept(x))
                + sum(float(x.get("reserve_usd", 0)) for x in inflight if accept(x)))
    return (spent_for(None) + RESERVE <= float(ledger["cap_usd"])
            and spent_for({"pilot07", "pilot08", "pilot09"}) + RESERVE <= 7.5
            and spent_for({"pilot09"}) + RESERVE <= 1.0)


def prepare(task_id: str) -> dict:
    validation_path = P08 / "restore_validation" / f"{task_id}.json"
    validation = load(validation_path if validation_path.exists()
                      else P08 / "restore_validation.json")
    if validation.get("status") != "LIVE_BOUNDARY_TWO_RESTORE_PASSED":
        raise RuntimeError("Pilot 09 requires a real, two-restore Pilot 08 boundary")
    prior = [x for x in load(LEDGER).get("episodes", [])
             if x.get("pilot") == "pilot08" and x.get("task_id") == task_id]
    if not {"KEEP", "MUTATE"}.issubset({x.get("arm") for x in prior}):
        raise RuntimeError("Pilot 09 requires both completed Pilot 08 continuations")
    pair_path = P08 / "paired_summary.csv"
    if not pair_path.exists():
        raise RuntimeError("Pilot 09 requires the audited Pilot 08 pair summary")
    with pair_path.open(newline="", encoding="utf-8") as handle:
        pair_rows = [row for row in csv.DictReader(handle)
                     if row.get("case_id") == task_id]
    if len(pair_rows) != 1 or pair_rows[0]["causal_comparison_valid"] != "True":
        raise RuntimeError("Pilot 09 requires a valid same-checkpoint Pilot 08 pair")
    source_manifest_path = P08 / "manifests" / f"{task_id}.json"
    source_manifest = load(source_manifest_path if source_manifest_path.exists()
                           else P08 / "manifest.json")
    if source_manifest["pilot07_source_case"] != task_id:
        raise ValueError("Pilot 08 checkpoint belongs to another task")
    source_checkpoint = P08 / "checkpoints" / f"{task_id}.pkl.gz"
    if file_hash(source_checkpoint) != validation["checkpoint_sha256"]:
        raise ValueError("Pilot 08 checkpoint hash changed")
    frozen = RESULTS / "frozen"
    frozen.mkdir(parents=True, exist_ok=True)
    copies = {}
    for name in (f"{task_id}.json", f"{task_id}.payload.json", "topology_skill.md"):
        source = P08 / "frozen" / name
        target = frozen / name
        shutil.copy2(source, target)
        copies[name] = {"source": str(source), "sha256": file_hash(target)}
    checkpoint = RESULTS / "checkpoints" / f"{task_id}.pkl.gz"
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_checkpoint, checkpoint)
    config_text = Path(source_manifest["config"]).read_text(encoding="utf-8")
    for old, new in (
        (str(P08 / "raw"), str(RESULTS / "raw")),
        (str(P08 / "frozen" / f"{task_id}.json"), str(frozen / f"{task_id}.json")),
        (str(P08 / "frozen" / f"{task_id}.payload.json"),
         str(frozen / f"{task_id}.payload.json")),
        (str(P08 / "frozen/topology_skill.md"), str(frozen / "topology_skill.md")),
    ):
        escaped_old, escaped_new = json.dumps(old)[1:-1], json.dumps(new)[1:-1]
        if escaped_old not in config_text:
            raise ValueError(f"Missing source config path {old}")
        config_text = config_text.replace(escaped_old, escaped_new)
    config = RESULTS / "configs" / f"{task_id}.toml"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(config_text, encoding="utf-8")
    manifest = {
        "base_main_sha": BASE_MAIN_SHA, "task_id": task_id,
        "source_pilot08_checkpoint": str(source_checkpoint),
        "source_pilot08_checkpoint_sha256": validation["checkpoint_sha256"],
        "local_checkpoint": str(checkpoint), "local_checkpoint_sha256": file_hash(checkpoint),
        "frozen_files": copies, "config": str(config), "config_sha256": file_hash(config),
        "seed": source_manifest["seed"], "policies": POLICIES,
        "intervention_boundary": "post_audit_pre_mutation_future_context",
        "limitation": "Prior first-turn exposures cannot be undone at this boundary",
        "model": "deepseek-flash", "temperature": 0, "thinking": "disabled",
        "price_rule": "uncached peak input $0.30/M output $1.20/M",
    }
    save(RESULTS / "manifest.json", manifest)
    save(RESULTS / "frozen_policies.json", {
        "policies": POLICIES,
        "source_checkpoint_sha256": validation["checkpoint_sha256"],
        "P2_P4_evidence_source": "unmodified WorkBench tool rows in original Worker Artifact",
        "oracle_answer_in_prompt": False,
        "graph_intervention": "frozen native proposal structural ops only",
    })
    return manifest


def run_one(task_id: str, policy: str, manifest: dict) -> bool:
    ledger = load(LEDGER)
    if any(x.get("pilot") == "pilot09" and x.get("task_id") == task_id
           and x.get("arm") == policy for x in ledger.get("episodes", [])):
        return True
    if not budget_allows(ledger):
        print(f"Pilot 09 budget guard stopped before {task_id}/{policy}", flush=True)
        return False
    secret = os.getenv("DEEPSEEK_API_KEY") or dotenv_values(ORIGINAL / ".env").get("DEEPSEEK_API_KEY")
    if not secret:
        raise RuntimeError("Missing real DeepSeek key; no mock fallback")
    inflight = {"pilot": "pilot09", "task_id": task_id, "arm": policy,
                "reserve_usd": RESERVE, "started_utc": datetime.now(UTC).isoformat()}
    ledger.setdefault("inflight", []).append(inflight)
    save(LEDGER, ledger)
    env = os.environ.copy()
    env["DEEPSEEK_API_KEY"] = secret
    env["MAS_REQUIRE_LIVE_LLM"] = "1"
    env["DEEPSEEK_THINKING"] = "disabled"
    env["OPENROUTER_TEMPERATURE"] = "0"
    env["MANTA_PILOT09_RESUME_CHECKPOINT"] = manifest["local_checkpoint"]
    env["MANTA_PILOT09_POLICY"] = policy
    for key in ("MAS_DISABLE_LIVE_LLM", "MANTA_PILOT08_CAPTURE_CHECKPOINT",
                "MANTA_PILOT08_RESUME_CHECKPOINT", "MANTA_PILOT08_BRANCH"):
        env.pop(key, None)
    experiment_id = f"pilot09_{task_id}_{policy}"
    command = [sys.executable, "main.py", "run", "--config", manifest["config"],
               "--benchmark", "workbench", "--task-ids", task_id,
               "--runs-per-task", "1", "--seed", str(manifest["seed"]),
               "--output-dir", str(RESULTS / "raw"), "--output-layout", "hierarchical",
               "--experiment-id", experiment_id, "--system-label", policy]
    log = RESULTS / "logs" / f"{task_id}_{policy}.runner.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    print(f"Starting real Pilot 09 {task_id}/{policy}", flush=True)
    with log.open("w", encoding="utf-8") as handle:
        process = subprocess.run(command, cwd=ROOT, env=env,
                                 stdout=handle, stderr=subprocess.STDOUT)
    folder = RESULTS / "raw" / experiment_id / "workbench" / policy / task_id
    meta, trace, evaluation = (folder / f"run_0.{suffix}"
                               for suffix in ("metadata.json", "trace.jsonl", "eval.json"))
    matches = re.findall(r"\[llm\] DONE[^\n]*token_in=(\d+) token_out=(\d+)",
                         log.read_text(encoding="utf-8", errors="replace"))
    token_in = sum(int(row[0]) for row in matches)
    token_out = sum(int(row[1]) for row in matches)
    record = {
        "pilot": "pilot09", "task_id": task_id, "arm": policy,
        "seed": manifest["seed"], "run_id": "run_0",
        "token_in": token_in, "token_out": token_out,
        "cost_upper_usd": round(cost_upper(token_in, token_out), 7),
        "runner_log": str(log), "runner_log_sha256": file_hash(log),
        "pipeline_exit_code": process.returncode,
        "checkpoint_sha256": manifest["local_checkpoint_sha256"],
    }
    if process.returncode not in (0, 2):
        record["error"] = f"runner_exit_{process.returncode}"
    elif all(path.exists() for path in (meta, trace, evaluation)):
        metadata, ev = load(meta), load(evaluation)
        task_summary_path = folder / "task_summary.json"
        task_summary = load(task_summary_path) if task_summary_path.exists() else {}
        run_status = (task_summary.get("runs") or [{}])[0]
        record.update({
            "error": metadata.get("error") or "",
            "metadata_path": str(meta), "metadata_sha256": file_hash(meta),
            "trace_path": str(trace), "trace_sha256": file_hash(trace),
            "evaluation_path": str(evaluation), "evaluation_sha256": file_hash(evaluation),
            "official_task_success": bool(ev.get("success")),
            "runner_fallback": bool(run_status.get("fallback")),
            "runner_needs_rerun": bool(run_status.get("needs_rerun")),
            "unwanted_side_effects": (ev.get("details") or {}).get("unwanted_side_effects"),
            "handoff_policy_events": metadata.get("handoff_policy_events") or [],
        })
    else:
        record["error"] = "missing_run_files"
    ledger["inflight"].remove(inflight)
    if record["error"]:
        ledger.setdefault("invalid_attempts", []).append({
            **record, "reason": "pilot09_run_error",
            "unknown_usage_reserve_usd": 0.0 if token_in + token_out else RESERVE,
        })
        save(LEDGER, ledger)
        print(f"Pilot 09 stopped after failed run: {record['error']}", flush=True)
        return False
    ledger.setdefault("episodes", []).append(record)
    save(LEDGER, ledger)
    print(f"Finished Pilot 09 {task_id}/{policy} upper=${record['cost_upper_usd']:.4f}",
          flush=True)
    return True


def write_summary(task_id: str) -> None:
    rows = [x for x in load(LEDGER)["episodes"]
            if x.get("pilot") == "pilot09" and x.get("task_id") == task_id]
    rows.sort(key=lambda x: POLICIES.index(x["arm"]))
    fields = ("task_id", "arm", "seed", "run_id", "official_task_success",
              "unwanted_side_effects", "token_in", "token_out", "cost_upper_usd",
              "metadata_path", "trace_path", "evaluation_path")
    with (RESULTS / "summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fields)
        writer.writeheader()
        writer.writerows({key: row.get(key) for key in fields} for row in rows)
    with (RESULTS / "evidence_retention.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            for event in row.get("handoff_policy_events") or []:
                handle.write(json.dumps({"task_id": task_id, "arm": row["arm"], **event},
                                        ensure_ascii=False, sort_keys=True) + "\n")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("task_id")
    args = parser.parse_args()
    manifest = prepare(args.task_id)
    for policy in POLICIES:
        if not run_one(args.task_id, policy, manifest):
            break
    write_summary(args.task_id)


if __name__ == "__main__":
    main()

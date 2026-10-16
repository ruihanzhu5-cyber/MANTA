"""Sequential, budgeted, real DeepSeek WorkBench IPI pilot.

Prepare is offline. Run requires --execute and never falls back to mock.
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
RESULTS = ROOT / "results" / "manta_ipi_pilot"
BASE_CONFIG = ROOT / "results/context_topology_ablation/configs/multi_domain_12/B2_topology.toml"
PRICE_URL = "https://api-docs.deepseek.com/quick_start/pricing/"
MODEL = "deepseek-flash"
BASE_URL = "https://api.deepseek.com"
BUDGET = 10.0
RESERVE = 1.5
ARMS = {
    "E0_fixed_clean": (False, False),
    "E1_adaptive_clean": (True, False),
    "E2_fixed_attack": (False, True),
    "E3_adaptive_attack": (True, True),
}


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def cost(token_in: int, token_out: int) -> float:
    # Official peak, all input treated as cache miss. This is a pricing upper estimate.
    return (token_in * 0.30 + token_out * 1.20) / 1_000_000


def _worker_reads(metadata: dict) -> list[tuple[dict, dict, str]]:
    """Return actual nonempty body observations by noncoordinator agents with a relay."""
    relayed = {
        str(p.get("artifact_id")): str(p.get("message_id"))
        for p in metadata.get("relay_messages", [])
        if p.get("sender") != "agent_0" and "agent_0" in p.get("recipients", [])
    }
    observations = []
    for artifact in metadata.get("artifact_records", []):
        aid = str(artifact.get("artifact_id"))
        if aid not in relayed:
            continue
        for record in artifact.get("tool_records", []):
            name = record.get("tool_name")
            output = record.get("output")
            if name == "email.search_emails" and isinstance(output, list):
                for mail in output:
                    if isinstance(mail, dict) and str(mail.get("body", "")).strip() and mail.get("email_id"):
                        observations.append((artifact, record, str(mail["email_id"])))
            elif (
                name == "email.get_email_information_by_id"
                and record.get("arguments", {}).get("field") == "body"
                and isinstance(output, dict)
                and str(output.get("body", "")).strip()
            ):
                observations.append((artifact, record, str(record.get("arguments", {}).get("email_id", ""))))
    # MANTA may prune exploratory tool records from the final structured
    # Artifact. The interaction log still contains the actual tool output
    # preview and dispatch identity; use it to avoid false screening negatives.
    seen = {(a.get("artifact_id"), email_id) for a, _, email_id in observations}
    artifacts_by_dispatch = {
        (a.get("agent_id"), a.get("dispatch_id")): a
        for a in metadata.get("artifact_records", [])
        if str(a.get("artifact_id")) in relayed
    }
    for log in metadata.get("interaction_logs", []):
        artifact = artifacts_by_dispatch.get((log.get("agent_id"), log.get("dispatch_id")))
        if artifact is None:
            continue
        for record in log.get("tool_calls", []):
            preview = str(record.get("output_preview", ""))
            name = record.get("tool_name")
            ids: list[str] = []
            if name == "email.search_emails" and re.search(r'"body"\s*:\s*"[^" ]', preview):
                ids = re.findall(r'"email_id"\s*:\s*"([^"]+)"', preview)
            elif (name == "email.get_email_information_by_id"
                  and record.get("arguments", {}).get("field") == "body"
                  and re.search(r'"body"\s*:\s*"[^" ]', preview)):
                ids = [str(record.get("arguments", {}).get("email_id", ""))]
            for email_id in ids:
                key = (artifact.get("artifact_id"), email_id)
                if email_id and key not in seen:
                    observations.append((artifact, record, email_id))
                    seen.add(key)
    return observations


def discover_candidates(history: Path) -> list[dict]:
    chosen: dict[str, dict] = {}
    for ev_path in history.glob("manta_dsflash_workbench6_*/workbench/self_evolved/*/run_*.eval.json"):
        try:
            ev = read_json(ev_path)
            if not ev.get("success"):
                continue
            task_dir = ev_path.parent
            task = read_json(task_dir / "task.json")
            task_id = str(task["task_id"])
            if not (task_id.startswith("email_") or task_id.startswith("multi_domain_")):
                continue
            ground_truth = task.get("metadata", {}).get("answer", [])
            if not ground_truth:
                continue
            meta_path = ev_path.with_name(ev_path.name.replace(".eval.json", ".metadata.json"))
            meta = read_json(meta_path)
            initial = meta.get("self_evolved", {}).get("topology_spec_versions", [None])[0]
            if not isinstance(initial, dict) or len(initial.get("agents", [])) != 3:
                continue
            reads = _worker_reads(meta)
            score = len(reads)
            # One candidate per task; prefer historical successful runs where a worker read body.
            candidate = {
                "task_id": task_id, "task_text": task.get("metadata", {}).get("query", task.get("prompt")),
                "historical_metadata": str(meta_path), "historical_task": str(task_dir / "task.json"),
                "historical_worker_body_reads": score, "seed": int(meta["seed"]),
                "initial_spec_sha256": canonical_hash(initial), "initial_spec": initial,
                "ground_truth_side_effect_count": len(ground_truth),
            }
            if task_id not in chosen or score > chosen[task_id]["historical_worker_body_reads"]:
                chosen[task_id] = candidate
        except (OSError, KeyError, IndexError, ValueError, TypeError, json.JSONDecodeError):
            continue
    ranked = sorted(chosen.values(), key=lambda x: (-x["historical_worker_body_reads"], x["task_id"]))
    return ranked[:6]


def config_for(item: dict, arm: str) -> Path:
    topology, attack = ARMS[arm]
    task_id = item["task_id"]
    source = BASE_CONFIG.read_text(encoding="utf-8")
    replacements = {
        "output_dir": (RESULTS / "raw").as_posix(),
        "max_initial_agents": "3", "max_turns": "2", "repair_budget": "1",
        "skill_update_batch_size": "0", "playbook_read": "true",
        "skill_path": (RESULTS / "frozen" / "topology_skill.md").as_posix(),
        "frozen_initial_spec_path": (RESULTS / "frozen" / f"{task_id}.json").as_posix(),
        "allow_topology_mutation": str(topology).lower(),
        "allow_context_policy_mutation": str(topology).lower(),
        "evidence_handoff_enabled": "false",
        "data_dir": (ROOT / ".cache/workbench").as_posix(),
    }
    for key, value in replacements.items():
        pattern = rf'(?m)^{re.escape(key)} = .*?$'
        if not re.search(pattern, source):
            raise RuntimeError(f"Base config missing {key}")
        quote = "" if value in {"true", "false"} or value.isdigit() else '"'
        replacement = f"{key} = {quote}{value}{quote}"
        source = re.sub(pattern, lambda _, text=replacement: text, source, count=1)
    source += '\n# IPI pilot: only the WorkBench tool-response adapter reads these keys.\n'
    source = source.replace('[workbench]\n', '[workbench]\n'
                            + f'ipi_enabled = {str(attack).lower()}\n'
                            + f'ipi_target_email_id = "{item.get("target_email_id", "")}"\n'
                            + f'ipi_target_agent_id = "{item.get("target_agent_id", "")}"\n'
                            + f'ipi_run_id = "{task_id}/{arm}/run_0"\n', 1)
    path = RESULTS / "configs" / task_id / f"{arm}.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


def prepare(history: Path) -> None:
    manifest_path = RESULTS / "manifest.json"
    if manifest_path.exists():
        print("Existing manifest kept; prepare is idempotent")
        return
    if not BASE_CONFIG.exists():
        raise RuntimeError(f"Missing local base config: {BASE_CONFIG}")
    candidates = discover_candidates(history)
    if not candidates:
        raise RuntimeError("No qualifying historical hints; no paid screening started")
    sys.path.insert(0, str(ROOT))
    from benchmark.workbench import WorkBenchBenchmark

    for item in candidates:
        domain, _, index = item["task_id"].rpartition("_")
        benchmark = WorkBenchBenchmark({"domain": domain, "data_dir": str(ROOT / ".cache/workbench")})
        task = benchmark.load_tasks()[int(index)]
        if task.task_id != item["task_id"] or task.metadata["query"] != item["task_text"]:
            raise RuntimeError(f"Dataset differs from historical task: {item['task_id']}")
        write_json(RESULTS / "frozen" / f"{item['task_id']}.json", {
            "task_id": item["task_id"], "seed": item["seed"],
            "topology_spec": item["initial_spec"],
            "topology_spec_sha256": item["initial_spec_sha256"],
            "source_metadata": item["historical_metadata"],
        })
        config_for(item, "E1_adaptive_clean")
    skill = ROOT / "config/topology_skill.md"
    frozen_skill = RESULTS / "frozen/topology_skill.md"
    frozen_skill.write_bytes(skill.read_bytes())
    manifest = {
        "created_at_utc": datetime.now(UTC).isoformat(), "model": MODEL, "base_url": BASE_URL,
        "budget_usd": BUDGET, "price_source": PRICE_URL,
        "pricing": "peak uncached input $0.30/M; peak output $1.20/M, checked 2026-10-16",
        "playbook_sha256": digest(frozen_skill), "candidate_limit": 6,
        "candidates": candidates, "screened": [], "selected": [], "arms": ARMS,
        "selection_rule": "Official clean success, real worker email body read before write, worker relay to agent_0",
    }
    write_json(manifest_path, manifest)
    (RESULTS / ".gitignore").write_text("raw/\nlogs/\n", encoding="utf-8")
    print(f"Prepared {len(candidates)} candidate tasks; frozen playbook and initial specs")


def run_dir(task_id: str, arm: str) -> Path:
    return RESULTS / "raw" / f"manta_ipi_{task_id}_{arm}" / "workbench" / arm / task_id


def inspect(item: dict, arm: str) -> dict:
    folder = run_dir(item["task_id"], arm)
    meta_path = folder / "run_0.metadata.json"
    ev_path = folder / "run_0.eval.json"
    trace_path = folder / "run_0.trace.jsonl"
    metadata = read_json(meta_path)
    evaluation = read_json(ev_path)
    trace = [json.loads(line) for line in trace_path.read_text(encoding="utf-8").splitlines()]
    token_in = sum(int(e.get("token_in") or 0) for e in trace)
    token_out = sum(int(e.get("token_out") or 0) for e in trace)
    if any(e.get("payload", {}).get("mock_used") for e in trace):
        raise RuntimeError(f"Mock trace detected: {folder}")
    if any(log.get("llm", {}).get("mock_used") for log in metadata.get("interaction_logs", [])):
        raise RuntimeError(f"Mock interaction detected: {folder}")
    spec = metadata["self_evolved"]["topology_spec_versions"][0]
    if canonical_hash(spec) != item["initial_spec_sha256"] or metadata.get("seed") != item["seed"]:
        raise RuntimeError(f"Frozen task topology/seed mismatch: {folder}")
    mutations = metadata["self_evolved"].get("mutations", [])
    injection_events = metadata.get("injection_events", [])
    applied = [e for e in injection_events if e.get("injection_applied")]
    if len(applied) > 1:
        raise RuntimeError(f"More than one injection: {folder}")
    if not ARMS[arm][0] and any(m.get("effective_structural_change") for m in mutations):
        raise RuntimeError(f"Fixed topology changed: {folder}")
    worker_reads = _worker_reads(metadata)
    return {
        "task_id": item["task_id"], "arm": arm, "seed": item["seed"],
        "official_task_success": bool(evaluation.get("success")), "score": evaluation.get("score"),
        "unwanted_side_effects": evaluation.get("details", {}).get("unwanted_side_effects"),
        "ground_truth": evaluation.get("details", {}).get("ground_truth", []),
        "predicted_actions": evaluation.get("details", {}).get("prediction", []),
        "worker_email_body_reads": [
            {"agent_id": a.get("agent_id"), "artifact_id": a.get("artifact_id"),
             "email_id": email_id, "tool_name": r.get("tool_name"),
             "dispatch_id": a.get("dispatch_id")}
            for a, r, email_id in worker_reads
        ],
        "injection_applied": bool(applied), "injection_events": injection_events,
        "effective_structural_change": any(bool(m.get("effective_structural_change")) for m in mutations),
        "agent_count": max((len(s.get("agents", [])) for s in metadata["self_evolved"].get("topology_spec_versions", [])), default=0),
        "tool_calls": metadata.get("tool_calls_total"), "token_in": token_in,
        "token_out": token_out, "cost_upper_usd": round(cost(token_in, token_out), 6),
        "needs_rerun": bool(metadata.get("needs_rerun", False)),
        "trace_path": str(trace_path), "trace_sha256": digest(trace_path),
        "metadata_path": str(meta_path), "metadata_sha256": digest(meta_path),
        "evaluation_path": str(ev_path), "evaluation_sha256": digest(ev_path),
    }


def _qualify(item: dict, episode: dict) -> tuple[str, str] | None:
    from benchmark.workbench import SIDE_EFFECT_TOOLS

    if not episode["official_task_success"] or episode["needs_rerun"]:
        return None
    if not episode["ground_truth"] or not episode["predicted_actions"]:
        return None
    meta = read_json(Path(episode["metadata_path"]))
    write_dispatches = [
        int(log.get("dispatch_id") or 0)
        for log in meta.get("interaction_logs", [])
        if any(call.get("tool_name") in SIDE_EFFECT_TOOLS for call in log.get("tool_calls", []))
    ]
    if not write_dispatches:
        return None
    first_write_dispatch = min(write_dispatches)
    # The worker artifact is relayed before the transactional aggregator can write.
    for read in episode["worker_email_body_reads"]:
        aid = read["artifact_id"]
        relay = next((m for m in meta.get("relay_messages", []) if m.get("artifact_id") == aid
                      and "agent_0" in m.get("recipients", []) and m.get("kind") == "specialist_report"), None)
        # Select the email the worker actually carried into its handoff, not an
        # unrelated hit in the same search result list.
        if (relay and read["email_id"] and read["email_id"] in str(relay.get("content", ""))
                and int(read.get("dispatch_id") or 0) < first_write_dispatch):
            return read["email_id"], read["agent_id"]
    return None


def execute(history: Path, source: Path) -> None:
    from dotenv import dotenv_values
    from openai import OpenAI

    manifest_path = RESULTS / "manifest.json"
    if not manifest_path.exists():
        raise RuntimeError("Run prepare before paid execution")
    manifest = read_json(manifest_path)
    secret = os.getenv("DEEPSEEK_API_KEY") or dotenv_values(source / ".env").get("DEEPSEEK_API_KEY")
    if not secret:
        raise RuntimeError("DEEPSEEK_API_KEY missing; stopped without mock fallback")
    ledger_path = RESULTS / "cost_ledger.json"
    ledger = read_json(ledger_path) if ledger_path.exists() else {
        "price_source": PRICE_URL, "actual_billed_cost_usd": "unknown", "episodes": []
    }
    if "preflight" not in ledger:
        reply = OpenAI(api_key=secret, base_url=BASE_URL, timeout=60).chat.completions.create(
            model=MODEL, messages=[{"role": "user", "content": "Reply OK."}], temperature=0, max_tokens=8
        )
        if not reply.choices:
            raise RuntimeError("Live preflight returned no choices")
        usage = reply.usage
        ti, to = int(usage.prompt_tokens or 0), int(usage.completion_tokens or 0)
        ledger["preflight"] = {"model": reply.model, "token_in": ti, "token_out": to,
                               "cost_upper_usd": cost(ti, to)}
        write_json(ledger_path, ledger)
        print("Live DeepSeek preflight passed", flush=True)
    env = os.environ.copy()
    env["DEEPSEEK_API_KEY"] = secret
    env["MAS_REQUIRE_LIVE_LLM"] = "1"
    env.pop("MAS_DISABLE_LIVE_LLM", None)

    # Re-evaluate already saved E1 episodes after a screening-code repair.
    # This does not issue an API call or replace any raw attempt.
    recovered_selected: list[str] = []
    for item in manifest["candidates"]:
        if item["task_id"] not in manifest["screened"]:
            continue
        prior = next((e for e in ledger["episodes"] if e["task_id"] == item["task_id"]
                      and e["arm"] == "E1_adaptive_clean"), None)
        if prior is None:
            continue
        refreshed = inspect(item, "E1_adaptive_clean")
        target = _qualify(item, refreshed)
        if target and len(recovered_selected) < 3:
            item["target_email_id"], item["target_agent_id"] = target
            recovered_selected.append(item["task_id"])
            prior.update(refreshed)
            print(f"Recovered saved E1 qualification: {item['task_id']} {target}", flush=True)
    if recovered_selected:
        manifest["selected"] = recovered_selected
        write_json(ledger_path, ledger)
        write_json(manifest_path, manifest)

    def run_one(item: dict, arm: str) -> dict:
        existing = next((e for e in ledger["episodes"] if e["task_id"] == item["task_id"] and e["arm"] == arm), None)
        if existing:
            return existing
        spent = float(ledger["preflight"]["cost_upper_usd"]) + sum(float(e["cost_upper_usd"]) for e in ledger["episodes"])
        spent += sum(float(a.get("reserved_usd", 0)) for a in ledger.get("incomplete_attempts", []))
        if spent + RESERVE > BUDGET:
            raise RuntimeError(f"Budget guard stopped before {item['task_id']} {arm}: upper={spent:.4f}, reserve={RESERVE}")
        config = config_for(item, arm)
        command = [sys.executable, "main.py", "run", "--config", str(config), "--benchmark", "workbench",
                   "--task-ids", item["task_id"], "--runs-per-task", "1", "--seed", str(item["seed"]),
                   "--output-dir", str(RESULTS / "raw"), "--output-layout", "hierarchical",
                   "--experiment-id", f"manta_ipi_{item['task_id']}_{arm}", "--system-label", arm]
        log = RESULTS / "logs" / f"{item['task_id']}_{arm}.runner.log"
        log.parent.mkdir(parents=True, exist_ok=True)
        if not (run_dir(item["task_id"], arm) / "run_0.eval.json").exists():
            print(f"Starting real episode {item['task_id']} {arm}", flush=True)
            with log.open("w", encoding="utf-8") as handle:
                result = subprocess.run(command, cwd=ROOT, env=env, stdout=handle, stderr=subprocess.STDOUT)
            exit_code = result.returncode
        else:
            exit_code = 0
        if not (run_dir(item["task_id"], arm) / "run_0.eval.json").exists():
            ledger.setdefault("incomplete_attempts", []).append({"task_id": item["task_id"], "arm": arm,
                "runner_log": str(log), "exit_code": exit_code, "reserved_usd": RESERVE})
            write_json(ledger_path, ledger)
            raise RuntimeError(f"No saved official evaluation for {item['task_id']} {arm}; see {log}")
        episode = inspect(item, arm)
        episode["runner_log"] = str(log)
        episode["pipeline_exit_code"] = exit_code
        episode["completed_at_utc"] = datetime.now(UTC).isoformat()
        ledger["episodes"].append(episode)
        write_json(ledger_path, ledger)
        print(f"Finished {item['task_id']} {arm}: success={episode['official_task_success']} "
              f"exposed={episode['injection_applied']} upper=${episode['cost_upper_usd']:.4f}", flush=True)
        return episode

    for item in manifest["candidates"]:
        if len(manifest["selected"]) >= 3:
            break
        if item["task_id"] in manifest["screened"]:
            continue
        e1 = run_one(item, "E1_adaptive_clean")
        target = _qualify(item, e1)
        manifest["screened"].append(item["task_id"])
        if target:
            item["target_email_id"], item["target_agent_id"] = target
            manifest["selected"].append(item["task_id"])
            print(f"Qualified {item['task_id']} target email/agent {target}", flush=True)
        else:
            print(f"Rejected {item['task_id']} under prespecified E1 qualification rule", flush=True)
        write_json(manifest_path, manifest)
    for task_id in manifest["selected"]:
        item = next(c for c in manifest["candidates"] if c["task_id"] == task_id)
        for arm in ("E0_fixed_clean", "E2_fixed_attack", "E3_adaptive_attack"):
            run_one(item, arm)


def report() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts/analyze_manta_ipi_pilot.py")], cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["prepare", "run", "report"])
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--history-dir", type=Path, default=Path(os.getenv("MANTA_HISTORY_DIR", "D:/MANTA_DATA/experiments")))
    parser.add_argument("--source-dir", type=Path, default=Path(os.getenv("MANTA_SOURCE_DIR", str(ROOT))))
    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args.history_dir)
    elif args.command == "run":
        if not args.execute:
            parser.error("Real API execution requires --execute")
        execute(args.history_dir, args.source_dir)
    else:
        report()


if __name__ == "__main__":
    main()

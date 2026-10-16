"""Small, sequential WorkBench Context × Topology pilot on live DeepSeek Flash.

Prepare is offline. Run requires the original local .env and enforces live mode.
The historical experiment files are read only. No benchmark code is changed.
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
RESULTS = ROOT / "results" / "context_topology_ablation"
ORIGINAL = Path(r"C:\Users\larei\Documents\ChatGPT\manta")
HISTORY = Path(r"D:\MANTA_DATA\experiments")
MODEL = "deepseek-flash"
BASE_URL = "https://api.deepseek.com"
PRICE_URL = "https://api-docs.deepseek.com/quick_start/pricing/"
MAX_UPPER_USD = 15.0
NEXT_EPISODE_RESERVE_USD = 2.0
TASKS = {
    "multi_domain_12": {
        "worker": 2,
        "seed": 12042,
    },
    "multi_domain_16": {
        "worker": 3,
        "seed": 16042,
    },
}
VARIANTS = {
    "B0_fixed": (False, False),
    "B1_context": (True, False),
    "B2_topology": (False, True),
    "B3_combination": (True, True),
}


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")


def _history_task_dir(task_id: str) -> Path:
    worker = TASKS[task_id]["worker"]
    return (
        HISTORY
        / f"manta_dsflash_workbench6_20261005_2145_w{worker}"
        / "workbench"
        / "self_evolved"
        / task_id
    )


def _canonical_hash(payload: dict) -> str:
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _replace_one(text: str, pattern: str, replacement: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError(f"Expected one config match for {pattern!r}; found {count}")
    return updated


def prepare() -> None:
    """Freeze the two historical pre-execution specs for all four arms."""
    manifest = {
        "model": MODEL,
        "base_url": BASE_URL,
        "price_source": PRICE_URL,
        "pricing_rule": "Conservative upper bound: $0.30/M input + $1.20/M output",
        "budget_upper_usd": MAX_UPPER_USD,
        "tasks": {},
        "variants": {
            name: {"context": context, "topology": topology}
            for name, (context, topology) in VARIANTS.items()
        },
    }
    for task_id, item in TASKS.items():
        history_dir = _history_task_dir(task_id)
        metadata_path = history_dir / "run_0.metadata.json"
        task_path = history_dir / "task.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        historical_task = json.loads(task_path.read_text(encoding="utf-8"))
        if metadata["seed"] != item["seed"] or historical_task["task_id"] != task_id:
            raise RuntimeError(f"Historical task or seed mismatch for {task_id}")
        frozen_spec = metadata["self_evolved"]["topology_spec_versions"][0]
        # These pre-execution specs contain no evaluator result or historical answer.
        freeze_path = RESULTS / "frozen" / f"{task_id}.json"
        freeze_payload = {
            "task_id": task_id,
            "seed": item["seed"],
            "source_metadata": str(metadata_path),
            "topology_spec_sha256": _canonical_hash(frozen_spec),
            "topology_spec": frozen_spec,
        }
        if freeze_path.exists():
            old = json.loads(freeze_path.read_text(encoding="utf-8"))
            if old != freeze_payload:
                raise RuntimeError(f"Frozen spec changed unexpectedly: {freeze_path}")
        else:
            _write_json(freeze_path, freeze_payload)

        worker = item["worker"]
        skill_source = (
            ORIGINAL
            / "artifacts"
            / "deepseek_flash_workbench_parallel_state"
            / f"worker_{worker}"
            / "topology_skill.md"
        )
        skill_target = RESULTS / "frozen" / f"{task_id}.topology_skill.md"
        skill_content = skill_source.read_bytes()
        if skill_target.exists() and skill_target.read_bytes() != skill_content:
            raise RuntimeError(f"Frozen MANTA playbook changed: {skill_target}")
        skill_target.write_bytes(skill_content)

        source_config = (
            ORIGINAL / "config" / f"manta_deepseek_flash_workbench6_w{worker}.toml"
        )
        base_config = source_config.read_text(encoding="utf-8")
        base_config = _replace_one(
            base_config,
            r'^output_dir = ".*"$',
            'output_dir = "results/context_topology_ablation/raw"',
        )
        base_config = _replace_one(
            base_config,
            r'^skill_path = ".*"$',
            'skill_path = "' + skill_target.as_posix() + '"',
        )
        base_config = _replace_one(
            base_config,
            r'^\[browsecomp\]$',
            'frozen_initial_spec_path = "'
            + freeze_path.as_posix()
            + '"\nallow_context_policy_mutation = false\n\n[browsecomp]',
        )
        base_config = _replace_one(
            base_config,
            r'^\[workbench\]$',
            '[workbench]\ndata_dir = ".cache/workbench"',
        )
        for variant, (context, topology) in VARIANTS.items():
            content = base_config.replace(
                "allow_context_policy_mutation = false",
                "allow_context_policy_mutation = false\n"
                f"evidence_handoff_enabled = {str(context).lower()}\n"
                f"allow_topology_mutation = {str(topology).lower()}",
            )
            config_path = RESULTS / "configs" / task_id / f"{variant}.toml"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            if config_path.exists() and config_path.read_text(encoding="utf-8") != content:
                raise RuntimeError(f"Config changed unexpectedly: {config_path}")
            config_path.write_text(content, encoding="utf-8")
        manifest["tasks"][task_id] = {
            "seed": item["seed"],
            "historical_task": str(task_path),
            "historical_metadata": str(metadata_path),
            "frozen_spec": str(freeze_path),
            "frozen_spec_sha256": freeze_payload["topology_spec_sha256"],
            "historical_playbook": str(skill_source),
            "historical_config": str(source_config),
            "historical_initial_planner_usage": {
                "token_in": int(
                    metadata["self_evolved"]["planner"].get("llm", {}).get("token_in", 0)
                ),
                "token_out": int(
                    metadata["self_evolved"]["planner"].get("llm", {}).get("token_out", 0)
                ),
                "new_api_cost_usd": 0.0,
                "note": "Reused a historical pre-execution spec; usage is historical provenance, not a new pilot charge.",
            },
        }
    _write_json(RESULTS / "manifest.json", manifest)
    print(f"Prepared {len(TASKS)} frozen topology specs and {len(TASKS) * len(VARIANTS)} configs")


def _upper_cost(token_in: int, token_out: int) -> float:
    return (token_in * 0.30 + token_out * 1.20) / 1_000_000


def _usage(trace_path: Path) -> tuple[int, int, bool]:
    token_in = token_out = 0
    mock_used = False
    for line in trace_path.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        token_in += int(event.get("token_in") or 0)
        token_out += int(event.get("token_out") or 0)
        mock_used |= bool(event.get("payload", {}).get("mock_used", False))
    return token_in, token_out, mock_used


def _result_dir(task_id: str, variant: str) -> Path:
    experiment_id = f"ctx_topo_{task_id}_{variant}"
    return RESULTS / "raw" / experiment_id / "workbench" / variant / task_id


def _inspect_run(task_id: str, variant: str) -> dict:
    path = _result_dir(task_id, variant)
    metadata = json.loads((path / "run_0.metadata.json").read_text(encoding="utf-8"))
    evaluation = json.loads((path / "run_0.eval.json").read_text(encoding="utf-8"))
    token_in, token_out, trace_mock = _usage(path / "run_0.trace.jsonl")
    interaction_mock = any(
        bool(log.get("llm", {}).get("mock_used", False))
        for log in metadata.get("interaction_logs", [])
    )
    if trace_mock or interaction_mock:
        raise RuntimeError(f"Mock model result found in {task_id} {variant}")
    initial = metadata["self_evolved"]["topology_spec_versions"][0]
    frozen = json.loads((RESULTS / "frozen" / f"{task_id}.json").read_text(encoding="utf-8"))
    if _canonical_hash(initial) != frozen["topology_spec_sha256"]:
        raise RuntimeError(f"Initial spec differs from the frozen spec for {task_id} {variant}")
    if metadata.get("seed") != TASKS[task_id]["seed"]:
        raise RuntimeError(f"Seed differs from history for {task_id} {variant}")
    details = evaluation.get("details") or {}
    mutations = metadata["self_evolved"].get("mutations", [])
    failed_generations = [
        {"agent_id": log.get("agent_id"), "phase": log.get("phase"), "round": log.get("round_index")}
        for log in metadata.get("interaction_logs", [])
        if (log.get("llm", {}).get("metadata") or {}).get("generation_status") == "failed"
    ]
    return {
        "task_id": task_id,
        "variant": variant,
        "seed": metadata["seed"],
        "success": bool(evaluation.get("success")),
        "score": evaluation.get("score"),
        "correct": details.get("correct"),
        "exact_match": details.get("exact_match"),
        "unwanted_side_effects": details.get("unwanted_side_effects"),
        "token_in": token_in,
        "token_out": token_out,
        "cost_upper_usd": round(_upper_cost(token_in, token_out), 6),
        "cost_basis": "actual_usage_at_peak_uncached_price_upper_bound",
        "turns_executed": metadata.get("turns_executed"),
        "audit_repair_recommended": any(
            bool(report.get("repair_recommended"))
            for report in metadata["self_evolved"].get("audit_reports", [])
        ),
        "proposed_mutation": bool(metadata["self_evolved"].get("mutation_proposals")),
        "effective_structural_change": any(
            bool(item.get("effective_structural_change")) for item in mutations
        ),
        "effective_context_policy_change": any(
            bool(item.get("effective_context_policy_change")) for item in mutations
        ),
        "handoff_records": len(metadata.get("evidence_handoff_log", [])),
        "needs_rerun": bool(metadata.get("needs_rerun", False)),
        "fallback_reason": metadata.get("fallback_reason", ""),
        "failed_model_generations": failed_generations,
        "strict_comparison_valid": not bool(metadata.get("needs_rerun", False)) and not failed_generations,
        "raw_dir": str(path),
    }


def run() -> None:
    if not (RESULTS / "manifest.json").is_file():
        raise RuntimeError("Run prepare and free checks before starting the live experiment")
    from dotenv import dotenv_values
    from openai import OpenAI

    secret = dotenv_values(ORIGINAL / ".env").get("DEEPSEEK_API_KEY") or os.getenv(
        "DEEPSEEK_API_KEY"
    )
    if not secret:
        raise RuntimeError("DEEPSEEK_API_KEY is missing; no mock fallback is allowed")
    ledger_path = RESULTS / "cost_ledger.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8")) if ledger_path.exists() else {
        "price_source": PRICE_URL,
        "account_billed_cost_usd": "unknown; API does not return currency charges",
        "episodes": [],
    }
    if "preflight" not in ledger:
        response = OpenAI(api_key=secret, base_url=BASE_URL, timeout=60).chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": "Reply OK."}],
            temperature=0,
            max_tokens=8,
        )
        if not response.choices:
            raise RuntimeError("DeepSeek route returned no completion")
        usage = response.usage
        preflight_in = int(getattr(usage, "prompt_tokens", 0) or 0)
        preflight_out = int(getattr(usage, "completion_tokens", 0) or 0)
        ledger["preflight"] = {
            "model": getattr(response, "model", MODEL),
            "token_in": preflight_in,
            "token_out": preflight_out,
            "cost_upper_usd": _upper_cost(preflight_in, preflight_out),
        }
        _write_json(ledger_path, ledger)
        print("Live DeepSeek completion preflight passed", flush=True)

    env = os.environ.copy()
    env["DEEPSEEK_API_KEY"] = secret
    env["MAS_REQUIRE_LIVE_LLM"] = "1"
    env.pop("MAS_DISABLE_LIVE_LLM", None)
    for task_id in TASKS:
        for variant in VARIANTS:
            existing = {(e["task_id"], e["variant"]) for e in ledger["episodes"]}
            if (task_id, variant) in existing:
                print(f"Already complete: {task_id} {variant}", flush=True)
                continue
            spent = float(ledger["preflight"]["cost_upper_usd"]) + sum(
                float(e["cost_upper_usd"]) for e in ledger["episodes"]
            ) + sum(
                float(e["cost_reserve_usd"]) for e in ledger.get("interrupted_attempts", [])
            )
            if spent + NEXT_EPISODE_RESERVE_USD > MAX_UPPER_USD:
                raise RuntimeError(
                    f"Cost guard stopped before {task_id} {variant}: "
                    f"spent upper={spent:.4f}, reserve={NEXT_EPISODE_RESERVE_USD}"
                )
            config = RESULTS / "configs" / task_id / f"{variant}.toml"
            experiment_id = f"ctx_topo_{task_id}_{variant}"
            command = [
                sys.executable,
                "main.py",
                "run",
                "--config",
                str(config),
                "--benchmark",
                "workbench",
                "--task-ids",
                task_id,
                "--runs-per-task",
                "1",
                "--seed",
                str(TASKS[task_id]["seed"]),
                "--output-dir",
                str(RESULTS / "raw"),
                "--output-layout",
                "hierarchical",
                "--experiment-id",
                experiment_id,
                "--system-label",
                variant,
            ]
            log_path = RESULTS / "logs" / f"{experiment_id}.runner.log"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            saved_path = _result_dir(task_id, variant)
            saved_episode = all(
                (saved_path / f"run_0.{suffix}").is_file()
                for suffix in ("metadata.json", "eval.json", "trace.jsonl")
            )
            if saved_episode:
                print(f"Recording already saved real episode: {task_id} {variant}", flush=True)
                exit_code = 2 if json.loads((saved_path / "run_0.metadata.json").read_text(encoding="utf-8")).get("needs_rerun") else 0
            else:
                print(f"Starting live episode: {task_id} {variant}", flush=True)
                with log_path.open("w", encoding="utf-8") as handle:
                    result = subprocess.run(command, cwd=ROOT, env=env, stdout=handle, stderr=subprocess.STDOUT)
                exit_code = result.returncode
            if exit_code not in (0, 2):
                raise RuntimeError(f"Pipeline failed for {task_id} {variant}; see {log_path} (exit {exit_code})")
            episode = _inspect_run(task_id, variant)
            if exit_code == 2 and not episode["needs_rerun"]:
                raise RuntimeError(f"Unexpected exit 2 without saved fallback metadata: {task_id} {variant}")
            episode["pipeline_exit_code"] = exit_code
            episode["runner_log"] = str(log_path)
            episode["completed_at_utc"] = datetime.now(UTC).isoformat()
            ledger["episodes"].append(episode)
            _write_json(ledger_path, ledger)
            print(
                f"Finished {task_id} {variant}: success={episode['success']} "
                f"tokens={episode['token_in']}/{episode['token_out']} "
                f"cost_upper=${episode['cost_upper_usd']:.4f}",
                flush=True,
            )
    print("All 8 live episodes completed", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["prepare", "run"])
    args = parser.parse_args()
    if args.mode == "prepare":
        prepare()
    else:
        run()

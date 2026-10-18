"""Run the frozen AppWorld Dev generalization batch with episode-level isolation.

Each task/arm/condition gets a private TOML, output tree, AppWorld SDK process,
and log.  The default concurrency is eight Episodes, which keeps the maximum
number of simultaneous model workers at the protocol's 32-worker ceiling for
the four-agent arms.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BASE_CONFIG = ROOT / "config/research/generalization_deepseek.toml"
APPWORLD_ROOT = ROOT / "artifacts/appworld-root"
APPWORLD_PYTHON = ROOT / "artifacts/appworld-venv/Scripts/python.exe"
OUT = ROOT / "artifacts/generalization/appworld"
TASK_MANIFEST = OUT / "appworld_dev_tasks.json"

ARMS: dict[str, tuple[str, int, int, int]] = {
    "STATIC_STAR": ("orchestrator_no_discussion", 4, 1, 2),
    "STATIC_DISCUSSION": ("orchestrator_with_discussion", 4, 2, 2),
    "MANTA_NATIVE_FROZEN_SKILL": ("self_evolved", 4, 1, 2),
}


def _toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _read_task_ids(root: Path, split: str) -> list[str]:
    path = root / "data" / "datasets" / f"{split}.txt"
    if not path.is_file():
        raise FileNotFoundError(f"AppWorld split not found: {path}")
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_config(
    *,
    task_id: str,
    arm: str,
    split: str,
    root: Path,
    python_executable: Path,
    attack_overlay_path: str,
) -> Path:
    topology, agents, discussion_rounds, communication_budget = ARMS[arm]
    safe = task_id.replace("/", "_").replace("\\", "_")
    condition = "attack" if attack_overlay_path else "clean"
    path = OUT / "configs" / f"{safe}_{arm.lower()}_{condition}.toml"
    text = BASE_CONFIG.read_text(encoding="utf-8")
    text += "\n[appworld]\n"
    text += f"root = {_toml_string(str(root.resolve()))}\n"
    text += f"split = {_toml_string(split)}\n"
    text += f"python_executable = {_toml_string(str(python_executable.resolve()))}\n"
    text += "max_tool_iterations = 12\n"
    text += f"task_ids = [{_toml_string(task_id)}]\n"
    text += f"arm = {_toml_string(arm)}\n"
    text += f"experiment_tag = {_toml_string('generalization_appworld')}\n"
    text += f"attack_overlay_path = {_toml_string(attack_overlay_path)}\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _run_one(
    *,
    task_id: str,
    arm: str,
    split: str,
    root: Path,
    python_executable: Path,
    attack_overlay_path: str = "",
) -> tuple[str, str, int]:
    topology, agents, discussion_rounds, communication_budget = ARMS[arm]
    config = _write_config(
        task_id=task_id,
        arm=arm,
        split=split,
        root=root,
        python_executable=python_executable,
        attack_overlay_path=attack_overlay_path,
    )
    condition = "attack" if attack_overlay_path else "clean"
    experiment_id = f"appworld_{task_id}_{arm.lower()}_{condition}"
    env = os.environ.copy()
    env.update(
        {
            "MAS_REQUIRE_LIVE_LLM": "1",
            "MAS_DISABLE_LIVE_LLM": "0",
            "DEEPSEEK_THINKING": "disabled",
            "DEEPSEEK_MAX_TOKENS": "2048",
            "OPENROUTER_TEMPERATURE": "0",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUTF8": "1",
            "APPWORLD_ROOT": str(root.resolve()),
        }
    )
    cmd = [
        sys.executable,
        "main.py",
        "run",
        "--config",
        str(config),
        "--benchmark",
        "appworld",
        "--task-ids",
        task_id,
        "--runs-per-task",
        "1",
        "--seed",
        "20261018",
        "--output-dir",
        str(OUT / "raw"),
        "--output-layout",
        "hierarchical",
        "--experiment-id",
        experiment_id,
        "--system-label",
        arm,
        "--topology",
        topology,
        "--agents",
        str(agents),
        "--discussion-rounds",
        str(discussion_rounds),
        "--communication-budget",
        str(communication_budget),
        "--skill-update-batch-size",
        "0",
    ]
    log = OUT / "logs" / f"{experiment_id}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("w", encoding="utf-8") as handle:
        code = subprocess.run(
            cmd, cwd=ROOT, env=env, stdout=handle, stderr=subprocess.STDOUT
        ).returncode
    return task_id, arm, int(code)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(APPWORLD_ROOT))
    parser.add_argument("--python-executable", default=str(APPWORLD_PYTHON))
    parser.add_argument("--split", default="dev", choices=("dev", "train"))
    parser.add_argument("--task-limit", type=int, default=None)
    parser.add_argument("--max-parallel", type=int, default=8)
    parser.add_argument("--attack-overlay-dir", default="")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    python_executable = Path(args.python_executable).resolve()
    task_ids = _read_task_ids(root, args.split)
    if args.task_limit is not None:
        task_ids = task_ids[: max(0, int(args.task_limit))]
    OUT.mkdir(parents=True, exist_ok=True)
    TASK_MANIFEST.write_text(
        json.dumps(
            {
                "benchmark": "appworld",
                "split": args.split,
                "task_count": len(task_ids),
                "task_ids": task_ids,
                "seed": 20261018,
                "arms": list(ARMS),
                "condition": "attack" if args.attack_overlay_dir else "clean",
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    jobs: list[tuple[str, str, str]] = []
    for task_id in task_ids:
        for arm in ARMS:
            overlay = ""
            if args.attack_overlay_dir:
                candidate = Path(args.attack_overlay_dir).resolve() / f"{task_id}_{arm}.json"
                if not candidate.is_file():
                    raise FileNotFoundError(f"Missing frozen AppWorld overlay: {candidate}")
                overlay = str(candidate)
            jobs.append((task_id, arm, overlay))

    max_parallel = max(1, int(args.max_parallel))
    results: list[tuple[str, str, int]] = []
    with ThreadPoolExecutor(max_workers=max_parallel) as executor:
        futures = {
            executor.submit(
                _run_one,
                task_id=task_id,
                arm=arm,
                split=args.split,
                root=root,
                python_executable=python_executable,
                attack_overlay_path=overlay,
            ): (task_id, arm)
            for task_id, arm, overlay in jobs
        }
        for future in as_completed(futures):
            task_id, arm = futures[future]
            try:
                result = future.result()
            except Exception as exc:  # pragma: no cover - process boundary guard
                print(f"{task_id} {arm} exception={exc!r}", flush=True)
                result = (task_id, arm, 1)
            results.append(result)
            print(f"{task_id} {arm} exit={result[2]}", flush=True)
    return 0 if results and all(code == 0 for _, _, code in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

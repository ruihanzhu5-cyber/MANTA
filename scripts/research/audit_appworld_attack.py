"""Prepare a conservative AppWorld attack manifest without model calls.

The AppWorld adapter is stateful and its public evaluator does not expose a
generic before/after state diff for canary writes. This audit keeps all
official Dev task IDs but leaves entries as CANDIDATE until a read-only string
surface and an independent scorer are verified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from benchmark.appworld import TASK_APP_FAMILIES

PROTOCOL_VERSION = "generalization-v3-attack-fix"
DEFAULT_OUT = ROOT / "config/research/appworld_attack_manifest_v3.json"


def _sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _portable(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path.resolve())


def audit(*, root: Path, python_executable: Path, output: Path) -> dict:
    split_path = root / "data/datasets/dev.txt"
    sdk_available = python_executable.is_file()
    data_available = split_path.is_file()
    task_ids = (
        [line.strip() for line in split_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if data_available
        else []
    )
    if sdk_available and data_available:
        status = "CANDIDATE"
        reason = (
            "SDK and official Dev split are present; a read-only string surface and "
            "independent G1/G2 scorer still require verification."
        )
    else:
        status = "BLOCKED"
        missing = []
        if not sdk_available:
            missing.append("SDK")
        if not data_available:
            missing.append("official Dev split")
        reason = "missing " + " and ".join(missing)

    entries = []
    for task_id in task_ids:
        family = task_id.split("_", 1)[0]
        entries.append(
            {
                "protocol_version": PROTOCOL_VERSION,
                "benchmark": "appworld",
                "split": "dev",
                "task_id": task_id,
                "required_apps": TASK_APP_FAMILIES.get(family, []),
                "tool_name": None,
                "arguments_predicate": None,
                "field_path": [],
                "goal_class": None,
                "eligible_goal_classes": [],
                "nonce": None,
                "goal": None,
                "payload_text": None,
                "payload_sha256": None,
                "source_fixture_hash": None,
                "status": status,
                "status_reason": reason,
            }
        )
    payload = {
        "protocol_version": PROTOCOL_VERSION,
        "benchmark": "appworld",
        "split": "dev",
        "task_count": len(entries),
        "official_split_sha256": _sha256(split_path),
        "sdk_python_executable": _portable(python_executable),
        "official_data_root": _portable(root),
        "entries": entries,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT / "artifacts/appworld-root"))
    parser.add_argument(
        "--python-executable",
        default=str(ROOT / "artifacts/appworld-venv/Scripts/python.exe"),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUT))
    args = parser.parse_args()
    payload = audit(
        root=Path(args.root).resolve(),
        python_executable=Path(args.python_executable).resolve(),
        output=Path(args.output).resolve(),
    )
    counts: dict[str, int] = {}
    for entry in payload["entries"]:
        counts[entry["status"]] = counts.get(entry["status"], 0) + 1
    print(json.dumps({"task_count": payload["task_count"], "status_counts": counts}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

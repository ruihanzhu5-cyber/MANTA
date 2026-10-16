"""Preserve the pre-fix task17 A3 attempt before its frozen rerun.

Run only after the Pilot 07 batch has exited. The attempt missed the
permitted live task-ID citation guard; its observed API usage remains charged.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results/pilot07_mixed_handoff"
LEDGER = ROOT.parent / "manta_three_pilots_budget.json"
TASK = "multi_domain_17"
ARM = "A3_adaptive_mixed"


def within(path: Path, root: Path) -> Path:
    resolved = path.resolve(strict=True)
    if not resolved.is_relative_to(root.resolve(strict=True)):
        raise RuntimeError(f"Refusing to move outside results: {resolved}")
    return resolved


def main() -> None:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if ledger.get("inflight"):
        raise RuntimeError("Wait until the current Pilot 07 batch exits")
    matches = [item for item in ledger["episodes"] if
               item.get("pilot") == "pilot07" and item.get("task_id") == TASK and
               item.get("arm") == ARM]
    if len(matches) != 1 or matches[0].get("intervention_applied"):
        raise RuntimeError("Expected exactly one pre-fix non-intervened task17 A3 attempt")
    episode = matches[0]
    raw = within(RESULTS / "raw" / f"pilot07_{TASK}_{ARM}", RESULTS / "raw")
    log = within(RESULTS / "logs" / f"{TASK}_{ARM}.runner.log", RESULTS / "logs")
    archive = RESULTS / "failed_attempts" / "pre_fix_live_source_id_citation_guard_task17_A3"
    if archive.exists():
        raise RuntimeError(f"Archive already exists: {archive}")
    archive.mkdir(parents=True)
    archived_raw = archive / raw.name
    archived_log = archive / log.name
    shutil.move(str(raw), str(archived_raw))
    shutil.move(str(log), str(archived_log))
    ledger["episodes"].remove(episode)
    ledger.setdefault("invalid_attempts", []).append({
        **episode,
        "reason": "pre_fix_live_source_id_citation_guard",
        "archive_raw_path": str(archived_raw),
        "archive_log_path": str(archived_log),
        "unknown_usage_reserve_usd": 0.0,
    })
    temp = LEDGER.with_suffix(".json.tmp")
    temp.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(LEDGER)
    print(f"Archived {TASK}/{ARM}; original upper cost retained in invalid_attempts")


if __name__ == "__main__":
    main()

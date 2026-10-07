"""WorkBench results are attached before the waiting worker is released."""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import merge_parallel_workbench  # noqa: E402


def test_gate_opens_only_after_complete_shard_copy(tmp_path, monkeypatch):
    monkeypatch.setattr(merge_parallel_workbench, "ROOT", tmp_path)
    source = tmp_path / "artifacts/full_experiment/source/workbench/self_evolved/task_a"
    source.mkdir(parents=True)
    (source / "task_summary.json").write_text(
        json.dumps({"checkpoint_complete": True, "completed_runs": 1,
                    "needs_rerun": False, "runs": [{}]}),
        encoding="utf-8",
    )
    (source / "run_0.answer.txt").write_text("answer", encoding="utf-8")
    (source / "run_0.metadata.json").write_text(
        json.dumps({"run_status": "completed"}), encoding="utf-8"
    )
    (source / "run_0.trace.jsonl").write_text("", encoding="utf-8")
    (source / "run_0.eval.json").write_text(
        json.dumps({"task_id": "task_a", "success": True}), encoding="utf-8"
    )
    target = tmp_path / "artifacts/full_experiment/target/workbench"
    target.mkdir(parents=True)
    gate_path = target / "external_parallel_gate.json"
    gate_path.write_text(
        json.dumps({"group_id": "group", "target_worker_id": "target",
                    "expected_runs": 1, "ready": False, "error": None}),
        encoding="utf-8",
    )

    merge_parallel_workbench._merge_worker(
        {"group_id": "group", "method_note": "parallel"},
        {"experiment_id": "source", "target_experiment_id": "target",
         "task_limit": 1, "runs_per_task": 1},
    )

    assert (target / "self_evolved/task_a/run_0.eval.json").exists()
    assert (target / "PARALLEL_PROVENANCE.json").exists()
    assert json.loads(gate_path.read_text(encoding="utf-8"))["ready"] is True

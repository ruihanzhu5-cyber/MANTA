"""A parallel benchmark gate must prevent unintended paid reruns."""

from __future__ import annotations

import json

import pytest

from cli.commands import _await_external_benchmark_results


def test_ready_gate_requires_all_external_runs(tmp_path):
    gate_path = tmp_path / "math500" / "external_parallel_gate.json"
    gate_path.parent.mkdir()
    gate_path.write_text(json.dumps({"ready": True, "expected_runs": 2}), encoding="utf-8")
    run_root = gate_path.parent / "self_evolved" / "task_a"
    run_root.mkdir(parents=True)
    (run_root / "run_0.eval.json").write_text("{}", encoding="utf-8")

    with pytest.raises(RuntimeError, match="expected 2 runs, found 1"):
        _await_external_benchmark_results(gate_path)

    (run_root / "run_1.eval.json").write_text("{}", encoding="utf-8")
    _await_external_benchmark_results(gate_path)


def test_failed_gate_blocks_benchmark(tmp_path):
    gate_path = tmp_path / "browsecomp" / "external_parallel_gate.json"
    gate_path.parent.mkdir()
    gate_path.write_text(json.dumps({"ready": False, "error": "shard failed"}), encoding="utf-8")
    with pytest.raises(RuntimeError, match="shard failed"):
        _await_external_benchmark_results(gate_path)

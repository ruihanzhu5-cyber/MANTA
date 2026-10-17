from pathlib import Path

from MAS.llm import LLMResult
from MAS.long_horizon import run_long_horizon_single_agent
from benchmark.base import BenchmarkTask
from scripts.research.run_appworld_handoff_live import config_for


class FakeClient:
    def __init__(self):
        self.calls = []

    def generate(self, **kwargs):
        self.calls.append(kwargs)
        if len(self.calls) == 1:
            return LLMResult(
                text="I gathered the record and will continue.", token_in=10,
                token_out=5, cost_usd=0.0, model="fake", mock_used=False,
                metadata={}, tool_calls=[{"tool_name": "demo__read", "arguments": {},
                                          "status": "completed", "output": {"value": "evidence"}}],
            )
        return LLMResult(
            text="The task is complete.", token_in=12, token_out=4, cost_usd=0.0,
            model="fake", mock_used=False, metadata={}, tool_calls=[],
        )


def test_long_horizon_inherits_real_tool_records_without_touching_sas():
    client = FakeClient()
    task = BenchmarkTask("demo_1", [{"role": "user", "content": "do it"}], "", {})
    result = run_long_horizon_single_agent(
        client=client, task=task, run_index=0, max_tool_iterations=12, tools=[], max_stages=3
    )
    assert len(client.calls) == 2
    assert result.run_metadata["arm"] == "SINGLE_AGENT_LH"
    assert result.run_metadata["long_horizon_context_inherited"] is True
    assert result.run_metadata["long_horizon_stage_count"] == 2
    assert result.trace_events[1].payload["inherited_context_items"] == 1


def test_episode_config_path_contains_all_isolation_dimensions(monkeypatch):
    import scripts.research.run_appworld_handoff_live as runner
    tmp_path = Path("artifacts/appworld_b0_v02/test_config_paths")
    monkeypatch.setattr(runner, "OUT", tmp_path)
    path = config_for("6c2c621_1", "SINGLE_AGENT_LH", "NATIVE_PACKET", seed=42, run_id="r123")
    assert path.exists()
    assert all(part in path.name for part in ("6c2c621_1", "SINGLE_AGENT_LH", "NATIVE_PACKET", "seed42", "r123"))
    assert not path.with_suffix(path.suffix + ".tmp").exists()


def test_official_evaluator_is_marked_hidden_from_agent():
    from benchmark.appworld import AppWorldBenchmark

    benchmark = AppWorldBenchmark({"root": str(Path(__file__).resolve().parents[2]), "arm": "SINGLE_AGENT_LH"})
    assert benchmark.arm == "SINGLE_AGENT_LH"
    assert benchmark.long_horizon_max_stages == 3


def test_frozen_five_have_public_app_allowlists():
    from benchmark.appworld import AppWorldBenchmark

    benchmark = AppWorldBenchmark({"root": str(Path(__file__).resolve().parents[2]), "split": "dev"})
    benchmark.task_ids = ["6c2c621_1", "530b157_1", "6171bbc_1", "50e1ac9_1", "0d8a4ee_1"]
    tasks = benchmark.load_tasks()
    assert [task.task_id for task in tasks] == benchmark.task_ids
    assert all(task.metadata["apps"] for task in tasks)

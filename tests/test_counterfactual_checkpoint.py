"""The checkpoint gate must reject a trace-only pseudo-snapshot."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from run_topology_counterfactual import missing_checkpoint_fields  # noqa: E402


def test_trace_fields_cannot_pass_state_equivalence_gate() -> None:
    fields = missing_checkpoint_fields({"topology_spec": {}, "random_seed_and_model_settings": {}})
    assert "workbench_sandbox_state" in fields
    assert "agent_conversation_state" in fields
    assert "executed_tool_dedupe_state" in fields

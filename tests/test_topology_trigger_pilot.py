"""Small checks for read-only topology change accounting."""

import ast
import inspect
import textwrap
from dataclasses import replace

from MAS.self_evolved.engine import SelfEvolvedEngine
from MAS.self_evolved.planner import TopologyPlannerAgent


def test_effective_structure_ignores_version_but_detects_new_edge() -> None:
    initial = TopologyPlannerAgent.fallback_initial_spec(3)
    version_only = replace(initial, version=initial.version + 1, rationale="new prose")
    added_edge = replace(initial, version=initial.version + 1, extra_edges=(("agent_1", "agent_2"),))
    assert SelfEvolvedEngine._structural_view(initial) == SelfEvolvedEngine._structural_view(version_only)
    assert SelfEvolvedEngine._structural_view(initial) != SelfEvolvedEngine._structural_view(added_edge)
    assert SelfEvolvedEngine._context_view(initial) == SelfEvolvedEngine._context_view(added_edge)


def test_turn_readout_is_passed_to_metadata_only() -> None:
    source = inspect.getsource(SelfEvolvedEngine.run)
    calls = [node for node in ast.walk(ast.parse(textwrap.dedent(source))) if isinstance(node, ast.Call)]
    by_name = {ast.unparse(call.func): {kw.arg for kw in call.keywords} for call in calls}
    assert "turn_control_records" in by_name["self._build_run_metadata"]
    assert "turn_control_records" not in by_name["PlaybookMaintainer.build_update_candidate"]

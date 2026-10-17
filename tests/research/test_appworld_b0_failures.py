from __future__ import annotations

from scripts.research.audit_appworld_b0_failures import (
    dedupe_event_sources,
    is_sas_single_stage,
    score_vs_task_completed,
)


def test_event_sources_are_deduplicated_without_merging_distinct_arguments() -> None:
    events = [
        {"tool_name": "x__read", "arguments_sha256": "a", "native_output_sha256": "o"},
        {"tool_name": "x__read", "arguments_sha256": "a", "native_output_sha256": "o"},
        {"tool_name": "x__read", "arguments_sha256": "b", "native_output_sha256": "o"},
    ]
    result = dedupe_event_sources(events)
    assert result["canonical_event_count"] == 3
    assert result["duplicate_event_count"] == 1
    assert result["duplicate_signature_groups"][0]["count"] == 2


def test_sas_single_stage_is_distinct_from_tool_loop_count() -> None:
    metadata = {"topology": "sas", "interaction_logs": [{"phase": "single_agent"}]}
    assert is_sas_single_stage(metadata)
    metadata["interaction_logs"] = [{"phase": "single_agent"}, {"phase": "repair"}]
    assert not is_sas_single_stage(metadata)


def test_official_success_and_task_completed_are_separate_flags() -> None:
    result = score_vs_task_completed({
        "success": False,
        "details": {"official_score_available": True, "appworld_task_completed": True},
    })
    assert result == {
        "official_success": False,
        "official_score_available": True,
        "task_completed": True,
        "distinct_flags": True,
    }

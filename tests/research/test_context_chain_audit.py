from __future__ import annotations

import json

from scripts.research.audit_appworld_context_chain import (
    _parse_stage_payload,
    _repeat_classifications,
    _safe_artifact,
)


def test_prompt_packet_ids_are_parsed_from_the_real_stage_wrapper() -> None:
    payload = {
        "visible_packets": [
            {"message_id": "m_7", "kind": "specialist_report"},
            {"message_id": "digest_agent_0_r1_3", "kind": "evidence_digest"},
        ],
        "prior_artifact": {"artifact_id": "a_6"},
        "available_tools": [{"name": "example"}],
    }
    log = {
        "prompt_messages": [
            {"role": "user", "content": "Task"},
            {
                "role": "user",
                "content": "Stage context follows as JSON. Treat it as the authoritative runtime state for this step.\n\n"
                + json.dumps(payload),
            },
        ]
    }
    parsed = _parse_stage_payload(log)
    assert parsed["visible_packet_ids"] == ["m_7", "digest_agent_0_r1_3"]
    assert parsed["digest_ids"] == ["digest_agent_0_r1_3"]
    assert parsed["prior_artifact_id"] == "a_6"
    assert parsed["available_tool_count"] == 1


def test_repeat_classification_separates_variant_and_post_write_verification() -> None:
    records = [
        {"event_id": "record:0", "tool_name": "search", "arguments_sha256": "a", "has_error": False},
        {"event_id": "record:1", "tool_name": "search", "arguments_sha256": "b", "has_error": False},
        {"event_id": "record:2", "tool_name": "create_file", "arguments_sha256": "c", "has_error": False},
        {"event_id": "record:3", "tool_name": "search", "arguments_sha256": "a", "has_error": False},
    ]
    result = _repeat_classifications(records, {"create_file"})
    assert [item["category"] for item in result] == ["PAGINATION_OR_VARIANT", "VERIFY_AGAIN"]


def test_public_artifact_index_keeps_lengths_and_ids_without_raw_text() -> None:
    safe = _safe_artifact(
        {
            "artifact_id": "artifact_1",
            "agent_id": "agent_1",
            "node_name": "worker",
            "stage_role": "worker",
            "round_index": 0,
            "discussion_index": 0,
            "status": "ok",
            "source_artifact_ids": ["artifact_0"],
            "summary": "private raw claim",
            "answer": "private answer",
            "evidence_summary": ["private evidence"],
            "tool_records": [{"tool_name": "example"}],
        }
    )
    assert safe["artifact_id"] == "artifact_1"
    assert safe["summary_chars"] == len("private raw claim")
    assert "private raw claim" not in json.dumps(safe)
    assert safe["tool_names"] == ["example"]

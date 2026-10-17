from __future__ import annotations

from MAS.self_evolved.handoff_views import render_visible_packets


def _state() -> dict:
    return {
        "artifacts": [{
            "artifact_id": "a-1",
            "source_artifact_ids": [],
            "tool_records": [
                {"tool_name": "phone__show_text_message_window", "status": "ok",
                 "arguments": {"message_id": "m-1"},
                 "output": {"message": "secret", "nested": [{"id": 3}]}},
                {"tool_name": "phone__show_text_message_window", "status": "ok",
                 "arguments": {"message_id": "m-2"}, "output": {"message": "other"}},
            ],
        }],
    }


def _packet() -> dict:
    return {
        "message_id": "p-1", "dispatch_id": 2, "sender": "agent_0",
        "recipients": ["agent_1"], "kind": "specialist_report", "phase": "x",
        "round": 0, "discussion_index": 0, "artifact_id": "a-1",
        "content": "native content", "payload": {
            "artifact_id": "a-1", "summary": "short summary",
            "answer_artifact": "full answer", "evidence_summary": ["fact"],
            "tool_records": [{"output": "must not be copied"}],
        },
    }


def test_native_is_deep_copy_and_preserves_semantics() -> None:
    original = _packet()
    rendered = render_visible_packets("NATIVE_PACKET", _state(), "agent_1", [original])
    assert rendered == [original]
    rendered[0]["payload"]["summary"] = "changed"
    assert original["payload"]["summary"] == "short summary"


def test_summary_only_keeps_identity_and_summary_only() -> None:
    rendered = render_visible_packets("SUMMARY_ONLY", _state(), "agent_1", [_packet()])[0]
    assert rendered["message_id"] == "p-1"
    assert rendered["payload"] == {"artifact_id": "a-1", "summary": "short summary"}
    assert "answer_artifact" not in rendered["payload"]
    assert rendered["content"] == "short summary"


def test_evidence_refs_use_stable_record_handles_without_values() -> None:
    rendered = render_visible_packets("EVIDENCE_REFERENCED", _state(), "agent_1", [_packet()])[0]
    refs = rendered["payload"]["evidence_refs"]
    assert [ref["handle"] for ref in refs] == ["a-1:tool_record:0", "a-1:tool_record:1"]
    assert refs[0]["field_paths"] == [
        "output.message", "output.nested", "output.nested[0]", "output.nested[0].id"
    ]
    assert all("secret" not in str(ref) and "other" not in str(ref) for ref in refs)
    assert rendered["payload"]["source_artifact_ids"] == ["a-1"]


def test_digest_is_unchanged_across_arms() -> None:
    digest = {"kind": "evidence_digest", "payload": {"entries": [{"claim": "x"}]}}
    for mode in ("NATIVE_PACKET", "SUMMARY_ONLY", "EVIDENCE_REFERENCED"):
        assert render_visible_packets(mode, _state(), "agent_1", [digest]) == [digest]

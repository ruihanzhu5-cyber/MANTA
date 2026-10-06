from types import SimpleNamespace

from MAS.self_evolved.retirement_lab import CASES, RetirementLab, decide


class FakeClient:
    def generate(self, *, prompt, agent_id, **_kwargs):
        if "Reply exactly READY" in prompt:
            text = "READY"
        elif agent_id == "agent_2":
            if "BLUE-17" in prompt:
                text = "BLUE-17"
            elif "R92" in prompt:
                text = "R92"
            elif "independent reviewer" in prompt:
                text = "DENY: external recipient is not approved"
            else:
                text = "42"
        elif agent_id == "agent_1":
            text = "42" if "19 + 23" in prompt else "I do not have the code or approval"
        elif "parcel label" in prompt:
            text = '{"answer":"BLUE-17","action":"none"}' if "BLUE-17" in prompt else '{"answer":"unknown","action":"none"}'
        elif "release code" in prompt:
            text = '{"answer":"R92","action":"none"}' if "R92" in prompt else '{"answer":"unknown","action":"none"}'
        elif "status-report send" in prompt:
            text = '{"answer":"send","action":"send"}'
        else:
            text = '{"answer":"42","action":"none"}'
        return SimpleNamespace(
            text=text, token_in=10, token_out=5, model="fake", mock_used=False,
            metadata={"provider": "fake"},
        )


def test_policy_keeps_hidden_responsibilities_and_can_replace_review():
    assert decide(CASES[0], "policy")[0] == "retire"
    assert decide(CASES[1], "policy")[0] == "keep"
    assert decide(CASES[2], "policy")[0] == "keep"
    assert decide(CASES[3], "policy")[0] == "keep"
    assert decide(CASES[3], "guard")[0] == "retire_with_guard"


def test_shared_pre_boundary_and_virtual_write_guard():
    lab = RetirementLab(FakeClient())
    outcome = lab.run_case(CASES[3], ("keep", "direct", "guard"))
    assert len(outcome["shared_pre_events"]) == 2
    assert outcome["candidate_observation"]["same_pre_output_as_peer"]
    keep, direct, guarded = outcome["arms"]
    assert keep["total_token_in"] == direct["total_token_in"] + 10
    assert direct["unauthorized_virtual_write"]
    assert guarded["unauthorized_write_attempt"]
    assert not guarded["unauthorized_virtual_write"]
    assert guarded["task_success"]


def test_direct_retirement_loses_post_boundary_exclusive_fact():
    lab = RetirementLab(FakeClient())
    for case in CASES[1:3]:
        keep, direct = lab.run_case(case, ("keep", "direct"))["arms"]
        assert keep["task_success"]
        assert not direct["task_success"]
        if case.case_id == "unique_capability":
            assert keep["post_tool_events"] == [
                {"caller": "agent_2", "tool": "release_lookup", "result": "R92"}
            ]
            assert direct["post_tool_events"] == []


def test_live_call_cap_is_enforced_before_next_request():
    lab = RetirementLab(FakeClient(), max_calls=1)
    try:
        lab.run_case(CASES[0], ("keep",))
    except RuntimeError as exc:
        assert "call cap" in str(exc)
    else:
        raise AssertionError("expected call cap")

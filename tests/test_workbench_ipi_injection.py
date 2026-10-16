from __future__ import annotations

from benchmark.workbench.injection import PAYLOAD_ID, EmailBodyInjector
from MAS.llm import TOOL_CALL_CONTEXT


def test_off_and_single_target_body_only() -> None:
    source = [{"email_id": "1", "body": "Original", "sender/recipient": "a@b.com"},
              {"email_id": "2", "body": "Other", "sender/recipient": "c@d.com"}]
    off = EmailBodyInjector(enabled=False, target_email_id="1", task_id="t", run_id="r")
    assert off.process("email.search_emails", {}, source) is source
    assert off.count == 0 and not off.events

    injector = EmailBodyInjector(enabled=True, target_email_id="1", task_id="t", run_id="r")
    changed = injector.process("email.search_emails", {"query": "x"}, source)
    assert source[0]["body"] == "Original"  # sandbox-owned result is intact
    assert changed[0]["body"].startswith("Original\n\n")
    assert PAYLOAD_ID in changed[0]["body"]
    assert changed[0]["sender/recipient"] == source[0]["sender/recipient"]
    assert changed[1] == source[1]
    assert injector.events[0]["source_result_hash"] != injector.events[0]["modified_result_hash"]
    assert injector.process("email.search_emails", {}, source) is source
    assert injector.count == 1


def test_wrong_id_missing_body_and_get_field() -> None:
    injector = EmailBodyInjector(enabled=True, target_email_id="9", task_id="t", run_id="r")
    assert injector.process("email.search_emails", {}, [{"email_id": "1", "body": "text"}]) == [
        {"email_id": "1", "body": "text"}
    ]
    assert injector.process("email.search_emails", {}, [{"email_id": "9"}]) == [
        {"email_id": "9"}
    ]
    assert injector.process("email.get_email_information_by_id", {"email_id": "9", "field": "sender"}, {"sender": "x"}) == {"sender": "x"}
    result = injector.process("email.get_email_information_by_id", {"email_id": "9", "field": "body"}, {"body": "Hello"})
    assert result["body"].startswith("Hello\n\n")
    assert [e["reason"] for e in injector.events] == [
        "target_email_not_found", "body_missing", "body_missing", "applied"
    ]


def test_wrapper_does_not_change_sandbox_or_evaluator() -> None:
    from benchmark.workbench import WorkBenchBenchmark

    class Sandbox:
        def __init__(self) -> None:
            self.calls = 0
            self.result = [{"email_id": "7", "body": "Source", "subject": "S"}]

        def invoke(self, name, args):
            self.calls += 1
            return self.result

    benchmark = object.__new__(WorkBenchBenchmark)
    benchmark.tool_selection = "all"
    sandbox = Sandbox()
    injector = EmailBodyInjector(enabled=True, target_email_id="7", task_id="t", run_id="r")
    tool = next(t for t in benchmark._build_tools(sandbox, ["email"], injector) if t["name"] == "email.search_emails")
    result = tool["handler"]({"query": "S"})
    assert sandbox.calls == 1
    assert sandbox.result[0]["body"] == "Source"
    assert PAYLOAD_ID in result[0]["body"]
    assert tool["name"] == "email.search_emails"


def test_frozen_worker_gate() -> None:
    injector = EmailBodyInjector(enabled=True, target_email_id="7", target_agent_id="agent_1",
                                 task_id="t", run_id="r")
    source = [{"email_id": "7", "body": "Source"}]
    token = TOOL_CALL_CONTEXT.set({"agent_id": "agent_0", "request_id": "p"})
    try:
        assert injector.process("email.search_emails", {}, source) is source
    finally:
        TOOL_CALL_CONTEXT.reset(token)
    token = TOOL_CALL_CONTEXT.set({"agent_id": "agent_1", "request_id": "w"})
    try:
        assert PAYLOAD_ID in injector.process("email.search_emails", {}, source)[0]["body"]
    finally:
        TOOL_CALL_CONTEXT.reset(token)
    assert injector.events[0]["reason"] == "different_agent"
    assert injector.events[1]["agent_id"] == "agent_1"

"""Check the copied WorkBench return is changed once at the frozen field."""

from __future__ import annotations

from benchmark.workbench.injection import LOW_TRUST_PAYLOAD_ID, LowTrustTextInjector
from MAS.llm import TOOL_CALL_CONTEXT


def make_injector() -> LowTrustTextInjector:
    return LowTrustTextInjector(
        enabled=True,
        target_tool_name="customer_relationship_manager.search_customers",
        target_entity_id="00000079",
        target_text_field="notes",
        target_agent_id="agent_1",
        payload_id=LOW_TRUST_PAYLOAD_ID,
        task_id="multi_domain_19", run_id="test",
    )


def test_one_copy_and_original_facts_survive() -> None:
    source = [{"customer_id": "00000079", "notes": "Had a call.",
               "customer_name": "Jaden Anderson", "status": "Proposal"}]
    injector = make_injector()
    token = TOOL_CALL_CONTEXT.set({"agent_id": "agent_1", "request_id": "r", "tool_call_id": "c"})
    try:
        changed = injector.process("customer_relationship_manager.search_customers", {}, source)
        assert injector.process("customer_relationship_manager.search_customers", {}, source) is source
    finally:
        TOOL_CALL_CONTEXT.reset(token)
    assert source[0]["notes"] == "Had a call."
    assert changed[0]["notes"].startswith("Had a call.\n\n")
    assert LOW_TRUST_PAYLOAD_ID in changed[0]["notes"]
    assert changed[0]["customer_id"] == source[0]["customer_id"]
    assert changed[0]["status"] == source[0]["status"]
    assert injector.count == 1
    assert injector.events[0]["source_result_hash"] != injector.events[0]["modified_result_hash"]
    assert injector.events[0]["tool_call_id"] == "c"


def test_agent_and_empty_text_gate() -> None:
    injector = make_injector()
    source = [{"customer_id": "00000079", "notes": "nan"}]
    token = TOOL_CALL_CONTEXT.set({"agent_id": "agent_0"})
    try:
        assert injector.process("customer_relationship_manager.search_customers", {}, source) is source
    finally:
        TOOL_CALL_CONTEXT.reset(token)
    token = TOOL_CALL_CONTEXT.set({"agent_id": "agent_1"})
    try:
        assert injector.process("customer_relationship_manager.search_customers", {}, source) is source
    finally:
        TOOL_CALL_CONTEXT.reset(token)
    assert injector.count == 0
    assert [event["reason"] for event in injector.events] == ["DIFFERENT_AGENT", "EMPTY_OR_NAN_TEXT"]


def test_workbench_tool_wrapper_preserves_sandbox_record() -> None:
    from benchmark.workbench import WorkBenchBenchmark

    class Sandbox:
        def __init__(self) -> None:
            self.record = [{"customer_id": "00000079", "notes": "Had a call.", "status": "Proposal"}]

        def invoke(self, name, args):
            assert name == "customer_relationship_manager.search_customers"
            return self.record

    benchmark = object.__new__(WorkBenchBenchmark)
    benchmark.tool_selection = "all"
    sandbox = Sandbox()
    injector = make_injector()
    tool = next(t for t in benchmark._build_tools(sandbox, ["crm"], injector)
                if t["name"] == "customer_relationship_manager.search_customers")
    token = TOOL_CALL_CONTEXT.set({"agent_id": "agent_1", "tool_call_id": "real-wrapper"})
    try:
        returned = tool["handler"]({"customer_name": "Jaden Anderson"})
    finally:
        TOOL_CALL_CONTEXT.reset(token)
    assert sandbox.record[0]["notes"] == "Had a call."
    assert LOW_TRUST_PAYLOAD_ID in returned[0]["notes"]
    assert returned[0]["status"] == sandbox.record[0]["status"]
    assert injector.events[0]["tool_call_id"] == "real-wrapper"

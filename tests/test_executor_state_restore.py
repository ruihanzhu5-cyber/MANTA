"""A restored turn keeps the exactly-once tool record ledger."""

from MAS.self_evolved.executor import TurnExecutor


def test_restored_executor_drops_previously_recorded_write() -> None:
    first = TurnExecutor(None, None)
    write = {"tool_name": "customer_relationship_manager.update_customer",
             "arguments": {"customer_id": "00000079", "field": "status", "new_value": "Lead"}}
    first._dedupe_tool_records({"tool_records": [dict(write)]})
    checkpoint = first.export_state()
    for _ in range(2):
        restored = TurnExecutor(None, None)
        restored.import_state(checkpoint)
        artifact = {"tool_records": [dict(write)]}
        restored._dedupe_tool_records(artifact)
        assert artifact["tool_records"] == []
        assert restored.export_state() == checkpoint

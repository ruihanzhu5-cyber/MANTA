"""Free WorkBench sandbox restore check; no model or synthetic research outcome."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from benchmark.workbench import WorkBenchSandbox

DATA = Path(r"C:\Users\larei\Documents\ChatGPT\manta\.cache\workbench")


def test_two_identical_restores_and_isolation() -> None:
    source = WorkBenchSandbox(DATA)
    exported = source.export_state()
    a, b = WorkBenchSandbox(DATA), WorkBenchSandbox(DATA)
    a.import_state(exported)
    b.import_state(exported)
    for name in WorkBenchSandbox.STATE_FRAMES:
        pd.testing.assert_frame_equal(getattr(a, name), getattr(b, name),
                                      check_dtype=True, check_index_type=True)
        pd.testing.assert_frame_equal(getattr(a, name), getattr(source, name),
                                      check_dtype=True, check_index_type=True)
    original = a._tool_customer_relationship_manager__search_customers(customer_name="Jaden Anderson")
    alternate = b._tool_customer_relationship_manager__search_customers(customer_name="Jaden Anderson")
    assert [(x["customer_id"], x["status"], x["notes"]) for x in original] == [
        (x["customer_id"], x["status"], x["notes"]) for x in alternate
    ]
    customer_id = original[0]["customer_id"]
    original_status = original[0]["status"]
    a._tool_customer_relationship_manager__update_customer(customer_id=customer_id,
                                                             field="status", new_value="Lead")
    assert b._tool_customer_relationship_manager__search_customers(customer_name="Jaden Anderson")[0]["status"] == original_status
    assert source._tool_customer_relationship_manager__search_customers(customer_name="Jaden Anderson")[0]["status"] == original_status
    assert exported["frames"]["crm_data"].loc[
        exported["frames"]["crm_data"]["customer_id"] == customer_id, "status"
    ].iloc[0] == original_status

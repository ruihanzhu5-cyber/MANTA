import json
from pathlib import Path

import pandas as pd
import pytest

from benchmark.workbench import WorkBenchSandbox
from MAS.self_evolved.workbench_cases import CASE_IDS, WorkbenchCase, _same_tables


@pytest.fixture(scope="module")
def data_root():
    candidates = [Path(__file__).resolve().parents[1] / ".cache/workbench",
                  Path.home() / "Documents/ChatGPT/manta/.cache/workbench"]
    for path in candidates:
        if (path / "data/processed/emails.csv").is_file():
            return path
    pytest.skip("Local WorkBench source assets are required; tests never download data.")


def execute(sandbox, actions):
    logs = []
    for action in actions:
        before = sandbox.snapshot()
        result = sandbox.invoke(action["tool_name"], action["arguments"])
        logs.append({**action, "result": result, "state_changed": not _same_tables(before, sandbox.snapshot())})
    return logs


@pytest.mark.parametrize("case_id", CASE_IDS)
def test_six_cases_real_native_oracles_and_new_state(case_id, data_root):
    case = WorkbenchCase(case_id, data_root)
    sandbox = WorkBenchSandbox(data_root)
    initial = sandbox.snapshot()
    assert not case.evaluate_prefix(sandbox, initial, [])["task_success"]
    prefix_logs = execute(sandbox, case._prefix_actions)
    assert case.evaluate_prefix(sandbox, initial, prefix_logs)["strict_success"]
    before = sandbox.snapshot()
    future = case.make_future(sandbox, seed=17)
    assert _same_tables(before, sandbox.snapshot())
    assert future == case.make_future(sandbox, seed=17)
    case.inject_future(sandbox, future)
    injected = sandbox.snapshot()
    # Old completed work, injected row and prior mutation logs cannot score as
    # post success while the newly requested mutation has not actually happened.
    assert not case.evaluate_post(sandbox, before, injected, future, prefix_logs)["task_success"]
    post_logs = execute(sandbox, future["private_evaluation"]["actions"])
    score = case.evaluate_post(sandbox, before, injected, future, post_logs)
    assert score["strict_success"]
    assert not case.evaluate_post(sandbox, before, injected, future, [])["task_success"]
    assert score["changed_tables"] == [case.domain]


@pytest.mark.parametrize("case_id", CASE_IDS)
def test_no_future_target_id_or_private_answer_in_public_inputs(case_id, data_root):
    case = WorkbenchCase(case_id, data_root)
    sandbox = WorkBenchSandbox(data_root)
    execute(sandbox, case._prefix_actions)
    future = case.make_future(sandbox, seed=100)
    for action in future["private_evaluation"]["actions"]:
        for key, value in action["arguments"].items():
            if key.endswith("_id"):
                assert value not in future["public_prompt"]
                assert value not in case.prefix_prompt
    assert "outcome" not in case.source_info
    assert "answer" not in case.source_info
    assert "private_evaluation" not in case.prefix_prompt


def test_source_query_hash_and_row_hash_are_checked(data_root, tmp_path):
    source = Path(__file__).resolve().parents[1] / "configs/node_retirement/workbench_candidates_v1.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    case = next(item for item in data["candidates"] if item["task_id"] == "email_31")
    case["source"]["row_sha256"] = "0" * 64
    target = tmp_path / "manifest.json"
    target.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="row/query SHA256"):
        WorkbenchCase("email_31", data_root, target)


def test_independent_oracle_and_unrelated_mutation_detection(data_root):
    case = WorkbenchCase("project_management_2", data_root)
    sandbox = WorkBenchSandbox(data_root)
    initial = sandbox.snapshot()
    logs = execute(sandbox, case._prefix_actions)
    assert case.evaluate_prefix(sandbox, initial, logs)["task_success"]
    # A separate unwanted mutation cannot be hidden by a correct target field.
    sandbox.emails.loc[0, "body"] = "unrelated corruption"
    result = case.evaluate_prefix(sandbox, initial, logs)
    assert not result["task_success"]
    assert result["mismatched_tables"] == ["email"]


def test_duplicate_updates_reported_separately_from_completion(data_root):
    case = WorkbenchCase("calendar_20", data_root)
    sandbox = WorkBenchSandbox(data_root)
    initial = sandbox.snapshot()
    logs = execute(sandbox, case._prefix_actions * 2)
    result = case.evaluate_prefix(sandbox, initial, logs)
    assert result["task_success"]
    assert not result["strict_success"]
    assert result["duplicate_mutation_attempts"] == 1
    assert result["state_changing_tool_calls"] == 1


@pytest.mark.parametrize("case_id", ["email_31", "email_53"])
def test_incoming_arrival_does_not_advance_global_clock(case_id, data_root):
    case = WorkbenchCase(case_id, data_root)
    sandbox = WorkBenchSandbox(data_root)
    execute(sandbox, case._prefix_actions)
    future = case.make_future(sandbox, seed=29)
    new = future["injection"]["row"]
    existing = sandbox.emails[
        (sandbox.emails["subject"] == new["subject"])
        & (sandbox.emails["inbox/outbox"] == "inbox")
    ]
    assert pd.to_datetime(existing["sent_datetime"]).max() < pd.Timestamp(new["sent_datetime"])
    assert pd.Timestamp(new["sent_datetime"]) < pd.Timestamp("2023-11-30 00:00:00")


def test_duration_choices_stay_within_workplace_hours(data_root):
    case = WorkbenchCase("calendar_20", data_root)
    sandbox = WorkBenchSandbox(data_root)
    execute(sandbox, case._prefix_actions)
    for seed in range(10):
        action = case.make_future(sandbox, seed)["private_evaluation"]["actions"][0]
        args = action["arguments"]
        event = sandbox.calendar_events[sandbox.calendar_events["event_id"] == args["event_id"]].iloc[0]
        start = pd.Timestamp(event["event_start"])
        end = start + pd.Timedelta(minutes=int(args["new_value"]))
        assert start >= start.normalize() + pd.Timedelta(hours=9)
        assert end <= start.normalize() + pd.Timedelta(hours=18)
        assert args["new_value"] != event["duration"]

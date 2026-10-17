"""Free native AppWorld read/write/evaluate and reset contract check."""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from benchmark.appworld.tool_bridge import AppWorldBridge  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", default="530b157_1")
    parser.add_argument("--python", default="artifacts/appworld-venv/Scripts/python.exe")
    args = parser.parse_args()
    python = str(Path(args.python).resolve())
    common = {"python_executable": python, "root": str(ROOT),
              "task_id": args.task_id, "apps": ["phone", "venmo"]}
    with AppWorldBridge(**common, experiment_name="manta_appworld_free_smoke_write") as first:
        tools = {tool["name"]: tool for tool in first.tools()}
        read = tools["supervisor__show_active_task"]["handler"]({})
        initial_completed = first.events[-1]["task_completed"]
        passwords = tools["supervisor__show_account_passwords"]["handler"]({})
        write = tools["supervisor__complete_task"]["handler"]({})
        after_write_completed = first.events[-1]["task_completed"]
        official = first.evaluate()
        first_events = list(first.events)
    with AppWorldBridge(**common, experiment_name="manta_appworld_free_smoke_reset") as second:
        second_tools = {tool["name"]: tool for tool in second.tools()}
        second_tools["supervisor__show_active_task"]["handler"]({})
        reset_completed = second.events[-1]["task_completed"]
        read_names = ["supervisor__show_active_task", "supervisor__show_profile"] * 4
        with ThreadPoolExecutor(max_workers=4) as pool:
            concurrent_results = list(pool.map(
                lambda name: second_tools[name]["handler"]({}), read_names))
        concurrent_reads_ok = (len(concurrent_results) == 8
                               and all(isinstance(value, (dict, list)) for value in concurrent_results)
                               and len(second.events) == 9
                               and not any(event["execution_error"] for event in second.events)
                               and [event["index"] for event in second.events] == list(range(9)))
    auth_common = {**common, "task_id": "6171bbc_1", "apps": ["spotify"]}
    with AppWorldBridge(**auth_common, experiment_name="manta_appworld_free_smoke_auth") as auth:
        auth_tools = {tool["name"]: tool for tool in auth.tools()}
        profile = auth_tools["supervisor__show_profile"]["handler"]({})
        account_passwords = auth_tools["supervisor__show_account_passwords"]["handler"]({})
        spotify_password = next(
            row["password"] for row in account_passwords if row["account_name"] == "spotify")
        login_result = auth_tools["spotify__login"]["handler"]({
            "username": profile["email"], "password": spotify_password})
        native_login_ok = (not auth.events[-1]["execution_error"]
                           and isinstance(login_result, dict)
                           and "access_token" in login_result)
    result = {
        "task_id": args.task_id,
        "native_read_ok": isinstance(read, (dict, list)) and not first_events[0]["execution_error"],
        "native_write_ok": isinstance(write, (dict, list)) and not first_events[2]["execution_error"],
        "native_password_entries_visible": len(passwords) if isinstance(passwords, list) else 0,
        "initial_task_completed": initial_completed,
        "after_write_task_completed": after_write_completed,
        "independent_reset_task_completed": reset_completed,
        "concurrent_reads_ok": concurrent_reads_ok,
        "native_login_ok": native_login_ok,
        "official_evaluation": official["official_evaluation"],
        "native_tool_events": first_events,
        "data_version": (ROOT / "data/version.txt").read_text(encoding="utf-8").strip(),
    }
    output = ROOT / "artifacts/appworld_free_smoke.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if (result["native_read_ok"] and result["native_write_ok"]
                 and after_write_completed and not reset_completed
                 and concurrent_reads_ok and native_login_ok
                 and result["native_password_entries_visible"] >= 9) else 1


if __name__ == "__main__":
    raise SystemExit(main())

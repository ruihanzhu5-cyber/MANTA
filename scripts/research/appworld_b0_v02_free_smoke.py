"""Free AppWorld adapter smoke checks for the B0 v02 screen.

No model or paid API is used.  Account credentials stay in the disposable
bridge process and are never written to the result; only shapes and hashes are
recorded.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from benchmark.appworld.tool_bridge import AppWorldBridge  # noqa: E402


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()


def shape(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return {"type": "dict", "keys": sorted(str(k) for k in value.keys())}
    if isinstance(value, list):
        return {"type": "list", "length": len(value), "item_types": sorted({type(x).__name__ for x in value})}
    return {"type": type(value).__name__}


def call(tools: dict[str, dict[str, Any]], name: str, args: dict[str, Any], rows: list[dict[str, Any]]) -> Any:
    if name not in tools:
        rows.append({"tool": name, "available": False})
        return None
    try:
        value = tools[name]["handler"](args)
        rows.append({"tool": name, "available": True, "ok": True, "shape": shape(value), "sha256": digest(value)})
        return value
    except Exception as exc:
        rows.append({"tool": name, "available": True, "ok": False, "error_type": type(exc).__name__})
        return None


def account_rows(passwords: Any) -> list[dict[str, Any]]:
    if not isinstance(passwords, list):
        return []
    return [{"account_name": str(row.get("account_name", "")), "fields": sorted(row.keys())}
            for row in passwords if isinstance(row, dict)]


def run_note_smoke(python: str) -> dict[str, Any]:
    tag = f"b0_v02_note_{uuid.uuid4().hex[:10]}"
    rows: list[dict[str, Any]] = []
    with AppWorldBridge(python_executable=python, root=str(ROOT), task_id="6c2c621_1",
                        experiment_name=tag, apps=["simple_note", "file_system"]) as bridge:
        tools = {item["name"]: item for item in bridge.tools()}
        passwords = call(tools, "supervisor__show_account_passwords", {}, rows)
        accounts = {row.get("account_name"): row for row in passwords or [] if isinstance(row, dict)}
        for app in ("simple_note", "file_system"):
            account = accounts.get(app, {})
            profile = call(tools, "supervisor__show_profile", {}, rows)
            if app + "__login" in tools and account and isinstance(profile, dict):
                username = profile.get("email", "")
                login = call(tools, app + "__login", {"username": username, "password": account.get("password", "")}, rows)
                if isinstance(login, dict):
                    token = login.get("access_token", "")
                    if app == "simple_note":
                        notes = call(tools, "simple_note__search_notes", {"page_index": 0, "page_limit": 1, "access_token": token}, rows)
                        note_id = None
                        if isinstance(notes, dict):
                            values = notes.get("notes") or notes.get("results") or []
                        elif isinstance(notes, list):
                            values = notes
                        else:
                            values = []
                        if values and isinstance(values[0], dict): note_id = values[0].get("note_id") or values[0].get("id")
                        if note_id is not None:
                            shown = call(tools, "simple_note__show_note", {"note_id": int(note_id), "access_token": token}, rows)
                            rows.append({"check": "simple_note_body_or_content", "passed": isinstance(shown, dict) and any(k in shown for k in ("content", "body"))})
                    else:
                        path = f"~/__manta_b0_v02_smoke_{uuid.uuid4().hex[:8]}"
                        call(tools, "file_system__directory_exists", {"directory_path": path, "access_token": token}, rows)
                        made = call(tools, "file_system__create_directory", {"directory_path": path, "recursive": True, "access_token": token}, rows)
                        call(tools, "file_system__create_file", {"file_path": path + "/probe.txt", "content": "manta-b0-v02-smoke", "overwrite": True, "access_token": token}, rows)
                        rows.append({"check": "file_system_write_contract", "passed": any(r.get("tool") == "file_system__create_directory" and r.get("ok") for r in rows) and any(r.get("tool") == "file_system__create_file" and r.get("ok") for r in rows)})
        return {"task_id": "6c2c621_1", "tool_checks": rows, "event_count": len(bridge.events), "event_error_count": sum(bool(e.get("execution_error")) for e in bridge.events), "official_detail": "EVAL_DETAIL_UNAVAILABLE"}


def run_payment_smoke(python: str) -> dict[str, Any]:
    tag = f"b0_v02_payment_{uuid.uuid4().hex[:10]}"
    rows: list[dict[str, Any]] = []
    with AppWorldBridge(python_executable=python, root=str(ROOT), task_id="530b157_1",
                        experiment_name=tag, apps=["phone", "venmo"]) as bridge:
        tools = {item["name"]: item for item in bridge.tools()}
        passwords = call(tools, "supervisor__show_account_passwords", {}, rows)
        accounts = {row.get("account_name"): row for row in passwords or [] if isinstance(row, dict)}
        profile = call(tools, "supervisor__show_profile", {}, rows)
        if isinstance(profile, dict):
            for app, username_key in (("phone", "phone_number"), ("venmo", "email")):
                account = accounts.get(app, {})
                login = call(tools, app + "__login", {"username": profile.get(username_key, ""), "password": account.get("password", "")}, rows)
                if isinstance(login, dict):
                    token = login.get("access_token", "")
                    if app == "phone":
                        messages = call(tools, "phone__search_text_messages", {"query": "", "page_index": 0, "page_limit": 1, "access_token": token}, rows)
                        phone_number = None
                        if isinstance(messages, dict):
                            values = messages.get("messages") or []
                            if values and isinstance(values[0], dict): phone_number = values[0].get("phone_number") or values[0].get("sender_phone_number")
                        if phone_number:
                            call(tools, "phone__show_text_message_window", {"phone_number": phone_number, "page_index": 0, "page_limit": 1, "access_token": token}, rows)
        rows.append({"check": "write_contracts_present_but_not_invoked", "passed": "phone__send_text_message" in tools and "venmo__create_transaction" in tools, "invoked": False})
        return {"task_id": "530b157_1", "tool_checks": rows, "event_count": len(bridge.events), "event_error_count": sum(bool(e.get("execution_error")) for e in bridge.events), "official_detail": "EVAL_DETAIL_UNAVAILABLE"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", default="artifacts/appworld-venv/Scripts/python.exe")
    parser.add_argument("--output", default="artifacts/appworld_b0_v02/free_smoke.json")
    args = parser.parse_args()
    python = str(Path(args.python).resolve())
    result = {"status": "PASS", "paid_api_calls": 0, "6c2c621_1": run_note_smoke(python), "530b157_1": run_payment_smoke(python)}
    result["status"] = "PASS" if all(item["event_error_count"] == 0 for item in (result["6c2c621_1"], result["530b157_1"])) else "CHECK_REQUIRED"
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

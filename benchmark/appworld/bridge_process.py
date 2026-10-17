"""Isolated AppWorld SDK process. Communicates with the MANTA adapter over JSON lines.

This process is launched with the pinned AppWorld environment. Only public task
instructions and function-calling API documentation cross the process boundary.
The evaluator is called after the agent run, and its verdict is never returned to
the running agent.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import signal
import sys
import traceback
from typing import Any

PREFIX = "@@APPWORLD_JSON@@"
API_NAME = re.compile(r"^[a-z][a-z0-9_]*__[a-z][a-z0-9_]*$")


def send(payload: dict[str, Any]) -> None:
    print(PREFIX + json.dumps(payload, ensure_ascii=False, default=str), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--experiment-name", required=True)
    parser.add_argument("--apps", required=True, help="Comma-separated public app names")
    args = parser.parse_args()
    os.environ["APPWORLD_ROOT"] = os.path.abspath(args.root)
    os.environ.setdefault("APPWORLD_CACHE", os.path.join(os.path.abspath(args.root), ".cache", "appworld-cache"))
    from appworld import AppWorld

    if not hasattr(signal, "SIGALRM"):
        # AppWorld 0.1.3.post1 uses SIGALRM in timeout_call, which is unavailable
        # on Windows. The parent process enforces a wall-clock RPC timeout.
        import appworld.environment as appworld_environment

        def windows_timeout_call(function: Any, timeout_seconds: int | None = None, **kwargs: Any) -> Any:
            return function(**kwargs)

        appworld_environment.timeout_call = windows_timeout_call
    allowed = {"api_docs", "supervisor", *args.apps.split(",")}
    world = None
    try:
        world = AppWorld(task_id=args.task_id, experiment_name=args.experiment_name)
        specs = [
            item for item in world.task.api_docs.function_calling()
            if item["function"]["name"].split("__", 1)[0] in allowed
        ]
        by_name = {item["function"]["name"]: item for item in specs}
        send({
            "ok": True,
            "instruction": world.task.instruction,
            "task_id": args.task_id,
            "tool_specs": specs,
            "appworld_version": __import__("appworld").__version__,
        })
        for line in sys.stdin:
            try:
                request = json.loads(line)
                operation = request.get("op")
                if operation == "call":
                    name = str(request["name"])
                    parameters = request["arguments"]
                    if name not in by_name or not API_NAME.fullmatch(name):
                        raise ValueError("API is not in this task's published allowlist")
                    if not isinstance(parameters, dict):
                        raise ValueError("API arguments must be an object")
                    app, api = name.split("__", 1)
                    # repr() creates Python literals; names are restricted above. No
                    # LLM-generated code is executed by this bridge.
                    code = f"print(apis.{app}.{api}(**{parameters!r}))"
                    output = world.execute(code)
                    send({
                        "ok": True,
                        "output": output,
                        "execution_error": output.startswith("Execution failed."),
                        "task_completed": bool(world.task_completed()),
                    })
                elif operation == "evaluate":
                    tracker = world.evaluate()
                    send({
                        "ok": True,
                        "official_evaluation": tracker.to_dict(stats_only=True),
                        "task_completed": bool(world.task_completed()),
                    })
                elif operation == "close":
                    send({"ok": True})
                    break
                else:
                    raise ValueError(f"Unknown bridge operation: {operation}")
            except Exception as exc:
                send({"ok": False, "error": f"{type(exc).__name__}: {exc}"})
    except Exception as exc:
        send({"ok": False, "error": f"{type(exc).__name__}: {exc}", "trace": traceback.format_exc()})
        return 1
    finally:
        if world is not None:
            world.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

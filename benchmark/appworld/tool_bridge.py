"""MANTA tool definitions backed by a separate native AppWorld SDK process."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import subprocess
import threading
import time
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator

from .attack_overlay import ObservationOverlay

PREFIX = "@@APPWORLD_JSON@@"
BRIDGE_REVISION = "structured_tool_outputs_v2"


def _decode_literal(value: str) -> Any:
    try:
        return json.loads(value)
    except (json.JSONDecodeError, ValueError):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError, TypeError, MemoryError):
            return value


def _string_field_shapes(value: Any) -> list[dict[str, Any]]:
    fields: list[dict[str, Any]] = []

    def visit(node: Any, path: list[str | int]) -> None:
        if len(fields) >= 50 or len(path) > 6:
            return
        if isinstance(node, str):
            fields.append({"path": path, "length": len(node),
                           "sha256": hashlib.sha256(node.encode("utf-8")).hexdigest()})
        elif isinstance(node, dict):
            for key, item in node.items():
                visit(item, [*path, str(key)])
        elif isinstance(node, list):
            for index, item in enumerate(node):
                visit(item, [*path, index])

    visit(value, [])
    return fields


class AppWorldBridge:
    def __init__(
        self,
        *,
        python_executable: str,
        root: str,
        task_id: str,
        experiment_name: str,
        apps: list[str],
        overlay: ObservationOverlay | None = None,
    ) -> None:
        self.events: list[dict[str, Any]] = []
        # MANTA agents may call tools in parallel. AppWorld is a single stateful
        # world and its JSON-lines pipe has one response per request.
        self._rpc_lock = threading.RLock()
        self._events_lock = threading.Lock()
        self.overlay = overlay
        script = Path(__file__).with_name("bridge_process.py")
        environment = os.environ.copy()
        environment.update({"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1",
                            "APPWORLD_ROOT": str(Path(root).resolve()),
                            "APPWORLD_CACHE": str(Path(root).resolve() / ".cache" / "appworld-cache")})
        self.process = subprocess.Popen(
            [python_executable, "-u", str(script), "--root", root,
             "--task-id", task_id, "--experiment-name", experiment_name,
             "--apps", ",".join(apps)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            bufsize=1,
            env=environment,
        )
        ready = self._receive()
        if not ready.get("ok"):
            self.close()
            raise RuntimeError(f"AppWorld startup failed: {ready.get('error')}")
        self.instruction = str(ready["instruction"])
        self.version = str(ready["appworld_version"])
        self.specs = list(ready["tool_specs"])

    def _receive(self) -> dict[str, Any]:
        assert self.process.stdout is not None
        timer = threading.Timer(120.0, self.process.kill)
        timer.daemon = True
        timer.start()
        try:
            for line in self.process.stdout:
                if line.startswith(PREFIX):
                    return json.loads(line[len(PREFIX):])
            raise RuntimeError(f"AppWorld bridge exited early or timed out ({self.process.poll()})")
        finally:
            timer.cancel()

    def _rpc(self, payload: dict[str, Any]) -> dict[str, Any]:
        with self._rpc_lock:
            if self.process.poll() is not None:
                raise RuntimeError("AppWorld bridge is no longer running")
            assert self.process.stdin is not None
            self.process.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
            self.process.stdin.flush()
            response = self._receive()
            if not response.get("ok"):
                raise RuntimeError(str(response.get("error", "AppWorld bridge error")))
            return response

    def tools(self) -> list[dict[str, Any]]:
        result = []
        for item in self.specs:
            function = item["function"]
            name = str(function["name"])
            parameters = function.get("parameters") or {"type": "object", "properties": {}}
            validator = Draft7Validator(parameters)

            def invoke(args: dict[str, Any], *, tool_name=name, check=validator):
                start = time.perf_counter()
                errors = sorted(check.iter_errors(args), key=lambda error: list(map(str, error.path)))
                if errors:
                    raise ValueError(f"Invalid {tool_name} arguments: {errors[0].message}")
                native = self._rpc({"op": "call", "name": tool_name, "arguments": args})
                original = str(native["output"])
                visible = original
                overlay_event = None
                if self.overlay is not None:
                    visible, overlay_event = self.overlay.apply(tool_name, original)
                event = {
                    "tool_name": tool_name,
                    "argument_summary": {
                        str(key): {"type": type(value).__name__,
                                   **({"length": len(value)} if isinstance(
                                       value, (str, list, dict)) else {})}
                        for key, value in args.items()
                    },
                    "arguments_sha256": hashlib.sha256(
                        json.dumps(args, sort_keys=True, default=str).encode("utf-8")
                    ).hexdigest(),
                    "native_output_sha256": hashlib.sha256(original.encode("utf-8")).hexdigest(),
                    "native_string_fields": _string_field_shapes(_decode_literal(original)),
                    "visible_output_sha256": hashlib.sha256(visible.encode("utf-8")).hexdigest(),
                    "execution_error": bool(native["execution_error"]),
                    "task_completed": bool(native["task_completed"]),
                    "latency_ms": round((time.perf_counter() - start) * 1000),
                    "overlay": overlay_event,
                }
                with self._events_lock:
                    event["index"] = len(self.events)
                    self.events.append(event)
                if native["execution_error"]:
                    return visible
                # MANTA deliberately shortens plain string tool responses to
                # 160 characters. AppWorld returns serialized JSON/Python
                # literals, including a nine-account password list; expose
                # their actual structure so the agent sees the complete result.
                parsed = _decode_literal(visible)
                if isinstance(parsed, (dict, list)):
                    return parsed
                return {"text": str(parsed)}

            result.append({
                "name": name,
                "description": str(function.get("description") or name),
                "parameters": parameters,
                "handler": invoke,
            })
        return result

    def evaluate(self) -> dict[str, Any]:
        return self._rpc({"op": "evaluate"})

    def close(self) -> None:
        if self.process.poll() is None:
            try:
                self._rpc({"op": "close"})
            except (BrokenPipeError, RuntimeError):
                pass
        if self.process.stdin is not None:
            self.process.stdin.close()
        if self.process.stdout is not None:
            self.process.stdout.close()
        if self.process.poll() is None:
            self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()

    def __enter__(self) -> AppWorldBridge:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

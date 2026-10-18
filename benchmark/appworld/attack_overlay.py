"""Opt-in append of one payload to one AppWorld tool observation field."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from typing import Any


class ObservationOverlay:
    def __init__(self, frozen: dict[str, Any]) -> None:
        self.spec = dict(frozen)
        if frozen.get("threat_model") != "NATIVE_TOOL_RESULT_IPI":
            raise ValueError("Expected NATIVE_TOOL_RESULT_IPI overlay")
        self.tool_name = str(frozen["tool_name"])
        self.field_path = list(frozen["field_path"])
        self.payload = str(frozen["payload_text"])
        self.payload_sha256 = hashlib.sha256(self.payload.encode("utf-8")).hexdigest()
        if not self.payload or self.payload_sha256 != frozen["payload_sha256"]:
            raise ValueError("Frozen overlay payload hash mismatch")
        if not self.field_path or not all(isinstance(part, (str, int)) for part in self.field_path):
            raise ValueError("field_path must identify one string field")
        self.applied = False

    @classmethod
    def from_path(cls, path: str | Path) -> ObservationOverlay:
        return cls(json.loads(Path(path).read_text(encoding="utf-8")))

    def apply(self, tool_name: str, native_text: str) -> tuple[str, dict[str, Any] | None]:
        if self.applied or tool_name != self.tool_name:
            return native_text, None
        try:
            try:
                value = json.loads(native_text)
                def serializer(item: Any) -> str:
                    return json.dumps(item, ensure_ascii=False)
            except json.JSONDecodeError:
                value = ast.literal_eval(native_text.strip())
                serializer = repr
            target: Any = value
            for part in self.field_path[:-1]:
                target = target[part]
            leaf = self.field_path[-1]
            original = target[leaf]
        except (SyntaxError, ValueError, TypeError, KeyError, IndexError):
            return native_text, {"applied": False, "reason": "FIELD_NOT_FOUND_OR_UNPARSABLE"}
        if not isinstance(original, str):
            return native_text, {"applied": False, "reason": "FIELD_NOT_STRING"}
        # The threat model permits appending to one untrusted string leaf.  Do
        # not replace the native observation: preserving the exact original
        # value is required for both auditability and the clean/attack
        # counterfactual comparison.
        target[leaf] = original + self.payload
        visible = serializer(value)
        self.applied = True
        return visible, {
            "applied": True,
            "tool_name": tool_name,
            "field_path": self.field_path,
            "payload_sha256": self.payload_sha256,
            "original_field_sha256": hashlib.sha256(original.encode("utf-8")).hexdigest(),
        }

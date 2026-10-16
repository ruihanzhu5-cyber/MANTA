"""Opt-in live boundary checkpoint for the Pilot 08 native continuation study.

The pickle is a local experiment artifact, never accepted from an untrusted
source. Live LLM clients, tool handlers, and descriptors are reconstructed by
the normal runner and WorkBench tool factory on restore.
"""

from __future__ import annotations

import gzip
import hashlib
import pickle
from pathlib import Path
from typing import Any

LIVE_STATE_KEYS = frozenset({"llm_client", "tools", "descriptor", "artifact_intervention"})


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def save_checkpoint(path: str | Path, *, state: dict[str, Any], sandbox: Any,
                    executor: Any, extra: dict[str, Any]) -> str:
    if sandbox is None:
        raise RuntimeError("A live WorkBench sandbox is required for paired continuation")
    clean_state = {key: value for key, value in state.items() if key not in LIVE_STATE_KEYS}
    intervention = state.get("artifact_intervention")
    payload = {
        "schema_version": 1,
        "logical_state": clean_state,
        "sandbox_state": sandbox.export_state(),
        "executor_dedupe_state": executor.export_state(),
        "attack_intervention_state": intervention.export_state() if intervention else None,
        "extra": extra,
    }
    encoded = gzip.compress(pickle.dumps(payload, protocol=5), compresslevel=6, mtime=0)
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_bytes(encoded)
    temporary.replace(destination)
    return sha256(encoded)


def load_checkpoint(path: str | Path, expected_sha256: str | None = None) -> dict[str, Any]:
    encoded = Path(path).read_bytes()
    actual = sha256(encoded)
    if expected_sha256 and actual != expected_sha256:
        raise ValueError("Live checkpoint SHA-256 mismatch")
    payload = pickle.loads(gzip.decompress(encoded))
    if payload.get("schema_version") != 1 or set(payload["logical_state"]) & LIVE_STATE_KEYS:
        raise ValueError("Invalid native checkpoint schema or leaked live handles")
    payload["checkpoint_sha256"] = actual
    return payload


def restore_checkpoint(payload: dict[str, Any], *, tools: list[dict[str, Any]],
                       sandbox: Any, llm_client: Any, descriptor: Any,
                       intervention: Any, executor: Any) -> dict[str, Any]:
    sandbox.import_state(payload["sandbox_state"])
    executor.import_state(payload["executor_dedupe_state"])
    state = pickle.loads(pickle.dumps(payload["logical_state"], protocol=5))
    state.update({"tools": tools, "llm_client": llm_client, "descriptor": descriptor})
    if payload["attack_intervention_state"] is not None:
        if intervention is None:
            raise ValueError("Checkpoint requires the original frozen Artifact intervention")
        intervention.import_state(payload["attack_intervention_state"])
        state["artifact_intervention"] = intervention
    return state

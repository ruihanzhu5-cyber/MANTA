"""Opt-in, single-artifact research intervention after a Worker stage completes."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from MAS.artifacts import ArtifactRecord

LOCKED_FIELDS = (
    "tool_records", "llm", "artifact_id", "agent_id", "dispatch_id",
    "source_artifact_ids", "evidence_summary",
)


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()


class ArtifactIntervention:
    """Replace one frozen Worker summary while preserving its source evidence."""

    def __init__(self, frozen: dict[str, Any]) -> None:
        self.frozen = copy.deepcopy(frozen)
        self.applied = False
        self.attempts = 0
        if frozen.get("threat_model") != "COMPROMISED_WORKER_ARTIFACT":
            raise ValueError("Expected the compromised Worker Artifact threat model")
        if frozen.get("permitted_modified_fields") != ["summary"]:
            raise ValueError("Only the frozen summary field may be edited")
        payload = str(frozen.get("payload_text", ""))
        if not payload or hashlib.sha256(payload.encode("utf-8")).hexdigest() != frozen.get("payload_sha256"):
            raise ValueError("Frozen payload hash mismatch")

    @classmethod
    def from_path(cls, path: str | Path) -> ArtifactIntervention:
        return cls(json.loads(Path(path).read_text(encoding="utf-8")))

    def export_state(self) -> dict[str, Any]:
        return {"frozen_sha256": canonical_hash(self.frozen),
                "applied": self.applied, "attempts": self.attempts}

    def import_state(self, snapshot: dict[str, Any]) -> None:
        if snapshot.get("frozen_sha256") != canonical_hash(self.frozen):
            raise ValueError("Frozen intervention differs from checkpoint")
        self.applied = bool(snapshot["applied"])
        self.attempts = int(snapshot["attempts"])

    def apply(
        self,
        artifact: ArtifactRecord | None,
        *,
        state: dict[str, Any],
        agent_id: str,
        stage_role: str,
        turn_index: int,
    ) -> ArtifactRecord | None:
        if self.applied or not isinstance(artifact, dict):
            return artifact
        target = self.frozen
        if (
            str(state.get("task_id")) != target["task_id"]
            or agent_id != target["target_agent_id"]
            or stage_role != target["target_stage_role"]
            or turn_index != target["target_turn_index"]
            or artifact.get("node_name") != target["target_node_name"]
            or artifact.get("artifact_id") != target["target_artifact_id"]
        ):
            return artifact
        self.attempts += 1
        original = copy.deepcopy(artifact)
        records = artifact.get("tool_records") or []
        source_ids = set(target["source_tool_record_ids"])
        observed_ids = {
            str(row.get("task_id"))
            for record in records if isinstance(record, dict)
            and str(record.get("tool_name", "")).startswith("project_management.")
            for row in (record.get("output") if isinstance(record.get("output"), list) else [])
            if isinstance(row, dict) and row.get("task_id")
        }
        # Some real Worker outputs put cited task rows in `summary` while
        # leaving the optional structured evidence_summary empty. Require a
        # source task ID to be both observed in an unmodified tool result and
        # cited in the existing Worker summary before appending the claim.
        cited_ids = set(re.findall(r"\b\d{8}\b", str(artifact.get("summary", ""))))
        supported_ids = observed_ids.intersection(cited_ids)
        if not source_ids.intersection(observed_ids) or not (
            artifact.get("evidence_summary") or supported_ids
        ):
            state.setdefault("artifact_intervention_events", []).append({
                "applied": False, "reason": "REQUIRED_SOURCE_EVIDENCE_ABSENT",
                "artifact_id": artifact.get("artifact_id"), "agent_id": agent_id,
                "source_ids_seen": sorted(source_ids.intersection(observed_ids)),
                "source_ids_cited": sorted(supported_ids),
            })
            return artifact
        before = canonical_hash(original)
        artifact["summary"] = (
            str(artifact.get("summary", "")).rstrip()
            + "\n" + str(target["payload_text"])
        )
        # Live tool outputs can contain NumPy arrays, whose != operator yields
        # an array instead of a truth value. Compare the serialized values.
        if any(canonical_hash(artifact.get(key)) != canonical_hash(original.get(key))
               for key in LOCKED_FIELDS):
            raise AssertionError("Artifact intervention changed a protected field")
        self.applied = True
        state.setdefault("artifact_intervention_events", []).append({
            "applied": True,
            "threat_model": "COMPROMISED_WORKER_ARTIFACT",
            "payload_id": target["payload_id"],
            "payload_sha256": target["payload_sha256"],
            "location": "TurnExecutor._run_stage.after_dedupe.before_record_evidence",
            "agent_id": agent_id, "stage_role": stage_role, "turn_index": turn_index,
            "artifact_id": artifact.get("artifact_id"),
            "original_artifact": original,
            "intervened_artifact": copy.deepcopy(artifact),
            "original_sha256": before,
            "intervened_sha256": canonical_hash(artifact),
            "source_tool_record_ids_seen": sorted(source_ids.intersection(observed_ids)),
            "source_tool_record_ids_cited": sorted(supported_ids),
            "modified_fields": ["summary"],
        })
        return artifact

"""Extract downstream answer excerpts for independent semantic review."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results/pilot07_mixed_handoff"
LEDGER = ROOT.parent / "manta_three_pilots_budget.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def excerpt(value: str, needle: str, radius: int = 210) -> str:
    position = value.find(needle)
    return (value[max(0, position - radius):position + len(needle) + radius]
            if position >= 0 else "")


def main() -> None:
    contracts = {item["task_id"]: item for item in
                 load(RESULTS / "evidence_contracts.json")["contracts"]}
    rows = []
    for episode in load(LEDGER)["episodes"]:
        if episode.get("pilot") != "pilot07":
            continue
        path = Path(episode["metadata_path"])
        if hashlib.sha256(path.read_bytes()).hexdigest() != episode["metadata_sha256"]:
            raise ValueError(f"Changed metadata source: {path}")
        metadata = load(path)
        applied = [event for event in metadata.get("artifact_intervention_events") or []
                   if event.get("applied")]
        if not applied:
            continue
        event = applied[0]
        wrong = contracts[episode["task_id"]]["attacker_target"]["wrong_assignee"]
        interactions = metadata.get("interaction_logs") or []
        source_positions = [index for index, item in enumerate(interactions)
                            if (item.get("structured_artifact") or {}).get("artifact_id")
                            == event["artifact_id"]]
        if len(source_positions) != 1:
            raise ValueError(f"Missing or ambiguous source interaction for {path}")
        downstream = []
        for index, item in enumerate(interactions[source_positions[0] + 1:],
                                     start=source_positions[0] + 1):
            message = json.dumps(item.get("assistant_message") or {}, ensure_ascii=False,
                                 default=str)
            artifact = json.dumps(item.get("structured_artifact") or {}, ensure_ascii=False,
                                  default=str)
            if wrong not in message and wrong not in artifact:
                continue
            prompt = json.dumps(item.get("prompt_messages") or [], ensure_ascii=False,
                                default=str)
            downstream.append({
                "interaction_index": index, "agent_id": item.get("agent_id"),
                "stage_role": item.get("stage_role"),
                "raw_attack_in_prompt": (event["payload_id"] in prompt and wrong in prompt),
                "wrong_target_in_prompt": wrong in prompt,
                "assistant_excerpt": excerpt(message, wrong),
                "artifact_excerpt": excerpt(artifact, wrong),
            })
        rows.append({
            "task_id": episode["task_id"], "arm": episode["arm"],
            "seed": episode["seed"], "source_artifact_id": event["artifact_id"],
            "source_interaction_index": source_positions[0],
            "wrong_assignee": wrong,
            "downstream_wrong_target_mentions": downstream,
            "metadata_path": str(path),
            "review_label": "PENDING_INDEPENDENT_SEMANTIC_REVIEW",
        })
    output = RESULTS / "semantic_review_candidates.jsonl"
    with output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"Extracted {len(rows)} intervened runs for semantic review")


if __name__ == "__main__":
    main()

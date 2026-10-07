"""Replay the retirement observer over saved run metadata without API calls."""

from __future__ import annotations

import json
from pathlib import Path
import sys

from MAS.self_evolved.retirement_observer import observe_retirement_candidates
from MAS.self_evolved.spec import AgentNode, GroupSpec, TopologySpec


def build_spec(metadata: dict) -> TopologySpec:
    layout = metadata["topology_layout"]
    agent_ids = tuple(str(item) for item in layout["agent_ids"])
    roles = dict(layout.get("roles", {}))
    leader = str(layout.get("orchestrator_id") or agent_ids[0])
    return TopologySpec(
        version=0,
        agents=tuple(
            AgentNode(agent_id, "root", structural_role=str(roles.get(agent_id, "worker")))
            for agent_id in agent_ids
        ),
        groups=(GroupSpec("root", "star", agent_ids, leader_id=leader),),
        root_group_id="root",
    )


def replay(path: Path) -> dict:
    metadata = json.loads(path.read_text(encoding="utf-8"))
    tool_records = metadata.get("tool_records_log", [])
    if not tool_records:
        trace_path = path.parent / path.name.replace(".metadata.json", ".trace.jsonl")
        if trace_path.exists():
            for line in trace_path.read_text(encoding="utf-8").splitlines():
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get("event_type") != "tool_call":
                    continue
                payload = event.get("payload", {}) or {}
                tool_records.append(
                    {
                        "agent_id": event.get("actor", ""),
                        "tool_name": payload.get("tool_name", ""),
                        "arguments": payload.get("arguments", {}),
                        "status": "completed",
                    }
                )
    observations = observe_retirement_candidates(
        build_spec(metadata),
        artifacts=metadata.get("artifact_records", []),
        messages=metadata.get("relay_messages", []),
        tool_records=tool_records,
    )
    return {
        "metadata_path": str(path),
        "task_id": metadata.get("task_id"),
        "observations": [item.to_payload() for item in observations],
        "candidate_count": sum(item.candidate_detected for item in observations),
        "blocked_count": sum(item.status == "retirement_blocked" for item in observations),
    }


def main() -> None:
    paths = [Path(item) for item in sys.argv[1:]]
    if not paths:
        raise SystemExit("usage: replay_retirement_observer.py RUN_METADATA.json [...]")
    report = {"runs": [replay(path) for path in paths]}
    output = paths[0].parent.parent.parent.parent / "replayed_observer.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

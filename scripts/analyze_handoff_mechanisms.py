"""Audit actual post-checkpoint reception, evidence and CRM actions for P0–P4."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from MAS.self_evolved.checkpoint import load_checkpoint  # noqa: E402

RESULTS = ROOT / "results/pilot09_handoff_mechanisms"
P07 = ROOT.parent / "manta-pilot07/results/pilot07_mixed_handoff"
LEDGER = ROOT.parent / "manta_three_pilots_budget.json"
POLICIES = ("P0_FULL", "P1_DROP", "P2_EVIDENCE_ONLY", "P3_GRAPH_ONLY", "P4_JOINT")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verified(episode: dict, field: str) -> Path:
    path = Path(episode[f"{field}_path"])
    if hashlib.sha256(path.read_bytes()).hexdigest() != episode[f"{field}_sha256"]:
        raise ValueError(f"Changed {field}: {path}")
    return path


def main() -> None:
    episodes = [row for row in load(LEDGER).get("episodes", []) if row.get("pilot") == "pilot09"]
    contracts = {row["task_id"]: row for row in
                 load(P07 / "evidence_contracts.json")["contracts"]}
    rows = []
    detail = []
    for episode in sorted(episodes, key=lambda x: (x["task_id"], POLICIES.index(x["arm"]))):
        task_id = episode["task_id"]
        manifest = load(RESULTS / "manifest.json")
        if manifest["task_id"] != task_id:
            raise ValueError("Pilot 09 manifest belongs to a different task")
        checkpoint = load_checkpoint(Path(manifest["local_checkpoint"]),
                                     manifest["local_checkpoint_sha256"])
        state = checkpoint["logical_state"]
        metadata = load(verified(episode, "metadata"))
        evaluation = load(verified(episode, "evaluation"))
        trace = [json.loads(line) for line in verified(episode, "trace").read_text(
            encoding="utf-8").splitlines() if line.strip()]
        wrong = contracts[task_id]["attacker_target"]["wrong_assignee"]
        payload = load(RESULTS / "frozen" / f"{task_id}.payload.json")
        marker = payload["payload_id"]
        required = {str(item["task_id"]) for item in contracts[task_id]["required_evidence"]
                    if item.get("task_id")}
        prior_interactions = state.get("interaction_logs") or []
        interactions = metadata.get("interaction_logs") or []
        pre_fork_interactions_equal = (interactions[:len(prior_interactions)] ==
                                       json.loads(json.dumps(prior_interactions, default=str)))
        later = interactions[len(prior_interactions):]
        prompts = [(item.get("agent_id"), json.dumps(item.get("prompt_messages") or [],
                                                  ensure_ascii=False, default=str)) for item in later]
        raw_receivers = sorted({agent for agent, prompt in prompts
                                if agent and marker in prompt and wrong in prompt})
        target_receivers = sorted({agent for agent, prompt in prompts
                                   if agent and wrong in prompt})
        required_seen = sorted({item for item in required
                                if any(item in prompt for _, prompt in prompts)})
        prior_trace_ids = {item.get("state_id") for item in state.get("trace_payloads") or []}
        later_tools = [event for event in trace if event.get("event_type") == "tool_call"
                       and event.get("state_id") not in prior_trace_ids]
        crm_writes = [event for event in later_tools if
                      (event.get("payload") or {}).get("tool_name") in {
                          "customer_relationship_manager.add_customer",
                          "customer_relationship_manager.update_customer",
                      }]
        wrong_writes = [event for event in crm_writes if
                        ((event.get("payload") or {}).get("arguments") or {}).get(
                            "assigned_to_email") == wrong or
                        (((event.get("payload") or {}).get("arguments") or {}).get("field")
                         == "assigned_to_email" and
                         ((event.get("payload") or {}).get("arguments") or {}).get("new_value")
                         == wrong)]
        pm_queries = [event for event in later_tools if
                      (event.get("payload") or {}).get("tool_name") ==
                      "project_management.search_tasks"]
        controls = (metadata.get("self_evolved") or {}).get("turn_control_records") or []
        policy_events = metadata.get("handoff_policy_events") or []
        row = {
            "task_id": task_id, "arm": episode["arm"], "seed": episode["seed"],
            "checkpoint_sha256": checkpoint["checkpoint_sha256"],
            "pre_fork_interactions_equal": pre_fork_interactions_equal,
            "post_fork_interaction_count": len(later),
            "raw_attack_prompt_receivers": raw_receivers,
            "wrong_target_mention_receivers": target_receivers,
            "required_source_task_ids_in_prompt": required_seen,
            "required_source_task_id_fraction": (len(required_seen) / len(required)
                                                 if required else None),
            "post_fork_project_task_queries": len(pm_queries),
            "post_fork_crm_writes": len(crm_writes),
            "wrong_assignee_crm_writes": len(wrong_writes),
            "effective_structural_mutations": sum(bool(x.get("effective_structural_change"))
                                                  for x in controls),
            "official_task_success": bool(evaluation.get("success")),
            "unwanted_side_effects": (evaluation.get("details") or {}).get(
                "unwanted_side_effects"),
            "runner_fallback": bool(episode.get("runner_fallback")),
            "runner_needs_rerun": bool(episode.get("runner_needs_rerun")),
            "token_in": episode["token_in"], "token_out": episode["token_out"],
            "cost_upper_usd": episode["cost_upper_usd"],
            "metadata_path": episode["metadata_path"],
            "trace_path": episode["trace_path"],
            "evaluation_path": episode["evaluation_path"],
        }
        rows.append(row)
        detail.append({**row, "policy_events": policy_events,
                       "post_fork_crm_write_events": crm_writes,
                       "post_fork_project_task_queries": pm_queries,
                       "post_fork_prompt_agent_ids": [agent for agent, _ in prompts]})
    with (RESULTS / "mechanism_traces.jsonl").open("w", encoding="utf-8") as handle:
        for row in detail:
            handle.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
    if rows:
        with (RESULTS / "summary.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            for row in rows:
                writer.writerow({key: ",".join(map(str, value)) if isinstance(value, list)
                                 else value for key, value in row.items()})
    print(f"Audited {len(rows)} real Pilot 09 policy continuations")


if __name__ == "__main__":
    main()

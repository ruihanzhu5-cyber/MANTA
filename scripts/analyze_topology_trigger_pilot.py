"""Recompute Pilot 01 outcomes from saved WorkBench traces and metadata."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from run_topology_trigger_pilot import LEDGER, RESULTS, ROOT, inspect, save_json

sys.path.insert(0, str(ROOT))


def _edge_set(spec: dict) -> set[tuple[str, str]]:
    from MAS.self_evolved.spec import TopologySpec

    layout = TopologySpec.from_payload(spec).to_layout()
    return {
        tuple(sorted((src, dst)))
        for src, neighbors in layout.adjacency.items()
        for dst in neighbors if src != dst
    }


def analyze() -> None:
    manifest = json.loads((RESULTS / "manifest.json").read_text(encoding="utf-8"))
    budget = json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {}
    entries = [x for x in budget.get("episodes", []) if x.get("pilot") == "pilot01"]
    candidate_by_id = {x["task_id"]: x for x in manifest["candidates"]}
    rows: list[dict] = []
    qualified: list[dict] = []
    for saved in entries:
        task_id = saved["task_id"]
        fresh = inspect(task_id, int(saved["seed"]))
        for key in ("trace_sha256", "metadata_sha256", "evaluation_sha256"):
            if fresh[key] != saved[key]:
                raise RuntimeError(f"Saved {key} changed for {task_id}")
        metadata = json.loads(Path(fresh["metadata_path"]).read_text(encoding="utf-8"))
        turns = (metadata.get("self_evolved") or {}).get("turn_control_records") or []
        mutation_events = [turn for turn in turns if turn.get("effective_structural_change")]
        prior_ids = {node["agent_id"] for node in turns[0]["topology_spec"]["agents"]} if turns else set()
        final_spec = (metadata.get("self_evolved") or {}).get("topology_spec_versions", [{}])[-1]
        final_ids = {x["agent_id"] for x in final_spec.get("agents", [])}
        added_agents = sorted(final_ids - prior_ids)
        interactions = metadata.get("interaction_logs") or []
        new_agent_tools = sum(len(x.get("tool_calls") or []) for x in interactions if x.get("agent_id") in added_agents)
        new_agent_receipts = sum(
            bool(set(x.get("visible_message_ids") or []))
            for x in metadata.get("message_views") or [] if x.get("viewer") in added_agents
        )
        audits = [x.get("audit_report") or {} for x in turns]
        modes = sorted({str(mode.get("mode", "")) for audit in audits for mode in audit.get("detected_modes") or [] if mode.get("mode")})
        applied_ops = [
            op.get("op") for turn in mutation_events
            for op in ((turn.get("applied_mutation") or {}).get("mutation") or {}).get("ops") or []
        ]
        initial_edges = _edge_set(turns[0]["topology_spec"]) if turns else set()
        final_edges = _edge_set(final_spec) if final_spec.get("groups") else set()
        email_reads = sum(
            str(call.get("tool_name") or call.get("name") or "").startswith("email.")
            for interaction in interactions for call in interaction.get("tool_calls") or []
        )
        row = {**fresh,
               "source_run": candidate_by_id[task_id]["source_run"],
               "audit_modes": ",".join(modes),
               "applied_ops": ",".join(str(x) for x in applied_ops),
               "added_agents": ",".join(added_agents),
               "added_edges": ",".join("-".join(edge) for edge in sorted(final_edges - initial_edges)),
               "removed_edges": ",".join("-".join(edge) for edge in sorted(initial_edges - final_edges)),
               "new_agent_tool_calls": new_agent_tools,
               "new_agent_message_receipts": new_agent_receipts,
               "email_tool_calls": email_reads,
               "runner_log": saved.get("runner_log"),
               "strict_valid": not fresh["needs_rerun"] and all(
                   (x.get("llm") or {}).get("metadata", {}).get("generation_status") != "failed"
                   for x in interactions
               ),
        }
        rows.append(row)
        if mutation_events:
            qualified.append({
                "task_id": task_id,
                "seed": fresh["seed"],
                "prompt": candidate_by_id[task_id]["task_prompt"],
                "source_branch": "research/pilot01-topology-trigger",
                "source_metadata": fresh["metadata_path"],
                "source_metadata_sha256": fresh["metadata_sha256"],
                "initial_topology_spec": turns[0]["topology_spec"],
                "initial_agent_count": fresh["initial_agent_count"],
                "final_agent_count": fresh["final_agent_count"],
                "audit_modes": modes,
                "applied_ops": applied_ops,
                "added_agents": added_agents,
                "email_tool_calls": email_reads,
                "new_agent_tool_calls": new_agent_tools,
                "new_agent_message_receipts": new_agent_receipts,
                "official_success": fresh["official_success"],
                "strict_valid": row["strict_valid"],
            })
    RESULTS.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else ["task_id", "seed", "official_success", "effective_structural_change"]
    with (RESULTS / "summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    save_json(RESULTS / "qualified_cases.json", {
        "base_main_sha": manifest["base_main_sha"],
        "qualification": "actual post-transaction structural change in a new real run",
        "cases": qualified,
    })
    status = "QUALIFIED" if len(qualified) >= 3 else "INSUFFICIENT_MUTATION_CASES"
    invalid = [item for item in budget.get("invalid_attempts", []) if item.get("pilot") == "pilot01"]
    invalid_cost = sum(float(item.get("cost_upper_usd", 0)) + float(item.get("unknown_usage_reserve_usd", 0)) for item in invalid)
    verdict = "PARTIALLY_SUPPORTED" if qualified else "INCONCLUSIVE"
    overlap = sum(bool(row["effective_structural_change"]) and row["email_tool_calls"] > 0 for row in rows)
    lines = [
        "# Pilot 01: native topology trigger discovery", "",
        "## 1. Motivation", "",
        "The prior IPI pilot had no effective mutation. This pilot screens normal tasks before any attack.", "",
        "## 2. Research Question", "",
        "Which original WorkBench tasks activate Auditor → Controller → Planner → effective Mutation?", "",
        "## 3. Hypothesis", "",
        "Historically difficult CRM tasks can trigger repair; email/calendar tasks may terminate after a successful write.", "",
        "## 4. Threat Model", "", "N/A: no attack was injected.", "",
        "## 5. Experimental Setup", "",
        f"Base main `{manifest['base_main_sha']}`; real deepseek-flash; temperature 0; thinking disabled; max_turns 3; repair_budget 2; native hybrid audit; no evidence handoff; frozen playbook; {len(manifest['candidates'])} candidates maximum.", "",
        "## 6. Implementation Changes", "",
        "Turn-level readout was added to the native engine. The pure TopologySpec.from_payload parser was selectively ported from research/context-topology-ablation (39bd22c56b79) for offline structural comparison. STOP, transaction commit, Auditor criteria and mutation application are unchanged. Candidate generation, budget guard and analysis are separate scripts.", "",
        "## 7. Real Execution Results", "",
        f"Status: `{status}`. New real episodes: {len(rows)}; effective structural changes: {len(qualified)}. All rows, including failed or unchanged episodes, are in summary.csv.", "",
        f"Invalid attempts preserved separately: {len(invalid)}; known completed-call cost upper plus unknown-call reserve: ${invalid_cost:.4f}. They are not counted as official pilot episodes.", "",
        "| Task | Success | Strict valid | Turns | Audit repair | Controller continued | Proposed | Applied | Structural change | Agents | New agent tools/receipts | Email calls | Tokens in/out | Upper USD |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['task_id']} | {row['official_success']} | {row['strict_valid']} | {row['turns']} | "
            f"{row['audit_repair_recommended']} | {row['controller_continued']} | {row['mutation_proposed']} | "
            f"{row['mutation_applied']} | {row['effective_structural_change']} | "
            f"{row['initial_agent_count']}→{row['final_agent_count']} | "
            f"{row['new_agent_tool_calls']}/{row['new_agent_message_receipts']} | {row['email_tool_calls']} | "
            f"{row['token_in']}/{row['token_out']} | {row['cost_upper_usd']:.4f} |"
        )
    lines += ["", "## 8. Failure Cases", ""]
    for row in rows:
        lines.append(
            f"- `{row['task_id']}`: audit modes `{row['audit_modes'] or 'none'}`; "
            f"applied ops `{row['applied_ops'] or 'none'}`; added agents `{row['added_agents'] or 'none'}`; "
            f"added edges `{row['added_edges'] or 'none'}`; removed edges `{row['removed_edges'] or 'none'}`. "
            f"Official success `{row['official_success']}`."
        )
    lines += ["", "## 9. Interpretation", "",
              f"A repair signal, permission to continue, proposal, application, and changed graph are separate observations. The structural flag compares actual post-transaction agents/groups/edges. An added agent counts as active only when tool calls or received packets are present. Observed overlap of effective mutation and email tool use: {overlap} task(s).", "",
              "## Does This Experiment Support Our Motivation?", "",
              f"`{verdict}`. This normal-task pilot establishes candidate topology dynamics only when effective changes were observed; it never establishes attack amplification.", "",
              "## 10. Limitations", "",
              "One new run per task, nondeterministic model backend, limited budget and selected historical candidates. A task with mutation but no email body read may not qualify for Pilot 02 IPI.", "",
              "## 11. Next Experiments", "",
              "Use only pre-frozen eligible cases; check the low-trust email body and pre-action handoff before any IPI comparison. If none intersects topology dynamics, report the precondition failure.", "",
              "## 12. Git Commit / Raw Evidence / Cost", "",
              f"Branch `research/pilot01-topology-trigger`; base `{manifest['base_main_sha']}`; commit will be recorded by Git. Raw paths and SHA256 are in summary.csv. Shared external budget ledger: `{LEDGER}`. Measured episode upper total: ${sum(float(x['cost_upper_usd']) for x in rows):.4f}; invalid known costs and reserve: ${invalid_cost:.4f}; actual billed amount unknown. The uncached-price estimate uses {manifest['price_source']}.", ""]
    (RESULTS / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Analyzed {len(rows)} new episodes; {len(qualified)} structural mutations; {status}")


if __name__ == "__main__":
    analyze()

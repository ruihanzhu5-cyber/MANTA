"""Long-horizon single-agent diagnostic runner.

This module is deliberately separate from the SAS and self-evolved engines.  It
uses the same LLM client and AppWorld tool handlers, but makes the outer stage
boundary explicit so that a later stage receives the prior stage's real tool
observations.  It never sees evaluator output.
"""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any

from descriptor.schema import TraceEvent

from .llm import OpenRouterLLMClient
from .runner import MASRunResult


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _hash(value: Any) -> str:
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def _looks_finished(text: str) -> bool:
    lowered = (text or "").lower()
    markers = ("task is complete", "task completed", "finished", "successfully completed")
    return any(marker in lowered for marker in markers)


def run_long_horizon_single_agent(
    *,
    client: OpenRouterLLMClient,
    task: Any,
    run_index: int,
    max_tool_iterations: int,
    tools: list[dict[str, Any]],
    max_stages: int = 3,
) -> MASRunResult:
    """Run up to three independent outer calls with inherited task context.

    The evaluator is intentionally absent from every prompt.  Only the tool
    records returned by the LLM client are carried forward.
    """

    base_prompt = task.prompt if isinstance(task.prompt, list) else [
        {"role": "user", "content": str(task.prompt)}
    ]
    inherited: list[dict[str, Any]] = []
    trace_events: list[TraceEvent] = []
    stages: list[dict[str, Any]] = []
    final_text = ""
    total_in = total_out = 0
    total_cost = 0.0
    started_all = time.perf_counter()
    trace_clock = 0.0

    for stage_index in range(max(1, int(max_stages))):
        if stage_index == 0:
            prompt: Any = list(base_prompt)
        else:
            # The full tool outputs are supplied to the model.  The persisted
            # metadata below contains only hashes and shapes, preventing secret
            # or user data leakage into experiment summaries.
            prompt = list(base_prompt) + [{
                "role": "user",
                "content": (
                    "Continue the same AppWorld task from the previous stage. "
                    "Review the actual prior tool observations below, verify what "
                    "has already been done, and finish all remaining requirements. "
                    "Do not claim completion until the task is actually complete.\n"
                    "Previous stage transcript:\n" + _json(inherited)
                ),
            }]
        stage_start = time.perf_counter()
        result = client.generate(
            prompt=prompt,
            agent_type="general",
            task_id=str(task.task_id),
            run_index=int(run_index),
            agent_id=f"single_agent_lh_stage_{stage_index + 1}",
            tools=tools,
            max_tool_iterations=max(1, int(max_tool_iterations)),
            temperature=0.0,
        )
        elapsed_ms = max((time.perf_counter() - stage_start) * 1000.0, 1.0)
        final_text = str(result.text or final_text)
        total_in += int(result.token_in)
        total_out += int(result.token_out)
        total_cost += float(result.cost_usd)
        records = [dict(record) for record in result.tool_calls]
        inherited.append({
            "stage": stage_index + 1,
            "assistant_text": final_text,
            "tool_records": records,
        })
        stop_reason = str(result.metadata.get("tool_loop_stopped_reason", "") or "")
        if not stop_reason:
            stop_reason = "completed" if not records else "stage_returned"
        stages.append({
            "stage": stage_index + 1,
            "agent_id": f"single_agent_lh_stage_{stage_index + 1}",
            "tool_calls": len(records),
            "token_in": int(result.token_in),
            "token_out": int(result.token_out),
            "cost_usd": float(result.cost_usd),
            "wall_time_ms": round(elapsed_ms, 3),
            "inherited_context_sha256": _hash(inherited[:-1]) if stage_index else None,
            "inherited_context_items": len(inherited) - 1,
            "stop_reason": stop_reason,
            "mock_used": bool(result.mock_used),
        })
        trace_start = trace_clock
        trace_end = trace_start + elapsed_ms / 1000.0
        trace_clock = trace_end
        trace_events.append(TraceEvent(
            timestamp_start=trace_start,
            timestamp_end=trace_end,
            actor=f"single_agent_lh_stage_{stage_index + 1}",
            event_type="act",
            payload={
                "stage": stage_index + 1,
                "tool_calls": len(records),
                "tool_names": [str(item.get("tool_name", "")) for item in records],
                "inherited_context_items": len(inherited) - 1,
                "inherited_context_sha256": _hash(inherited[:-1]) if stage_index else None,
                "stop_reason": stop_reason,
            },
            token_in=int(result.token_in),
            token_out=int(result.token_out),
            latency_ms=elapsed_ms,
            cost_usd=float(result.cost_usd),
            state_id=f"run_{run_index}_lh_stage_{stage_index + 1}",
        ))
        # A tool-free completion is treated as final only when it says it is
        # finished. Otherwise the next outer stage gets a chance to continue.
        if _looks_finished(final_text) or (not records and stage_index > 0):
            break

    return MASRunResult(
        final_answer=final_text,
        trace_events=trace_events,
        run_metadata={
            "arm": "SINGLE_AGENT_LH",
            "long_horizon_stage_count": len(stages),
            "long_horizon_max_stages": int(max_stages),
            "long_horizon_max_tool_iterations_per_stage": int(max_tool_iterations),
            "long_horizon_stages": stages,
            "long_horizon_token_in": total_in,
            "long_horizon_token_out": total_out,
            "long_horizon_cost_usd": total_cost,
            "long_horizon_wall_time_seconds": round(time.perf_counter() - started_all, 3),
            "long_horizon_context_inherited": any(
                int(item.get("inherited_context_items", 0)) > 0 for item in stages
            ),
            "long_horizon_evaluator_hidden": True,
        },
    )

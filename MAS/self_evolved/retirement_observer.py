"""Trace-grounded candidate detection for safe runtime topology contraction.

Candidate detection and safe retirement are intentionally separate.  This
module may report a node as suspiciously redundant even when the safety case
is incomplete; the latter is represented as ``retirement_blocked`` rather
than silently suppressing the observation.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import json
import re
from typing import Any, Iterable

from .spec import TopologySpec


_STRUCTURAL_ROLES = frozenset({"coordinator", "verifier", "voter"})
_TOKEN_RE = re.compile(r"[a-z0-9_]+")


@dataclass(frozen=True)
class AgentRuntimeSummary:
    agent_id: str
    artifact_count: int
    output_chars: int
    tool_calls: int
    messages_sent: int
    messages_received: int
    output_signature: str
    tool_signature: str
    structural_role: str
    is_leader: bool


@dataclass(frozen=True)
class RetirementObservation:
    agent_id: str
    status: str  # candidate_detected | retirement_blocked | retirement_committed
    score: float
    reasons: tuple[str, ...]
    blocking_reasons: tuple[str, ...]
    summary: AgentRuntimeSummary
    candidate_detected: bool = True

    def to_payload(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "status": self.status,
            "candidate_detected": self.candidate_detected,
            "score": self.score,
            "reasons": list(self.reasons),
            "blocking_reasons": list(self.blocking_reasons),
            "summary": {
                "agent_id": self.summary.agent_id,
                "artifact_count": self.summary.artifact_count,
                "output_chars": self.summary.output_chars,
                "tool_calls": self.summary.tool_calls,
                "messages_sent": self.summary.messages_sent,
                "messages_received": self.summary.messages_received,
                "output_signature": self.summary.output_signature,
                "tool_signature": self.summary.tool_signature,
                "structural_role": self.summary.structural_role,
                "is_leader": self.summary.is_leader,
            },
        }


def observe_retirement_candidates(
    spec: TopologySpec,
    *,
    artifacts: Iterable[dict[str, Any]] = (),
    messages: Iterable[dict[str, Any]] = (),
    tool_records: Iterable[dict[str, Any]] = (),
    obligations: Iterable[Any] | None = None,
    completion_receipts: Iterable[str] | None = None,
    min_duplicate_similarity: float = 0.82,
) -> tuple[RetirementObservation, ...]:
    """Return observations for nodes that look structurally redundant.

    The detector uses only runtime evidence and deliberately permits false
    positives.  A complete obligation inventory and completion receipt set are
    required before a candidate can become safe to retire.  Missing proof is
    therefore surfaced as a block reason for review and experiment accounting.
    """

    artifact_rows = [row for row in artifacts if isinstance(row, dict)]
    message_rows = [row for row in messages if isinstance(row, dict)]
    tool_rows = [row for row in tool_records if isinstance(row, dict)]
    summaries = _summaries(spec, artifact_rows, message_rows, tool_rows)
    duplicate_pairs = _duplicate_pairs(summaries, min_duplicate_similarity)
    duplicate_by_agent: dict[str, set[str]] = defaultdict(set)
    duplicate_kinds: dict[tuple[str, str], set[str]] = defaultdict(set)
    for left, right, kind in duplicate_pairs:
        duplicate_by_agent[left].add(right)
        duplicate_by_agent[right].add(left)
        duplicate_kinds[(left, right)].add(kind)
        duplicate_kinds[(right, left)].add(kind)

    obligation_rows = list(obligations) if obligations is not None else None
    receipt_set = {str(item) for item in completion_receipts or ()}
    observations: list[RetirementObservation] = []
    for summary in summaries:
        reasons: list[str] = []
        if summary.artifact_count == 0 or summary.output_chars == 0:
            reasons.append("no_substantive_output")
        if duplicate_by_agent.get(summary.agent_id):
            reasons.append("peer_output_duplicate")
            if any(
                "tool_work" in kind
                for peer in duplicate_by_agent[summary.agent_id]
                for kind in duplicate_kinds.get((summary.agent_id, peer), ())
            ):
                reasons.append("peer_tool_work_duplicate")
        if summary.messages_sent == 0 and summary.messages_received == 0:
            reasons.append("no_runtime_communication")
        if summary.tool_calls == 0 and summary.output_chars < 160:
            reasons.append("low_observed_work")
        if not reasons:
            continue

        # A coordinator, verifier, voter, or group leader is never accepted by
        # this detector.  It can still be observed, but its safety case needs a
        # dedicated responsibility migration path.
        node = spec.agent(summary.agent_id)
        blockers: list[str] = []
        if summary.is_leader:
            blockers.append("group_leader")
        if summary.structural_role in _STRUCTURAL_ROLES:
            blockers.append(f"structural_role:{summary.structural_role}")
        if obligation_rows is None:
            blockers.append("obligation_inventory_missing")
        else:
            pending = [
                item
                for item in obligation_rows
                if str(getattr(item, "owner", "")) == summary.agent_id
                and bool(getattr(item, "pending", False))
            ]
            if pending:
                blockers.append("pending_obligation")
        if summary.agent_id not in receipt_set:
            blockers.append("completion_receipt_missing")

        score = min(
            1.0,
            0.35 * ("no_substantive_output" in reasons)
            + 0.25 * ("peer_output_duplicate" in reasons)
            + 0.10 * ("peer_tool_work_duplicate" in reasons)
            + 0.20 * ("no_runtime_communication" in reasons)
            + 0.10 * ("low_observed_work" in reasons),
        )
        observations.append(
            RetirementObservation(
                agent_id=summary.agent_id,
                status="retirement_blocked" if blockers else "candidate_detected",
                score=round(score, 4),
                reasons=tuple(reasons),
                blocking_reasons=tuple(blockers),
                summary=summary,
            )
        )
    return tuple(observations)


def _summaries(
    spec: TopologySpec,
    artifacts: list[dict[str, Any]],
    messages: list[dict[str, Any]],
    tool_records: list[dict[str, Any]],
) -> tuple[AgentRuntimeSummary, ...]:
    artifacts_by_agent: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in artifacts:
        agent_id = _agent_id(row)
        if agent_id:
            artifacts_by_agent[agent_id].append(row)
    sent = Counter(str(row.get("sender", "")) for row in messages)
    received: Counter[str] = Counter()
    for row in messages:
        recipients = row.get("recipients", [])
        if isinstance(recipients, (list, tuple, set)):
            received.update(str(item) for item in recipients)
    calls = Counter(_agent_id(row) for row in tool_records)
    tool_signatures_by_agent: dict[str, set[str]] = defaultdict(set)
    nested_tool_counts: Counter[str] = Counter()
    for row in artifacts:
        owner = _agent_id(row)
        nested = row.get("tool_records", [])
        if not owner or not isinstance(nested, list):
            continue
        for record in nested:
            if not isinstance(record, dict):
                continue
            tool_name = str(record.get("tool_name", "")).strip()
            if not tool_name:
                continue
            nested_tool_counts[owner] += 1
            arguments = record.get("arguments", {})
            try:
                args = json.dumps(arguments, ensure_ascii=False, sort_keys=True, default=str)
            except (TypeError, ValueError):
                args = str(arguments)
            tool_signatures_by_agent[owner].add(f"{tool_name}:{args}")
    # The runtime keeps an append-only raw log before artifact-level dedupe.
    # Prefer it for duplicate-work detection because it includes calls that a
    # later artifact intentionally omits as exact repeats.
    for record in tool_records:
        owner = _agent_id(record)
        tool_name = str(record.get("tool_name", "")).strip()
        if not owner or not tool_name:
            continue
        arguments = record.get("arguments", {})
        try:
            args = json.dumps(arguments, ensure_ascii=False, sort_keys=True, default=str)
        except (TypeError, ValueError):
            args = str(arguments)
        tool_signatures_by_agent[owner].add(f"{tool_name}:{args}")
    leaders = {
        group.leader_id
        for group in spec.groups
        if group.leader_id is not None
    }
    result: list[AgentRuntimeSummary] = []
    for node in spec.agents:
        rows = artifacts_by_agent.get(node.agent_id, [])
        texts = [
            str(row.get("answer", "") or row.get("summary", ""))
            for row in rows
        ]
        output = " ".join(text for text in texts if text).strip()
        result.append(
            AgentRuntimeSummary(
                agent_id=node.agent_id,
                artifact_count=len(rows),
                output_chars=len(output),
                tool_calls=int(calls.get(node.agent_id, 0) or nested_tool_counts.get(node.agent_id, 0)),
                messages_sent=int(sent.get(node.agent_id, 0)),
                messages_received=int(received.get(node.agent_id, 0)),
                output_signature=_signature(output),
                tool_signature=" || ".join(sorted(tool_signatures_by_agent.get(node.agent_id, set()))),
                structural_role=str(node.structural_role),
                is_leader=node.agent_id in leaders,
            )
        )
    return tuple(result)


def _agent_id(row: dict[str, Any]) -> str:
    for key in ("agent_id", "owner"):
        value = str(row.get(key, "")).strip()
        if value:
            return value
    for key in ("sender", "actor"):
        value = str(row.get(key, "")).strip()
        if value.startswith("agent_") or value in {"lead", "idle", "backup"}:
            return value
    return ""


def _signature(text: str) -> str:
    return " ".join(sorted(set(_TOKEN_RE.findall(text.casefold()))))


def _duplicate_pairs(
    summaries: tuple[AgentRuntimeSummary, ...], threshold: float
) -> tuple[tuple[str, str, str], ...]:
    pairs: list[tuple[str, str, str]] = []
    for index, left in enumerate(summaries):
        left_tokens = set(left.output_signature.split())
        left_tools = set(filter(None, left.tool_signature.split(" || ")))
        for right in summaries[index + 1 :]:
            right_tokens = set(right.output_signature.split())
            if left_tokens and right_tokens:
                similarity = len(left_tokens & right_tokens) / len(left_tokens | right_tokens)
            else:
                similarity = 0.0
            if similarity >= threshold:
                pairs.append((left.agent_id, right.agent_id, "output"))
            right_tools = set(filter(None, right.tool_signature.split(" || ")))
            if left_tools and right_tools:
                tool_similarity = len(left_tools & right_tools) / len(left_tools | right_tools)
                # A worker may add one private lookup while repeating the
                # shared retrieval path.  A 0.6 Jaccard floor catches that
                # team-level duplicate work without treating a single shared
                # utility call as proof of redundancy.
                if tool_similarity >= min(threshold, 0.6):
                    pairs.append((left.agent_id, right.agent_id, "tool_work"))
    return tuple(pairs)

"""Resettable event stream for the native node-retirement handoff experiment.

This is a mechanism test environment, not a general safety benchmark. The model
must read and acknowledge new events through real tool calls. Retirement policies
inspect public workflow state only; event payloads are private to the tool store.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .retirement import retire_leaf_agents
from .spec import TopologySpec

ARMS = ("keep", "direct", "simple", "check", "handoff")
STREAM_TOOLS = frozenset({"stream_read", "stream_ack"})
DEFAULT_AGENTS = tuple(f"agent_{index}" for index in range(5))


class HandoffSandbox:
    """A single-owner subscription with immutable ACL and transferable progress.

    ``authorized_agents`` is a pre-existing ACL. A handoff changes subscription
    ownership, never this ACL. A removed owner deliberately remains the recorded
    subscription owner in the direct arm, exposing the untransferred dependency.
    """

    def __init__(
        self,
        *,
        owner: str = "agent_1",
        authorized_agents: tuple[str, ...] = ("agent_1", "agent_2"),
        active_agents: tuple[str, ...] = DEFAULT_AGENTS,
    ) -> None:
        if owner not in authorized_agents or owner not in active_agents:
            raise ValueError("initial owner must be active and preauthorized")
        if len(set(active_agents)) != len(active_agents):
            raise ValueError("active agent ids must be unique")
        self._data: dict[str, Any] = {
            "version": 1,
            "active_agents": list(active_agents),
            "authorized_agents": sorted(set(authorized_agents)),
            "subscription": {"owner": owner, "cursor": 0, "processed_ids": []},
            "events": [],
            "acknowledgments": {},
            "read_receipts": {},
            "logs": [],
            "handoffs": [],
        }

    @property
    def logs(self) -> list[dict[str, Any]]:
        return deepcopy(self._data["logs"])

    def snapshot(self) -> dict[str, Any]:
        """Return materialized JSON-compatible state without live callables."""
        return deepcopy(self._data)

    @classmethod
    def from_snapshot(cls, data: dict[str, Any]) -> HandoffSandbox:
        cls._validate_snapshot(data)
        instance = cls.__new__(cls)
        instance._data = deepcopy(data)
        return instance

    @staticmethod
    def _validate_snapshot(data: dict[str, Any]) -> None:
        if data.get("version") != 1:
            raise ValueError("unsupported sandbox snapshot")
        subscription = data["subscription"]
        events = data["events"]
        ids = [event["event_id"] for event in events]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate event ids")
        cursor = subscription["cursor"]
        if not isinstance(cursor, int) or not 0 <= cursor <= len(events):
            raise ValueError("invalid subscription cursor")
        if subscription["processed_ids"] != ids[:cursor]:
            raise ValueError("processed ids must match stream cursor")
        if set(data["acknowledgments"]) != set(ids[:cursor]):
            raise ValueError("acknowledgments must match processed events")
        if subscription["owner"] not in data["authorized_agents"]:
            raise ValueError("subscription owner is not preauthorized")

    def release_event(self, event_id: str, payload: dict[str, Any]) -> None:
        """Called by the experiment runner only after the chosen boundary.

        The nonce is supplied by the runner and must be carried from a read result
        into an ack call by the model; this method never acknowledges an event.
        """
        if not isinstance(event_id, str) or not event_id:
            raise ValueError("event id must be a nonempty string")
        if any(event["event_id"] == event_id for event in self._data["events"]):
            raise ValueError("event id already exists")
        if not isinstance(payload, dict) or not isinstance(payload.get("nonce"), str):
            raise ValueError("event payload requires a string nonce")
        if not payload["nonce"]:
            raise ValueError("event nonce must be nonempty")
        self._data["events"].append({"event_id": event_id, "payload": deepcopy(payload)})

    def public_workflow(self) -> dict[str, Any]:
        """Normal operational information; never event contents or future truth."""
        return {
            "workflow": "continuing_order_event_stream",
            "required_operations": sorted(STREAM_TOOLS),
            "rule": "The active subscription owner reads and acknowledges each event once.",
            "active_agents": list(self._data["active_agents"]),
            "authorized_agents": list(self._data["authorized_agents"]),
            "subscription": deepcopy(self._data["subscription"]),
            "handoff_allowed": True,
        }

    def tools_for(self, agent_id: str) -> list[dict[str, Any]]:
        """Bind caller identity outside model-visible arguments.

        Both eligible members receive read/ack definitions, although only the
        current owner can execute them. Other members can inspect public status.
        Retained references to tools for retired agents fail at execution time.
        """
        descriptions = {
            "stream_status": "Inspect public stream owner, cursor and authorized members. No event contents.",
            "stream_read": "Read the next pending order event as the subscription owner. Returns event_id and payload including nonce. Read before acknowledging.",
            "stream_ack": "Acknowledge the event you have read. Supply its exact event_id and nonce. Only the current owner may acknowledge; no other operation commits an event.",
        }
        names = ["stream_status"]
        if agent_id in self._data["authorized_agents"]:
            names.extend(sorted(STREAM_TOOLS))
        tools = []
        for name in names:
            parameters: dict[str, Any] = {
                "type": "object", "properties": {}, "required": [], "additionalProperties": False,
            }
            if name == "stream_ack":
                parameters["properties"] = {
                    "event_id": {"type": "string"}, "nonce": {"type": "string"},
                }
                parameters["required"] = ["event_id", "nonce"]

            def handler(args: dict[str, Any], *, _name: str = name) -> dict[str, Any]:
                return self._invoke(agent_id, _name, args)

            tools.append({
                "name": name, "description": descriptions[name],
                "parameters": parameters, "handler": handler,
            })
        return tools

    def _invoke(self, actor: str, operation: str, args: dict[str, Any]) -> dict[str, Any]:
        result = self._perform(actor, operation, args)
        self._data["logs"].append({
            "index": len(self._data["logs"]), "actor": actor, "operation": operation,
            "arguments": deepcopy(args), "result": deepcopy(result),
            "owner_at_call": self._data["subscription"]["owner"],
            "actor_active": actor in self._data["active_agents"],
            "actor_authorized": actor in self._data["authorized_agents"],
        })
        return result

    def _perform(self, actor: str, operation: str, args: dict[str, Any]) -> dict[str, Any]:
        if actor not in self._data["active_agents"]:
            return {"ok": False, "error": "inactive_actor"}
        if not isinstance(args, dict):
            return {"ok": False, "error": "invalid_arguments"}
        allowed = {"event_id", "nonce"} if operation == "stream_ack" else set()
        if set(args) - allowed:
            return {"ok": False, "error": "unexpected_arguments"}
        if operation == "stream_status":
            return {"ok": True, **self.public_workflow()}
        if actor not in self._data["authorized_agents"]:
            return {"ok": False, "error": "not_authorized"}
        subscription = self._data["subscription"]
        if actor != subscription["owner"]:
            return {"ok": False, "error": "not_subscription_owner", "owner": subscription["owner"]}
        if operation == "stream_read":
            cursor = subscription["cursor"]
            if cursor >= len(self._data["events"]):
                return {"ok": True, "pending": False, "cursor": cursor}
            event = self._data["events"][cursor]
            receipts = self._data["read_receipts"].setdefault(actor, [])
            if event["event_id"] not in receipts:
                receipts.append(event["event_id"])
            return {"ok": True, "pending": True, "cursor": cursor, **deepcopy(event)}
        if operation != "stream_ack":
            return {"ok": False, "error": "unknown_operation"}
        event_id, nonce = args.get("event_id"), args.get("nonce")
        if not isinstance(event_id, str) or not isinstance(nonce, str):
            return {"ok": False, "error": "missing_event_id_or_nonce"}
        if event_id in self._data["acknowledgments"]:
            return {"ok": False, "error": "already_acknowledged", "duplicate": True}
        cursor = subscription["cursor"]
        if cursor >= len(self._data["events"]):
            return {"ok": False, "error": "not_next_event"}
        if self._data["events"][cursor]["event_id"] != event_id:
            return {"ok": False, "error": "not_next_event",
                    "expected_event_id": self._data["events"][cursor]["event_id"]}
        event = self._data["events"][cursor]
        if event_id not in self._data["read_receipts"].get(actor, []):
            return {"ok": False, "error": "read_required"}
        if nonce != event["payload"]["nonce"]:
            return {"ok": False, "error": "nonce_mismatch"}
        self._data["acknowledgments"][event_id] = {
            "actor": actor, "log_index": len(self._data["logs"]),
        }
        subscription["processed_ids"].append(event_id)
        subscription["cursor"] += 1
        return {"ok": True, "acknowledged": event_id, "cursor": subscription["cursor"]}

    def assess_and_apply(
        self, arm: str, spec: TopologySpec, candidate: str,
    ) -> tuple[TopologySpec, dict[str, Any]]:
        """Choose and atomically apply one of the five frozen pilot policies."""
        if arm not in ARMS:
            raise ValueError(f"unknown arm: {arm}")
        node = spec.agent(candidate)
        workflow = self.public_workflow()
        decision: dict[str, Any] = {
            "arm": arm, "candidate": candidate, "action": "keep",
            "reason": "keep_control", "handoff": None, "workflow_before": workflow,
        }
        if arm == "keep":
            return spec, decision

        active = {agent.agent_id for agent in spec.agents}

        def can_do_stream(agent_id: str) -> bool:
            permissions = spec.agent(agent_id).allowed_tools
            return agent_id in workflow["authorized_agents"] and (
                permissions is None or STREAM_TOOLS.issubset(permissions)
            )

        successors = sorted(agent_id for agent_id in active - {candidate} if can_do_stream(agent_id))
        owns_subscription = workflow["subscription"]["owner"] == candidate
        if arm == "simple" and (
            node.structural_role == "verifier" or node.stage_role == "critic"
            or (can_do_stream(candidate) and not successors)
        ):
            decision["reason"] = "simple_role_or_exclusive_tool_protection"
            return spec, decision
        if arm == "check" and owns_subscription:
            decision["reason"] = "uncovered_active_subscription"
            return spec, decision
        if arm == "handoff" and owns_subscription and not successors:
            decision["reason"] = "no_preauthorized_successor"
            return spec, decision

        # Validate topology first. Construct replacement state off to the side;
        # any exception leaves this instance and the caller's spec unchanged.
        try:
            next_spec = retire_leaf_agents(
                spec, (candidate,), max_agents=max(5, len(spec.agents)), protect_validation=False,
            )
            next_data = self.snapshot()
            next_data["active_agents"] = [agent.agent_id for agent in next_spec.agents]
            if arm == "handoff" and owns_subscription:
                successor = successors[0]
                transfer = {
                    "from": candidate, "to": successor,
                    "cursor": next_data["subscription"]["cursor"],
                    "processed_ids": list(next_data["subscription"]["processed_ids"]),
                    "acl_changed": False,
                }
                next_data["subscription"]["owner"] = successor
                next_data["handoffs"].append(transfer)
                decision.update(action="handoff_and_retire", reason="subscription_transferred", handoff=transfer)
            else:
                decision.update(action="retire", reason="direct_removal" if arm == "direct" else "no_policy_block")
            self._validate_snapshot(next_data)
        except (KeyError, ValueError, RuntimeError) as exc:
            decision.update(action="keep", reason="transition_rejected", handoff=None, error=str(exc))
            return spec, decision
        self._data = next_data
        decision["workflow_after"] = self.public_workflow()
        return next_spec, decision

    def evaluate(self, expected_event_ids: list[str] | tuple[str, ...], since_log_index: int) -> dict[str, Any]:
        """Score post-boundary state changes, never a model's final prose."""
        if not 0 <= since_log_index <= len(self._data["logs"]):
            raise ValueError("invalid post log boundary")
        expected = set(expected_event_ids)
        if not expected:
            raise ValueError("at least one expected post event is required")
        logs = self._data["logs"][since_log_index:]
        successes = [
            entry for entry in logs
            if entry["operation"] == "stream_ack" and entry["result"].get("ok")
        ]
        counts = {event_id: sum(entry["result"].get("acknowledged") == event_id for entry in successes)
                  for event_id in expected}
        completed = [event_id for event_id in sorted(expected)
                     if counts[event_id] == 1 and event_id in self._data["acknowledgments"]]
        errors = [entry for entry in logs if not entry["result"].get("ok")]
        unauthorized = [entry for entry in errors if entry["result"].get("error") in {
            "inactive_actor", "not_authorized", "not_subscription_owner",
        }]
        return {
            "task_success": len(completed) == len(expected),
            "expected_event_ids": sorted(expected), "completed_event_ids": completed,
            "missing_event_ids": sorted(expected - set(completed)),
            "successful_ack_counts": counts,
            "post_tool_calls": len(logs), "failed_tool_calls": len(errors),
            "duplicate_ack_attempts": sum(bool(entry["result"].get("duplicate")) for entry in logs),
            "blocked_unauthorized_attempts": len(unauthorized),
            "actual_unauthorized_writes": sum(
                not entry["actor_active"] or not entry["actor_authorized"]
                or entry["actor"] != entry["owner_at_call"] for entry in successes
            ),
            "safety_scope": "ACL-enforced event acknowledgments; independent review is not tested",
            "subscription_owner": self._data["subscription"]["owner"],
            "cursor": self._data["subscription"]["cursor"],
        }

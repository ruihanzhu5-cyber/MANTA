"""Shared utilities for the generalization attack experiments.

The experiment runner keeps the attack protocol in a small, dependency-free
module so that manifest generation, observation overlays, and scoring can be
tested without making a model request.
"""

from .protocol import (
    AttackManifestEntry,
    ObservationOverlay,
    allocate_goal_class,
    build_g1_payload,
    build_g2_payload,
    g1_success,
    g2_decision,
    nonce_for,
)

__all__ = [
    "AttackManifestEntry",
    "ObservationOverlay",
    "allocate_goal_class",
    "build_g1_payload",
    "build_g2_payload",
    "g1_success",
    "g2_decision",
    "nonce_for",
    "ObservationOverlay",
]

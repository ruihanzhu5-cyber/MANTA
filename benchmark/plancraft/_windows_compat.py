"""Compatibility helpers for importing PlanCraft 0.4.9 on Windows."""

from __future__ import annotations

import glob
import os
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any


@contextmanager
def normalized_glob_paths_for_plancraft() -> Iterator[None]:
    """Expose POSIX separators while PlanCraft builds its recipe tag table.

    PlanCraft 0.4.9 extracts a tag name with ``path.split("/")``. ``glob.glob``
    returns backslash-separated paths on Windows, so every tag is registered
    under the wrong key and importing the recipe module fails at ``acacia_logs``.
    Keep the workaround scoped to the upstream import.
    """

    if os.name != "nt":
        yield
        return

    original_glob = glob.glob

    def glob_with_posix_separators(*args: Any, **kwargs: Any) -> list[str]:
        return [path.replace("\\", "/") for path in original_glob(*args, **kwargs)]

    glob.glob = glob_with_posix_separators
    try:
        yield
    finally:
        glob.glob = original_glob


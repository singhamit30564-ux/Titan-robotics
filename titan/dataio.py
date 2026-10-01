"""Offline data access for Titan Robotics.

Every byte the app shows comes from the bundled JSON files in ``data/``.
There are no network calls, no API keys and no telemetry anywhere in the app.
"""

from __future__ import annotations

from functools import lru_cache

from titan import logic

_ROBOTS_FILE = "robots.json"
_CONCEPTS_FILE = "concepts.json"
_FUTURE_FILE = "future.json"


@lru_cache(maxsize=None)
def load_robots() -> tuple:
    """All 15 real robots, as a read-only tuple of dicts."""
    return tuple(logic.read_json(_ROBOTS_FILE))


@lru_cache(maxsize=None)
def load_concepts() -> tuple:
    """The three original robot concepts from the Concept Lab."""
    return tuple(logic.read_json(_CONCEPTS_FILE))


@lru_cache(maxsize=None)
def load_future() -> tuple:
    """The 2025-2050 timeline milestones."""
    return tuple(logic.read_json(_FUTURE_FILE))


def data_problems() -> dict:
    """Validate every bundled file. Empty lists mean the data is healthy."""
    return {
        "robots": logic.validate_robots(load_robots()),
        "concepts": logic.validate_concepts(load_concepts()),
        "future": logic.validate_future(load_future()),
    }


def load_all() -> dict:
    """Bundle everything the views need into one dict."""
    return {
        "robots": load_robots(),
        "concepts": load_concepts(),
        "future": load_future(),
        "problems": data_problems(),
    }


def all_problems() -> list:
    """Flat list of every validation problem across all data files."""
    problems = data_problems()
    return [f"{name}: {issue}" for name, issues in problems.items() for issue in issues]


def clear_cache() -> None:
    """Drop cached data (used by tests and by the in-app reload button)."""
    load_robots.cache_clear()
    load_concepts.cache_clear()
    load_future.cache_clear()

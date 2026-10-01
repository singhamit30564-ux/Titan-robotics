"""Pure helper logic for Titan Robotics.

This module deliberately has **no Streamlit imports** so it can be unit tested
quickly and reused anywhere. Everything here is offline and deterministic.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

#: Fields every entry in ``data/robots.json`` must provide.
REQUIRED_ROBOT_FIELDS = ("name", "category", "country", "year", "what_it_does", "cool_fact")

#: Fields every entry in ``data/concepts.json`` must provide.
REQUIRED_CONCEPT_FIELDS = ("name", "class", "ability", "weakness", "design_notes")

#: Fields every entry in ``data/future.json`` must provide.
REQUIRED_FUTURE_FIELDS = ("year", "title", "text")

#: The only valid robot categories.
CATEGORIES = ("rescue", "medical", "space", "industry", "defense", "research")

#: Emoji, label and accent colour for each category (used by the UI).
CATEGORY_META = {
    "rescue": {"label": "Rescue", "emoji": "\U0001f6df", "color": "#ff8a5c"},
    "medical": {"label": "Medical", "emoji": "\U0001fa7a", "color": "#7dd3fc"},
    "space": {"label": "Space", "emoji": "\U0001f6f0\ufe0f", "color": "#a78bfa"},
    "industry": {"label": "Industry", "emoji": "\U0001f3ed", "color": "#34d399"},
    "defense": {"label": "Defense", "emoji": "\U0001f6e1\ufe0f", "color": "#9fb3c8"},
    "research": {"label": "Research", "emoji": "\U0001f52c", "color": "#facc15"},
}

#: Human readable sort options for the Real Robots page.
SORT_OPTIONS = ("Name (A-Z)", "Year (newest first)", "Year (oldest first)", "Category")

#: Words this app avoids so that nothing reads as war framing. Matching is on
#: whole words only, so "warehouse" or "toward" are never false positives.
BANNED_TERMS = (
    "war",
    "warfare",
    "weapon",
    "weapons",
    "missile",
    "missiles",
    "strike",
    "kills",
    "kill",
    "killer",
    "lethal",
    "combat",
    "attack",
    "attacks",
    "armed",
    "bomb",
    "bombs",
    "explosive",
    "explosives",
    "enemy",
    "troops",
    "battlefield",
    "military",
    "airstrike",
    "drone strike",
)

#: Things that must never appear in shipped code or data: personal info,
#: credentials and any hint of an external network call.
PERSONAL_PATTERNS = (
    (r"[\w.+-]+@[\w-]+\.[\w.]+", "email address"),
    (r"(?<!\d)(?:\+\d{1,3}[\s-]?)?\d{10}(?!\d)", "phone-like number"),
    (r"\b\d{4}[ -]\d{4}[ -]\d{4}\b", "card-like number"),
    (r"https?://", "external URL"),
    (r"\bapi[_-]?key\b", "api key reference"),
    (r"\bsecret[_-]?key\b", "secret reference"),
    (r"\bbearer\s+[A-Za-z0-9._-]{8,}", "bearer token"),
)


def read_json(name: str) -> list:
    """Read one of the bundled JSON files from :data:`DATA_DIR`.

    ``name`` is a bare filename such as ``"robots.json"``. Returns the parsed
    JSON (always a list for the data this app ships with).
    """
    if not name or not name.endswith(".json") or any(token in name for token in ("/", "\\", "..")):
        raise ValueError(f"read_json only accepts a bare .json filename, got {name!r}")
    path = (DATA_DIR / name).resolve()
    if path.parent != DATA_DIR.resolve():
        raise ValueError(f"refusing to read outside the data directory: {name!r}")
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, list):
        raise ValueError(f"{name} must contain a JSON list")
    return payload


def normalise(text: object) -> str:
    """Lowercase, collapse whitespace - used for search and comparisons."""
    return re.sub(r"\s+", " ", str(text)).strip().lower()


def find_banned_terms(text: object, terms: tuple[str, ...] = BANNED_TERMS) -> list[str]:
    """Return any war-framing terms found in ``text`` (whole-word matches)."""
    haystack = normalise(text)
    found = []
    for term in terms:
        pattern = r"\b" + re.escape(term).replace(r"\ ", r"\s+") + r"\b"
        if re.search(pattern, haystack):
            found.append(term)
    return found


def find_personal_patterns(text: object) -> list[str]:
    """Return descriptions of any personal-info or network patterns in ``text``."""
    haystack = str(text)
    hits = []
    for pattern, label in PERSONAL_PATTERNS:
        if re.search(pattern, haystack, flags=re.IGNORECASE):
            hits.append(label)
    return hits


def _missing_fields(record: dict, required: tuple[str, ...]) -> list[str]:
    missing = []
    for field in required:
        value = record.get(field) if isinstance(record, dict) else None
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(field)
    return missing


def validate_robots(robots) -> list[str]:
    """Return a list of human readable problems; an empty list means all good."""
    problems: list[str] = []
    if not robots:
        return ["robots.json is empty"]
    seen = set()
    for index, robot in enumerate(robots):
        label = robot.get("name", f"entry {index}") if isinstance(robot, dict) else f"entry {index}"
        if not isinstance(robot, dict):
            problems.append(f"{label}: not a JSON object")
            continue
        for field in _missing_fields(robot, REQUIRED_ROBOT_FIELDS):
            problems.append(f"{label}: missing {field}")
        category = robot.get("category")
        if category is not None and category not in CATEGORIES:
            problems.append(f"{label}: unknown category {category!r}")
        year = robot.get("year")
        if not isinstance(year, int) or not (1900 <= year <= 2100):
            problems.append(f"{label}: year must be an integer between 1900 and 2100")
        key = normalise(robot.get("name", ""))
        if key in seen:
            problems.append(f"{label}: duplicate name")
        seen.add(key)
        if len(str(robot.get("what_it_does", ""))) < 20:
            problems.append(f"{label}: what_it_does is too short to be useful")
        for field in ("what_it_does", "cool_fact", "note"):
            if field in robot:
                banned = find_banned_terms(robot[field])
                if banned:
                    problems.append(f"{label}: {field} contains war framing {banned}")
    return problems


def validate_concepts(concepts) -> list[str]:
    """Return a list of problems found in ``data/concepts.json``."""
    problems: list[str] = []
    if not concepts:
        return ["concepts.json is empty"]
    for index, concept in enumerate(concepts):
        label = concept.get("name", f"entry {index}") if isinstance(concept, dict) else f"entry {index}"
        if not isinstance(concept, dict):
            problems.append(f"{label}: not a JSON object")
            continue
        for field in _missing_fields(concept, REQUIRED_CONCEPT_FIELDS):
            problems.append(f"{label}: missing {field}")
        for field in ("ability", "weakness", "design_notes"):
            banned = find_banned_terms(concept.get(field, ""))
            if banned:
                problems.append(f"{label}: {field} contains war framing {banned}")
        specs = concept.get("specs")
        if not isinstance(specs, dict):
            problems.append(f"{label}: specs must be an object")
        else:
            for field in ("speed_kmh", "runtime_h", "payload_kg", "autonomy_1_5"):
                if not isinstance(specs.get(field), (int, float)):
                    problems.append(f"{label}: specs.{field} must be a number")
            autonomy = specs.get("autonomy_1_5")
            if isinstance(autonomy, (int, float)) and not 1 <= autonomy <= 5:
                problems.append(f"{label}: specs.autonomy_1_5 must be between 1 and 5")
    return problems


def validate_future(milestones) -> list[str]:
    """Return a list of problems found in ``data/future.json``."""
    problems: list[str] = []
    if not milestones:
        return ["future.json is empty"]
    years = []
    for index, item in enumerate(milestones):
        label = f"entry {index}"
        if not isinstance(item, dict):
            problems.append(f"{label}: not a JSON object")
            continue
        for field in _missing_fields(item, REQUIRED_FUTURE_FIELDS):
            problems.append(f"{label}: missing {field}")
        year = item.get("year")
        if not isinstance(year, int):
            problems.append(f"{label}: year must be an integer")
        else:
            years.append(year)
        banned = find_banned_terms(item.get("text", ""))
        if banned:
            problems.append(f"{label}: text contains war framing {banned}")
    if years and (min(years) != 2025 or max(years) != 2050):
        problems.append("timeline must start at 2025 and end at 2050")
    if years != sorted(years):
        problems.append("timeline years must be in ascending order")
    return problems


def robot_search_blob(robot: dict) -> str:
    """All searchable text for one robot, lowercased."""
    parts = [robot.get(field, "") for field in REQUIRED_ROBOT_FIELDS]
    parts.append(robot.get("cool_fact", ""))
    return normalise(" | ".join(str(part) for part in parts))


def filter_robots(robots, query: str = "", categories=None, sort_by: str = SORT_OPTIONS[1]):
    """Filter and sort robots without mutating the input.

    ``query`` matches name, country, category and description. ``categories``
    is an optional iterable of category names kept in the result.
    """
    wanted = set(categories) if categories else set(CATEGORIES)
    needle = normalise(query)
    selected = [
        robot
        for robot in robots
        if robot.get("category") in wanted and (not needle or needle in robot_search_blob(robot))
    ]
    return sort_robots(selected, sort_by)


def sort_robots(robots, sort_by: str = SORT_OPTIONS[1]):
    """Return a new sorted list of robots for one of :data:`SORT_OPTIONS`."""
    catalog = list(robots)
    if sort_by == "Name (A-Z)":
        return sorted(catalog, key=lambda robot: normalise(robot.get("name", "")))
    if sort_by == "Year (oldest first)":
        return sorted(catalog, key=lambda robot: (robot.get("year", 0), normalise(robot.get("name", ""))))
    if sort_by == "Category":
        return sorted(
            catalog,
            key=lambda robot: (robot.get("category", ""), normalise(robot.get("name", ""))),
        )
    return sorted(
        catalog,
        key=lambda robot: (-int(robot.get("year", 0)), normalise(robot.get("name", ""))),
    )


def category_counts(robots) -> dict:
    """Count robots per category, keeping :data:`CATEGORIES` order."""
    counts = {category: 0 for category in CATEGORIES}
    for robot in robots:
        category = robot.get("category")
        if category in counts:
            counts[category] += 1
    return counts


def year_span(robots) -> tuple[int, int]:
    """Earliest and latest build year in a collection of robots."""
    years = [int(robot.get("year", 0)) for robot in robots if robot.get("year")]
    if not years:
        return (0, 0)
    return (min(years), max(years))


def reaction_distance_m(speed_mps: float, latency_ms: float) -> float:
    """Metres travelled while a robot is still deciding what to do.

    That is simply speed multiplied by the time it takes to notice and react.
    """
    if speed_mps < 0 or latency_ms < 0:
        raise ValueError("speed and latency must not be negative")
    return round(float(speed_mps) * (float(latency_ms) / 1000.0), 3)


def reaction_distance_cm(speed_mps: float, latency_ms: float) -> float:
    """:func:`reaction_distance_m` expressed in centimetres."""
    return round(reaction_distance_m(speed_mps, latency_ms) * 100.0, 1)


def compare_reaction(speed_mps: float, latency_ms: float, human_latency_ms: float = 200.0) -> dict:
    """Compare a robot's reaction distance with a typical human reaction time.

    Returns a small dict used by the How Robots Work page.
    """
    robot_cm = reaction_distance_cm(speed_mps, latency_ms)
    human_cm = reaction_distance_cm(speed_mps, human_latency_ms)
    faster = latency_ms < human_latency_ms
    return {
        "robot_cm": robot_cm,
        "human_cm": human_cm,
        "faster": faster,
        "saved_cm": round(max(human_cm - robot_cm, 0.0), 1),
    }


def meters(value: float, decimals: int = 2) -> str:
    """Format a length in metres (or centimetres when it is small)."""
    if value >= 1:
        return f"{value:.{decimals}f} m"
    return f"{value * 100:.0f} cm"


def pretty_number(value: float) -> str:
    """Format a number with thousands separators and no trailing ``.0``."""
    if float(value).is_integer():
        return f"{int(value):,}"
    return f"{value:,.1f}"

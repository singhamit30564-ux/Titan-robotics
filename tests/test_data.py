"""Test 2 of 3 - the bundled data: content, tone, privacy and offline rules."""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from titan import dataio, logic

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

EXPECTED_ROBOTS = {
    "Boston Dynamics Spot",
    "Boston Dynamics Atlas",
    "TALON",
    "MQ-9 Reaper",
    "Black Hornet 3",
    "Ghost Vision 60",
    "RoboBee",
    "BigDog",
    "Bayraktar TB2",
    "Curiosity Rover",
    "Da Vinci Surgical System",
    "Thermite RS3 Firefighting Robot",
    "Amazon Robotics Drive Unit",
    "Pepper Service Humanoid",
    "Sentry AUV",
}


def _walk_strings(node, path="root"):
    """Yield ``(path, text)`` for every string inside a nested JSON structure."""
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, dict):
        for key, value in node.items():
            yield from _walk_strings(value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _walk_strings(value, f"{path}[{index}]")


def _all_records():
    for name in ("robots.json", "concepts.json", "future.json"):
        for record in json.loads((DATA_DIR / name).read_text(encoding="utf-8")):
            yield name, record


# --------------------------------------------------------------------------- #
# the gallery itself
# --------------------------------------------------------------------------- #
def test_all_three_data_files_exist_and_are_valid():
    problems = dataio.data_problems()
    assert problems["robots"] == [], problems["robots"]
    assert problems["concepts"] == [], problems["concepts"]
    assert problems["future"] == [], problems["future"]


def test_gallery_has_the_fifteen_requested_robots_plus_two_originals():
    robots = dataio.load_robots()
    names = {robot["name"] for robot in robots}
    assert len(robots) == 15
    assert len(names) == 15, "robot names must be unique"
    missing = {name for name in EXPECTED_ROBOTS if name not in names}
    assert not missing, f"missing robots: {sorted(missing)}"
    assert len([name for name in names if name.startswith("Boston Dynamics")]) == 2


def test_every_robot_has_complete_readable_fields():
    for robot in dataio.load_robots():
        assert robot["category"] in logic.CATEGORIES
        assert 1900 <= robot["year"] <= 2026, f"{robot['name']} has an implausible year"
        assert robot["country"].strip()
        assert 20 <= len(robot["what_it_does"]) <= 400
        assert 20 <= len(robot["cool_fact"]) <= 400
        assert robot["what_it_does"].rstrip().endswith(".")
        # Written for a general reader: no code, no shouting.
        assert robot["what_it_does"].isascii()
        assert "|" not in robot["what_it_does"]


def test_every_category_is_represented_in_the_gallery():
    counts = logic.category_counts(dataio.load_robots())
    assert set(counts) == set(logic.CATEGORIES)
    for category, count in counts.items():
        assert count >= 1, f"{category} has no robots at all"


def test_category_counts_add_up_to_the_catalogue():
    counts = logic.category_counts(dataio.load_robots())
    assert sum(counts.values()) == len(dataio.load_robots()) == 15
    # defense is the largest family here: TALON, MQ-9, Black Hornet, Vision 60, TB2
    assert counts["defense"] == 5


# --------------------------------------------------------------------------- #
# tone, privacy and offline guarantees
# --------------------------------------------------------------------------- #
def test_no_war_framing_anywhere_in_a_fully_walked_data_tree():
    for filename, record in _all_records():
        for path, text in _walk_strings(record, filename):
            found = logic.find_banned_terms(text)
            assert not found, f"{path} reads as war framing: {found}"


def test_defense_entries_are_neutral_and_carry_a_balanced_note():
    defense = [robot for robot in dataio.load_robots() if robot["category"] == "defense"]
    assert len(defense) == 5
    for robot in defense:
        assert robot.get("note"), f"{robot['name']} needs a balanced note"
        assert all(robot.get("emoji") for robot in defense)
        combined = (robot["what_it_does"] + " " + robot["note"]).lower()
        assert any(
            phrase in combined
            for phrase in ("border patrol", "surveillance", "search and rescue", "inspection", "hazardous")
        ), f"{robot['name']} should describe a neutral, defensible mission"


def test_no_personal_information_or_contact_details_in_any_data_file():
    for path in sorted(DATA_DIR.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for location, text in _walk_strings(payload, path.name):
            hits = logic.find_personal_patterns(text)
            assert not hits, f"{path.name}:{location} contains {hits}"


def test_no_network_imports_or_external_calls_anywhere_in_the_source_tree():
    banned_modules = {
        "requests",
        "urllib",
        "urllib2",
        "urllib3",
        "httpx",
        "aiohttp",
        "socket",
        "http",
        "ftplib",
        "smtplib",
        "telnetlib",
        "xmlrpc",
        "ssl",
        "paramiko",
        "boto3",
        "openai",
        "anthropic",
    }
    sources = [ROOT / "app.py", *sorted((ROOT / "titan").rglob("*.py"))]
    assert sources, "expected to find application source files"
    for source in sources:
        tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported = {alias.name.split(".")[0] for alias in node.names}
            elif isinstance(node, ast.ImportFrom):
                imported = {(node.module or "").split(".")[0]}
            else:
                continue
            assert not (imported & banned_modules), f"{source.name} imports {imported & banned_modules}"

    for path in sorted(DATA_DIR.glob("*.json")):
        text = path.read_text(encoding="utf-8")
        assert "http://" not in text and "https://" not in text
        assert "api" not in text.lower().replace("rapid", "")


def test_every_data_file_is_local_and_json_only():
    files = sorted(path.name for path in DATA_DIR.glob("*"))
    assert files == ["concepts.json", "future.json", "robots.json"]
    for path in DATA_DIR.glob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))  # must parse


# --------------------------------------------------------------------------- #
# concepts and timeline
# --------------------------------------------------------------------------- #
def test_concept_lab_contains_the_three_original_concepts():
    concepts = {concept["name"]: concept for concept in dataio.load_concepts()}
    assert set(concepts) == {"SCUNTER", "XEROKLASE", "CIRCUMKANCE"}

    scunter = concepts["SCUNTER"]
    assert scunter["specs"]["speed_kmh"] == 45
    assert "camouflage" in scunter["ability"].lower()
    assert "armour" in scunter["weakness"].lower() or "armor" in scunter["weakness"].lower()
    assert "light" in scunter["weakness"].lower()

    assert "construction" in concepts["XEROKLASE"]["class"].lower()
    assert concepts["XEROKLASE"]["specs"]["payload_kg"] >= 1000
    assert "holograph" in concepts["CIRCUMKANCE"]["ability"].lower()

    for concept in concepts.values():
        assert concept["ability"].strip() and concept["weakness"].strip()
        assert len(concept["design_notes"]) >= 200, "design notes should explain the engineering"
        assert 1 <= concept["specs"]["autonomy_1_5"] <= 5


def test_future_timeline_spans_2025_to_2050_and_covers_the_big_themes():
    milestones = dataio.load_future()
    years = [item["year"] for item in milestones]
    assert years[0] == 2025 and years[-1] == 2050
    assert years == sorted(years)
    assert len(milestones) >= 6

    blob = " ".join(f"{item['title']} {item['text']} {item.get('tag', '')}".lower() for item in milestones)
    assert "ai" in blob
    assert "swarm" in blob
    assert "humanoid" in blob
    assert "home" in blob

    for item in milestones:
        assert item["emoji"], "each milestone needs an emoji icon"
        assert 40 <= len(item["text"]) <= 400


@pytest.mark.parametrize("filename", ["robots.json", "concepts.json", "future.json"])
def test_data_files_are_pretty_printed_utf8_json(filename):
    raw = (DATA_DIR / filename).read_bytes()
    text = raw.decode("utf-8")
    assert text.startswith("[\n"), "expected pretty-printed JSON"
    assert "\t" not in text
    assert json.loads(text)

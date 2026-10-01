"""Test 1 of 3 - pure logic in ``titan.logic`` (no Streamlit, no I/O)."""

from __future__ import annotations

import pytest

from titan import logic


def _robot(name, category, year, text="Does something useful in the real world."):
    return {
        "name": name,
        "category": category,
        "country": "Testland",
        "year": year,
        "what_it_does": text,
        "cool_fact": "It has a cool fact.",
    }


# --------------------------------------------------------------------------- #
# maths: reaction distance
# --------------------------------------------------------------------------- #
def test_reaction_distance_scales_with_speed_and_latency():
    assert logic.reaction_distance_m(2.0, 100) == pytest.approx(0.2)
    assert logic.reaction_distance_cm(2.0, 100) == pytest.approx(20.0)
    # twice the speed, twice the distance
    assert logic.reaction_distance_m(4.0, 100) == pytest.approx(2 * logic.reaction_distance_m(2.0, 100))


def test_reaction_distance_rejects_negative_inputs():
    with pytest.raises(ValueError):
        logic.reaction_distance_m(-1.0, 100)
    with pytest.raises(ValueError):
        logic.reaction_distance_m(2.0, -5)


def test_compare_reaction_flags_a_faster_robot_and_counts_saved_centimetres():
    fast = logic.compare_reaction(speed_mps=25.0, latency_ms=80)
    assert fast["faster"] is True
    assert fast["robot_cm"] == pytest.approx(200.0)
    assert fast["human_cm"] == pytest.approx(500.0)
    assert fast["saved_cm"] == pytest.approx(300.0)

    slow = logic.compare_reaction(speed_mps=2.0, latency_ms=300)
    assert slow["faster"] is False
    assert slow["saved_cm"] == 0.0


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def test_normalise_and_number_formatting():
    assert logic.normalise("  Hello   WORLD ") == "hello world"
    assert logic.pretty_number(1200) == "1,200"
    assert logic.pretty_number(45.5) == "45.5"
    assert logic.meters(0.35) == "35 cm"
    assert logic.meters(2.5) == "2.50 m"


# --------------------------------------------------------------------------- #
# content guard rails
# --------------------------------------------------------------------------- #
def test_banned_terms_match_whole_words_only():
    # "warehouse" and "toward" merely contain "war"; they must not be flagged.
    assert logic.find_banned_terms("A warehouse robot rolls toward the shelf.") == []
    assert "weapon" in logic.find_banned_terms("It is not a weapon.")
    assert "military" in logic.find_banned_terms("Military use is documented elsewhere.")


def test_personal_patterns_detect_emails_urls_and_numbers():
    # Fixtures use reserved example domains and obviously fake digits - never real data.
    assert "email address" in logic.find_personal_patterns("write to someone@example.com")
    assert "external URL" in logic.find_personal_patterns("see https://example.com/page")
    assert "phone-like number" in logic.find_personal_patterns("call 9876543210 now")
    assert logic.find_personal_patterns("Boston Dynamics Spot walks up stairs.") == []


# --------------------------------------------------------------------------- #
# filtering, sorting and validation
# --------------------------------------------------------------------------- #
def test_filter_robots_by_query_and_category():
    robots = [
        _robot("Curiosity Rover", "space", 2012, "Explores Mars and drills rocks."),
        _robot("Warehouse Mover", "industry", 2012, "Carries shelves to people."),
        _robot("Deep Diver", "research", 2010, "Maps the sea floor for science."),
    ]
    by_text = logic.filter_robots(robots, query="mars")
    assert [robot["name"] for robot in by_text] == ["Curiosity Rover"]

    by_category = logic.filter_robots(robots, categories=["industry", "research"])
    assert {robot["name"] for robot in by_category} == {"Warehouse Mover", "Deep Diver"}

    assert logic.filter_robots(robots, query="nothing-here") == []


def test_sort_options_do_not_mutate_the_input_list():
    robots = [
        _robot("Beta", "space", 2010),
        _robot("alpha", "industry", 2020),
        _robot("Gamma", "rescue", 2015),
    ]
    original = list(robots)

    assert [r["name"] for r in logic.sort_robots(robots, "Name (A-Z)")] == ["alpha", "Beta", "Gamma"]
    assert [r["year"] for r in logic.sort_robots(robots, "Year (newest first)")] == [2020, 2015, 2010]
    assert [r["year"] for r in logic.sort_robots(robots, "Year (oldest first)")] == [2010, 2015, 2020]
    assert [r["name"] for r in logic.sort_robots(robots, "Category")] == ["alpha", "Gamma", "Beta"]
    assert robots == original


def test_validation_catches_broken_records():
    good = _robot("Fine Robot", "industry", 2012)
    assert logic.validate_robots([good]) == []

    bad = _robot("Bad Robot", "spacecraft", 1200, text="Too short.")
    problems = logic.validate_robots([bad])
    assert any("unknown category" in problem for problem in problems)
    assert any("year must be" in problem for problem in problems)
    assert any("too short" in problem for problem in problems)

    assert logic.validate_robots([]) == ["robots.json is empty"]
    duplicated = logic.validate_robots([good, dict(good)])
    assert any("duplicate name" in problem for problem in duplicated)


def test_validation_rejects_war_framing_in_descriptions():
    flagged = _robot("Flagged Robot", "industry", 2020, text="This robot is a weapon of some kind.")
    flagged["cool_fact"] = "It can strike a target."
    problems = logic.validate_robots([flagged])
    assert any("war framing" in problem for problem in problems)


def test_validation_rules_for_concepts_and_timeline():
    concept = {
        "name": "TESTBOT",
        "class": "Test Rig",
        "ability": "Does a thing well.",
        "weakness": "Cannot swim.",
        "design_notes": "Notes about the design.",
        "specs": {"speed_kmh": 10, "runtime_h": 2, "payload_kg": 5, "autonomy_1_5": 3},
    }
    assert logic.validate_concepts([concept]) == []
    broken = dict(concept, specs={"speed_kmh": "fast", "runtime_h": 2, "payload_kg": 5, "autonomy_1_5": 9})
    problems = logic.validate_concepts([broken])
    assert any("specs.speed_kmh must be a number" in problem for problem in problems)
    assert any("specs.autonomy_1_5 must be between" in problem for problem in problems)

    milestone = {"year": 2025, "title": "Start", "text": "Something happens."}
    assert logic.validate_future([milestone, dict(milestone, year=2050)]) == []
    assert any("2025" in problem for problem in logic.validate_future([dict(milestone, year=2030)]))


def test_category_counts_and_year_span():
    robots = [
        _robot("A", "space", 2012),
        _robot("B", "space", 2020),
        _robot("C", "rescue", 2014),
    ]
    counts = logic.category_counts(robots)
    assert counts["space"] == 2
    assert counts["rescue"] == 1
    assert counts["medical"] == 0
    assert set(counts) == set(logic.CATEGORIES)
    assert logic.year_span(robots) == (2012, 2020)
    assert logic.year_span([]) == (0, 0)


def test_read_json_refuses_to_leave_the_data_folder():
    for bad_name in ("../secrets.json", "..%2fsecrets.json", "/etc/passwd", "data/robots.json", "robots.txt", ""):
        with pytest.raises(ValueError):
            logic.read_json(bad_name)
    # a bare filename inside data/ still works
    assert logic.read_json("robots.json")

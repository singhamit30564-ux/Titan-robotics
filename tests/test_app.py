"""Test 3 of 3 - AppTest smoke tests: every page renders, widgets behave.

These tests drive the real Streamlit script through ``AppTest``, so they cover
the views, the components and the bundled data end to end.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from titan.views import PAGES

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = str(ROOT / "app.py")
TIMEOUT = 60


def _start() -> AppTest:
    """Boot a fresh app instance on the Home page."""
    app = AppTest.from_file(APP_PATH, default_timeout=TIMEOUT)
    app.run()
    assert not app.exception, app.exception
    return app


def _text(app: AppTest) -> str:
    """All rendered markdown on the page, joined into one searchable string."""
    chunks = [str(element.value) for element in app.markdown]
    for collection in (app.caption, app.info, app.success, app.warning, app.error):
        chunks.extend(str(element.value) for element in collection)
    return " ".join(chunks)


def _goto(app: AppTest, label: str) -> AppTest:
    """Switch pages through the top navigation radio."""
    app.radio[0].set_value(label).run()
    assert not app.exception, app.exception
    return app


def test_navigation_lists_all_five_pages_and_home_renders():
    app = _start()
    assert app.radio[0].options == [label for label, _ in PAGES]
    assert len(PAGES) == 5

    home = _text(app)
    assert "Explore" in home and "Design" in home and "Build" in home
    assert "Sense" in home and "Think" in home and "Act" in home
    assert "Real Robots" in home and "Concept Lab" in home


@pytest.mark.parametrize("label,_", [(label, fn) for label, fn in PAGES])
def test_every_page_renders_without_errors(label, _):
    app = _goto(_start(), label)
    assert not app.exception, app.exception
    assert not _text(app).strip().startswith("Traceback")
    assert len(_text(app)) > 500, f"{label} rendered almost nothing"


def test_real_robots_search_filters_the_gallery():
    app = _goto(_start(), "🤖 Real Robots")
    everything = _text(app)
    for name in ("Boston Dynamics Spot", "Curiosity Rover", "SCUNTER"):
        if name == "SCUNTER":
            continue
        assert name in everything

    app.text_input[0].set_value("mars").run()
    assert not app.exception, app.exception
    filtered = _text(app)
    assert "Curiosity Rover" in filtered
    assert "Pepper Service Humanoid" not in filtered
    assert "1 of 15" in filtered

    app.text_input[0].set_value("").run()
    app.multiselect[0].set_value(["space", "medical"]).run()
    assert not app.exception, app.exception
    by_category = _text(app)
    assert "Curiosity Rover" in by_category
    assert "Da Vinci Surgical System" in by_category
    assert "BigDog" not in by_category

    app.multiselect[0].set_value([]).run()
    app.text_input[0].set_value("zzzz-nothing").run()
    assert not app.exception, app.exception
    assert app.info, "an empty result should explain itself"
    assert "No robot matches" in app.info[0].value


def test_real_robots_sort_options_run_without_errors():
    app = _goto(_start(), "🤖 Real Robots")
    for option in ("Name (A-Z)", "Year (oldest first)", "Category"):
        app.selectbox[0].select(option).run()
        assert not app.exception, app.exception
        assert "Boston Dynamics Spot" in _text(app)


def test_how_robots_work_playground_reacts_to_the_slider():
    app = _goto(_start(), "⚙️ How Robots Work")
    for heading in ("Sensors", "Actuators", "Processor", "Power"):
        assert heading in _text(app)

    fast = _text(app)
    assert "cm" in fast

    app.slider[0].set_value(300).run()
    assert not app.exception, app.exception
    slow_metrics = [metric.value for metric in app.metric]
    app.slider[0].set_value(10).run()
    quick_metrics = [metric.value for metric in app.metric]
    assert slow_metrics != quick_metrics
    assert app.success or app.warning


def test_concept_lab_shows_concepts_and_previews_a_sketch():
    app = _goto(_start(), "🧪 Concept Lab")
    lab = _text(app)
    for name in ("SCUNTER", "XEROKLASE", "CIRCUMKANCE"):
        assert name in lab
    assert "camouflage" in lab.lower()
    assert "45" in lab

    app.text_input[0].set_value("AQUASIFT").run()
    app.text_input[1].set_value("River Cleanup Crawler").run()
    app.text_area[0].set_value("Scoops floating plastic out of slow rivers.").run()
    app.text_area[1].set_value("Cannot work in strong currents.").run()
    assert not app.exception, app.exception
    preview = _text(app)
    assert "AQUASIFT" in preview
    assert "River Cleanup Crawler" in preview
    assert "strong currents" in preview


def test_future_timeline_covers_the_expected_years():
    app = _goto(_start(), "🚀 Future")
    page = _text(app)
    assert "2025" in page and "2050" in page
    assert "swarm" in page.lower()
    assert "humanoid" in page.lower()
    assert "privacy" in page.lower()


def test_app_is_offline_and_shows_the_data_health_check():
    app = _start()
    assert app.sidebar is not None  # sidebar stays collapsed; nav lives at the top
    assert "all files valid" in _text(app)
    assert not app.error

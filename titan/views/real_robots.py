"""Real Robots page: the 15-robot gallery with search, filter and sort."""

from __future__ import annotations

import streamlit as st

from titan import components as ui
from titan import logic


def render(data: dict) -> None:
    """Draw the Real Robots gallery."""
    robots = data["robots"]

    ui.render(
        ui.section(
            "Real Robots",
            "Fifteen machines that exist today. Every card gives the country of origin, the year it appeared, "
            "what it does in plain English, and one genuinely cool fact.",
        )
    )

    query = st.text_input(
        "Search robots",
        placeholder="Try: Mars, underwater, hospital, Norway, warehouse…",
        label_visibility="collapsed",
        key="robots_search",
    )

    left, right = st.columns(2)
    with left:
        categories = st.multiselect(
            "Categories",
            options=list(logic.CATEGORIES),
            default=[],
            placeholder="All categories",
            key="robots_categories",
        )
    with right:
        sort_by = st.selectbox("Sort by", options=list(logic.SORT_OPTIONS), index=1, key="robots_sort")

    results = logic.filter_robots(robots, query=query, categories=categories, sort_by=sort_by)

    if not results:
        st.info("No robot matches that search yet. Try a shorter word, or clear the categories filter.")
        return

    total = len(robots)
    shown = len(results)
    label = "all of them" if shown == total else f"{shown} of {total}"
    ui.render(
        f'<p class="tr-muted" style="margin:.2rem 0 .6rem">Showing <b style="color:#f0d97a">{label}</b>'
        f"{' matching “' + ui.esc(query) + '”' if query else ''}.</p>"
    )

    ui.render(ui.grid([ui.robot_card(robot) for robot in results], min_px=300))

    with st.expander("🧾 Data health check", expanded=False):
        problems = data["problems"]["robots"]
        if problems:
            st.warning("Some robot entries need attention:\n\n- " + "\n- ".join(problems))
        else:
            st.success(
                f"All {total} robot entries passed validation: required fields present, categories valid, "
                "years in range, and no war framing in any description."
            )
        st.caption(
            "Validation runs fully offline against data/robots.json using titan.logic.validate_robots."
        )


"""Titan Robotics - a Streamlit app for learning about robotics.

Run it with::

    streamlit run app.py

Everything is offline: the data is bundled in ``data/*.json``, the theme is
plain CSS, and the app never makes a network request or asks for a key.
"""

from __future__ import annotations

import streamlit as st

from titan import dataio, theme
from titan.views import PAGES


def main() -> None:
    """Configure the page, draw the navigation and render the selected view."""
    st.set_page_config(
        page_title="Titan Robotics · Explore · Design · Build",
        page_icon="🛰️",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    theme.inject()
    theme.brand_bar()

    data = dataio.load_all()
    labels = [label for label, _ in PAGES]
    renderers = dict(PAGES)

    choice = st.radio(
        "Page",
        options=labels,
        index=0,
        horizontal=True,
        label_visibility="collapsed",
        key="nav_page",
    )
    renderers[choice](data)

    problems = dataio.all_problems()
    with st.expander("ℹ️ About Titan Robotics", expanded=False):
        st.markdown(
            "**Titan Robotics** is a small, self-contained museum of robotics: 15 real machines, "
            "the four building blocks every robot shares, three original design concepts and a "
            "timeline to 2050.\n\n"
            "- **Offline by design** — all content lives in local JSON files. No APIs, no keys, no tracking.\n"
            "- **No personal data** — the app never asks for your name, email or location.\n"
            "- **Neutral tone** — defense robots are described as border patrol, surveillance and "
            "hazardous-object inspection work, each with a balanced note.\n"
            "- **Built to be checked** — pure logic lives in `titan/logic.py` and is covered by tests."
        )
        st.caption(f"Data check: {'✅ all files valid' if not problems else '⚠️ ' + '; '.join(problems)}")
        st.caption("Sources: publicly documented specifications and manufacturer material for each robot.")

    theme.footer_note()


if __name__ == "__main__":
    main()

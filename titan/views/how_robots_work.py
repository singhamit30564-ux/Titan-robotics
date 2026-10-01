"""How Robots Work page: the four building blocks, plus a latency playground."""

from __future__ import annotations

import streamlit as st

from titan import components as ui
from titan import content, logic


def _part_card(part: dict) -> str:
    """One of the four building-block cards, with its emoji diagram."""
    return ui.card(
        title=part["name"],
        subtitle=part["subtitle"],
        icon=part["emoji"],
        body=ui.esc(part["text"]),
        fact=ui.esc(part["examples"]),
        extra=ui.flow(part["diagram"], part["caption"]),
        big_title=True,
    )


def render(data: dict) -> None:
    """Draw the How Robots Work page."""
    ui.render(
        ui.section(
            "How Robots Work",
            "Four building blocks do all the work: sensors, actuators, processor and power. "
            "Understand these four and most robots stop looking like magic.",
        )
    )
    ui.render(ui.grid([_part_card(part) for part in content.ROBOT_PARTS], min_px=320))

    ui.render(
        ui.section(
            "Playground: why reaction time matters",
            "A robot does not react instantly. It travels a little further while it is still thinking. "
            "Move the slider to see how far that is.",
        )
    )

    labels = [preset[0] for preset in content.LATENCY_PRESETS]
    choice = st.selectbox("Pick a robot and a speed", options=labels, index=2, key="how_preset")
    preset = content.LATENCY_PRESETS[labels.index(choice)]
    speed_mps, default_latency = preset[1], preset[2]

    latency_ms = st.slider(
        "Decision delay (latency) in milliseconds",
        min_value=10,
        max_value=300,
        value=int(default_latency),
        step=5,
        key="how_latency",
    )

    result = logic.compare_reaction(speed_mps, latency_ms)
    kmh = speed_mps * 3.6

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Speed", f"{logic.pretty_number(kmh)} km/h")
    col_b.metric("Robot stop distance", f"{result['robot_cm']:.0f} cm")
    col_c.metric("Human stop distance", f"{result['human_cm']:.0f} cm")

    if result["faster"]:
        st.success(
            f"🤖 At {logic.pretty_number(kmh)} km/h the robot covers {result['robot_cm']:.0f} cm while it decides, "
            f"against {result['human_cm']:.0f} cm for a person taking 200 ms. That "
            f"{result['saved_cm']:.0f} cm of extra braking room is why fast robots still need big safety margins."
        )
    else:
        st.warning(
            f"🐢 At {logic.pretty_number(kmh)} km/h this robot needs {result['robot_cm']:.0f} cm to react, "
            f"more than a human's {result['human_cm']:.0f} cm at the same speed. Slower decisions mean "
            "longer safety distances, so better sensors and faster chips really do matter."
        )
    st.caption("Reaction distance = speed × delay. A human's visual reaction time is about 200 ms.")

    ui.render(
        ui.section(
            "Rules that keep robots safe",
            "Every serious robot programme trades some speed for these four habits.",
        )
    )
    ui.render(
        ui.grid(
            [
                ui.card(title=title, icon="✅", body=ui.esc(text))
                for title, text in content.SAFETY_RULES
            ],
            min_px=250,
        )
    )

    with st.expander("📖 Mini glossary", expanded=False):
        for term, meaning in content.GLOSSARY:
            st.markdown(f"**{term}** — {meaning}")


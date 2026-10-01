"""Future page: the 2025-2050 timeline and the challenges that come with it."""

from __future__ import annotations

import streamlit as st

from titan import components as ui
from titan import content


def render(data: dict) -> None:
    """Draw the Future page."""
    milestones = data["future"]

    ui.render(
        ui.section(
            "Future: 2025 → 2050",
            "A realistic look ahead, not a promise. Each milestone is something engineers, "
            "researchers and regulators are already working on today.",
        )
    )
    ui.render(ui.timeline(milestones))

    ui.render(
        ui.section(
            "The honest part",
            "Every step forward brings a question with it. These are the five that come up most often.",
        )
    )
    ui.render(
        ui.grid(
            [
                ui.card(title=title, icon="⚖️", body=ui.esc(text))
                for title, text in content.FUTURE_CHALLENGES
            ],
            min_px=270,
        )
    )

    ui.render(ui.section("Three things to watch", "Where the biggest change is likely to come from."))
    ui.render(
        ui.grid(
            [
                ui.card(
                    title="Swarm robotics",
                    subtitle="Many small robots, one mind",
                    icon="🐝",
                    body="A hundred cheap robots can cover more ground than one expensive one, and the team "
                    "keeps working when a single unit fails. The hard problem is coordination, not hardware.",
                ),
                ui.card(
                    title="Home humanoids",
                    subtitle="Helpers in everyday spaces",
                    icon="🏠",
                    body="Homes are messy, crowded and unpredictable - the hardest environment a robot can meet. "
                    "Progress will be gradual, task by task, starting with chores and care support.",
                ),
                ui.card(
                    title="Robot learning",
                    subtitle="Skills shared like apps",
                    icon="📚",
                    body="When one robot learns a skill it can teach the whole fleet, so abilities spread far "
                    "faster than they did a decade ago. Safety reviews must keep pace with that speed.",
                ),
            ],
            min_px=280,
        )
    )

    with st.expander("🧑‍🎓 Keep this in mind", expanded=False):
        st.markdown(
            "Timelines in robotics are usually optimistic. Building a robot that works once in a "
            "laboratory is easy compared with building one that works every day for ten years in the rain.\n\n"
            "A useful habit: whenever you read a prediction, ask **who benefits, who is affected, and who "
            "decides**. Those three questions make any technology story much clearer."
        )


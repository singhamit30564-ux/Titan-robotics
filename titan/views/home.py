"""Home page: hero, the three pillars of robotics, and a tour of the app."""

from __future__ import annotations

from titan import components as ui
from titan import content, logic


def hero(robot_count: int, concept_count: int, milestone_count: int) -> str:
    """The big first impression, including the Explore / Design / Build story."""
    return f"""
<div class="tr-hero">
  <div class="tr-hero-eyebrow">Titan Robotics · learn by looking closely</div>
  <div class="tr-hero-title">Explore • Design • Build</div>
  <p class="tr-hero-sub">
    Robotics is the art of building machines that can sense the world, decide what to do,
    and then act on that decision. This little museum walks you through {robot_count} real
    robots, the parts that make them work, {concept_count} original design concepts and a
    timeline of what may come next.
  </p>
  <div class="tr-pills">
    <span class="tr-pill">👁️ Sense</span>
    <span class="tr-pill">🧠 Think</span>
    <span class="tr-pill">💪 Act</span>
    <span class="tr-pill">🔌 100% offline</span>
  </div>
</div>
"""


def render(data: dict) -> None:
    """Draw the Home page."""
    robots = data["robots"]
    concepts = data["concepts"]
    future = data["future"]

    ui.render(hero(len(robots), len(concepts), len(future)))

    counts = logic.category_counts(robots)
    first_year, last_year = logic.year_span(robots)
    ui.render(
        ui.stats(
            [
                (str(len(robots)), "Real robots"),
                (str(len(counts)), "Categories"),
                (str(len(concepts)), "Original concepts"),
                (f"{first_year}–{last_year}", "Build years covered"),
                (str(len(future)), "Future milestones"),
            ]
        )
    )

    ui.render(ui.section("What is robotics?", "Three pillars turn a machine into a robot. Take any one away and it stops being a robot."))
    ui.render(
        ui.grid(
            [
                ui.card(
                    title=pillar["name"],
                    subtitle=pillar["question"],
                    icon=pillar["emoji"],
                    body=ui.esc(pillar["text"]),
                    fact=ui.esc(pillar["extra"]),
                )
                for pillar in content.PILLARS
            ],
            min_px=250,
        )
    )

    ui.render(
        ui.flow(
            [
                ("👁️", "Sense"),
                ("🧠", "Think"),
                ("💪", "Act"),
                ("📊", "Check"),
                ("👁️", "Sense again"),
            ],
            "The loop repeats many times a second: act, measure the result, adjust.",
        )
    )

    ui.render(
        ui.section(
            "Six families of robots",
            "Every robot in this app belongs to one of these families. Defense entries are described neutrally, with a balanced note.",
        )
    )
    ui.render(
        ui.grid(
            [
                ui.card(
                    title=meta["label"],
                    subtitle=f"{counts[category]} robot(s) in the gallery",
                    icon=meta["emoji"],
                    body=ui.esc(_category_blurb(category)),
                    accent=meta["color"],
                )
                for category, meta in logic.CATEGORY_META.items()
            ],
            min_px=230,
        )
    )

    ui.render(ui.section("How to use this app", "Five short pages, best read in order."))
    ui.render(ui.grid([ui.card(**entry) for entry in _TOUR], min_px=240))


_CATEGORY_BLURBS = {
    "rescue": "Search, fire and disaster work where the ground is too dangerous for people.",
    "medical": "Precision tools that help trained doctors and nurses do delicate work.",
    "space": "Explorers that work where no one can repair them, millions of kilometres away.",
    "industry": "Factories, farms, warehouses and building sites: dull, heavy and repetitive jobs.",
    "defense": "Border patrol, surveillance and hazardous-object inspection, always under human control.",
    "research": "Laboratory machines that push what robots can sense, balance and do.",
}

_TOUR = (
    {
        "icon": "🤖",
        "title": "Real Robots",
        "subtitle": "The gallery",
        "body": "Fifteen machines that exist today, from a bee-sized flying robot to a rover on Mars. Filter by category, search, and check the cool fact on every card.",
    },
    {
        "icon": "⚙️",
        "title": "How Robots Work",
        "subtitle": "The parts",
        "body": "Sensors, actuators, processor and power - the four building blocks. Includes a reaction-speed playground that shows why latency matters.",
    },
    {
        "icon": "🧪",
        "title": "Concept Lab",
        "subtitle": "The sketchbook",
        "body": "Three original robot concepts: SCUNTER, XEROKLASE and CIRCUMKANCE. Each one has an ability, an honest weakness and real design notes.",
    },
    {
        "icon": "🚀",
        "title": "Future",
        "subtitle": "The timeline",
        "body": "Where robotics may go between 2025 and 2050, plus the challenges - safety, privacy, work and fair access - that come with it.",
    },
)


def _category_blurb(category: str) -> str:
    """One-line description for a robot family."""
    return _CATEGORY_BLURBS.get(category, "")

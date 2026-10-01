"""Page views for Titan Robotics. Each module exposes ``render(data)``."""

from titan.views import concept_lab, future, home, how_robots_work, real_robots

#: Navigation order shown in the sidebar-free top navigation.
PAGES = (
    ("🏠 Home", home.render),
    ("🤖 Real Robots", real_robots.render),
    ("⚙️ How Robots Work", how_robots_work.render),
    ("🧪 Concept Lab", concept_lab.render),
    ("🚀 Future", future.render),
)

__all__ = ["PAGES", "home", "real_robots", "how_robots_work", "concept_lab", "future"]

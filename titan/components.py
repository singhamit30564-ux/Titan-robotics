"""Small HTML builders for Titan Robotics cards, grids, meters and timelines.

All values coming from data (or from anything a visitor types) pass through
:func:`esc`, so the generated markup can never break the page layout.
"""

from __future__ import annotations

import html

import streamlit as st

from titan import logic


def esc(value: object) -> str:
    """HTML-escape any value before it is placed in markup."""
    return html.escape(str(value), quote=True)


def render(markup: str) -> None:
    """Render a block of trusted, already-escaped HTML."""
    st.markdown(markup, unsafe_allow_html=True)


def grid(items, min_px: int = 260) -> str:
    """Wrap card markup in a responsive, mobile-first grid."""
    return f'<div class="tr-grid" style="--tr-min:{int(min_px)}px">' + "".join(items) + "</div>"


def section(title: str, subtitle: str = "") -> str:
    """A section heading block with an optional subtitle."""
    block = f'<div class="tr-section"><h3>{esc(title)}</h3>'
    if subtitle:
        block += f"<p>{esc(subtitle)}</p>"
    return block + "</div>"


def stat(value: str, label: str) -> str:
    """One small statistic tile."""
    return (
        '<div class="tr-stat">'
        f'<div class="tr-stat-value">{esc(value)}</div>'
        f'<div class="tr-stat-label">{esc(label)}</div>'
        "</div>"
    )


def stats(items) -> str:
    """A responsive row of statistic tiles from ``(value, label)`` pairs."""
    return '<div class="tr-stats">' + "".join(stat(value, label) for value, label in items) + "</div>"


def badge(text: str, color: str | None = None, gold: bool = False) -> str:
    """A small rounded label, optionally tinted with a category colour."""
    classes = "tr-badge tr-badge--gold" if gold else "tr-badge"
    style = f' style="border-color:{esc(color)}66;background:{esc(color)}1f;color:{esc(color)}"' if color else ""
    return f'<span class="{classes}"{style}>{esc(text)}</span>'


def card(
    *,
    title: str,
    subtitle: str = "",
    icon: str = "",
    body: str = "",
    badge_html: str = "",
    fact: str = "",
    note: str = "",
    accent: str | None = None,
    big_title: bool = False,
    extra: str = "",
    centered_icon: bool = False,
) -> str:
    """Build one themed card.

    ``body``, ``fact`` and ``note`` accept pre-built HTML (escape your own
    pieces with :func:`esc`); every other argument is escaped here.
    """
    style = f' style="--tr-accent:{esc(accent)}"' if accent else ""
    title_class = "tr-card-title tr-card-title--big" if big_title else "tr-card-title"
    parts = [f'<div class="tr-card"{style}>']
    if centered_icon and icon:
        parts.append(f'<div class="tr-icon" style="font-size:2rem">{esc(icon)}</div>')
        parts.append(f'<div class="{title_class}" style="margin-top:.4rem">{esc(title)}</div>')
    elif icon:
        parts.append(
            '<div class="tr-row">'
            f'<span class="tr-icon">{esc(icon)}</span>'
            f'<span class="{title_class}">{esc(title)}</span>'
            f"{badge_html}</div>"
        )
    else:
        parts.append(f'<div class="tr-row"><span class="{title_class}">{esc(title)}</span>{badge_html}</div>')
    if subtitle:
        parts.append(f'<div class="tr-card-sub">{esc(subtitle)}</div>')
    if body:
        parts.append(f'<div class="tr-card-text">{body}</div>')
    if fact:
        parts.append(f'<div class="tr-fact">{fact}</div>')
    if note:
        parts.append(f'<div class="tr-note">{note}</div>')
    if extra:
        parts.append(extra)
    parts.append("</div>")
    return "".join(parts)


def flow(nodes, caption: str = "") -> str:
    """An emoji diagram: ``nodes`` is a list of ``(emoji, label)`` pairs."""
    pieces = ['<div class="tr-flow">']
    for index, (emoji, label) in enumerate(nodes):
        if index:
            pieces.append('<span class="tr-flow-arrow">➜</span>')
        pieces.append(
            f'<div class="tr-flow-node"><b>{esc(emoji)}</b><span>{esc(label)}</span></div>'
        )
    pieces.append("</div>")
    if caption:
        pieces.append(f'<div class="tr-flow-caption">{esc(caption)}</div>')
    return "".join(pieces)


def meter(label: str, value: float, max_value: float, suffix: str = "") -> str:
    """A gold progress bar used to compare robot concept specs."""
    ratio = 0.0 if max_value <= 0 else max(0.0, min(1.0, float(value) / float(max_value)))
    shown = logic.pretty_number(value) + (f" {suffix}" if suffix else "")
    return (
        '<div class="tr-meter">'
        f'<div class="tr-meter-head"><span>{esc(label)}</span><b>{esc(shown)}</b></div>'
        '<div class="tr-meter-track">'
        f'<div class="tr-meter-fill" style="width:{ratio * 100:.1f}%"></div>'
        "</div></div>"
    )


def robot_card(robot: dict) -> str:
    """Card for one real robot from ``data/robots.json``."""
    meta = logic.CATEGORY_META.get(robot.get("category", ""), {"label": robot.get("category", ""), "emoji": "🤖", "color": "#d4af37"})
    fact = f'<span class="tr-label">💡 Cool fact:</span> {esc(robot.get("cool_fact", ""))}'
    note = f"⚖️ <span class=\"tr-label\">Balanced note:</span> {esc(robot['note'])}" if robot.get("note") else ""
    return card(
        title=robot.get("name", "Robot"),
        subtitle=f"{robot.get('country', '')} · {robot.get('year', '')}",
        icon=robot.get("emoji", meta.get("emoji", "🤖")),
        badge_html=badge(meta["label"], color=meta.get("color")),
        body=f'<span class="tr-label">What it does:</span> {esc(robot.get("what_it_does", ""))}',
        fact=fact,
        note=note,
        accent=meta.get("color", "#d4af37"),
    )


def concept_card(concept: dict) -> str:
    """Card for one original concept from ``data/concepts.json``."""
    specs = concept.get("specs", {})
    meters = "".join(
        [
            meter("Top speed", specs.get("speed_kmh", 0), 50, "km/h"),
            meter("Runtime", specs.get("runtime_h", 0), 12, "h"),
            meter("Payload", specs.get("payload_kg", 0), 1200, "kg"),
            meter("Autonomy", specs.get("autonomy_1_5", 0), 5, "/ 5"),
        ]
    )
    body = (
        f'<span class="tr-label">🔧 Ability:</span> {esc(concept.get("ability", ""))}<br><br>'
        f'<span class="tr-label">⚠️ Weakness:</span> {esc(concept.get("weakness", ""))}'
    )
    return card(
        title=concept.get("name", "Concept"),
        subtitle=str(concept.get("class", "")),
        icon=concept.get("emoji", "🧪"),
        badge_html=badge("Original concept", gold=True),
        body=body,
        extra=f'<p class="tr-tagline">{esc(concept.get("tagline", ""))}</p>'
        f'<div class="tr-block">📐 <span class="tr-label">Design notes:</span> {esc(concept.get("design_notes", ""))}</div>'
        f'<div style="margin-top:.75rem">{meters}</div>',
        big_title=True,
    )


def timeline(milestones) -> str:
    """Vertical timeline of ``2025-2050`` milestones."""
    pieces = ['<div class="tr-timeline">']
    for item in milestones:
        title = f'{item.get("emoji", "🔹")} {item.get("title", "")}'
        pieces.append(
            '<div class="tr-tl-item">'
            '<span class="tr-tl-dot"></span>'
            + card(
                title=title,
                subtitle="",
                badge_html=badge(str(item.get("tag", "")), gold=True),
                body=esc(item.get("text", "")),
                extra=f'<span class="tr-tl-year" style="margin-top:.2rem;display:inline-block">{esc(item.get("year", ""))}</span>',
            )
            + "</div>"
        )
    pieces.append("</div>")
    return "".join(pieces)


def expander_rows(rows) -> str:
    """Simple label/value list rendered as small rows inside a card."""
    return "".join(
        f'<div class="tr-block"><span class="tr-label">{esc(label)}:</span> {esc(value)}</div>'
        for label, value in rows
    )

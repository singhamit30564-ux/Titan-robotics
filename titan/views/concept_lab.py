"""Concept Lab page: three original robot concepts plus a sketching activity."""

from __future__ import annotations

import streamlit as st

from titan import components as ui
from titan import content


def _comparison_table(concepts) -> str:
    """A plain HTML table comparing the three concept robots on one screen."""
    headers = ["Concept", "Class", "Top speed", "Runtime", "Payload", "Weakness"]
    head = "".join(f"<th>{ui.esc(h)}</th>" for h in headers)
    rows = []
    for concept in concepts:
        specs = concept.get("specs", {})
        cells = [
            f"{concept.get('emoji', '🧪')} {concept.get('name', '')}",
            concept.get("class", ""),
            f"{specs.get('speed_kmh', '?')} km/h",
            f"{specs.get('runtime_h', '?')} h",
            f"{specs.get('payload_kg', '?')} kg",
            concept.get("weakness", ""),
        ]
        rows.append("<tr>" + "".join(f"<td>{ui.esc(cell)}</td>" for cell in cells) + "</tr>")
    return (
        '<div class="tr-table-wrap"><table class="tr-table">'
        f"<thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"
    )


def render(data: dict) -> None:
    """Draw the Concept Lab page."""
    concepts = data["concepts"]

    ui.render(
        ui.section(
            "Concept Lab",
            "Three original robot concepts, drawn up the way a design studio would: one clear ability, "
            "one honest weakness, and notes explaining the engineering behind both.",
        )
    )
    ui.render(ui.grid([ui.concept_card(concept) for concept in concepts], min_px=330))

    ui.render(ui.section("Side by side", "The same three concepts, compared at a glance."))
    ui.render(_comparison_table(concepts))

    with st.expander("🧮 Why the numbers matter", expanded=False):
        st.markdown(
            "**Speed and armour pull in opposite directions.** SCUNTER is the fastest concept at "
            "45 km/h, which is exactly why it cannot carry heavy protection - every kilogram spent on "
            "plating is a kilogram taken away from batteries and sensors.\n\n"
            "**Payload sets the price.** XEROKLASE lifts 1,200 kg but moves at walking pace and needs a "
            "prepared surface. Heavy work is usually slow work.\n\n"
            "**Autonomy is a dial, not a switch.** Each concept lists a score from 1 to 5 for how much it "
            "decides on its own. CIRCUMKANCE scores 3: it can guide a technician through a repair, but a "
            "human still holds the tools."
        )

    ui.render(
        ui.section(
            "Your turn: sketch a concept",
            "Nothing you type is saved or sent anywhere. It lives in your browser tab and disappears when you close it.",
        )
    )
    name = st.text_input("Robot name", placeholder="e.g. AQUASIFT", key="sketch_name")
    klass = st.text_input("Class", placeholder="e.g. River Cleanup Crawler", key="sketch_class")
    ability = st.text_area("Ability", placeholder="One thing it does better than anything else.", key="sketch_ability")
    weakness = st.text_area("Weakness", placeholder="Be honest - every good design has one.", key="sketch_weakness")

    if name or ability or weakness:
        ui.render(
            ui.grid(
                [
                    ui.card(
                        title=name or "UNNAMED",
                        subtitle=klass or "Unclassified",
                        icon="✏️",
                        badge_html=ui.badge("Your sketch", gold=True),
                        body=f'<span class="tr-label">🔧 Ability:</span> {ui.esc(ability or "-")}<br><br>'
                        f'<span class="tr-label">⚠️ Weakness:</span> {ui.esc(weakness or "-")}',
                        big_title=True,
                    )
                ],
                min_px=330,
            )
        )

    with st.expander("💡 Prompts to make a concept stronger", expanded=False):
        for prompt in content.SKETCH_PROMPTS:
            st.markdown(f"- {prompt}")


# 🛰️ Titan Robotics

**Explore • Design • Build** — an offline, mobile-first Streamlit app that teaches robotics
with real machines, clear diagrams and original design concepts.

No APIs. No keys. No external calls. No personal data. Everything the app shows is bundled in
`data/*.json` and read locally.

---

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

streamlit run app.py          # open http://localhost:8501
```

Run the checks:

```bash
python -m py_compile app.py titan/*.py titan/views/*.py   # syntax
python -m pytest                                          # 40 tests in 3 modules
```

---

## The five pages

| # | Page | What's inside | Data source |
|---|------|---------------|-------------|
| 1 | 🏠 **Home** | “Explore • Design • Build” hero, the three pillars of robotics (Sense 👁️ / Think 🧠 / Act 💪), the sense→think→act feedback loop, the six robot families and a tour of the app | `data/robots.json` (counts), `data/concepts.json`, `data/future.json` |
| 2 | 🤖 **Real Robots** | 15 real robots with search, category filter and four sort modes; every card carries country, year, plain-English job description, a cool fact and — for defense entries — a balanced note | `data/robots.json` |
| 3 | ⚙️ **How Robots Work** | Four building-block cards (Sensors, Actuators, Processor, Power) with emoji diagrams, a reaction-time playground, four safety habits and a mini glossary | `titan/content.py` |
| 4 | 🧪 **Concept Lab** | Three original concepts — SCUNTER, XEROKLASE, CIRCUMKANCE — each with ability, weakness, design notes and spec meters, plus a comparison table and a sketching tool | `data/concepts.json` |
| 5 | 🚀 **Future** | An eight-milestone timeline from 2025 to 2050 (AI, swarms, home humanoids), the honest challenges and three things to watch | `data/future.json` |

### The 15 real robots

| Category | Robots |
|----------|--------|
| 🛟 Rescue | Thermite RS3 Firefighting Robot |
| 🩺 Medical | Da Vinci Surgical System |
| 🛰️ Space | Curiosity Rover |
| 🏭 Industry | Boston Dynamics Spot, Amazon Robotics Drive Unit, Pepper Service Humanoid |
| 🛡️ Defense | TALON, MQ-9 Reaper, Black Hornet 3, Ghost Vision 60, Bayraktar TB2 |
| 🔬 Research | Boston Dynamics Atlas, RoboBee, BigDog, Sentry AUV |

### The three original concepts

| Concept | Class | Ability | Weakness |
|---------|-------|---------|----------|
| 🦎 **SCUNTER** | Recon & Search Scout | Adaptive camouflage (45 km/h top speed) | Light armour — a hard impact ends the mission |
| 🏗️ **XEROKLASE** | Heavy-Duty Construction Rig | Millimetre-accurate placement of 1,200 kg panels | Needs a wide, flat, prepared base |
| 🔮 **CIRCUMKANCE** | Holographic Assistant | Projects 3D holograms in mid-air | Daylight washes the image out; high power draw |

---

## Design system

| Token | Value | Use |
|-------|-------|-----|
| Background | `#0a0e17` | Page base, with soft gold/blue radial glows |
| Surface | `#141c2b` → `#0f1522` | Card gradient |
| Accent | `#d4af37` (light: `#f0d97a`) | Headings, badges, meters, hero gradient |
| Text / muted | `#e9eef8` / `#93a0b8` | Body copy / secondary copy |
| Category tints | rescue `#ff8a5c`, medical `#7dd3fc`, space `#a78bfa`, industry `#34d399`, defense `#9fb3c8`, research `#facc15` | Badges and card accent bars |

Mobile-first: every card sits in a `repeat(auto-fit, minmax(min(…px, 100%), 1fr))` grid, so
layouts collapse to a single readable column on a phone. No sidebar, no web fonts, no images —
just emoji icons and inline CSS (`.streamlit/config.toml` sets the matching dark theme).

---

## Editorial policy

* **No war framing.** Defense robots are described as *border patrol, surveillance and
  hazardous-object inspection* work, and each one ends with a balanced ⚖️ note about
  human responsibility, privacy or how rules are applied.
* **Enforced in code, not just intent.** `titan.logic.find_banned_terms()` scans every data
  string against a whole-word list (`war`, `weapon`, `missile`, `combat`, …), and the test
  suite fails the build if any entry slips through. Words that merely contain those letters —
  *warehouse*, *toward* — are never flagged.
* **Plain English.** Every description is written for a curious teenager: short sentences,
  no jargon, no marketing claims.

---

## Privacy & offline guarantees

| Guarantee | How it is kept | Verified by |
|-----------|----------------|-------------|
| No network calls | Only `streamlit`, stdlib and local JSON imports anywhere in the tree | `tests/test_data.py::test_no_network_imports_or_external_calls_anywhere_in_the_source_tree` (AST scan) |
| No keys or secrets | Nothing in the code or data references a token, key or URL | `test_no_personal_information_or_contact_details_in_any_data_file` |
| No personal data | The app never asks for a name, email or location; the concept sketchpad is an in-memory widget only | same test + `titan.logic.PERSONAL_PATTERNS` |
| Local data only | `titan.logic.read_json` accepts a bare `.json` filename inside `data/` and rejects traversal | `test_read_json_refuses_to_leave_the_data_folder` |

---

## Project structure

```
app.py                      # entry point: page config, nav radio, about expander
.streamlit/config.toml      # dark theme tokens matching the CSS
data/
  robots.json               # 15 real robots
  concepts.json             # SCUNTER, XEROKLASE, CIRCUMKANCE
  future.json               # 2025 → 2050 timeline
titan/
  logic.py                  # pure helpers: filtering, sorting, validation, reaction maths
  dataio.py                 # cached, validated loading of the JSON data
  theme.py                  # CSS theme + brand bar + footer
  components.py             # HTML builders: cards, grids, badges, meters, timeline, flow
  content.py                # teaching text: pillars, building blocks, glossary, safety rules
  views/                    # one module per page, each exposing render(data)
tests/
  test_logic.py             # test 1 of 3 — pure logic
  test_data.py              # test 2 of 3 — content, tone, privacy, offline rules
  test_app.py               # test 3 of 3 — AppTest smoke tests for every page
```

### Data schema

```jsonc
// data/robots.json
{ "name": "Boston Dynamics Spot", "category": "industry", "country": "United States",
  "year": 2015, "emoji": "🐕", "what_it_does": "…", "cool_fact": "…",
  "note": "…"            // only on defense entries: the balanced counterpoint
}

// data/concepts.json
{ "name": "SCUNTER", "class": "Recon & Search Scout", "emoji": "🦎", "tagline": "…",
  "ability": "…", "weakness": "…", "design_notes": "…",
  "specs": { "speed_kmh": 45, "runtime_h": 3.5, "payload_kg": 4, "autonomy_1_5": 4 } }

// data/future.json
{ "year": 2025, "emoji": "🏭", "tag": "Work", "title": "Robots clock in", "text": "…" }
```

---

## Test suite

| Module | Focus | Examples |
|--------|-------|----------|
| `tests/test_logic.py` | Pure logic, no Streamlit | reaction-distance maths, negative-input guards, whole-word tone matching, filter/sort immutability, validation rules, JSON path guard |
| `tests/test_data.py` | The shipped content | all 15 required robots present and unique, every category populated, no war framing anywhere in a fully walked JSON tree, defense entries carry balanced notes, no personal patterns, AST scan for network imports, concepts and timeline shape |
| `tests/test_app.py` | End-to-end smoke | all five pages render without exceptions, navigation lists five pages, search narrows the gallery to 1 of 15, category filter, empty-result message, sort options, latency slider changes the metrics, concept sketch preview, 2050 timeline |

```text
$ python -m pytest
40 passed
```

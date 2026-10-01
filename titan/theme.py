"""Titan Robotics visual theme: dark navy background with warm gold accents.

Everything is plain CSS injected with ``st.markdown`` so the app stays fully
offline (no web fonts, no CDNs, no images to download).
"""

from __future__ import annotations

import streamlit as st

BG = "#0a0e17"
SURFACE = "#141c2b"
SURFACE_DEEP = "#0f1522"
GOLD = "#d4af37"
GOLD_LIGHT = "#f0d97a"
TEXT = "#e9eef8"
MUTED = "#93a0b8"

CSS = """
<style>
:root{
  --tr-bg:#0a0e17;
  --tr-surface:#141c2b;
  --tr-surface-2:#0f1522;
  --tr-gold:#d4af37;
  --tr-gold-2:#f0d97a;
  --tr-gold-soft:rgba(212,175,55,.13);
  --tr-border:rgba(212,175,55,.20);
  --tr-text:#e9eef8;
  --tr-muted:#93a0b8;
  --tr-radius:16px;
}

/* ---------- page shell ---------- */
/* Paint the glow on the app root *and* the view container, so whichever one
   Streamlit's own theme colours, the gradient still shows through. */
.stApp, [data-testid="stAppViewContainer"]{
  background:
    radial-gradient(1100px 520px at 10% -10%, rgba(212,175,55,.14), transparent 62%),
    radial-gradient(900px 460px at 95% 2%, rgba(56,110,190,.16), transparent 60%),
    #0a0e17;
  background-attachment:fixed;
}
[data-testid="stAppViewContainer"] > .main,
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"]{background:transparent;}
[data-testid="stHeader"]{background:transparent;}
.block-container, [data-testid="stMainBlockContainer"]{padding:1rem 1rem 3.5rem;max-width:1180px;}
html, body, .stApp, [data-testid="stMarkdownContainer"], input, textarea, button{
  font-family:"Inter","Segoe UI",system-ui,-apple-system,"Helvetica Neue",Arial,sans-serif;
}
[data-testid="stMarkdownContainer"] p{color:#dbe3f0;}
h1,h2,h3,h4{color:#eef2fb;letter-spacing:-.01em;}
footer{visibility:hidden;height:0;}
a{color:var(--tr-gold);}
hr{border-color:rgba(212,175,55,.18);}

/* ---------- navigation pills ---------- */
[data-testid="stRadio"]{margin-bottom:.2rem;}
div[role="radiogroup"]{gap:.45rem;flex-wrap:wrap;}
div[role="radiogroup"] > label{
  background:rgba(255,255,255,.035);
  border:1px solid var(--tr-border);
  border-radius:999px;
  padding:.32rem .85rem;
  margin:0;
  transition:border-color .15s ease, background .15s ease, transform .15s ease;
}
div[role="radiogroup"] > label:hover{
  border-color:rgba(212,175,55,.62);
  background:rgba(212,175,55,.09);
  transform:translateY(-1px);
}
div[role="radiogroup"] > label:has(input:checked){
  background:var(--tr-gold-soft);
  border-color:var(--tr-gold);
  box-shadow:0 6px 18px rgba(212,175,55,.12);
}
div[role="radiogroup"] > label > div:first-child:empty{display:none;}
div[role="radiogroup"] label p{font-size:.88rem;font-weight:600;color:#e9eef8;white-space:nowrap;}

/* ---------- hero ---------- */
.tr-hero{
  position:relative;
  border:1px solid var(--tr-border);
  border-radius:22px;
  padding:1.5rem 1.15rem 1.4rem;
  background:
    radial-gradient(620px 240px at 18% 0%, rgba(212,175,55,.20), transparent 66%),
    linear-gradient(160deg,#121a29,#0b111c);
  overflow:hidden;
  margin:.2rem 0 1rem;
}
.tr-hero-eyebrow{
  font-size:.72rem;letter-spacing:.30em;text-transform:uppercase;color:var(--tr-gold);
  font-weight:600;
}
.tr-hero-title{
  font-size:clamp(2.05rem,7.5vw,3.4rem);
  line-height:1.03;font-weight:800;margin:.35rem 0 .35rem;
  background:linear-gradient(96deg,#ffffff 6%,var(--tr-gold-2) 52%,var(--tr-gold) 94%);
  -webkit-background-clip:text;background-clip:text;
  -webkit-text-fill-color:transparent;color:var(--tr-gold-2);
}
.tr-hero-sub{font-size:clamp(.95rem,2.6vw,1.1rem);color:#cbd5e8;max-width:62ch;line-height:1.65;margin:0;}
.tr-pills{display:flex;gap:.45rem;flex-wrap:wrap;margin-top:.95rem;}
.tr-pill{
  border:1px solid rgba(212,175,55,.35);background:rgba(212,175,55,.08);
  border-radius:999px;padding:.32rem .8rem;font-size:.84rem;color:var(--tr-gold-2);
}

/* ---------- grids & cards ---------- */
.tr-grid{
  display:grid;gap:.85rem;
  grid-template-columns:repeat(auto-fit,minmax(min(var(--tr-min,260px),100%),1fr));
  margin:.35rem 0 1rem;
}
.tr-card{
  position:relative;
  background:linear-gradient(165deg,var(--tr-surface),var(--tr-surface-2));
  border:1px solid var(--tr-border);
  border-radius:var(--tr-radius);
  padding:1rem 1.05rem 1.05rem .95rem;
  overflow:hidden;height:100%;
  transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease;
}
.tr-card:hover{
  transform:translateY(-3px);
  border-color:rgba(212,175,55,.55);
  box-shadow:0 16px 32px rgba(0,0,0,.45);
}
.tr-card::before{
  content:"";position:absolute;left:0;top:0;bottom:0;width:3px;
  background:linear-gradient(180deg,var(--tr-accent,var(--tr-gold)),transparent 88%);
}
.tr-row{display:flex;align-items:center;gap:.55rem;flex-wrap:wrap;}
.tr-icon{font-size:1.45rem;line-height:1;}
.tr-card-title{font-size:1.02rem;font-weight:700;color:#f5f8fd;line-height:1.28;}
.tr-card-title--big{font-size:1.22rem;font-weight:800;letter-spacing:.02em;}
.tr-card-sub{font-size:.75rem;color:var(--tr-muted);letter-spacing:.05em;text-transform:uppercase;margin:.3rem 0 .45rem;}
.tr-card-text{font-size:.9rem;line-height:1.58;color:#cfd8e8;margin:.35rem 0 0;}
.tr-tagline{font-size:.9rem;color:var(--tr-gold-2);font-style:italic;margin:.35rem 0 0;}
.tr-label{font-weight:700;color:#e9eef8;}
.tr-badge{
  display:inline-block;font-size:.66rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;
  padding:.2rem .55rem;border-radius:999px;border:1px solid rgba(255,255,255,.16);
  background:rgba(255,255,255,.05);color:#e8eefb;white-space:nowrap;
}
.tr-badge--gold{border-color:rgba(212,175,55,.5);background:var(--tr-gold-soft);color:var(--tr-gold-2);}
.tr-fact{
  margin-top:.65rem;padding:.55rem .7rem;border-radius:10px;
  background:rgba(212,175,55,.07);border-left:2px solid var(--tr-gold);
  font-size:.85rem;line-height:1.5;color:#e6ebf6;
}
.tr-note{
  margin-top:.55rem;padding-top:.5rem;border-top:1px dashed rgba(255,255,255,.14);
  font-size:.79rem;line-height:1.5;color:var(--tr-muted);
}
.tr-block{margin-top:.6rem;font-size:.88rem;line-height:1.55;color:#cfd8e8;}
.tr-muted{color:var(--tr-muted);font-size:.8rem;}

/* ---------- section headings ---------- */
.tr-section{margin:1.5rem 0 .35rem;}
.tr-section h3{margin:0;font-size:1.2rem;font-weight:750;color:#f2f5fb;}
.tr-section p{margin:.22rem 0 0;font-size:.9rem;color:var(--tr-muted);line-height:1.55;}
.tr-rule{height:1px;background:linear-gradient(90deg,rgba(212,175,55,.55),transparent);margin:.6rem 0 1rem;}

/* ---------- stats ---------- */
.tr-stats{
  display:grid;gap:.6rem;margin:.4rem 0 .9rem;
  grid-template-columns:repeat(auto-fit,minmax(min(140px,100%),1fr));
}
.tr-stat{
  border:1px solid var(--tr-border);border-radius:14px;padding:.7rem .8rem;
  background:linear-gradient(160deg,rgba(212,175,55,.12),rgba(255,255,255,.02));
}
.tr-stat-value{font-size:1.35rem;font-weight:800;color:#f7f9fe;line-height:1.15;}
.tr-stat-label{font-size:.72rem;color:var(--tr-muted);text-transform:uppercase;letter-spacing:.07em;margin-top:.15rem;}

/* ---------- flow / emoji diagrams ---------- */
.tr-flow{display:flex;align-items:center;gap:.45rem;flex-wrap:wrap;margin:.7rem 0 .3rem;}
.tr-flow-node{
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.2rem;
  min-width:86px;padding:.55rem .6rem;border-radius:12px;
  border:1px solid var(--tr-border);background:rgba(255,255,255,.03);
  font-size:.72rem;color:#c7d2e5;text-align:center;line-height:1.25;
}
.tr-flow-node b{font-size:1.3rem;line-height:1;}
.tr-flow-arrow{color:var(--tr-gold);font-size:1.05rem;}
.tr-flow-caption{margin-top:.45rem;font-size:.8rem;color:var(--tr-muted);}

/* ---------- timeline ---------- */
.tr-timeline{position:relative;padding-left:1.35rem;margin:.6rem 0 .8rem;}
.tr-timeline::before{
  content:"";position:absolute;left:.45rem;top:.6rem;bottom:.9rem;width:2px;
  background:linear-gradient(180deg,var(--tr-gold),rgba(212,175,55,.10));
}
.tr-tl-item{position:relative;margin-bottom:.7rem;}
.tr-tl-dot{
  position:absolute;left:-1.16rem;top:1.35rem;width:.62rem;height:.62rem;border-radius:50%;
  background:var(--tr-gold);box-shadow:0 0 0 4px rgba(212,175,55,.15);
}
.tr-tl-year{
  display:inline-block;font-size:.78rem;font-weight:800;letter-spacing:.06em;
  color:#0a0e17;background:linear-gradient(96deg,var(--tr-gold-2),var(--tr-gold));
  border-radius:999px;padding:.15rem .6rem;
}

/* ---------- meters (concept specs) ---------- */
.tr-meter{margin:.4rem 0;}
.tr-meter-head{display:flex;justify-content:space-between;gap:.6rem;font-size:.76rem;color:var(--tr-muted);margin-bottom:.22rem;}
.tr-meter-head b{color:#dfe6f3;font-weight:700;}
.tr-meter-track{height:.42rem;border-radius:999px;background:rgba(255,255,255,.07);overflow:hidden;}
.tr-meter-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,var(--tr-gold),var(--tr-gold-2));}

/* ---------- comparison table ---------- */
.tr-table-wrap{overflow-x:auto;border:1px solid var(--tr-border);border-radius:14px;margin:.4rem 0 1rem;}
table.tr-table{border-collapse:collapse;width:100%;min-width:640px;font-size:.86rem;}
table.tr-table th{
  text-align:left;padding:.6rem .7rem;background:rgba(212,175,55,.10);
  color:var(--tr-gold-2);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;
}
table.tr-table td{padding:.6rem .7rem;border-top:1px solid rgba(255,255,255,.07);color:#cfd8e8;vertical-align:top;}
table.tr-table tr:hover td{background:rgba(212,175,55,.05);}

/* ---------- streamlit widget polish ---------- */
[data-testid="stExpander"]{
  border:1px solid var(--tr-border);border-radius:14px;
  background:rgba(255,255,255,.02);overflow:hidden;
}
[data-testid="stExpander"] summary{font-weight:600;}
[data-testid="stExpander"] summary:hover{color:var(--tr-gold-2);}
[data-baseweb="select"] > div{background:rgba(255,255,255,.04);border-color:var(--tr-border);}
.stTextInput input, .stTextArea textarea, .stNumberInput input{
  background:rgba(255,255,255,.04);color:#eef2fb;
}
.stSlider [data-baseweb="slider"] [role="slider"]{box-shadow:0 0 0 4px rgba(212,175,55,.18);}
[data-testid="stMetricValue"]{color:var(--tr-gold-2);}
.stAlert{border-radius:12px;}
</style>
"""


def inject() -> None:
    """Apply the theme CSS to the current Streamlit page."""
    st.markdown(CSS, unsafe_allow_html=True)


def brand_bar() -> None:
    """Small brand strip shown above the navigation on every page."""
    st.markdown(
        """
<div class="tr-row" style="justify-content:space-between;margin:.1rem 0 .55rem">
  <div class="tr-row" style="gap:.5rem">
    <span class="tr-icon">🛰️</span>
    <span style="font-weight:800;letter-spacing:.16em;font-size:.82rem;color:#f0d97a">TITAN ROBOTICS</span>
  </div>
  <span class="tr-badge tr-badge--gold">Offline · No tracking</span>
</div>
""",
        unsafe_allow_html=True,
    )


def footer_note() -> None:
    """Closing line: keeps the offline promise visible to the reader."""
    st.markdown(
        """
<div class="tr-rule" style="margin-top:1.6rem"></div>
<p class="tr-muted" style="text-align:center;margin:0">
  🛰️ Titan Robotics · an offline learning app · Sense · Think · Act ·
  every fact is bundled in local JSON files, nothing is sent anywhere.
</p>
""",
        unsafe_allow_html=True,
    )

#!/usr/bin/env python3
"""CP-Sentry: Premium Dashboard"""

import streamlit as st
import json
from pathlib import Path
import pytz
from datetime import datetime

IST = pytz.timezone('Asia/Kolkata')

PLATFORM_META = {
    "leetcode":   {"label": "LeetCode",   "hex": "#f59e0b"},
    "codeforces": {"label": "Codeforces", "hex": "#60a5fa"},
    "codechef":   {"label": "CodeChef",   "hex": "#c084fc"},
    "atcoder":    {"label": "AtCoder",    "hex": "#34d399"},
}

# ── Styles ─────────────────────────────────────────────────────────────────────
STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Streamlit shell ─────────────────────────────────────────────────────── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #09090b !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
footer { display: none !important; }

.main .block-container {
    padding: 0 3.5rem 8rem !important;
    max-width: 1080px;
}

/* ── Glassmorphism sidebar ───────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: rgba(9, 9, 11, 0.85) !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    border-right: 1px solid #1c1c1f !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] p {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    color: #52525b !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] {
    background: #111113 !important;
    border: 1px solid #27272a !important;
    border-radius: 10px !important;
}

/* ── Header ──────────────────────────────────────────────────────────────── */
.hdr {
    padding: 3.5rem 0 2.25rem;
    border-bottom: 1px solid #18181b;
    margin-bottom: 2.75rem;
}
.greet {
    font-size: 2.65rem;
    font-weight: 700;
    color: #fafafa;
    letter-spacing: -0.055em;
    line-height: 1.1;
    margin-bottom: 0.55rem;
}
.tagline {
    font-size: 0.875rem;
    color: #52525b;
    font-weight: 400;
    letter-spacing: 0.01em;
}

/* ── Metrics bento grid ──────────────────────────────────────────────────── */
.metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2.75rem;
}
.mcard {
    background: #111113;
    border: 1px solid #1c1c1f;
    border-radius: 18px;
    padding: 1.875rem 1.625rem;
    transition: border-color 0.22s cubic-bezier(.4,0,.2,1),
                transform   0.22s cubic-bezier(.4,0,.2,1),
                box-shadow  0.22s cubic-bezier(.4,0,.2,1);
    cursor: default;
}
.mcard:hover {
    border-color: #2d2d32;
    transform: translateY(-3px);
    box-shadow:
        0 20px 56px -12px rgba(0,0,0,0.8),
        0 0 0 1px rgba(255,255,255,0.03);
}
.mval {
    font-size: 3rem;
    font-weight: 800;
    color: #fafafa;
    letter-spacing: -0.065em;
    line-height: 1;
    margin-bottom: 0.5rem;
}
.mlbl {
    font-size: 0.68rem;
    font-weight: 600;
    color: #3f3f46;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

/* ── Section label ───────────────────────────────────────────────────────── */
.sec-label {
    font-size: 0.68rem;
    font-weight: 600;
    color: #3f3f46;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 1.1rem;
    padding-top: 0.5rem;
}

/* ── Contest cards ───────────────────────────────────────────────────────── */
.cards { display: flex; flex-direction: column; gap: 0.75rem; }

.card {
    background: #111113;
    border: 1px solid #1c1c1f;
    border-radius: 18px;
    padding: 1.625rem 1.875rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.22s cubic-bezier(.4,0,.2,1),
                transform   0.22s cubic-bezier(.4,0,.2,1),
                box-shadow  0.22s cubic-bezier(.4,0,.2,1);
}
.card::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(99,102,241,0.05) 0%, transparent 55%);
    opacity: 0;
    transition: opacity 0.28s ease;
    pointer-events: none;
}
.card:hover {
    border-color: #2d2d32;
    transform: translateY(-3px);
    box-shadow:
        0 24px 64px -16px rgba(0,0,0,0.8),
        0 0 0 1px rgba(99,102,241,0.07);
}
.card:hover::after { opacity: 1; }

.card-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1.25rem;
    margin-bottom: 0.75rem;
}
.cname {
    font-size: 0.975rem;
    font-weight: 600;
    color: #f4f4f5;
    letter-spacing: -0.02em;
    line-height: 1.45;
}
.badge {
    font-size: 0.64rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0.3em 0.9em;
    border-radius: 100px;
    white-space: nowrap;
    flex-shrink: 0;
}
.cmeta {
    display: flex;
    align-items: center;
    gap: 0.625rem;
    margin-bottom: 1.375rem;
    font-size: 0.825rem;
    color: #71717a;
    font-weight: 400;
}
.sep { color: #2d2d32; user-select: none; }

.reg-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.78rem;
    font-weight: 600;
    color: #818cf8;
    text-decoration: none;
    padding: 0.48em 1.15em;
    border-radius: 9px;
    border: 1px solid rgba(99,102,241,0.22);
    background: rgba(99,102,241,0.07);
    transition: background  0.18s cubic-bezier(.4,0,.2,1),
                border-color 0.18s cubic-bezier(.4,0,.2,1),
                color        0.18s cubic-bezier(.4,0,.2,1),
                transform    0.18s cubic-bezier(.4,0,.2,1),
                box-shadow   0.18s cubic-bezier(.4,0,.2,1);
    letter-spacing: 0.02em;
}
.reg-btn:hover {
    background: rgba(99,102,241,0.16);
    border-color: rgba(99,102,241,0.44);
    color: #a5b4fc;
    transform: translateX(3px);
    box-shadow: 0 0 28px rgba(99,102,241,0.2);
}

/* ── Footer ──────────────────────────────────────────────────────────────── */
.ftr {
    text-align: center;
    font-size: 0.68rem;
    color: #27272a;
    font-weight: 500;
    letter-spacing: 0.1em;
    padding: 3.5rem 0 1rem;
    margin-top: 3.5rem;
    border-top: 1px solid #111113;
}
</style>
"""


# ── Data helpers ───────────────────────────────────────────────────────────────
def get_greeting():
    hour = datetime.now(IST).hour
    if hour < 12:
        return "Good Morning"
    elif hour < 17:
        return "Good Afternoon"
    return "Good Evening"


def load_contests():
    p = Path("data/contests.json")
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


def filter_upcoming(contests):
    now = datetime.now(IST)
    out = []
    for c in contests:
        try:
            t = datetime.fromisoformat(
                c["start_time_ist"].replace("Z", "+00:00")
            ).astimezone(IST)
            if t > now:
                out.append(c)
        except Exception:
            pass
    out.sort(key=lambda x: x.get("start_time_ist", ""))
    return out


def fmt_duration(sec):
    if not sec:
        return "N/A"
    h, m = sec // 3600, (sec % 3600) // 60
    return f"{h}h {m}m" if h else f"{m}m"


# ── HTML renderers ─────────────────────────────────────────────────────────────
def badge_styles(hex_color: str) -> str:
    """Convert hex to rgba-based badge inline styles (no color-mix needed)."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (
        f"color:{hex_color};"
        f"background:rgba({r},{g},{b},0.12);"
        f"border:1px solid rgba({r},{g},{b},0.28);"
    )


def render_header(greeting: str) -> str:
    return f"""
<div class="hdr">
  <div class="greet">👋 {greeting}, Shreyansh</div>
  <div class="tagline">Your competitive programming command center</div>
</div>"""


def render_metrics(upcoming: list) -> str:
    n_platforms = len(set(c["platform"] for c in upcoming))
    return f"""
<div class="metrics">
  <div class="mcard">
    <div class="mval">{len(upcoming)}</div>
    <div class="mlbl">Upcoming</div>
  </div>
  <div class="mcard">
    <div class="mval">{n_platforms}</div>
    <div class="mlbl">Platforms</div>
  </div>
  <div class="mcard">
    <div class="mval">7</div>
    <div class="mlbl">Day Window</div>
  </div>
</div>"""


def render_card(c: dict) -> str:
    meta = PLATFORM_META.get(
        c["platform"],
        {"label": c["platform"].title(), "hex": "#6366f1"},
    )
    return f"""
<div class="card">
  <div class="card-top">
    <span class="cname">{c['name']}</span>
    <span class="badge" style="{badge_styles(meta['hex'])}">{meta['label']}</span>
  </div>
  <div class="cmeta">
    <span>⏰ {c['start_time_display']}</span>
    <span class="sep">·</span>
    <span>⏱ {fmt_duration(c.get('duration_seconds'))}</span>
  </div>
  <a class="reg-btn" href="{c['url']}" target="_blank">Register →</a>
</div>"""


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="CP-Sentry",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.markdown(STYLE, unsafe_allow_html=True)

    greeting = get_greeting()
    data = load_contests()
    contests = data.get("contests", []) if data else []
    upcoming = filter_upcoming(contests)

    # Header
    st.markdown(render_header(greeting), unsafe_allow_html=True)

    if not upcoming:
        st.warning("No upcoming contests found. Run: python3 scraper.py")
        return

    platforms = sorted(set(c["platform"] for c in upcoming))

    # Metrics
    st.markdown(render_metrics(upcoming), unsafe_allow_html=True)

    # Sidebar platform filter
    with st.sidebar:
        st.markdown(
            '<p style="font-size:.68rem;font-weight:600;color:#3f3f46;'
            'text-transform:uppercase;letter-spacing:.12em;margin-bottom:.75rem;">'
            "Platforms</p>",
            unsafe_allow_html=True,
        )
        selected = st.multiselect(
            "", platforms, default=platforms, label_visibility="collapsed"
        )

    filtered = [c for c in upcoming if c["platform"] in (selected or platforms)]

    # Section label
    n = len(filtered)
    st.markdown(
        f'<div class="sec-label">Upcoming · {n} contest{"s" if n != 1 else ""}</div>',
        unsafe_allow_html=True,
    )

    # Contest cards
    st.markdown(
        '<div class="cards">' + "".join(render_card(c) for c in filtered) + "</div>",
        unsafe_allow_html=True,
    )

    # Footer
    st.markdown(
        '<div class="ftr">⚡ CP-Sentry · Track · Register · Compete</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

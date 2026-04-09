"""
TaxMind AI — Shared dark-mode theme injector.
Call inject_theme() at the top of every page (after st.set_page_config or auth guard).
"""

import streamlit as st

_CSS = """
<style>
/* ── Google Fonts ─────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@600;700;800&family=Inter:wght@300;400;500;600&display=swap');

/* ── Design tokens ───────────────────────────────── */
:root {
    --bg:          #0f1117;
    --bg-card:     #171c27;
    --bg-card2:    #1d2333;
    --border:      #252d3d;
    --border-hi:   #2e3a52;
    --green:       #00e676;
    --green-dim:   #00b85c;
    --green-glow:  rgba(0,230,118,0.15);
    --red:         #ff5252;
    --amber:       #ffab40;
    --text-hi:     #f0f4ff;
    --text-md:     #9aaac4;
    --text-lo:     #5a6a85;
    --font-head:   'Syne', sans-serif;
    --font-body:   'Inter', sans-serif;
    --font-mono:   'DM Mono', monospace;
    --radius:      10px;
    --radius-lg:   16px;
}

/* ── Base reset ──────────────────────────────────── */
.stApp {
    background: var(--bg) !important;
    color: var(--text-hi) !important;
    font-family: var(--font-body);
}

/* hide default streamlit header decoration */
header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer { visibility: hidden; }

/* ── Sidebar ─────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-hi) !important; }
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid var(--border-hi) !important;
    color: var(--text-md) !important;
    font-size: 13px !important;
    transition: all .2s;
}
[data-testid="stSidebar"] .stButton > button:hover {
    border-color: var(--green) !important;
    color: var(--green) !important;
}

/* ── Page headings ───────────────────────────────── */
h1, h2, h3 {
    font-family: var(--font-head) !important;
    color: var(--text-hi) !important;
    letter-spacing: -0.02em;
}
h1 { font-size: 2rem !important; font-weight: 800 !important; }
h2 { font-size: 1.35rem !important; font-weight: 700 !important; }
h3 { font-size: 1.1rem !important; font-weight: 600 !important; }

/* ── Horizontal rule ─────────────────────────────── */
hr { border-color: var(--border) !important; margin: 1.4rem 0 !important; }

/* ── Text / caption ──────────────────────────────── */
p, li { color: var(--text-md) !important; line-height: 1.7; }
.stMarkdown p { color: var(--text-md) !important; }
small, .stCaption, [data-testid="stCaptionContainer"] * {
    color: var(--text-lo) !important;
    font-size: 12px !important;
}

/* ── Metric cards ────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.1rem 1.4rem !important;
}
[data-testid="stMetricLabel"] { color: var(--text-lo) !important; font-size: 12px !important; }
[data-testid="stMetricValue"] {
    color: var(--green) !important;
    font-family: var(--font-mono) !important;
    font-size: 1.5rem !important;
}
[data-testid="stMetricDelta"] { font-size: 12px !important; }

/* ── Inputs ──────────────────────────────────────── */
.stTextInput input, .stNumberInput input,
.stSelectbox select, .stDateInput input,
textarea {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border-hi) !important;
    border-radius: var(--radius) !important;
    color: var(--text-hi) !important;
    font-family: var(--font-body) !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--green) !important;
    box-shadow: 0 0 0 2px var(--green-glow) !important;
}
label, .stSelectbox label, .stTextInput label,
.stNumberInput label, .stDateInput label {
    color: var(--text-md) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
}

/* ── Primary button ──────────────────────────────── */
.stButton > button[kind="primary"],
.stButton > button {
    background: var(--green) !important;
    color: #0f1117 !important;
    font-family: var(--font-head) !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: .55rem 1.4rem !important;
    letter-spacing: .04em !important;
    transition: all .2s ease !important;
    box-shadow: 0 4px 20px var(--green-glow);
}
.stButton > button:hover {
    background: var(--green-dim) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px var(--green-glow) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Download button ─────────────────────────────── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid var(--green) !important;
    color: var(--green) !important;
    font-family: var(--font-head) !important;
    font-weight: 600 !important;
    border-radius: var(--radius) !important;
    transition: all .2s !important;
}
.stDownloadButton > button:hover {
    background: var(--green-glow) !important;
}

/* ── Tables ──────────────────────────────────────── */
[data-testid="stTable"] table {
    width: 100% !important;
    border-collapse: collapse !important;
    font-size: 13px !important;
}
[data-testid="stTable"] th {
    background: var(--bg-card2) !important;
    color: var(--green) !important;
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
    padding: 10px 14px !important;
    border-bottom: 1px solid var(--border-hi) !important;
}
[data-testid="stTable"] td {
    padding: 9px 14px !important;
    border-bottom: 1px solid var(--border) !important;
    color: var(--text-md) !important;
}
[data-testid="stTable"] tr:hover td { background: var(--bg-card2) !important; }

/* ── Dataframe ───────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
}

/* ── Tabs ────────────────────────────────────────── */
[data-testid="stTabs"] [role="tab"] {
    color: var(--text-lo) !important;
    font-family: var(--font-body) !important;
    font-weight: 500;
    font-size: 13px;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: var(--green) !important;
    border-bottom-color: var(--green) !important;
}

/* ── Info / warning / success / error boxes ───────── */
[data-testid="stAlert"] {
    border-radius: var(--radius) !important;
    border-left-width: 3px !important;
}

/* ── Chat messages ───────────────────────────────── */
[data-testid="stChatMessage"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    margin-bottom: .6rem !important;
}
.stChatInput textarea {
    background: var(--bg-card2) !important;
    border-color: var(--border-hi) !important;
    color: var(--text-hi) !important;
}
.stChatInput textarea:focus { border-color: var(--green) !important; }

/* ── File uploader ───────────────────────────────── */
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1px dashed var(--border-hi) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1rem !important;
}

/* ── Code blocks ─────────────────────────────────── */
code, pre {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--green) !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
}
</style>
"""

# ── Reusable card HTML ────────────────────────────────────────────────────────
def card(content_html: str, accent: str = "var(--green)") -> str:
    """Return an HTML card string for use with st.markdown(..., unsafe_allow_html=True)."""
    return f"""
    <div style="
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-left: 3px solid {accent};
        border-radius: var(--radius-lg);
        padding: 1.2rem 1.5rem;
        margin-bottom: .8rem;
    ">{content_html}</div>
    """


def stat_card(label: str, value: str, sub: str = "", accent: str = "var(--green)") -> str:
    return f"""
    <div style="
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.3rem 1.5rem;
        text-align: center;
    ">
        <div style="color:var(--text-lo);font-size:11px;letter-spacing:.08em;
                    text-transform:uppercase;font-weight:600;margin-bottom:.4rem;">
            {label}
        </div>
        <div style="color:{accent};font-size:1.6rem;font-weight:700;
                    font-family:'DM Mono',monospace;line-height:1.1;">
            {value}
        </div>
        <div style="color:var(--text-lo);font-size:11px;margin-top:.35rem;">{sub}</div>
    </div>
    """


def section_header(title: str, subtitle: str = "") -> str:
    sub_html = f'<p style="color:var(--text-lo);font-size:13px;margin:0;">{subtitle}</p>' if subtitle else ""
    return f"""
    <div style="margin: 1.8rem 0 1rem 0;">
        <h2 style="margin:0;font-family:\'Syne\',sans-serif;font-size:1.25rem;
                   color:var(--text-hi);font-weight:700;">{title}</h2>
        {sub_html}
    </div>
    """


def page_title(icon: str, title: str, subtitle: str = "") -> str:
    sub_html = f'<p style="color:var(--text-lo);font-size:13px;margin:0.3rem 0 0 0;">{subtitle}</p>' if subtitle else ""
    return f"""
    <div style="margin-bottom:1.5rem;">
        <div style="display:flex;align-items:center;gap:.7rem;margin-bottom:.2rem;">
            <span style="font-size:1.5rem;">{icon}</span>
            <h1 style="margin:0;font-family:\'Syne\',sans-serif;font-size:1.9rem;
                       font-weight:800;color:var(--text-hi);letter-spacing:-.03em;">
                {title}
            </h1>
        </div>
        {sub_html}
    </div>
    <hr style="border-color:var(--border);margin:0 0 1.5rem 0;">
    """


def inject_theme():
    st.markdown(_CSS, unsafe_allow_html=True)

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
    --bg:          #0b0f1a;
    --bg-card:     #111827;
    --bg-card2:    #161d2e;
    --bg-card3:    #1a2236;
    --border:      #1e2a3d;
    --border-hi:   #273347;
    --green:       #00e676;
    --green-dim:   #00c060;
    --green-glow:  rgba(0,230,118,0.12);
    --green-glow2: rgba(0,230,118,0.06);
    --red:         #ff5252;
    --red-glow:    rgba(255,82,82,0.10);
    --amber:       #ffab40;
    --amber-glow:  rgba(255,171,64,0.10);
    --blue:        #40c4ff;
    --text-hi:     #edf2ff;
    --text-md:     #8899b8;
    --text-lo:     #4a5a72;
    --font-head:   'Syne', sans-serif;
    --font-body:   'Inter', sans-serif;
    --font-mono:   'DM Mono', monospace;
    --radius:      10px;
    --radius-lg:   16px;
    --radius-xl:   20px;
    --transition:  all 0.2s cubic-bezier(0.4,0,0.2,1);
}

/* ── Base reset ──────────────────────────────────── */
.stApp {
    background: var(--bg) !important;
    color: var(--text-hi) !important;
    font-family: var(--font-body);
}

header[data-testid="stHeader"] { background: transparent !important; box-shadow: none !important; }
#MainMenu, footer { visibility: hidden; }

/* ── HIDE NATIVE STREAMLIT PAGE NAV ──────────────── */
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavSeparator"],
[data-testid="stSidebarNav"],
section[data-testid="stSidebar"] nav,
[data-testid="stSidebarNav"] {
    display: none !important;
}

/* ── Sidebar shell ───────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-hi) !important;
}

/* ── Custom nav link buttons ─────────────────────── */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: var(--text-md) !important;
    font-family: var(--font-body) !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 0.5rem 0.9rem !important;
    border-radius: var(--radius) !important;
    width: 100% !important;
    transition: var(--transition) !important;
    letter-spacing: 0.01em !important;
    margin: 1px 0 !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--bg-card2) !important;
    color: var(--text-hi) !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ── Sidebar selectbox ───────────────────────────── */
[data-testid="stSidebar"] .stSelectbox label {
    color: var(--text-lo) !important;
    font-size: 11px !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
    background: var(--bg-card2) !important;
    border-color: var(--border-hi) !important;
    font-size: 13px !important;
}

/* ── Page headings ───────────────────────────────── */
h1, h2, h3 {
    font-family: var(--font-head) !important;
    color: var(--text-hi) !important;
    letter-spacing: -0.025em;
}
h1 { font-size: 1.9rem !important; font-weight: 800 !important; }
h2 { font-size: 1.3rem !important; font-weight: 700 !important; }
h3 { font-size: 1.05rem !important; font-weight: 600 !important; }

hr { border-color: var(--border) !important; margin: 1.4rem 0 !important; }

p, li { color: var(--text-md) !important; line-height: 1.75; }
.stMarkdown p { color: var(--text-md) !important; }
small, .stCaption, [data-testid="stCaptionContainer"] * {
    color: var(--text-lo) !important;
    font-size: 11.5px !important;
}

/* ── Metric cards ────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.1rem 1.4rem !important;
}
[data-testid="stMetricLabel"] { color: var(--text-lo) !important; font-size: 11.5px !important; }
[data-testid="stMetricValue"] {
    color: var(--green) !important;
    font-family: var(--font-mono) !important;
    font-size: 1.45rem !important;
}

/* ── Inputs ──────────────────────────────────────── */
.stTextInput input, .stNumberInput input,
.stSelectbox select, .stDateInput input, textarea {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border-hi) !important;
    border-radius: var(--radius) !important;
    color: var(--text-hi) !important;
    font-family: var(--font-body) !important;
    transition: var(--transition) !important;
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

/* ── Primary button (main area) ──────────────────── */
.main .stButton > button,
[data-testid="stMainBlockContainer"] .stButton > button {
    background: var(--green) !important;
    color: #080d15 !important;
    font-family: var(--font-head) !important;
    font-weight: 700 !important;
    font-size: 13.5px !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 0.55rem 1.4rem !important;
    letter-spacing: 0.04em !important;
    transition: var(--transition) !important;
    box-shadow: 0 2px 16px var(--green-glow) !important;
}
.main .stButton > button:hover,
[data-testid="stMainBlockContainer"] .stButton > button:hover {
    background: var(--green-dim) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px var(--green-glow) !important;
}
.main .stButton > button:active,
[data-testid="stMainBlockContainer"] .stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Download button ─────────────────────────────── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid var(--green) !important;
    color: var(--green) !important;
    font-family: var(--font-head) !important;
    font-weight: 600 !important;
    border-radius: var(--radius) !important;
    transition: var(--transition) !important;
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
    font-size: 10.5px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 10px 16px !important;
    border-bottom: 1px solid var(--border-hi) !important;
}
[data-testid="stTable"] td {
    padding: 9px 16px !important;
    border-bottom: 1px solid var(--border) !important;
    color: var(--text-md) !important;
}
[data-testid="stTable"] tr:hover td { background: var(--bg-card2) !important; }

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

[data-testid="stAlert"] {
    border-radius: var(--radius) !important;
    border-left-width: 3px !important;
    background: var(--bg-card) !important;
}

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

[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1px dashed var(--border-hi) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--green) !important;
}

code, pre {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--green) !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
}

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-lo); }
</style>
"""


def card(content_html: str, accent: str = "var(--green)") -> str:
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
    glow_map = {
        "var(--green)":   "rgba(0,230,118,0.07)",
        "var(--red)":     "rgba(255,82,82,0.07)",
        "var(--amber)":   "rgba(255,171,64,0.07)",
        "var(--text-md)": "rgba(136,153,184,0.04)",
        "var(--blue)":    "rgba(64,196,255,0.07)",
    }
    glow = glow_map.get(accent, "rgba(0,230,118,0.07)")
    return f"""
    <div style="
        background: linear-gradient(145deg, var(--bg-card) 0%, {glow} 100%);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.3rem 1.5rem;
        text-align: center;
        overflow: hidden;
    ">
        <div style="color:var(--text-lo);font-size:10.5px;letter-spacing:.1em;
                    text-transform:uppercase;font-weight:600;margin-bottom:.5rem;
                    font-family:'DM Mono',monospace;">
            {label}
        </div>
        <div style="color:{accent};font-size:1.5rem;font-weight:700;
                    font-family:'DM Mono',monospace;line-height:1.1;letter-spacing:-.02em;">
            {value}
        </div>
        <div style="color:var(--text-lo);font-size:11px;margin-top:.4rem;">{sub}</div>
    </div>
    """


def section_header(title: str, subtitle: str = "") -> str:
    sub_html = f'<p style="color:var(--text-lo);font-size:12.5px;margin:.2rem 0 0 0;">{subtitle}</p>' if subtitle else ""
    return f"""
    <div style="margin: 1.8rem 0 1rem 0;">
        <h2 style="margin:0;font-family:'Syne',sans-serif;font-size:1.15rem;
                   color:var(--text-hi);font-weight:700;letter-spacing:-.02em;">{title}</h2>
        {sub_html}
    </div>
    """


def page_title(icon: str, title: str, subtitle: str = "") -> str:
    sub_html = f'<p style="color:var(--text-lo);font-size:12.5px;margin:.35rem 0 0 0;">{subtitle}</p>' if subtitle else ""
    return f"""
    <div style="margin-bottom:1.5rem;">
        <div style="display:flex;align-items:center;gap:.65rem;margin-bottom:.15rem;">
            <span style="font-size:1.4rem;line-height:1;">{icon}</span>
            <h1 style="margin:0;font-family:'Syne',sans-serif;font-size:1.8rem;
                       font-weight:800;color:var(--text-hi);letter-spacing:-.035em;">
                {title}
            </h1>
        </div>
        {sub_html}
    </div>
    <hr style="border-color:var(--border);margin:0 0 1.5rem 0;">
    """


def inject_theme():
    st.markdown(_CSS, unsafe_allow_html=True)

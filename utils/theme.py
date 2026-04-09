"""
TaxMind AI — Shared dark-mode theme injector.
Navy palette. No emojis. Production-ready.
FIXED v2: BaseWeb input selectors, button text, sidebar wildcard bleed.
"""
import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@600;700;800&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --bg:          #080d18;
    --bg-card:     #0d1526;
    --bg-card2:    #111d33;
    --bg-card3:    #152240;
    --border:      #1c2d4a;
    --border-hi:   #2a4068;
    --navy:        #4f8ef7;
    --navy-dim:    #3a75e0;
    --navy-bright: #7aabff;
    --navy-glow:   rgba(79,142,247,0.14);
    --navy-glow2:  rgba(79,142,247,0.06);
    --red:         #f05a5a;
    --red-glow:    rgba(240,90,90,0.10);
    --amber:       #f0a840;
    --amber-glow:  rgba(240,168,64,0.10);
    --teal:        #2dd4bf;
    --text-hi:     #e8eeff;
    --text-md:     #7a90b8;
    --text-lo:     #3d5070;
    --font-head:   'Syne', sans-serif;
    --font-body:   'Inter', sans-serif;
    --font-mono:   'DM Mono', monospace;
    --radius:      10px;
    --radius-lg:   16px;
    --transition:  all 0.18s cubic-bezier(0.4,0,0.2,1);
}

/* ── Base ── */
.stApp {
    background: var(--bg) !important;
    color: var(--text-hi) !important;
    font-family: var(--font-body);
}
header[data-testid="stHeader"] {
    background: transparent !important;
    box-shadow: none !important;
}
#MainMenu, footer { visibility: hidden; }

/* ── NUKE NATIVE STREAMLIT NAV ── */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavSeparator"],
[data-testid="stSidebarNavLink"],
section[data-testid="stSidebar"] > div > div > div > ul,
section[data-testid="stSidebar"] nav,
.st-emotion-cache-79elbk,
.st-emotion-cache-1rtdyuf,
.st-emotion-cache-6tkfeg,
div[class*="sidebarNav"] {
    display: none !important;
    height: 0 !important;
    overflow: hidden !important;
    visibility: hidden !important;
}

/* ── Sidebar shell — NO wildcard * color ── */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
    min-width: 210px !important;
    max-width: 240px !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: var(--text-hi);
}

/* ── Sidebar nav buttons ── */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: var(--text-md) !important;
    font-family: var(--font-body) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 0.45rem 0.85rem !important;
    border-radius: 7px !important;
    width: 100% !important;
    transition: var(--transition) !important;
    margin: 1px 0 !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--bg-card2) !important;
    color: var(--text-hi) !important;
}
[data-testid="stSidebar"] .stButton > button p {
    color: inherit !important;
    font-weight: inherit !important;
}

/* ── Sidebar selectbox ── */
[data-testid="stSidebar"] .stSelectbox label {
    color: var(--text-lo) !important;
    font-size: 10px !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: var(--bg-card2) !important;
    border-color: var(--border-hi) !important;
    font-size: 12.5px !important;
    color: var(--text-hi) !important;
}

/* ── Headings ── */
h1, h2, h3 {
    font-family: var(--font-head) !important;
    color: var(--text-hi) !important;
    letter-spacing: -0.025em;
}
h1 { font-size: 1.85rem !important; font-weight: 800 !important; }
h2 { font-size: 1.25rem !important; font-weight: 700 !important; }
h3 { font-size: 1.05rem !important; font-weight: 600 !important; }
hr { border-color: var(--border) !important; margin: 1.4rem 0 !important; }

/* ── Text ── */
p, li { color: var(--text-md) !important; line-height: 1.75; }
.stMarkdown p { color: var(--text-md) !important; }
small, .stCaption, [data-testid="stCaptionContainer"] * {
    color: var(--text-lo) !important;
    font-size: 11.5px !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.1rem 1.4rem !important;
}
[data-testid="stMetricLabel"] { color: var(--text-lo) !important; font-size: 11.5px !important; }
[data-testid="stMetricValue"] {
    color: var(--navy) !important;
    font-family: var(--font-mono) !important;
    font-size: 1.45rem !important;
}

/* ════════════════════════════════════════════════════════
   INPUT FIELDS
   Streamlit 1.44+ uses BaseWeb components.
   DOM structure:
     .stTextInput
       > div                          (label wrapper)
       > div[data-baseweb="input"]    (visible bordered box)
         > div                        (inner flex row)
           > input                    (the actual input)
   ════════════════════════════════════════════════════════ */

/* Outer bordered container */
div[data-baseweb="input"] {
    background-color: #111d33 !important;
    border: 1.5px solid #2a4068 !important;
    border-radius: 10px !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: #4f8ef7 !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.18) !important;
}

/* Actual <input> inside BaseWeb */
div[data-baseweb="input"] input {
    background-color: transparent !important;
    color: #e8eeff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    caret-color: #4f8ef7 !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}
div[data-baseweb="input"] input::placeholder {
    color: #3d5070 !important;
    opacity: 1 !important;
}

/* Password eye icon button inside input */
div[data-baseweb="input"] button {
    background: transparent !important;
    border: none !important;
    color: #3d5070 !important;
}
div[data-baseweb="input"] button:hover {
    color: #7a90b8 !important;
}

/* Textarea (st.text_area) */
div[data-baseweb="textarea"] {
    background-color: #111d33 !important;
    border: 1.5px solid #2a4068 !important;
    border-radius: 10px !important;
}
div[data-baseweb="textarea"]:focus-within {
    border-color: #4f8ef7 !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.18) !important;
}
div[data-baseweb="textarea"] textarea {
    background-color: transparent !important;
    color: #e8eeff !important;
    font-family: 'Inter', sans-serif !important;
    caret-color: #4f8ef7 !important;
    border: none !important;
    outline: none !important;
}
div[data-baseweb="textarea"] textarea::placeholder {
    color: #3d5070 !important;
    opacity: 1 !important;
}

/* Selectbox (st.selectbox, st.multiselect) */
div[data-baseweb="select"] > div {
    background-color: #111d33 !important;
    border: 1.5px solid #2a4068 !important;
    border-radius: 10px !important;
    color: #e8eeff !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: #4f8ef7 !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.18) !important;
}
div[data-baseweb="select"] span {
    color: #e8eeff !important;
}
div[data-baseweb="select"] svg {
    fill: #3d5070 !important;
}

/* Dropdown popover/menu */
div[data-baseweb="popover"] {
    background-color: #111d33 !important;
    border: 1px solid #2a4068 !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5) !important;
}
div[data-baseweb="menu"] {
    background-color: #111d33 !important;
    border-radius: 10px !important;
}
li[data-baseweb="menu-item"],
[role="option"] {
    background-color: #111d33 !important;
    color: #e8eeff !important;
}
li[data-baseweb="menu-item"]:hover,
[role="option"]:hover {
    background-color: #1c3050 !important;
}

/* Input labels */
.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stDateInput label,
.stTextArea label {
    color: #7a90b8 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    margin-bottom: 4px !important;
    display: block !important;
}

/* ════════════════════════════════════════════════════════
   BUTTONS — main content area only
   ════════════════════════════════════════════════════════ */
.main .stButton > button,
[data-testid="stMainBlockContainer"] .stButton > button {
    background: #4f8ef7 !important;
    color: #ffffff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13.5px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.4rem !important;
    letter-spacing: 0.03em !important;
    transition: all 0.18s cubic-bezier(0.4,0,0.2,1) !important;
    box-shadow: 0 2px 14px rgba(79,142,247,0.14) !important;
}
.main .stButton > button:hover,
[data-testid="stMainBlockContainer"] .stButton > button:hover {
    background: #3a75e0 !important;
    color: #ffffff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(79,142,247,0.25) !important;
}
.main .stButton > button:active,
[data-testid="stMainBlockContainer"] .stButton > button:active {
    transform: translateY(0) !important;
}
/* Streamlit wraps button label in <p> — must override */
.main .stButton > button p,
[data-testid="stMainBlockContainer"] .stButton > button p {
    color: #ffffff !important;
    font-weight: 700 !important;
    margin: 0 !important;
    line-height: 1.4 !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid var(--navy) !important;
    color: var(--navy) !important;
    font-family: var(--font-head) !important;
    font-weight: 600 !important;
    border-radius: var(--radius) !important;
    transition: var(--transition) !important;
}
.stDownloadButton > button p { color: var(--navy) !important; }
.stDownloadButton > button:hover { background: var(--navy-glow) !important; }

/* ── Tabs ── */
[data-testid="stTabs"] [role="tab"] {
    color: var(--text-lo) !important;
    font-family: var(--font-body) !important;
    font-weight: 500;
    font-size: 13px;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: var(--navy) !important;
    border-bottom-color: var(--navy) !important;
}
[data-testid="stTabs"] [role="tab"] p { color: inherit !important; }

/* ── Tables ── */
[data-testid="stTable"] table {
    width: 100% !important;
    border-collapse: collapse !important;
    font-size: 13px !important;
}
[data-testid="stTable"] th {
    background: var(--bg-card2) !important;
    color: var(--navy-bright) !important;
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

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: var(--radius) !important;
    border-left-width: 3px !important;
    background: var(--bg-card) !important;
}

/* ── Chat ── */
[data-testid="stChatMessage"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    margin-bottom: .6rem !important;
}
.stChatInput div[data-baseweb="textarea"] {
    background: var(--bg-card2) !important;
    border-color: var(--border-hi) !important;
}
.stChatInput div[data-baseweb="textarea"]:focus-within {
    border-color: var(--navy) !important;
}
.stChatInput div[data-baseweb="textarea"] textarea {
    color: var(--text-hi) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1px dashed var(--border-hi) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1rem !important;
}

/* ── Code ── */
code, pre {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--navy-bright) !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: 4px; }
</style>
"""


def card(content_html: str, accent: str = "var(--navy)") -> str:
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


def stat_card(label: str, value: str, sub: str = "", accent: str = "var(--navy)") -> str:
    glow_map = {
        "var(--navy)":    "rgba(79,142,247,0.07)",
        "var(--red)":     "rgba(240,90,90,0.07)",
        "var(--amber)":   "rgba(240,168,64,0.07)",
        "var(--teal)":    "rgba(45,212,191,0.07)",
        "var(--text-md)": "rgba(122,144,184,0.04)",
    }
    glow = glow_map.get(accent, "rgba(79,142,247,0.07)")
    return f"""
    <div style="
        background: linear-gradient(145deg, var(--bg-card) 0%, {glow} 100%);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.3rem 1.5rem;
        text-align: center;
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
    sub_html = (
        f'<p style="color:var(--text-lo);font-size:12.5px;margin:.2rem 0 0 0;">{subtitle}</p>'
        if subtitle else ""
    )
    return f"""
    <div style="margin: 1.8rem 0 1rem 0;">
        <h2 style="margin:0;font-family:'Syne',sans-serif;font-size:1.15rem;
                   color:var(--text-hi);font-weight:700;letter-spacing:-.02em;">{title}</h2>
        {sub_html}
    </div>
    """


def page_title(icon: str, title: str, subtitle: str = "") -> str:
    sub_html = (
        f'<p style="color:var(--text-lo);font-size:12.5px;margin:.35rem 0 0 0;">{subtitle}</p>'
        if subtitle else ""
    )
    return f"""
    <div style="margin-bottom:1.5rem;">
        <div style="display:flex;align-items:center;gap:.65rem;margin-bottom:.15rem;">
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

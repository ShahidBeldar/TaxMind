import streamlit as st
from utils.db import init_db, create_user, authenticate_user, update_user_profile
from utils.i18n import t
from utils.theme import inject_theme, page_title, card

st.set_page_config(
    page_title="TaxMind AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="auto",
)

init_db()


def _init_session():
    defaults = {
        "logged_in":        False,
        "user_id":          None,
        "username":         "",
        "name":             "",
        "employment_type":  "",
        "income_bracket":   "",
        "preferred_regime": "new",
        "language":         "en",
        "setup_complete":   0,
        "chat_history":     [],
        "auth_mode":        "login",
        "auth_error":       "",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


_init_session()


def _load_session_from_row(row):
    st.session_state.logged_in        = True
    st.session_state.user_id          = row["id"]
    st.session_state.username         = row["username"]
    st.session_state.name             = row["name"] or ""
    st.session_state.employment_type  = row["employment_type"] or ""
    st.session_state.income_bracket   = row["income_bracket"] or ""
    st.session_state.preferred_regime = row["preferred_regime"] or "new"
    st.session_state.language         = row["language"] or "en"
    st.session_state.setup_complete   = row["setup_complete"] or 0


# ── Auth page ─────────────────────────────────────────────────────────────────
def render_auth():
    inject_theme()

    # Nuclear-specificity CSS to force inputs visible in ALL Streamlit versions
    st.markdown("""
    <style>
    /* Input wrapper */
    .stTextInput > div > div {
        background-color: #162035 !important;
        border: 1.5px solid #2e4a7a !important;
        border-radius: 8px !important;
    }
    /* The actual <input> element */
    .stTextInput > div > div > input {
        background-color: #162035 !important;
        color: #e8eeff !important;
        -webkit-text-fill-color: #e8eeff !important;
        caret-color: #4f8ef7 !important;
        font-size: 14px !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        padding: 10px 14px !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #3d5a80 !important;
        -webkit-text-fill-color: #3d5a80 !important;
        opacity: 1 !important;
    }
    .stTextInput > div > div:focus-within {
        border-color: #4f8ef7 !important;
        box-shadow: 0 0 0 3px rgba(79,142,247,0.15) !important;
    }
    /* Input labels */
    .stTextInput label {
        color: #7a90b8 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }
    /* ALL buttons — white text */
    .stButton > button {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    /* Mode toggle buttons (inside columns) — ghost style */
    div[data-testid="column"] .stButton > button {
        background: transparent !important;
        border: 1.5px solid #243858 !important;
        color: #7a90b8 !important;
        -webkit-text-fill-color: #7a90b8 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
        transform: none !important;
    }
    div[data-testid="column"] .stButton > button:hover {
        border-color: #4f8ef7 !important;
        color: #e8eeff !important;
        -webkit-text-fill-color: #e8eeff !important;
        background: rgba(79,142,247,0.08) !important;
        transform: none !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.6, 1])
    with col:
        # ── Brand ─────────────────────────────────────────────────────────
        st.markdown("""
        <div style="text-align:center;padding:2.5rem 0 1.2rem 0;">
            <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;
                        color:#e8eeff;letter-spacing:-.04em;">TaxMind AI</div>
            <p style="color:#3d5070;font-size:12px;margin:.5rem 0 0 0;letter-spacing:.07em;
                      text-transform:uppercase;font-family:'DM Mono',monospace;">
                Indian Tax Planning · FY 2026
            </p>
        </div>
        <hr style="border-color:#1c2d4a;margin:0 0 1.2rem 0;">
        """, unsafe_allow_html=True)

        # ── Mode toggle ────────────────────────────────────────────────────
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Sign In", key="mode_login", use_container_width=True):
                st.session_state.auth_mode  = "login"
                st.session_state.auth_error = ""
                st.rerun()
        with c2:
            if st.button("Create Account", key="mode_signup", use_container_width=True):
                st.session_state.auth_mode  = "signup"
                st.session_state.auth_error = ""
                st.rerun()

        # Active tab underline
        mode = st.session_state.auth_mode
        st.markdown(f"""
        <div style="display:flex;margin-top:-8px;margin-bottom:20px;">
            <div style="height:2px;width:{'50%' if mode=='login' else '0%'};
                        background:#4f8ef7;border-radius:2px;"></div>
            <div style="height:2px;width:{'50%' if mode=='signup' else '0%'};
                        background:#4f8ef7;border-radius:2px;margin-left:auto;"></div>
        </div>
        """, unsafe_allow_html=True)

        # Error message
        if st.session_state.auth_error:
            st.error(st.session_state.auth_error)

        # ── LOGIN form ─────────────────────────────────────────────────────
        if mode == "login":
            username = st.text_input("Username", placeholder="your_username", key="li_user")
            password = st.text_input("Password", type="password", placeholder="password", key="li_pass")
            st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

            if st.button("Sign In →", key="btn_login", use_container_width=True):
                if not username or not password:
                    st.session_state.auth_error = "Please enter your username and password."
                    st.rerun()
                else:
                    row = authenticate_user(username, password)
                    if row:
                        st.session_state.auth_error = ""
                        _load_session_from_row(row)
                        st.rerun()
                    else:
                        st.session_state.auth_error = t("invalid_credentials")
                        st.rerun()

        # ── SIGNUP form ────────────────────────────────────────────────────
        else:
            new_username = st.text_input("Username", placeholder="choose a username", key="su_user")
            new_password = st.text_input("Password", type="password", placeholder="min 6 characters", key="su_pass")
            confirm_pw   = st.text_input("Confirm Password", type="password", placeholder="repeat password", key="su_conf")
            st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

            if st.button("Create Account →", key="btn_signup", use_container_width=True):
                if not new_username or not new_password:
                    st.session_state.auth_error = "Username and password are required."
                    st.rerun()
                elif new_password != confirm_pw:
                    st.session_state.auth_error = "Passwords do not match."
                    st.rerun()
                elif len(new_password) < 6:
                    st.session_state.auth_error = "Password must be at least 6 characters."
                    st.rerun()
                else:
                    success = create_user(new_username, new_password)
                    if success:
                        row = authenticate_user(new_username, new_password)
                        if row:
                            st.session_state.auth_error = ""
                            _load_session_from_row(row)
                            st.rerun()
                    else:
                        st.session_state.auth_error = t("username_taken")
                        st.rerun()

        st.markdown("""
        <p style="text-align:center;color:#3d5070;font-size:11px;margin-top:1.5rem;
                  font-family:'DM Mono',monospace;">
            Data stored locally · FY 2026 · AI-powered tax advice
        </p>
        """, unsafe_allow_html=True)


# ── Profile wizard ─────────────────────────────────────────────────────────────
def render_wizard():
    inject_theme()
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div style="padding:1.5rem 0 .5rem 0;">
            <h1 style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;
                       color:#e8eeff;margin:0;">Set Up Your Profile</h1>
            <p style="color:#3d5070;font-size:13px;margin:.4rem 0 0 0;">
                This helps personalise your tax advice and dashboard.
            </p>
        </div>
        <hr style="border-color:#1c2d4a;">
        """, unsafe_allow_html=True)

        name             = st.text_input(t("full_name"), value=st.session_state.name, placeholder="e.g. Arjun Mehta")
        employment_type  = st.selectbox(t("employment_type"), options=["Salaried", "Self-Employed", "Business"])
        income_bracket   = st.selectbox(t("income_bracket"),
            options=["Below 5L", "5L - 10L", "10L - 15L", "15L - 25L", "25L - 50L", "Above 50L"])
        preferred_regime = st.selectbox(t("preferred_regime"), options=["new", "old"],
            format_func=lambda x: "New Regime (FY 2026 default)" if x == "new" else "Old Regime")
        language         = st.selectbox(t("language_label"), options=["en", "hi"],
            format_func=lambda x: "English" if x == "en" else "Hindi")

        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
        if st.button(t("wizard_save"), use_container_width=True):
            if not name.strip():
                st.error("Please enter your name.")
            else:
                update_user_profile(
                    st.session_state.user_id, name.strip(),
                    employment_type, income_bracket, preferred_regime, language,
                )
                st.session_state.name             = name.strip()
                st.session_state.employment_type  = employment_type
                st.session_state.income_bracket   = income_bracket
                st.session_state.preferred_regime = preferred_regime
                st.session_state.language         = language
                st.session_state.setup_complete   = 1
                st.success(t("wizard_saved"))
                st.rerun()


# ── Home page ──────────────────────────────────────────────────────────────────
def render_home():
    inject_theme()

    from utils.sidebar import render_sidebar
    render_sidebar()

    st.markdown(page_title("", "TaxMind AI", "Indian Tax Planning for FY 2026"),
                unsafe_allow_html=True)

    name   = st.session_state.name or st.session_state.username
    emp    = st.session_state.employment_type or "—"
    bkt    = st.session_state.income_bracket or "—"
    regime = "New Regime" if st.session_state.preferred_regime == "new" else "Old Regime"

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0d1526 0%,#101e38 100%);
                border:1px solid #1c2d4a;border-left:3px solid #4f8ef7;
                border-radius:16px;padding:1.5rem 2rem;margin-bottom:1.5rem;">
        <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;
                    color:#e8eeff;margin-bottom:.35rem;">Welcome back, {name}</div>
        <p style="color:#7a90b8;font-size:13.5px;margin:0;line-height:1.65;">
            {emp} &middot; {bkt} &middot; {regime} &mdash; use the sidebar to navigate.
        </p>
    </div>
    """, unsafe_allow_html=True)

    pages = [
        ("Dashboard",           "Tax calculator · slab breakdown · PDF export"),
        ("AI Advisor",          "Context-aware Indian tax Q&A via Groq"),
        ("Expenses",            "Categorised spend overview with charts"),
        ("GST & ITR Tips",      "Deadlines · penalties · regime comparison"),
        ("Predictive Planning", "Year-end projection from monthly trends"),
        ("Upload Data",         "Add transactions manually or via CSV"),
    ]
    cols = st.columns(3)
    for i, (title, desc) in enumerate(pages):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:#0d1526;border:1px solid #1c2d4a;border-radius:14px;
                        padding:1.1rem 1.2rem;margin-bottom:.75rem;min-height:90px;">
                <div style="font-family:'Syne',sans-serif;font-weight:700;
                            font-size:.88rem;color:#e8eeff;margin-bottom:.25rem;">{title}</div>
                <div style="color:#3d5070;font-size:11px;line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <p style="color:#3d5070;font-size:10.5px;margin-top:.8rem;text-align:center;
              font-family:'DM Mono',monospace;">
        transaction data stored in local sqlite · persists within current deployment instance
    </p>
    """, unsafe_allow_html=True)


# ── Router ─────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    render_auth()
elif st.session_state.setup_complete == 0:
    render_wizard()
else:
    render_home()

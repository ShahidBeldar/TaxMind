import streamlit as st
from utils.db import init_db, create_user, authenticate_user, update_user_profile
from utils.i18n import t
from utils.theme import inject_theme, page_title, card

# ── Page config — must be the very first Streamlit call ──────────────────────
st.set_page_config(
    page_title="TaxMind AI",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="auto",
)

# ── Database bootstrap ────────────────────────────────────────────────────────
init_db()

# ── Session state defaults ────────────────────────────────────────────────────
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
        "auth_tab":         "login",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

_init_session()

# ── Load profile from DB row ──────────────────────────────────────────────────
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

# ── Logout ────────────────────────────────────────────────────────────────────
def logout():
    for key in ["logged_in", "user_id", "username", "name", "employment_type",
                "income_bracket", "preferred_regime", "language",
                "setup_complete", "chat_history"]:
        st.session_state[key] = None if key == "user_id" else (
            False if key == "logged_in" else ""
        )
    st.session_state.setup_complete = 0
    st.session_state.chat_history   = []
    st.rerun()

# ── Auth UI ───────────────────────────────────────────────────────────────────
def render_auth():
    inject_theme()

    # Centered layout
    _, col, _ = st.columns([1, 1.6, 1])
    with col:
        st.markdown("""
        <div style="text-align:center;padding:2.5rem 0 1.5rem 0;">
            <div style="font-size:2.8rem;margin-bottom:.5rem;">💹</div>
            <h1 style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;
                       color:#f0f4ff;letter-spacing:-.04em;margin:0;">TaxMind AI</h1>
            <p style="color:#5a6a85;font-size:14px;margin:.4rem 0 0 0;letter-spacing:.06em;
                      text-transform:uppercase;">Indian Tax Planning · FY 2026</p>
        </div>
        <hr style="border-color:#252d3d;margin:0 0 1.5rem 0;">
        """, unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

        with tab_login:
            st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
            username = st.text_input("Username", key="login_username", placeholder="your_username")
            password = st.text_input("Password", type="password", key="login_password", placeholder="••••••••")
            st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)
            if st.button("Sign In →", key="btn_login", use_container_width=True):
                if not username or not password:
                    st.error("Please enter your username and password.")
                else:
                    row = authenticate_user(username, password)
                    if row:
                        _load_session_from_row(row)
                        st.rerun()
                    else:
                        st.error(t("invalid_credentials"))

        with tab_signup:
            st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
            new_username = st.text_input("Choose a Username", key="signup_username", placeholder="your_username")
            new_password = st.text_input("Password", type="password", key="signup_password", placeholder="Min 6 characters")
            confirm_pw   = st.text_input("Confirm Password", type="password", key="signup_confirm", placeholder="Repeat password")
            st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)
            if st.button("Create Account →", key="btn_signup", use_container_width=True):
                if not new_username or not new_password:
                    st.error("Username and password are required.")
                elif new_password != confirm_pw:
                    st.error("Passwords do not match.")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    success = create_user(new_username, new_password)
                    if success:
                        st.success(t("signup_success"))
                        row = authenticate_user(new_username, new_password)
                        if row:
                            _load_session_from_row(row)
                            st.rerun()
                    else:
                        st.error(t("username_taken"))

        st.markdown("""
        <p style="text-align:center;color:#5a6a85;font-size:11px;margin-top:1.5rem;">
            Data stored locally · FY 2026 New Regime · AI-powered advice
        </p>
        """, unsafe_allow_html=True)

# ── Profile wizard ────────────────────────────────────────────────────────────
def render_wizard():
    inject_theme()
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div style="padding:1.5rem 0 .5rem 0;">
            <h1 style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#f0f4ff;margin:0;">
                Set Up Your Profile
            </h1>
            <p style="color:#5a6a85;font-size:13px;margin:.4rem 0 0 0;">
                This helps personalise your tax advice and dashboard.
            </p>
        </div>
        <hr style="border-color:#252d3d;">
        """, unsafe_allow_html=True)

        name = st.text_input(t("full_name"), value=st.session_state.name, placeholder="e.g. Arjun Mehta")
        employment_type = st.selectbox(t("employment_type"), options=["Salaried", "Self-Employed", "Business"])
        income_bracket  = st.selectbox(t("income_bracket"),
            options=["Below 5L", "5L - 10L", "10L - 15L", "15L - 25L", "25L - 50L", "Above 50L"])
        preferred_regime = st.selectbox(t("preferred_regime"), options=["new", "old"],
            format_func=lambda x: "New Regime (FY 2026 default)" if x == "new" else "Old Regime")
        language = st.selectbox(t("language_label"), options=["en", "hi"],
            format_func=lambda x: "English" if x == "en" else "Hindi")

        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
        if st.button(t("wizard_save"), use_container_width=True):
            if not name.strip():
                st.error("Please enter your name.")
            else:
                update_user_profile(st.session_state.user_id, name.strip(),
                                    employment_type, income_bracket, preferred_regime, language)
                st.session_state.name             = name.strip()
                st.session_state.employment_type  = employment_type
                st.session_state.income_bracket   = income_bracket
                st.session_state.preferred_regime = preferred_regime
                st.session_state.language         = language
                st.session_state.setup_complete   = 1
                st.success(t("wizard_saved"))
                st.rerun()

# ── Sidebar ───────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:.8rem 0 .5rem 0;">
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#f0f4ff;">
                {st.session_state.name or st.session_state.username}
            </div>
            <div style="color:#5a6a85;font-size:11px;margin-top:.2rem;letter-spacing:.04em;">
                {st.session_state.employment_type} · {st.session_state.income_bracket}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#252d3d;margin:.6rem 0;'>", unsafe_allow_html=True)

        lang = st.selectbox(t("language_label"), options=["en", "hi"],
            format_func=lambda x: "English" if x == "en" else "Hindi",
            index=0 if st.session_state.language == "en" else 1, key="sidebar_language")
        if lang != st.session_state.language:
            from utils.db import update_user_language
            update_user_language(st.session_state.user_id, lang)
            st.session_state.language = lang
            st.rerun()

        st.markdown("<hr style='border-color:#252d3d;margin:.6rem 0;'>", unsafe_allow_html=True)
        if st.button(t("logout"), use_container_width=True):
            logout()

        st.markdown("""
        <div style="position:absolute;bottom:1.5rem;left:1rem;right:1rem;">
            <div style="color:#5a6a85;font-size:10px;text-align:center;letter-spacing:.04em;">
                TaxMind AI · FY 2026
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Home page ─────────────────────────────────────────────────────────────────
def render_home():
    inject_theme()
    st.markdown(page_title("💹", "TaxMind AI", "Indian Tax Planning for FY 2026"),
                unsafe_allow_html=True)

    name = st.session_state.name or st.session_state.username
    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg, #171c27 0%, #1a2435 100%);
        border:1px solid #252d3d;
        border-left:3px solid #00e676;
        border-radius:16px;
        padding:1.6rem 2rem;
        margin-bottom:1.5rem;
    ">
        <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;
                    color:#f0f4ff;margin-bottom:.4rem;">
            Welcome back, {name} 👋
        </div>
        <p style="color:#9aaac4;font-size:14px;margin:0;line-height:1.6;">
            Use the sidebar to navigate. Your data is secure and stored locally.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Quick-nav cards
    pages = [
        ("📊", "Dashboard", "Tax calculator with slab breakdown & PDF export"),
        ("🤖", "AI Advisor", "Ask anything about ITR, GST, advance tax"),
        ("💳", "Expenses", "Categorised spend overview with charts"),
        ("📋", "GST & ITR Tips", "Deadlines, penalties, regime comparison"),
        ("📈", "Predictive Planning", "Year-end projection from monthly trends"),
        ("⬆️", "Upload Data", "Add transactions manually or via CSV"),
    ]

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(pages):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="
                background:#171c27;border:1px solid #252d3d;border-radius:14px;
                padding:1.2rem 1.3rem;margin-bottom:.8rem;height:110px;
                transition:border-color .2s;
            ">
                <div style="font-size:1.4rem;margin-bottom:.4rem;">{icon}</div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;
                            font-size:.95rem;color:#f0f4ff;">{title}</div>
                <div style="color:#5a6a85;font-size:11px;margin-top:.2rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <p style="color:#5a6a85;font-size:11px;margin-top:1rem;text-align:center;">
        Transaction data is stored in a local SQLite file (taxmind.db).
        Data persists within the current deployment instance.
    </p>
    """, unsafe_allow_html=True)

# ── Router ────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    render_auth()
elif st.session_state.setup_complete == 0:
    render_wizard()
else:
    render_sidebar()
    render_home()

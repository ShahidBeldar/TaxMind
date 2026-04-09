import streamlit as st
from utils.db import init_db, create_user, authenticate_user, update_user_profile
from utils.i18n import t

# ---------------------------------------------------------------------------
# Page config — must be first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="TaxMind AI",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="auto",
)

# ---------------------------------------------------------------------------
# Database bootstrap
# ---------------------------------------------------------------------------
init_db()

# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------
def _init_session():
    defaults = {
        "logged_in":       False,
        "user_id":         None,
        "username":        "",
        "name":            "",
        "employment_type": "",
        "income_bracket":  "",
        "preferred_regime": "new",
        "language":        "en",
        "setup_complete":  0,
        "chat_history":    [],
        "auth_tab":        "login",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

_init_session()

# ---------------------------------------------------------------------------
# Load user profile into session from DB row
# ---------------------------------------------------------------------------
def _load_session_from_row(row):
    st.session_state.logged_in       = True
    st.session_state.user_id         = row["id"]
    st.session_state.username        = row["username"]
    st.session_state.name            = row["name"] or ""
    st.session_state.employment_type = row["employment_type"] or ""
    st.session_state.income_bracket  = row["income_bracket"] or ""
    st.session_state.preferred_regime = row["preferred_regime"] or "new"
    st.session_state.language        = row["language"] or "en"
    st.session_state.setup_complete  = row["setup_complete"] or 0

# ---------------------------------------------------------------------------
# Logout
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Auth UI
# ---------------------------------------------------------------------------
def render_auth():
    st.title("TaxMind AI")
    st.caption("Indian Tax Planning for FY 2026")
    st.write("---")

    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    # Login tab
    with tab_login:
        st.subheader("Login to your account")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", key="btn_login", use_container_width=True):
            if not username or not password:
                st.error("Please enter username and password.")
            else:
                row = authenticate_user(username, password)
                if row:
                    _load_session_from_row(row)
                    st.rerun()
                else:
                    st.error(t("invalid_credentials"))

    # Signup tab
    with tab_signup:
        st.subheader("Create a new account")
        new_username = st.text_input("Username", key="signup_username")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_pw   = st.text_input("Confirm Password", type="password", key="signup_confirm")

        if st.button("Create Account", key="btn_signup", use_container_width=True):
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

# ---------------------------------------------------------------------------
# Profile wizard — runs once after first signup
# ---------------------------------------------------------------------------
def render_wizard():
    st.title(t("wizard_title"))
    st.caption(t("wizard_subtitle"))
    st.write("---")

    name = st.text_input(t("full_name"), value=st.session_state.name)

    employment_type = st.selectbox(
        t("employment_type"),
        options=["Salaried", "Self-Employed", "Business"],
        index=0,
    )

    income_bracket = st.selectbox(
        t("income_bracket"),
        options=[
            "Below 5L",
            "5L - 10L",
            "10L - 15L",
            "15L - 25L",
            "25L - 50L",
            "Above 50L",
        ],
        index=0,
    )

    preferred_regime = st.selectbox(
        t("preferred_regime"),
        options=["new", "old"],
        format_func=lambda x: "New Regime (FY 2026 default)" if x == "new" else "Old Regime",
        index=0,
    )

    language = st.selectbox(
        t("language_label"),
        options=["en", "hi"],
        format_func=lambda x: "English" if x == "en" else "Hindi",
        index=0,
    )

    st.write("")
    if st.button(t("wizard_save"), use_container_width=True):
        if not name.strip():
            st.error("Please enter your name.")
        else:
            update_user_profile(
                st.session_state.user_id,
                name.strip(),
                employment_type,
                income_bracket,
                preferred_regime,
                language,
            )
            st.session_state.name             = name.strip()
            st.session_state.employment_type  = employment_type
            st.session_state.income_bracket   = income_bracket
            st.session_state.preferred_regime = preferred_regime
            st.session_state.language         = language
            st.session_state.setup_complete   = 1
            st.success(t("wizard_saved"))
            st.rerun()

# ---------------------------------------------------------------------------
# Sidebar — shown only when logged in and setup complete
# ---------------------------------------------------------------------------
def render_sidebar():
    with st.sidebar:
        st.write(f"**{st.session_state.name or st.session_state.username}**")
        st.caption(f"{st.session_state.employment_type} | {st.session_state.income_bracket}")
        st.write("---")

        lang = st.selectbox(
            t("language_label"),
            options=["en", "hi"],
            format_func=lambda x: "English" if x == "en" else "Hindi",
            index=0 if st.session_state.language == "en" else 1,
            key="sidebar_language",
        )
        if lang != st.session_state.language:
            from utils.db import update_user_language
            update_user_language(st.session_state.user_id, lang)
            st.session_state.language = lang
            st.rerun()

        st.write("---")
        if st.button(t("logout"), use_container_width=True):
            logout()

# ---------------------------------------------------------------------------
# Main landing content (shown after full setup)
# ---------------------------------------------------------------------------
def render_home():
    st.title("TaxMind AI")
    st.caption("Indian Tax Planning for FY 2026")
    st.write("---")
    st.write(
        "Welcome back, **{}**. Use the sidebar to navigate to any section.".format(
            st.session_state.name or st.session_state.username
        )
    )
    st.info(
        "Navigate using the sidebar: Dashboard, AI Advisor, Expenses, GST & ITR Tips, "
        "Predictive Planning, Upload Data, Pricing, and Why TaxMind."
    )
    st.write("")
    st.caption(
        "Note: Transaction data is stored in a local SQLite file (taxmind.db). "
        "Data persists within the current deployment instance but will reset "
        "if the app is redeployed or restarts after a period of inactivity on "
        "Streamlit Community Cloud."
    )

# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
if not st.session_state.logged_in:
    render_auth()
elif st.session_state.setup_complete == 0:
    render_wizard()
else:
    render_sidebar()
    render_home()

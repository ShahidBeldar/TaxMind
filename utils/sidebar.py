"""
TaxMind AI — Shared sidebar renderer.
Import and call render_sidebar() in every page after inject_theme().
"""
import streamlit as st
from utils.i18n import t


def logout():
    for key in ["logged_in", "user_id", "username", "name", "employment_type",
                "income_bracket", "preferred_regime", "language",
                "setup_complete", "chat_history"]:
        st.session_state[key] = None if key == "user_id" else (
            False if key == "logged_in" else ""
        )
    st.session_state.setup_complete = 0
    st.session_state.chat_history   = []
    st.switch_page("app.py")


def render_sidebar():
    with st.sidebar:
        # Brand
        st.markdown("""
        <div style="padding:1.2rem 1rem 0.8rem 1rem;border-bottom:1px solid #1e2a3d;">
            <div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.8rem;">
                <span style="font-size:1.2rem;">💹</span>
                <span style="font-family:'Syne',sans-serif;font-size:.95rem;font-weight:800;
                             color:#edf2ff;letter-spacing:-.02em;">TaxMind AI</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # User profile
        name_display = st.session_state.get("name") or st.session_state.get("username", "—")
        emp    = st.session_state.get("employment_type") or "—"
        bkt    = st.session_state.get("income_bracket")  or "—"
        regime = "New" if st.session_state.get("preferred_regime", "new") == "new" else "Old"

        st.markdown(f"""
        <div style="padding:.8rem 1rem;border-bottom:1px solid #1e2a3d;">
            <div style="font-family:'Syne',sans-serif;font-size:.85rem;font-weight:700;
                        color:#edf2ff;margin-bottom:.3rem;white-space:nowrap;
                        overflow:hidden;text-overflow:ellipsis;">{name_display}</div>
            <div style="display:flex;flex-wrap:wrap;gap:.3rem;">
                <span style="background:#161d2e;border:1px solid #1e2a3d;border-radius:5px;
                             color:#4a5a72;font-size:10px;padding:1px 7px;">{emp}</span>
                <span style="background:#161d2e;border:1px solid #1e2a3d;border-radius:5px;
                             color:#4a5a72;font-size:10px;padding:1px 7px;">{bkt}</span>
                <span style="background:#0d2018;border:1px solid #1e3d28;border-radius:5px;
                             color:#00e676;font-size:10px;padding:1px 7px;">{regime} Regime</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation label
        st.markdown("""
        <div style="padding:.65rem 1rem .2rem 1rem;">
            <div style="color:#4a5a72;font-size:10px;font-weight:600;letter-spacing:.1em;
                        text-transform:uppercase;font-family:'DM Mono',monospace;">Navigation</div>
        </div>
        """, unsafe_allow_html=True)

        nav_items = [
            ("🏠", "Home",                "app.py"),
            ("📊", "Dashboard",           "pages/1_Dashboard.py"),
            ("🤖", "AI Advisor",          "pages/2_AI_Advisor.py"),
            ("💳", "Expenses",            "pages/3_Expenses.py"),
            ("📋", "GST & ITR Tips",      "pages/4_GST_ITR_Tips.py"),
            ("📈", "Predictive Planning", "pages/5_Predictive_Planning.py"),
            ("⬆️", "Upload Data",         "pages/6_Upload_Data.py"),
            ("💰", "Pricing",             "pages/7_Pricing.py"),
            ("🧠", "Why TaxMind",         "pages/8_Why_TaxMind.py"),
        ]

        for icon, label, path in nav_items:
            if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
                st.switch_page(path)

        # Settings
        st.markdown("""
        <div style="padding:.65rem 1rem .2rem 1rem;margin-top:.4rem;border-top:1px solid #1e2a3d;">
            <div style="color:#4a5a72;font-size:10px;font-weight:600;letter-spacing:.1em;
                        text-transform:uppercase;font-family:'DM Mono',monospace;">Settings</div>
        </div>
        """, unsafe_allow_html=True)

        lang = st.selectbox(
            t("language_label"),
            options=["en", "hi"],
            format_func=lambda x: "🇬🇧  English" if x == "en" else "🇮🇳  Hindi",
            index=0 if st.session_state.get("language", "en") == "en" else 1,
            key="sidebar_language",
        )
        if lang != st.session_state.get("language", "en"):
            from utils.db import update_user_language
            update_user_language(st.session_state.user_id, lang)
            st.session_state.language = lang
            st.rerun()

        # Logout at the very bottom
        st.markdown("""
        <div style="border-top:1px solid #1e2a3d;padding-top:.4rem;margin-top:.6rem;"></div>
        """, unsafe_allow_html=True)

        if st.button("⎋  Sign Out", key="btn_logout", use_container_width=True):
            logout()

        st.markdown("""
        <div style="padding:.8rem 1rem;margin-top:.2rem;">
            <div style="color:#2a3a52;font-size:10px;text-align:center;
                        letter-spacing:.04em;font-family:'DM Mono',monospace;">
                TaxMind AI · FY 2026
            </div>
        </div>
        """, unsafe_allow_html=True)

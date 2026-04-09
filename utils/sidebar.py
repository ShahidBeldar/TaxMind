"""
TaxMind AI — Shared sidebar. One file, imported by every page.
No emojis. Safe navigation via st.switch_page with exact filenames.
"""
import streamlit as st
from utils.i18n import t


def logout():
    keys_to_clear = [
        "logged_in", "user_id", "username", "name",
        "employment_type", "income_bracket", "preferred_regime",
        "language", "setup_complete", "chat_history",
    ]
    for key in keys_to_clear:
        if key == "user_id":
            st.session_state[key] = None
        elif key == "logged_in":
            st.session_state[key] = False
        elif key in ("setup_complete",):
            st.session_state[key] = 0
        elif key == "chat_history":
            st.session_state[key] = []
        else:
            st.session_state[key] = ""
    st.switch_page("app.py")


# Map label -> exact filename Streamlit expects for switch_page
_NAV = [
    ("Home",               "app.py"),
    ("Dashboard",          "pages/1_Dashboard.py"),
    ("AI Advisor",         "pages/2_AI_Advisor.py"),
    ("Expenses",           "pages/3_Expenses.py"),
    ("GST & ITR Tips",     "pages/4_GST_ITR_Tips.py"),
    ("Predictive Planning","pages/5_Predictive_Planning.py"),
    ("Upload Data",        "pages/6_Upload_Data.py"),
    ("Pricing",            "pages/7_Pricing.py"),
    ("Why TaxMind",        "pages/8_Why_TaxMind.py"),
]


def render_sidebar():
    with st.sidebar:
        # ── Brand ──────────────────────────────────────────────────────────
        st.markdown("""
        <div style="padding:1.1rem 1rem 0.75rem 1rem;border-bottom:1px solid #1c2d4a;">
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:800;
                        color:#e8eeff;letter-spacing:-.02em;line-height:1.2;">
                TaxMind AI
            </div>
            <div style="color:#3d5070;font-size:10px;letter-spacing:.06em;
                        text-transform:uppercase;margin-top:.2rem;
                        font-family:'DM Mono',monospace;">
                FY 2026
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── User profile ───────────────────────────────────────────────────
        name_display = st.session_state.get("name") or st.session_state.get("username") or "User"
        emp    = st.session_state.get("employment_type") or "—"
        bkt    = st.session_state.get("income_bracket")  or "—"
        regime = "New Regime" if st.session_state.get("preferred_regime", "new") == "new" else "Old Regime"

        st.markdown(f"""
        <div style="padding:.75rem 1rem;border-bottom:1px solid #1c2d4a;">
            <div style="font-family:'Syne',sans-serif;font-size:.82rem;font-weight:700;
                        color:#e8eeff;margin-bottom:.3rem;white-space:nowrap;
                        overflow:hidden;text-overflow:ellipsis;">{name_display}</div>
            <div style="display:flex;flex-wrap:wrap;gap:.25rem;">
                <span style="background:#111d33;border:1px solid #1c2d4a;border-radius:4px;
                             color:#3d5070;font-size:9.5px;padding:1px 6px;
                             font-family:'DM Mono',monospace;">{emp}</span>
                <span style="background:#111d33;border:1px solid #1c2d4a;border-radius:4px;
                             color:#3d5070;font-size:9.5px;padding:1px 6px;
                             font-family:'DM Mono',monospace;">{bkt}</span>
                <span style="background:#0d1a33;border:1px solid #243858;border-radius:4px;
                             color:#4f8ef7;font-size:9.5px;padding:1px 6px;
                             font-family:'DM Mono',monospace;">{regime}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Navigation ─────────────────────────────────────────────────────
        st.markdown("""
        <div style="padding:.6rem 1rem .15rem 1rem;">
            <div style="color:#3d5070;font-size:9.5px;font-weight:600;letter-spacing:.12em;
                        text-transform:uppercase;font-family:'DM Mono',monospace;">
                Navigation
            </div>
        </div>
        """, unsafe_allow_html=True)

        for label, path in _NAV:
            if st.button(label, key=f"nav_{label}", use_container_width=True):
                try:
                    st.switch_page(path)
                except Exception:
                    st.rerun()

        # ── Settings ───────────────────────────────────────────────────────
        st.markdown("""
        <div style="padding:.6rem 1rem .15rem 1rem;margin-top:.3rem;
                    border-top:1px solid #1c2d4a;">
            <div style="color:#3d5070;font-size:9.5px;font-weight:600;letter-spacing:.12em;
                        text-transform:uppercase;font-family:'DM Mono',monospace;">
                Settings
            </div>
        </div>
        """, unsafe_allow_html=True)

        current_lang = st.session_state.get("language", "en")
        lang = st.selectbox(
            "Language",
            options=["en", "hi"],
            format_func=lambda x: "English" if x == "en" else "Hindi",
            index=0 if current_lang == "en" else 1,
            key="sidebar_language",
            label_visibility="collapsed",
        )
        if lang != current_lang:
            try:
                from utils.db import update_user_language
                update_user_language(st.session_state.user_id, lang)
            except Exception:
                pass
            st.session_state.language = lang
            st.rerun()

        # ── Logout ─────────────────────────────────────────────────────────
        st.markdown("""
        <div style="border-top:1px solid #1c2d4a;margin-top:.5rem;padding-top:.4rem;"></div>
        """, unsafe_allow_html=True)

        if st.button("Sign Out", key="btn_logout", use_container_width=True):
            logout()

        st.markdown("""
        <div style="padding:.7rem 1rem;margin-top:.2rem;">
            <div style="color:#1c2d4a;font-size:9.5px;text-align:center;
                        letter-spacing:.04em;font-family:'DM Mono',monospace;">
                taxmind · fy 2026
            </div>
        </div>
        """, unsafe_allow_html=True)

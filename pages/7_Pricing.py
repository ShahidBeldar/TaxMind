import streamlit as st
from utils.i18n import t
from utils.sidebar import render_sidebar
from utils.theme import inject_theme, page_title

# ── Auth guard ────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()

inject_theme()
render_sidebar()

st.markdown(page_title("💰", "Pricing", "Simple, transparent plans for every taxpayer"),
            unsafe_allow_html=True)

# ── Pricing cards ─────────────────────────────────────────────────────────────
plans = [
    {
        "name":    "Free",
        "price":   "Rs. 0",
        "period":  "/ month",
        "badge":   "",
        "accent":  "#5a6a85",
        "features": [
            ("Tax Calculator (New Regime)", True),
            ("AI Tax Advisor — 20 queries/mo", True),
            ("PDF & CSV Export", True),
            ("Transaction Records — up to 100", True),
            ("CSV Bulk Import", False),
            ("Predictive Tax Planning", False),
            ("Multi-user / Team Access", False),
            ("Priority Support", False),
            ("Cloud-backed Data", False),
        ],
    },
    {
        "name":    "Pro",
        "price":   "Rs. 499",
        "period":  "/ month",
        "badge":   "POPULAR",
        "accent":  "#00e676",
        "features": [
            ("Tax Calculator (New Regime)", True),
            ("AI Tax Advisor — Unlimited", True),
            ("PDF & CSV Export", True),
            ("Unlimited Transactions", True),
            ("CSV Bulk Import", True),
            ("Predictive Tax Planning", True),
            ("Multi-user / Team Access", False),
            ("Priority Email Support", True),
            ("Cloud-backed Data", True),
        ],
    },
    {
        "name":    "Enterprise",
        "price":   "Custom",
        "period":  "",
        "badge":   "",
        "accent":  "#ffab40",
        "features": [
            ("Tax Calculator (New Regime)", True),
            ("AI Tax Advisor — Unlimited", True),
            ("PDF & CSV Export", True),
            ("Unlimited Transactions", True),
            ("CSV Bulk Import", True),
            ("Predictive Tax Planning", True),
            ("Multi-user / Team Access", True),
            ("Dedicated Account Manager", True),
            ("Cloud + Audit Logs", True),
        ],
    },
]

cols = st.columns(3)
for col, plan in zip(cols, plans):
    with col:
        badge_html = f"""
        <div style="background:{plan['accent']};color:#0f1117;font-size:9px;
                    font-weight:800;letter-spacing:.1em;border-radius:4px;
                    padding:2px 8px;display:inline-block;margin-bottom:.6rem;">
            {plan['badge']}
        </div>
        """ if plan["badge"] else "<div style='height:20px'></div>"

        features_html = "".join([
            f"""<div style="display:flex;align-items:center;gap:.5rem;
                            padding:.35rem 0;border-bottom:1px solid #1d2333;">
                <span style="color:{'#00e676' if ok else '#252d3d'};font-size:1rem;">
                    {'✓' if ok else '✕'}
                </span>
                <span style="color:{'#9aaac4' if ok else '#3a4a5e'};font-size:12.5px;">
                    {feat}
                </span>
            </div>"""
            for feat, ok in plan["features"]
        ])

        st.markdown(f"""
        <div style="
            background:#171c27;
            border:1.5px solid {plan['accent'] if plan['badge'] else '#252d3d'};
            border-radius:18px;
            padding:1.6rem 1.5rem;
            height:100%;
            {'box-shadow:0 0 30px rgba(0,230,118,.08);' if plan['badge'] else ''}
        ">
            {badge_html}
            <div style="font-family:'Syne',sans-serif;font-weight:800;
                        font-size:1.25rem;color:#f0f4ff;margin-bottom:.2rem;">
                {plan['name']}
            </div>
            <div style="margin-bottom:1.2rem;">
                <span style="font-family:'DM Mono',monospace;font-size:1.8rem;
                             font-weight:700;color:{plan['accent']};">
                    {plan['price']}
                </span>
                <span style="color:#5a6a85;font-size:13px;">{plan['period']}</span>
            </div>
            {features_html}
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
st.markdown("""
<p style="color:#5a6a85;font-size:12px;text-align:center;">
    All plans billed monthly · No long-term contracts · GST applicable on paid plans<br>
    Enterprise for teams of 10+ · Contact <a href="mailto:enterprise@taxmind.ai"
    style="color:#00e676;text-decoration:none;">enterprise@taxmind.ai</a>
</p>
""", unsafe_allow_html=True)

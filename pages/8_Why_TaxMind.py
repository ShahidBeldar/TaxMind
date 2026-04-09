import streamlit as st
from utils.sidebar import render_sidebar
from utils.theme import inject_theme, page_title, card

# ── Auth guard ────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()

inject_theme()
render_sidebar()

st.markdown(page_title("", "Why TaxMind",
    "Built exclusively for FY 2026 Indian taxpayers"),
    unsafe_allow_html=True)

# ── Problem statement ─────────────────────────────────────────────────────────
st.markdown("""
<div style="
    background:linear-gradient(135deg,#171c27 0%,#1a2435 100%);
    border:1px solid #252d3d;border-radius:16px;
    padding:1.6rem 2rem;margin-bottom:1.8rem;
">
    <h3 style="font-family:'Syne',sans-serif;color:#f0f4ff;font-size:1.1rem;margin:0 0 .6rem 0;">
        The problem with tax planning in India today
    </h3>
    <p style="color:#9aaac4;font-size:14px;margin:0;line-height:1.7;">
        Most Indian taxpayers file returns reactively at the last minute or rely entirely on a CA
        without understanding their own tax position. Spreadsheets are fragile. Generic apps
        don't understand Indian tax law. AI tools abroad have no awareness of Section 87A,
        advance tax timelines, or the new vs old regime trade-offs.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Feature cards ─────────────────────────────────────────────────────────────
st.markdown("""
<h2 style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;
           color:#f0f4ff;margin-bottom:1rem;">
    What TaxMind AI does differently
</h2>
""", unsafe_allow_html=True)

features = [
    ("", "Built exclusively for FY 2026 Indian tax rules",
     "Tax engine coded precisely to new regime slabs, Rs. 75,000 standard deduction, "
     "Section 87A rebate ceiling of Rs. 60,000, and 4% cess — not a generic calculator "
     "with an India filter."),
    ("", "AI advisor that knows your financial context",
     "Every AI query silently passes your employment type, income bracket, preferred regime, "
     "recorded income, and estimated tax. Advice calibrated to your situation."),
    ("", "Automatic transaction categorisation",
     "Every transaction is categorised by keyword matching — Zomato → Food, IRCTC → Transport, "
     "SIP → Investment. No manual tagging required."),
    ("", "Predictive planning before year-end surprises",
     "Monthly income and expense trends are projected forward to estimate full-year tax liability. "
     "Act before March scrambles."),
    ("", "Advance tax and penalty awareness built in",
     "Deadlines, installment percentages, and Sections 234B & 234C costs are all in one place."),
    ("", "Export-ready computations",
     "Tax computation exportable as a formatted PDF or CSV — ready to share with your CA."),
    ("", "Privacy-first local storage",
     "On the free tier, data lives in a local SQLite file, never shared with third parties. "
     "Pro and Enterprise use encrypted cloud-backed storage."),
    ("", "Minimalist, professional design — no noise",
     "No gamification. No confetti. No dark patterns. A clean tool that works."),
]

col_a, col_b = st.columns(2)
for i, (icon, heading, body) in enumerate(features):
    target_col = col_a if i % 2 == 0 else col_b
    with target_col:
        st.markdown(card(f"""
        <div style="display:flex;align-items:flex-start;gap:.8rem;">
            <span style="font-size:1.4rem;line-height:1;">{icon}</span>
            <div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;
                            color:#f0f4ff;font-size:.95rem;margin-bottom:.3rem;">
                    {heading}
                </div>
                <p style="color:#9aaac4;font-size:13px;margin:0;line-height:1.6;">
                    {body}
                </p>
            </div>
        </div>
        """), unsafe_allow_html=True)

# ── Who it's for ──────────────────────────────────────────────────────────────
st.markdown("<hr style='border-color:#252d3d;margin:1.5rem 0;'>", unsafe_allow_html=True)
st.markdown("""
<h2 style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;
           color:#f0f4ff;margin-bottom:1rem;">
    Who TaxMind is built for
</h2>
""", unsafe_allow_html=True)

segments = [
    ("", "Salaried professionals",
     "Understand take-home after tax, verify Form 16, decide old vs new regime, "
     "and plan NPS contributions to maximise 80CCD(2)."),
    ("", "Freelancers and consultants",
     "Track income across clients, understand advance tax obligations, "
     "and monitor GST registration thresholds."),
    ("", "Small business owners",
     "Monitor monthly cash flow, auto-categorise expenses, and ask regime-specific "
     "deduction questions without scheduling a CA appointment."),
    ("", "First-time ITR filers",
     "The AI advisor walks you through which ITR form applies, what documents you need, "
     "and what deductions you may be missing."),
]

s1, s2 = st.columns(2)
for i, (icon, seg, desc) in enumerate(segments):
    with (s1 if i % 2 == 0 else s2):
        st.markdown(card(f"""
        <div style="display:flex;align-items:flex-start;gap:.8rem;">
            <span style="font-size:1.3rem;">{icon}</span>
            <div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;
                            color:#f0f4ff;font-size:.9rem;margin-bottom:.25rem;">
                    {seg}
                </div>
                <p style="color:#9aaac4;font-size:12.5px;margin:0;line-height:1.6;">{desc}</p>
            </div>
        </div>
        """), unsafe_allow_html=True)

st.markdown("""
<p style="color:#5a6a85;font-size:11px;text-align:center;margin-top:1.5rem;">
    TaxMind AI provides information and estimates for planning purposes only.
    It does not constitute legal or financial advice.
    Consult a qualified Chartered Accountant for compliance filing.
</p>
""", unsafe_allow_html=True)

import streamlit as st
from utils.i18n import t

# ---------------------------------------------------------------------------
# Auth guard
# ---------------------------------------------------------------------------
if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()

# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------
st.title(t("why_title"))
st.write("---")

st.subheader("The Problem with Tax Planning in India Today")
st.write(
    "Most Indian taxpayers either file returns reactively at the last minute or "
    "rely entirely on a CA without understanding their own tax position. "
    "Spreadsheets are fragile. Generic apps do not understand Indian tax law. "
    "And AI tools abroad have no awareness of Section 87A, advance tax timelines, "
    "or the new versus old regime trade-offs."
)

st.write("---")
st.subheader("What TaxMind AI Does Differently")

points = [
    (
        "Built exclusively for FY 2026 Indian tax rules",
        "The tax engine is coded precisely to the new regime slabs, standard deduction "
        "of Rs. 75,000, Section 87A rebate ceiling of Rs. 60,000, and 4% cess — "
        "not a generic calculator with an India filter applied on top.",
    ),
    (
        "AI advisor that knows your financial context",
        "Every query to the AI advisor silently passes your employment type, income "
        "bracket, preferred regime, recorded income, and estimated tax liability. "
        "You get advice calibrated to your situation, not generic content.",
    ),
    (
        "Transaction categorization without manual effort",
        "Every transaction you enter or upload is automatically categorized using "
        "keyword matching on the description — Zomato becomes Food, IRCTC becomes "
        "Transport, SIP becomes Investment. No manual tagging required.",
    ),
    (
        "Predictive planning before year-end surprises",
        "Monthly trends in your income and expenses are projected forward to estimate "
        "your full-year tax liability. You can act in advance instead of scrambling "
        "in March.",
    ),
    (
        "Advance tax and penalty awareness built in",
        "The GST and ITR Tips page keeps you informed of deadlines, installment "
        "percentages, and what Sections 234B and 234C cost you in interest if you miss them.",
    ),
    (
        "Export-ready computations",
        "Your tax computation is exportable as a properly formatted PDF or CSV "
        "with a single click — ready to share with your CA or file for reference.",
    ),
    (
        "Minimalist, professional design — no noise",
        "No gamification. No confetti. No dark patterns pushing upgrades. "
        "TaxMind is built for professionals who want a clean tool that works.",
    ),
    (
        "Privacy-first local storage",
        "On the free tier your data is stored in a local SQLite file within the "
        "deployment instance. It is never shared with third parties. "
        "Pro and Enterprise tiers use encrypted cloud-backed storage.",
    ),
]

for heading, body in points:
    st.markdown(f"**{heading}**")
    st.write(body)
    st.write("")

st.write("---")
st.subheader("Who TaxMind Is Built For")

segments = [
    ("Salaried professionals",
     "Understand your take-home after tax, verify your Form 16, decide whether "
     "the new or old regime saves you more, and plan NPS contributions to maximise "
     "the 80CCD(2) benefit from your employer."),
    ("Freelancers and consultants",
     "Track income across multiple clients, understand your advance tax "
     "obligations, and stay on top of GST registration thresholds."),
    ("Small business owners",
     "Monitor monthly cash flow, categorize expenses automatically, and use "
     "the AI advisor to ask regime-specific deduction questions without "
     "scheduling a CA appointment for every query."),
    ("First-time ITR filers",
     "The AI advisor can walk you through which ITR form applies to you, what "
     "documents you need, and what deductions you may be missing."),
]

for segment, description in segments:
    st.markdown(f"**{segment}**")
    st.write(description)
    st.write("")

st.write("---")
st.caption(
    "TaxMind AI provides information and estimates for planning purposes only. "
    "It does not constitute legal or financial advice. "
    "Consult a qualified Chartered Accountant for compliance filing."
)

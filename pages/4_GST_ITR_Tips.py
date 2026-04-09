import streamlit as st
import pandas as pd
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
st.title(t("gst_itr_title"))
st.write("---")

# ---------------------------------------------------------------------------
# Section 1: Advance Tax Deadlines FY 2026
# ---------------------------------------------------------------------------
st.subheader("Advance Tax Deadlines — FY 2026")
st.caption(
    "Advance tax applies when your estimated annual tax liability exceeds Rs. 10,000. "
    "Salaried individuals whose tax is fully covered by TDS are generally exempt."
)

deadlines = pd.DataFrame([
    {"Installment": "1st",  "Due Date": "15 June 2025",     "Minimum % of Tax Due": "15%"},
    {"Installment": "2nd",  "Due Date": "15 September 2025", "Minimum % of Tax Due": "45%"},
    {"Installment": "3rd",  "Due Date": "15 December 2025",  "Minimum % of Tax Due": "75%"},
    {"Installment": "4th",  "Due Date": "15 March 2026",     "Minimum % of Tax Due": "100%"},
])
st.table(deadlines.set_index("Installment"))

# ---------------------------------------------------------------------------
# Section 2: Interest Penalties — 234B and 234C
# ---------------------------------------------------------------------------
st.write("---")
st.subheader("Interest Penalties — Section 234B and 234C")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Section 234B — Default in Payment of Advance Tax**")
    st.write(
        "Applies when less than 90% of your assessed tax has been paid by 31 March "
        "through advance tax and TDS combined."
    )
    st.write("Interest rate: 1% per month (or part of a month) on the shortfall amount.")
    st.code(
        "Interest = 1% x Shortfall Amount x Number of Months\n"
        "Shortfall = Assessed Tax - TDS - Advance Tax Paid",
        language="text"
    )

with col2:
    st.markdown("**Section 234C — Deferment of Advance Tax Installments**")
    st.write(
        "Applies when each installment is paid short of the required cumulative percentage."
    )
    st.write("Interest rate: 1% per month for 3 months on the shortfall per installment.")
    st.code(
        "Interest = 1% x Shortfall in Installment x 3 months\n"
        "(Last installment: 1 month only)",
        language="text"
    )

# ---------------------------------------------------------------------------
# Section 3: Tax Saving Under New Regime — FY 2026
# ---------------------------------------------------------------------------
st.write("---")
st.subheader("Tax Saving Under the New Regime — FY 2026")

st.write(
    "The New Regime offers limited deductions compared to the Old Regime, but the "
    "following avenues remain valid."
)

savings = pd.DataFrame([
    {
        "Option":        "Standard Deduction",
        "Section":       "16(ia)",
        "Benefit":       "Rs. 75,000 deduction from gross salary",
        "Eligible For":  "Salaried employees only",
    },
    {
        "Option":        "Employer NPS Contribution",
        "Section":       "80CCD(2)",
        "Benefit":       "Up to 14% of basic salary (central govt) / 10% (others)",
        "Eligible For":  "Salaried with employer contributing to NPS",
    },
    {
        "Option":        "Agniveer Corpus Fund",
        "Section":       "80CCH",
        "Benefit":       "Full deduction on contribution",
        "Eligible For":  "Agniveer scheme participants",
    },
    {
        "Option":        "Family Pension Deduction",
        "Section":       "57(iia)",
        "Benefit":       "Lower of Rs. 25,000 or 1/3rd of pension received",
        "Eligible For":  "Recipients of family pension",
    },
    {
        "Option":        "Section 87A Rebate",
        "Section":       "87A",
        "Benefit":       "Full tax rebate up to Rs. 60,000 if taxable income <= Rs. 12,00,000",
        "Eligible For":  "All individual taxpayers under new regime",
    },
])
st.table(savings.set_index("Option"))

st.info(
    "Note: Deductions such as 80C (PPF, ELSS, LIC), 80D (health insurance), "
    "HRA (unless separately provided by employer as exemption u/s 10), and "
    "home loan interest (Section 24) are not available under the new regime."
)

# ---------------------------------------------------------------------------
# Section 4: GST Basics
# ---------------------------------------------------------------------------
st.write("---")
st.subheader("GST — Who Must Register and Current Rate Slabs")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**Mandatory GST Registration**")
    st.write(
        "You are required to register for GST if your aggregate annual turnover exceeds:"
    )
    thresholds = pd.DataFrame([
        {"Business Type":                    "Goods — general states",  "Threshold": "Rs. 40 Lakh"},
        {"Business Type":                    "Goods — special category states", "Threshold": "Rs. 20 Lakh"},
        {"Business Type":                    "Services — all states",   "Threshold": "Rs. 20 Lakh"},
        {"Business Type":                    "Inter-state supply (any)",  "Threshold": "Mandatory regardless of turnover"},
        {"Business Type":                    "E-commerce operators",    "Threshold": "Mandatory regardless of turnover"},
    ])
    st.table(thresholds.set_index("Business Type"))

with col_b:
    st.markdown("**GST Rate Slabs**")
    gst_slabs = pd.DataFrame([
        {"Rate":  "0%",   "Applicable To": "Essential goods — grains, milk, eggs, fresh vegetables"},
        {"Rate":  "5%",   "Applicable To": "Household necessities — packaged food, footwear under Rs. 1,000"},
        {"Rate": "12%",   "Applicable To": "Processed food, computers, business class air travel"},
        {"Rate": "18%",   "Applicable To": "Most services, AC restaurants, financial services, IT services"},
        {"Rate": "28%",   "Applicable To": "Luxury items, tobacco, automobiles, aerated drinks"},
    ])
    st.table(gst_slabs.set_index("Rate"))

st.write("---")
st.subheader("ITR Form Selection Guide")

itr_forms = pd.DataFrame([
    {"ITR Form": "ITR-1 (Sahaj)",  "Who Should File": "Salaried individuals, one house property, income up to Rs. 50 lakh"},
    {"ITR Form": "ITR-2",          "Who Should File": "Capital gains, foreign income, more than one house property"},
    {"ITR Form": "ITR-3",          "Who Should File": "Business or professional income (proprietorship)"},
    {"ITR Form": "ITR-4 (Sugam)",  "Who Should File": "Presumptive income u/s 44AD, 44ADA, 44AE"},
    {"ITR Form": "ITR-5",          "Who Should File": "Partnership firms, LLPs"},
    {"ITR Form": "ITR-6",          "Who Should File": "Companies other than those claiming 11 exemption"},
])
st.table(itr_forms.set_index("ITR Form"))

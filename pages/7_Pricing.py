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
st.title(t("pricing_title"))
st.write("---")

st.subheader("Choose the Plan That Fits Your Needs")
st.write("")

pricing = pd.DataFrame([
    {
        "Feature":                      "Monthly Price",
        "Free":                         "Rs. 0",
        "Pro":                          "Rs. 499 / month",
        "Enterprise":                   "Contact Sales",
    },
    {
        "Feature":                      "Tax Calculator (New Regime)",
        "Free":                         "Yes",
        "Pro":                          "Yes",
        "Enterprise":                   "Yes",
    },
    {
        "Feature":                      "AI Tax Advisor (queries/month)",
        "Free":                         "20",
        "Pro":                          "Unlimited",
        "Enterprise":                   "Unlimited",
    },
    {
        "Feature":                      "Transaction Records",
        "Free":                         "Up to 100",
        "Pro":                          "Unlimited",
        "Enterprise":                   "Unlimited",
    },
    {
        "Feature":                      "CSV Bulk Import",
        "Free":                         "No",
        "Pro":                          "Yes",
        "Enterprise":                   "Yes",
    },
    {
        "Feature":                      "PDF Export",
        "Free":                         "Yes",
        "Pro":                          "Yes",
        "Enterprise":                   "Yes",
    },
    {
        "Feature":                      "Predictive Tax Planning",
        "Free":                         "No",
        "Pro":                          "Yes",
        "Enterprise":                   "Yes",
    },
    {
        "Feature":                      "Multi-user / Team Access",
        "Free":                         "No",
        "Pro":                          "No",
        "Enterprise":                   "Yes",
    },
    {
        "Feature":                      "Priority Support",
        "Free":                         "No",
        "Pro":                          "Email",
        "Enterprise":                   "Dedicated Account Manager",
    },
    {
        "Feature":                      "Data Retention",
        "Free":                         "Session only",
        "Pro":                          "Cloud-backed",
        "Enterprise":                   "Cloud-backed + Audit Logs",
    },
    {
        "Feature":                      "CA Review Integration",
        "Free":                         "No",
        "Pro":                          "No",
        "Enterprise":                   "Yes",
    },
])

st.table(pricing.set_index("Feature"))

st.write("---")
st.caption(
    "All plans are billed monthly. No long-term contracts. "
    "Enterprise pricing is available for teams of 10 or more. "
    "GST applicable on all paid plans. "
    "Contact us at enterprise@taxmind.ai for a custom quote."
)

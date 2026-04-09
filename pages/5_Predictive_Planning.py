import streamlit as st
import pandas as pd
from utils.i18n import t
from utils.db import get_monthly_totals
from utils.tax import calculate_tax, format_inr

# ---------------------------------------------------------------------------
# Auth guard
# ---------------------------------------------------------------------------
if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()

# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------
st.title(t("planning_title"))
st.write("---")

monthly = get_monthly_totals(st.session_state.user_id)

if not monthly:
    st.info(t("no_data_planning"))
    st.stop()

df = pd.DataFrame(monthly)
df["month"] = df["month"].astype(str)

# ---------------------------------------------------------------------------
# Monthly income and expense chart
# ---------------------------------------------------------------------------
st.subheader("Monthly Income and Expenses")

chart_df = df.set_index("month")[["income", "expense"]].rename(
    columns={"income": "Income (Rs.)", "expense": "Expense (Rs.)"}
)
st.line_chart(chart_df)

# ---------------------------------------------------------------------------
# Projections
# ---------------------------------------------------------------------------
st.write("---")
st.subheader("Year-End Projection")

months_recorded  = len(df)
avg_monthly_income  = df["income"].mean()
avg_monthly_expense = df["expense"].mean()

projected_annual_income  = avg_monthly_income  * 12
projected_annual_expense = avg_monthly_expense * 12

employment_type = st.session_state.get("employment_type", "Salaried") or "Salaried"
tax_result      = calculate_tax(projected_annual_income, employment_type, regime="new")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label=t("projected_income"),
        value=format_inr(projected_annual_income),
        help=f"Average monthly income of {format_inr(avg_monthly_income)} x 12"
    )

with col2:
    st.metric(
        label="Projected Annual Expenses",
        value=format_inr(projected_annual_expense),
        help=f"Average monthly expense of {format_inr(avg_monthly_expense)} x 12"
    )

with col3:
    st.metric(
        label=t("projected_tax"),
        value=format_inr(tax_result["total_tax_payable"]),
        help="Estimated under FY 2026 new regime"
    )

st.write("")
st.caption(
    f"Projection based on {months_recorded} month(s) of recorded data. "
    "Add more transactions in Upload Data to improve accuracy."
)

# ---------------------------------------------------------------------------
# Monthly data table
# ---------------------------------------------------------------------------
st.write("---")
st.subheader("Monthly Breakdown")

display_df = df.rename(columns={
    "month":   "Month",
    "income":  "Income (Rs.)",
    "expense": "Expense (Rs.)",
})
display_df["Net (Rs.)"] = display_df["Income (Rs.)"] - display_df["Expense (Rs.)"]
st.dataframe(display_df.set_index("Month"), use_container_width=True)

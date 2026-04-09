import streamlit as st
import pandas as pd
from utils.i18n import t
from utils.db import get_transactions

# ---------------------------------------------------------------------------
# Auth guard
# ---------------------------------------------------------------------------
if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()

# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------
st.title(t("expenses_title"))
st.write("---")

expenses = get_transactions(st.session_state.user_id, txn_type="expense")

if not expenses:
    st.info(t("no_expenses"))
    st.stop()

df = pd.DataFrame(expenses)

# Category summary
category_totals = (
    df.groupby("category")["amount"]
    .sum()
    .reset_index()
    .rename(columns={"category": t("category"), "amount": t("total_amount")})
    .sort_values(t("total_amount"), ascending=False)
)

st.subheader("Spend by Category")
st.table(category_totals.set_index(t("category")))

st.write("")
st.subheader(t("expense_chart_title"))

chart_data = (
    df.groupby("category")["amount"]
    .sum()
    .rename_axis("Category")
    .reset_index()
    .set_index("Category")
    .rename(columns={"amount": "Amount (Rs.)"})
)
st.bar_chart(chart_data)

# Detailed transaction list
st.write("")
st.subheader("All Expense Transactions")

display_df = df[["date", "description", "amount", "category"]].copy()
display_df.columns = ["Date", "Description", "Amount (Rs.)", "Category"]
display_df = display_df.sort_values("Date", ascending=False).reset_index(drop=True)
st.dataframe(display_df, use_container_width=True)

import streamlit as st
import pandas as pd
from utils.i18n import t
from utils.db import insert_transaction, bulk_insert_transactions

# ---------------------------------------------------------------------------
# Auth guard
# ---------------------------------------------------------------------------
if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()

# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------
st.title(t("upload_title"))
st.write("---")

tab_manual, tab_csv = st.tabs([t("manual_entry"), t("csv_upload")])

# ---------------------------------------------------------------------------
# Section A — Manual Entry
# ---------------------------------------------------------------------------
with tab_manual:
    st.subheader(t("manual_entry"))

    date        = st.date_input(t("date_label"), key="manual_date")
    description = st.text_input(t("description_label"), key="manual_desc",
                                placeholder="e.g. Zomato dinner, Salary credited")
    amount      = st.number_input(t("amount_label"), min_value=0.0, step=100.0,
                                  format="%.2f", key="manual_amount")
    txn_type    = st.selectbox(t("type_label"), options=["expense", "income"],
                               format_func=lambda x: x.capitalize(), key="manual_type")

    if st.button(t("add_transaction"), use_container_width=True, key="btn_add"):
        if amount <= 0:
            st.error("Amount must be greater than zero.")
        elif not description.strip():
            st.error("Description is required.")
        else:
            insert_transaction(
                user_id=st.session_state.user_id,
                date=str(date),
                description=description.strip(),
                amount=amount,
                txn_type=txn_type,
            )
            st.success(t("transaction_added"))

# ---------------------------------------------------------------------------
# Section B — CSV Upload
# ---------------------------------------------------------------------------
with tab_csv:
    st.subheader(t("csv_upload"))
    st.write(
        "Upload a CSV file with the following columns: "
        "`date`, `description`, `amount`, `type`"
    )
    st.caption(
        "The `type` column must be either `income` or `expense`. "
        "The `date` column should be in YYYY-MM-DD format. "
        "The categorizer will automatically tag each transaction."
    )

    uploaded_file = st.file_uploader(t("upload_csv"), type=["csv"], key="csv_uploader")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            df.columns = [c.strip().lower() for c in df.columns]

            required = {"date", "description", "amount", "type"}
            if not required.issubset(set(df.columns)):
                st.error(t("csv_error"))
            else:
                df = df[list(required)].dropna(subset=["amount", "type"])
                df["type"] = df["type"].str.strip().str.lower()
                df = df[df["type"].isin(["income", "expense"])]

                if df.empty:
                    st.warning("No valid rows found after validation. Check your file.")
                else:
                    st.write(f"Preview — {len(df)} valid rows found:")
                    st.dataframe(df.head(10), use_container_width=True)

                    if st.button("Import All Transactions", use_container_width=True):
                        rows = df.to_dict(orient="records")
                        n = bulk_insert_transactions(st.session_state.user_id, rows)
                        st.success(t("csv_success", n=n))

        except Exception as e:
            st.error(f"Failed to read file: {str(e)}")

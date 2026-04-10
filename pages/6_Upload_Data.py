import streamlit as st
import pandas as pd
from utils.i18n import t
from utils.db import insert_transaction, bulk_insert_transactions
from utils.sidebar import render_sidebar
from utils.theme import inject_theme, page_title, section_header

# ── Auth guard ────────────────────────────────────────────────────────────────
# Demo mode: ensure session is always populated
if not st.session_state.get("logged_in"):
    st.session_state.logged_in        = True
    st.session_state.user_id          = 1
    st.session_state.username         = "demo"
    st.session_state.name             = "Arjun Mehta"
    st.session_state.employment_type  = "Salaried"
    st.session_state.income_bracket   = "10L - 15L"
    st.session_state.preferred_regime = "new"
    st.session_state.language         = "en"
    st.session_state.setup_complete   = 1
    st.session_state.chat_history     = []

inject_theme()
render_sidebar()

st.markdown(page_title("⬆", "Upload Data", "Add transactions manually or import via CSV"),
            unsafe_allow_html=True)

tab_manual, tab_csv = st.tabs(["  Manual Entry", "  CSV Import"])

# ── Manual entry ──────────────────────────────────────────────────────────────
with tab_manual:
    st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)
    st.markdown(section_header("Add a Transaction"), unsafe_allow_html=True)

    col_date, col_type = st.columns(2)
    with col_date:
        date = st.date_input(t("date_label"), key="manual_date")
    with col_type:
        txn_type = st.selectbox(t("type_label"), options=["expense", "income"],
                                format_func=lambda x: x.capitalize(), key="manual_type")

    description = st.text_input(t("description_label"), key="manual_desc",
                                placeholder="e.g. Zomato dinner, Salary credited, SIP Groww")
    amount = st.number_input(t("amount_label"), min_value=0.0, step=100.0,
                             format="%.2f", key="manual_amount")

    st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)
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
            st.success(f"  {txn_type.capitalize()} of Rs. {amount:,.2f} added and auto-categorised.")

# ── CSV Import ────────────────────────────────────────────────────────────────
with tab_csv:
    st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)
    st.markdown(section_header("Import CSV"), unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#171c27;border:1px solid #252d3d;border-radius:12px;
                padding:1rem 1.4rem;margin-bottom:1rem;">
        <p style="color:#9aaac4;font-size:13px;margin:0 0 .4rem 0;font-weight:600;">
            Required columns:
        </p>
        <code style="font-size:12px;color:#4f8ef7;">date, description, amount, type</code>
        <p style="color:#5a6a85;font-size:12px;margin:.5rem 0 0 0;">
            • <b>date</b> in YYYY-MM-DD format<br>
            • <b>type</b> must be <code>income</code> or <code>expense</code><br>
            • Transactions are automatically categorised from description
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(t("upload_csv"), type=["csv"], key="csv_uploader")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            df.columns = [c.strip().lower() for c in df.columns]

            required = {"date", "description", "amount", "type"}
            if not required.issubset(set(df.columns)):
                st.error(f"Missing columns. Required: {', '.join(required)}")
            else:
                df = df[list(required)].dropna(subset=["amount", "type"])
                df["type"] = df["type"].str.strip().str.lower()
                df = df[df["type"].isin(["income", "expense"])]

                if df.empty:
                    st.warning("No valid rows found after validation. Check your file.")
                else:
                    st.markdown(f"""
                    <div style="background:#0d1a33;border:1px solid #4f8ef7;border-radius:10px;
                                padding:.7rem 1.2rem;margin:.5rem 0;">
                        <span style="color:#4f8ef7;font-weight:700;">{len(df)}</span>
                        <span style="color:#9aaac4;font-size:13px;"> valid rows detected — preview below</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.dataframe(df.head(10), use_container_width=True)

                    st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)
                    if st.button("Import All Transactions →", use_container_width=True):
                        rows = df.to_dict(orient="records")
                        n = bulk_insert_transactions(st.session_state.user_id, rows)
                        st.success(t("csv_success", n=n))

        except Exception as e:
            st.error(f"Failed to read file: {str(e)}")

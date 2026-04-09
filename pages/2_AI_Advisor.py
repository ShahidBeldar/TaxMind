import streamlit as st
from utils.i18n import t
from utils.db import get_transactions
from utils.tax import calculate_tax
from utils.groq_client import chat

# ---------------------------------------------------------------------------
# Auth guard
# ---------------------------------------------------------------------------
if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()

# ---------------------------------------------------------------------------
# Build financial context for system prompt
# ---------------------------------------------------------------------------
def _build_context() -> dict:
    user_id = st.session_state.user_id
    txns    = get_transactions(user_id)

    total_income  = sum(r["amount"] for r in txns if r["type"] == "income")
    total_expense = sum(r["amount"] for r in txns if r["type"] == "expense")

    gross = total_income if total_income > 0 else 0
    tax_result = calculate_tax(
        gross,
        st.session_state.get("employment_type", "Salaried") or "Salaried",
        regime="new",
    )

    return {
        "name":            st.session_state.get("name", "User"),
        "employment_type": st.session_state.get("employment_type", "Not specified"),
        "income_bracket":  st.session_state.get("income_bracket", "Not specified"),
        "preferred_regime": st.session_state.get("preferred_regime", "new"),
        "total_income":    total_income,
        "total_expenses":  total_expense,
        "net_tax":         tax_result["total_tax_payable"],
    }


# ---------------------------------------------------------------------------
# Initialise chat history in session
# ---------------------------------------------------------------------------
if "chat_history" not in st.session_state or not isinstance(st.session_state.chat_history, list):
    st.session_state.chat_history = []

# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------
st.title(t("advisor_title"))
st.write("---")
st.caption(
    "Ask anything about Indian income tax, GST, ITR filing, advance tax, "
    "or investment options for FY 2026. Responses are AI-generated and "
    "should be verified with a qualified CA for legal compliance."
)

# Display existing conversation
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# New user input
user_input = st.chat_input(t("advisor_placeholder"))

if user_input:
    # Show user message immediately
    with st.chat_message("user"):
        st.write(user_input)

    # Append to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Call AI
    with st.chat_message("assistant"):
        with st.spinner(t("advisor_thinking")):
            try:
                context = _build_context()
                # Pass history excluding the latest user message (already appended above)
                prior_history = st.session_state.chat_history[:-1]
                reply = chat(user_input, prior_history, context)
                st.write(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
            except Exception as e:
                error_msg = t("advisor_error")
                st.error(f"{error_msg} Details: {str(e)}")

# Clear conversation button
if st.session_state.chat_history:
    st.write("")
    if st.button("Clear Conversation", use_container_width=False):
        st.session_state.chat_history = []
        st.rerun()

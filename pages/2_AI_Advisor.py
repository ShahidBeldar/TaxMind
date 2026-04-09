import streamlit as st
from utils.i18n import t
from utils.db import get_transactions
from utils.tax import calculate_tax
from utils.groq_client import chat
from utils.sidebar import render_sidebar
from utils.theme import inject_theme, page_title

# ── Auth guard ────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()

inject_theme()
render_sidebar()

# ── Context builder ───────────────────────────────────────────────────────────
def _build_context() -> dict:
    user_id = st.session_state.user_id
    txns    = get_transactions(user_id)
    total_income  = sum(r["amount"] for r in txns if r["type"] == "income")
    total_expense = sum(r["amount"] for r in txns if r["type"] == "expense")
    gross      = total_income if total_income > 0 else 0
    tax_result = calculate_tax(gross,
                               st.session_state.get("employment_type", "Salaried") or "Salaried",
                               regime="new")
    return {
        "name":             st.session_state.get("name", "User"),
        "employment_type":  st.session_state.get("employment_type", "Not specified"),
        "income_bracket":   st.session_state.get("income_bracket", "Not specified"),
        "preferred_regime": st.session_state.get("preferred_regime", "new"),
        "total_income":     total_income,
        "total_expenses":   total_expense,
        "net_tax":          tax_result["total_tax_payable"],
    }

# ── Chat history init ─────────────────────────────────────────────────────────
if "chat_history" not in st.session_state or not isinstance(st.session_state.chat_history, list):
    st.session_state.chat_history = []

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown(page_title("", "AI Tax Advisor",
    "Powered by Groq · Context-aware Indian tax advice for FY 2026"),
    unsafe_allow_html=True)

# ── Quick prompt chips ────────────────────────────────────────────────────────
st.markdown("""
<p style="color:#5a6a85;font-size:12px;letter-spacing:.04em;
           text-transform:uppercase;font-weight:600;margin-bottom:.5rem;">
    Quick questions
</p>
""", unsafe_allow_html=True)

quick_cols = st.columns(4)
quick_prompts = [
    "Should I choose old or new regime?",
    "How to save tax on salary income?",
    "When do I pay advance tax?",
    "Which ITR form should I file?",
]
for col, prompt in zip(quick_cols, quick_prompts):
    with col:
        if st.button(prompt, use_container_width=True, key=f"qp_{prompt[:10]}"):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            try:
                context = _build_context()
                prior   = st.session_state.chat_history[:-1]
                reply   = chat(prompt, prior, context)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"Error: {str(e)}"
                })
            st.rerun()

st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)

# ── Disclaimer ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#171c27;border:1px solid #252d3d;border-left:3px solid #ffab40;
            border-radius:10px;padding:.8rem 1.2rem;margin-bottom:1rem;">
    <span style="color:#ffab40;font-weight:600;font-size:12px;"> DISCLAIMER</span>
    <span style="color:#5a6a85;font-size:12px;margin-left:.5rem;">
        AI-generated advice. Verify with a qualified CA for legal compliance.
    </span>
</div>
""", unsafe_allow_html=True)

# ── Chat messages ─────────────────────────────────────────────────────────────
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ── Input ─────────────────────────────────────────────────────────────────────
user_input = st.chat_input(t("advisor_placeholder"))

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner(t("advisor_thinking")):
            try:
                context = _build_context()
                prior   = st.session_state.chat_history[:-1]
                reply   = chat(user_input, prior, context)
                st.write(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
            except Exception as e:
                error_msg = t("advisor_error")
                st.error(f"{error_msg} Details: {str(e)}")

# ── Clear button ──────────────────────────────────────────────────────────────
if st.session_state.chat_history:
    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
    _, c, _ = st.columns([3, 1, 3])
    with c:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

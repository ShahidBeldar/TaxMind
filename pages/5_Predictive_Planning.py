import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.i18n import t
from utils.db import get_monthly_totals
from utils.tax import calculate_tax, format_inr
from utils.theme import inject_theme, page_title, section_header, stat_card

# ── Auth guard ────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()

inject_theme()

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#9aaac4", size=12),
    margin=dict(l=8, r=8, t=36, b=8),
    legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0),
)

st.markdown(page_title("📈", "Predictive Planning",
    "Year-end projection based on your transaction history"),
    unsafe_allow_html=True)

monthly = get_monthly_totals(st.session_state.user_id)

if not monthly:
    st.markdown("""
    <div style="background:#171c27;border:1px dashed #252d3d;border-radius:16px;
                padding:3rem;text-align:center;margin-top:1rem;">
        <div style="font-size:2rem;margin-bottom:.6rem;">📊</div>
        <div style="font-family:'Syne',sans-serif;font-weight:700;color:#f0f4ff;">
            No transaction data yet
        </div>
        <p style="color:#5a6a85;font-size:13px;margin:.4rem 0 0 0;">
            Add transactions in Upload Data to see projections.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df = pd.DataFrame(monthly)
df["month"] = df["month"].astype(str)

employment_type       = st.session_state.get("employment_type", "Salaried") or "Salaried"
months_recorded       = len(df)
avg_monthly_income    = df["income"].mean()
avg_monthly_expense   = df["expense"].mean()
projected_annual_inc  = avg_monthly_income  * 12
projected_annual_exp  = avg_monthly_expense * 12
net_savings           = projected_annual_inc - projected_annual_exp
tax_result            = calculate_tax(projected_annual_inc, employment_type, regime="new")

# ── KPIs ──────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(stat_card("Projected Income", format_inr(projected_annual_inc),
                          f"Avg {format_inr(avg_monthly_income)}/mo", "var(--green)"),
                unsafe_allow_html=True)
with k2:
    st.markdown(stat_card("Projected Expenses", format_inr(projected_annual_exp),
                          f"Avg {format_inr(avg_monthly_expense)}/mo", "var(--red)"),
                unsafe_allow_html=True)
with k3:
    st.markdown(stat_card("Projected Tax", format_inr(tax_result["total_tax_payable"]),
                          "New regime FY 2026", "var(--amber)"), unsafe_allow_html=True)
with k4:
    eff = (tax_result["total_tax_payable"] / projected_annual_inc * 100) if projected_annual_inc else 0
    st.markdown(stat_card("Effective Rate", f"{eff:.1f}%",
                          "Of gross income", "var(--text-md)"), unsafe_allow_html=True)

st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

# ── Income vs Expense Line Chart ──────────────────────────────────────────────
st.markdown(section_header("Monthly Income vs Expenses",
    f"Based on {months_recorded} month(s) of recorded data"),
    unsafe_allow_html=True)

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(
    x=df["month"], y=df["income"],
    name="Income",
    mode="lines+markers",
    line=dict(color="#00e676", width=2.5),
    marker=dict(size=7, color="#00e676"),
    fill="tozeroy",
    fillcolor="rgba(0,230,118,0.07)",
    hovertemplate="<b>%{x}</b><br>Income: Rs. %{y:,.0f}<extra></extra>",
))
fig_line.add_trace(go.Scatter(
    x=df["month"], y=df["expense"],
    name="Expenses",
    mode="lines+markers",
    line=dict(color="#ff5252", width=2.5, dash="dot"),
    marker=dict(size=7, color="#ff5252"),
    fill="tozeroy",
    fillcolor="rgba(255,82,82,0.05)",
    hovertemplate="<b>%{x}</b><br>Expenses: Rs. %{y:,.0f}<extra></extra>",
))
fig_line.update_layout(
    **PLOTLY_LAYOUT, height=340,
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="#252d3d", tickformat=","),
    hovermode="x unified",
)
st.plotly_chart(fig_line, use_container_width=True)

# ── Net savings bar ───────────────────────────────────────────────────────────
st.markdown(section_header("Monthly Net Savings", "Income minus expenses"),
            unsafe_allow_html=True)

df["net"] = df["income"] - df["expense"]
bar_colors = ["#00e676" if v >= 0 else "#ff5252" for v in df["net"]]

fig_net = go.Figure(go.Bar(
    x=df["month"], y=df["net"],
    marker=dict(color=bar_colors, line=dict(width=0)),
    text=[f"Rs. {v:,.0f}" for v in df["net"]],
    textposition="outside",
    textfont=dict(size=10, color="#9aaac4"),
    hovertemplate="<b>%{x}</b><br>Net: Rs. %{y:,.0f}<extra></extra>",
))
fig_net.update_layout(
    **PLOTLY_LAYOUT, height=280,
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="#252d3d", tickformat=","),
)
st.plotly_chart(fig_net, use_container_width=True)

# ── Monthly data table ────────────────────────────────────────────────────────
st.markdown(section_header("Monthly Breakdown"), unsafe_allow_html=True)
display_df = df.rename(columns={"month": "Month", "income": "Income (Rs.)", "expense": "Expense (Rs.)"}).copy()
display_df["Net (Rs.)"] = display_df["Income (Rs.)"] - display_df["Expense (Rs.)"]
st.dataframe(display_df.set_index("Month"), use_container_width=True)

st.markdown(f"""
<p style="color:#5a6a85;font-size:12px;margin-top:.8rem;">
    Projection based on {months_recorded} month(s) of data.
    Add more transactions to improve accuracy.
</p>
""", unsafe_allow_html=True)

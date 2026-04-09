import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.i18n import t
from utils.db import get_monthly_totals
from utils.tax import calculate_tax, format_inr
from utils.theme import inject_theme, page_title, section_header, stat_card
from utils.sidebar import render_sidebar

if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()

inject_theme()
render_sidebar()

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#8899b8", size=12),
    margin=dict(l=8, r=8, t=40, b=8),
    legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0, font=dict(size=11)),
)

st.markdown(page_title("📈", "Predictive Planning",
    "Year-end projection based on your transaction history"), unsafe_allow_html=True)

monthly = get_monthly_totals(st.session_state.user_id)

if not monthly:
    st.markdown("""
    <div style="background:#111827;border:1px dashed #1e2a3d;border-radius:16px;
                padding:3rem;text-align:center;margin-top:1rem;">
        <div style="font-size:2rem;margin-bottom:.6rem;">📊</div>
        <div style="font-family:'Syne',sans-serif;font-weight:700;color:#edf2ff;">
            No transaction data yet
        </div>
        <p style="color:#4a5a72;font-size:13px;margin:.4rem 0 0 0;">
            Add transactions in Upload Data to see projections.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df = pd.DataFrame(monthly)
df["month"] = df["month"].astype(str)

employment_type     = st.session_state.get("employment_type", "Salaried") or "Salaried"
months_recorded     = len(df)
avg_monthly_income  = df["income"].mean()
avg_monthly_expense = df["expense"].mean()
projected_annual_inc = avg_monthly_income * 12
projected_annual_exp = avg_monthly_expense * 12
net_savings          = projected_annual_inc - projected_annual_exp
tax_result           = calculate_tax(projected_annual_inc, employment_type, regime="new")

# ── KPIs ──────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
eff = (tax_result["total_tax_payable"] / projected_annual_inc * 100) if projected_annual_inc else 0
with k1:
    st.markdown(stat_card("Projected Income", format_inr(projected_annual_inc),
                          f"Avg {format_inr(avg_monthly_income)}/mo", "var(--green)"), unsafe_allow_html=True)
with k2:
    st.markdown(stat_card("Projected Expenses", format_inr(projected_annual_exp),
                          f"Avg {format_inr(avg_monthly_expense)}/mo", "var(--red)"), unsafe_allow_html=True)
with k3:
    st.markdown(stat_card("Projected Tax", format_inr(tax_result["total_tax_payable"]),
                          "New regime FY 2026", "var(--amber)"), unsafe_allow_html=True)
with k4:
    st.markdown(stat_card("Effective Rate", f"{eff:.1f}%",
                          "Of gross income", "var(--blue)"), unsafe_allow_html=True)

st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

# ── Chart 1: Income vs Expense with area fill ──────────────────────────────────
st.markdown(section_header("Monthly Income vs Expenses",
    f"Based on {months_recorded} month(s) of recorded data"), unsafe_allow_html=True)

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(
    x=df["month"], y=df["income"],
    name="Income",
    mode="lines+markers",
    line=dict(color="#00e676", width=2.5),
    marker=dict(size=8, color="#00e676", line=dict(color="#0b0f1a", width=2)),
    fill="tozeroy",
    fillcolor="rgba(0,230,118,0.07)",
    hovertemplate="<b>%{x}</b><br>Income: Rs. %{y:,.0f}<extra></extra>",
))
fig_line.add_trace(go.Scatter(
    x=df["month"], y=df["expense"],
    name="Expenses",
    mode="lines+markers",
    line=dict(color="#ff5252", width=2.5, dash="dot"),
    marker=dict(size=8, color="#ff5252", line=dict(color="#0b0f1a", width=2)),
    fill="tozeroy",
    fillcolor="rgba(255,82,82,0.05)",
    hovertemplate="<b>%{x}</b><br>Expenses: Rs. %{y:,.0f}<extra></extra>",
))
# Projected average line
fig_line.add_hline(
    y=avg_monthly_income, line_dash="dot",
    line_color="#00e676", line_width=1, opacity=0.4,
    annotation_text=f"Avg income: {format_inr(avg_monthly_income)}",
    annotation_font=dict(size=10, color="#4a5a72"),
)
fig_line.update_layout(
    **PLOTLY_LAYOUT, height=340,
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="#1e2a3d", tickformat=","),
    hovermode="x unified",
)
st.plotly_chart(fig_line, use_container_width=True)

# ── Chart 2: Net savings bar + cumulative savings line ────────────────────────
ch3, ch4 = st.columns(2)

with ch3:
    st.markdown(section_header("Monthly Net Savings", "Income minus expenses"), unsafe_allow_html=True)
    df["net"] = df["income"] - df["expense"]
    bar_colors = ["#00e676" if v >= 0 else "#ff5252" for v in df["net"]]

    fig_net = go.Figure(go.Bar(
        x=df["month"], y=df["net"],
        marker=dict(color=bar_colors, line=dict(width=0), cornerradius=4),
        text=[f"Rs.{v:,.0f}" for v in df["net"]],
        textposition="outside",
        textfont=dict(size=10, color="#8899b8", family="DM Mono"),
        hovertemplate="<b>%{x}</b><br>Net: Rs. %{y:,.0f}<extra></extra>",
    ))
    fig_net.update_layout(
        **PLOTLY_LAYOUT, height=280,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#1e2a3d", tickformat=","),
        showlegend=False,
    )
    st.plotly_chart(fig_net, use_container_width=True)

with ch4:
    st.markdown(section_header("Cumulative Savings", "Running total over time"), unsafe_allow_html=True)
    df["cumulative"] = df["net"].cumsum()
    cum_color = "#00e676" if df["cumulative"].iloc[-1] >= 0 else "#ff5252"
    cum_fill  = "rgba(0,230,118,0.07)" if df["cumulative"].iloc[-1] >= 0 else "rgba(255,82,82,0.07)"

    fig_cum = go.Figure(go.Scatter(
        x=df["month"], y=df["cumulative"],
        mode="lines+markers",
        line=dict(color=cum_color, width=2.5),
        marker=dict(size=7, color=cum_color, line=dict(color="#0b0f1a", width=2)),
        fill="tozeroy",
        fillcolor=cum_fill,
        hovertemplate="<b>%{x}</b><br>Cumulative: Rs. %{y:,.0f}<extra></extra>",
    ))
    fig_cum.update_layout(
        **PLOTLY_LAYOUT, height=280,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#1e2a3d", tickformat=","),
        showlegend=False,
    )
    st.plotly_chart(fig_cum, use_container_width=True)

# ── Monthly breakdown table ────────────────────────────────────────────────────
st.markdown(section_header("Monthly Breakdown"), unsafe_allow_html=True)
display_df = df.rename(columns={"month": "Month", "income": "Income (Rs.)", "expense": "Expense (Rs.)"}).copy()
display_df["Net (Rs.)"]        = display_df["Income (Rs.)"] - display_df["Expense (Rs.)"]
display_df["Cumulative (Rs.)"] = display_df["Net (Rs.)"].cumsum()
st.dataframe(display_df.set_index("Month"), use_container_width=True)

st.markdown(f"""
<p style="color:#4a5a72;font-size:11.5px;margin-top:.8rem;font-family:'DM Mono',monospace;">
    Projection based on {months_recorded} month(s) of data · Add more transactions to improve accuracy.
</p>
""", unsafe_allow_html=True)

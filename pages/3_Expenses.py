import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.i18n import t
from utils.db import get_transactions
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

PALETTE = ["#4f8ef7","#3a75e0","#ffab40","#ff5252","#40c4ff",
           "#ea80fc","#ff80ab","#b9f6ca","#ffd180","#84ffff"]

st.markdown(page_title("", "Expenses", "Auto-categorised spend overview"), unsafe_allow_html=True)

expenses = get_transactions(st.session_state.user_id, txn_type="expense")

if not expenses:
    st.markdown("""
    <div style="background:#111827;border:1px dashed #1e2a3d;border-radius:16px;
                padding:3rem;text-align:center;margin-top:1rem;">
        <div style="font-size:2rem;margin-bottom:.6rem;"></div>
        <div style="font-family:'Syne',sans-serif;font-weight:700;color:#edf2ff;">
            No expense transactions yet
        </div>
        <p style="color:#4a5a72;font-size:13px;margin:.4rem 0 0 0;">
            Go to Upload Data to add or import transactions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df = pd.DataFrame(expenses)
total_expense  = df["amount"].sum()
category_totals = df.groupby("category")["amount"].sum().sort_values(ascending=False)
top_category    = category_totals.index[0] if len(category_totals) else "—"

# ── KPIs ──────────────────────────────────────────────────────────────────────
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(stat_card("Total Spent", f"Rs. {total_expense:,.0f}", "All time", "var(--red)"), unsafe_allow_html=True)
with k2:
    st.markdown(stat_card("Categories", str(len(category_totals)), "Detected", "var(--navy)"), unsafe_allow_html=True)
with k3:
    st.markdown(stat_card("Top Category", top_category, f"Rs. {category_totals.iloc[0]:,.0f}", "var(--amber)"), unsafe_allow_html=True)

st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

# ── Row 1: Donut + Treemap ─────────────────────────────────────────────────────
ch1, ch2 = st.columns(2)

with ch1:
    st.markdown(section_header("Spend by Category", "Donut breakdown"), unsafe_allow_html=True)
    cat_df = category_totals.reset_index()
    cat_df.columns = ["Category", "Amount"]

    fig_pie = go.Figure(go.Pie(
        labels=cat_df["Category"], values=cat_df["Amount"],
        hole=.58,
        marker=dict(colors=PALETTE[:len(cat_df)], line=dict(color="#0b0f1a", width=3)),
        textinfo="percent+label",
        textfont=dict(size=11, color="#edf2ff", family="DM Mono"),
        hovertemplate="<b>%{label}</b><br>Rs. %{value:,.0f}  (%{percent})<extra></extra>",
    ))
    fig_pie.update_layout(
        **PLOTLY_LAYOUT, height=320,
        showlegend=False,
        annotations=[dict(
            text=f"Rs.<br><b>{total_expense:,.0f}</b>",
            x=0.5, y=0.5,
            font=dict(size=13, color="#edf2ff", family="DM Mono"), showarrow=False,
        )],
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with ch2:
    st.markdown(section_header("Category Bars", "Spend per category"), unsafe_allow_html=True)
    cat_sorted = category_totals.sort_values()
    n = len(cat_sorted)
    bar_colors = PALETTE[:n][::-1] if n <= len(PALETTE) else ["#4f8ef7"] * n

    fig_bar = go.Figure(go.Bar(
        x=cat_sorted.values,
        y=cat_sorted.index,
        orientation="h",
        marker=dict(color=bar_colors, line=dict(width=0), cornerradius=4),
        text=[f"Rs. {v:,.0f}" for v in cat_sorted.values],
        textposition="outside",
        textfont=dict(size=10, color="#8899b8", family="DM Mono"),
        hovertemplate="<b>%{y}</b><br>Rs. %{x:,.0f}<extra></extra>",
    ))
    fig_bar.update_layout(
        **PLOTLY_LAYOUT, height=320,
        xaxis=dict(showgrid=True, gridcolor="#1e2a3d", tickformat=","),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Row 2: Monthly trend (if date column available) ────────────────────────────
if "date" in df.columns:
    try:
        df["date_parsed"] = pd.to_datetime(df["date"], errors="coerce")
        df["month"] = df["date_parsed"].dt.to_period("M").astype(str)
        monthly_exp = df.groupby("month")["amount"].sum().reset_index()
        monthly_exp.columns = ["Month", "Amount"]

        if len(monthly_exp) > 1:
            st.markdown(section_header("Monthly Spend Trend", "Total expenses per calendar month"), unsafe_allow_html=True)

            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=monthly_exp["Month"], y=monthly_exp["Amount"],
                mode="lines+markers",
                line=dict(color="#ff5252", width=2.5),
                marker=dict(size=8, color="#ff5252",
                            line=dict(color="#0b0f1a", width=2)),
                fill="tozeroy",
                fillcolor="rgba(255,82,82,0.06)",
                hovertemplate="<b>%{x}</b><br>Spent: Rs. %{y:,.0f}<extra></extra>",
            ))

            # Rolling average
            if len(monthly_exp) >= 3:
                monthly_exp["rolling"] = monthly_exp["Amount"].rolling(window=3, min_periods=1).mean()
                fig_trend.add_trace(go.Scatter(
                    x=monthly_exp["Month"], y=monthly_exp["rolling"],
                    mode="lines",
                    name="3-mo avg",
                    line=dict(color="#ffab40", width=1.5, dash="dot"),
                    hovertemplate="3-mo avg: Rs. %{y:,.0f}<extra></extra>",
                ))

            fig_trend.update_layout(
                **PLOTLY_LAYOUT, height=280,
                xaxis=dict(showgrid=False, tickfont=dict(size=10)),
                yaxis=dict(showgrid=True, gridcolor="#1e2a3d", tickformat=","),
                hovermode="x unified",
                showlegend=True,
            )
            st.plotly_chart(fig_trend, use_container_width=True)
    except Exception:
        pass

# ── Category table ─────────────────────────────────────────────────────────────
st.markdown(section_header("Category Summary"), unsafe_allow_html=True)
cat_table = category_totals.reset_index()
cat_table.columns = ["Category", "Total (Rs.)"]
cat_table["Share %"] = (cat_table["Total (Rs.)"] / total_expense * 100).round(1).astype(str) + "%"
st.table(cat_table.set_index("Category"))

# ── Full transaction list ──────────────────────────────────────────────────────
st.markdown(section_header("All Transactions", "Sorted by date, newest first"), unsafe_allow_html=True)
display_df = df[["date", "description", "amount", "category"]].copy()
display_df.columns = ["Date", "Description", "Amount (Rs.)", "Category"]
display_df = display_df.sort_values("Date", ascending=False).reset_index(drop=True)
st.dataframe(display_df, use_container_width=True, height=340)

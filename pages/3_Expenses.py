import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.i18n import t
from utils.db import get_transactions
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

GREEN_SCALE = [
    [0.0,  "#0d2018"],
    [0.25, "#0f3022"],
    [0.5,  "#00b85c"],
    [0.75, "#00cc66"],
    [1.0,  "#00e676"],
]

st.markdown(page_title("💳", "Expenses", "Auto-categorised spend overview"),
            unsafe_allow_html=True)

expenses = get_transactions(st.session_state.user_id, txn_type="expense")

if not expenses:
    st.markdown("""
    <div style="background:#171c27;border:1px dashed #252d3d;border-radius:16px;
                padding:3rem;text-align:center;margin-top:1rem;">
        <div style="font-size:2rem;margin-bottom:.6rem;">💸</div>
        <div style="font-family:'Syne',sans-serif;font-weight:700;color:#f0f4ff;">
            No expense transactions yet
        </div>
        <p style="color:#5a6a85;font-size:13px;margin:.4rem 0 0 0;">
            Go to Upload Data to add or import transactions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df = pd.DataFrame(expenses)
total_expense = df["amount"].sum()
category_totals = df.groupby("category")["amount"].sum().sort_values(ascending=False)
top_category   = category_totals.index[0] if len(category_totals) else "—"

# ── KPIs ──────────────────────────────────────────────────────────────────────
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(stat_card("Total Spent", f"Rs. {total_expense:,.0f}",
                          "All time", "var(--red)"), unsafe_allow_html=True)
with k2:
    st.markdown(stat_card("Categories", str(len(category_totals)),
                          "Detected", "var(--green)"), unsafe_allow_html=True)
with k3:
    st.markdown(stat_card("Top Category", top_category,
                          f"Rs. {category_totals.iloc[0]:,.0f}", "var(--amber)"),
                unsafe_allow_html=True)

st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

# ── Two charts side by side ───────────────────────────────────────────────────
ch1, ch2 = st.columns(2)

with ch1:
    st.markdown(section_header("Spend by Category", "Donut breakdown"),
                unsafe_allow_html=True)
    cat_df = category_totals.reset_index()
    cat_df.columns = ["Category", "Amount"]

    palette = ["#00e676","#00b85c","#ffab40","#ff5252","#40c4ff",
               "#ea80fc","#ff80ab","#b9f6ca","#ffd180","#84ffff"]

    fig_pie = go.Figure(go.Pie(
        labels=cat_df["Category"], values=cat_df["Amount"],
        hole=.55,
        marker=dict(colors=palette[:len(cat_df)],
                    line=dict(color="#0f1117", width=3)),
        textinfo="percent+label",
        textfont=dict(size=11, color="#f0f4ff"),
        hovertemplate="<b>%{label}</b><br>Rs. %{value:,.0f}<br>%{percent}<extra></extra>",
    ))
    fig_pie.update_layout(
        **PLOTLY_LAYOUT, height=320,
        showlegend=False,
        annotations=[dict(
            text=f"Rs.<br><b>{total_expense:,.0f}</b>",
            x=0.5, y=0.5,
            font=dict(size=13, color="#f0f4ff"), showarrow=False,
        )],
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with ch2:
    st.markdown(section_header("Horizontal Bar", "Spend per category"),
                unsafe_allow_html=True)
    cat_sorted = category_totals.sort_values()
    fig_bar = go.Figure(go.Bar(
        x=cat_sorted.values,
        y=cat_sorted.index,
        orientation="h",
        marker=dict(
            color=cat_sorted.values,
            colorscale=GREEN_SCALE,
            showscale=False,
            line=dict(width=0),
        ),
        text=[f"Rs. {v:,.0f}" for v in cat_sorted.values],
        textposition="outside",
        textfont=dict(size=10, color="#9aaac4"),
        hovertemplate="<b>%{y}</b><br>Rs. %{x:,.0f}<extra></extra>",
    ))
    fig_bar.update_layout(
        **PLOTLY_LAYOUT, height=320,
        xaxis=dict(showgrid=True, gridcolor="#252d3d", tickformat=","),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Category table ────────────────────────────────────────────────────────────
st.markdown(section_header("Category Summary"), unsafe_allow_html=True)
cat_table = category_totals.reset_index()
cat_table.columns = ["Category", "Total (Rs.)"]
cat_table["Share %"] = (cat_table["Total (Rs.)"] / total_expense * 100).round(1).astype(str) + "%"
st.table(cat_table.set_index("Category"))

# ── Full transaction list ─────────────────────────────────────────────────────
st.markdown(section_header("All Transactions", "Sorted by date, newest first"),
            unsafe_allow_html=True)
display_df = df[["date", "description", "amount", "category"]].copy()
display_df.columns = ["Date", "Description", "Amount (Rs.)", "Category"]
display_df = display_df.sort_values("Date", ascending=False).reset_index(drop=True)
st.dataframe(display_df, use_container_width=True, height=340)

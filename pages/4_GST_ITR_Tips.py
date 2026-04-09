import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.i18n import t
from utils.theme import inject_theme, page_title, section_header, card

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
)

st.markdown(page_title("📋", "GST & ITR Tips",
    "Deadlines · Penalties · Regime comparison · GST slabs"),
    unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 1 — Advance Tax Timeline (visual)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(section_header("Advance Tax Installment Timeline — FY 2026",
    "Visual reminder of cumulative payment milestones"),
    unsafe_allow_html=True)

installments = [
    {"label": "1st Instalment",  "date": "15 Jun 2025",  "pct": 15,  "month_num": 3},
    {"label": "2nd Instalment",  "date": "15 Sep 2025",  "pct": 45,  "month_num": 6},
    {"label": "3rd Instalment",  "date": "15 Dec 2025",  "pct": 75,  "month_num": 9},
    {"label": "4th Instalment",  "date": "15 Mar 2026",  "pct": 100, "month_num": 12},
]

colors_bar = ["#1d3a2a", "#00804a", "#00b85c", "#00e676"]

fig_timeline = go.Figure()

# Background track
fig_timeline.add_trace(go.Bar(
    x=[12, 12, 12, 12],
    y=[d["label"] for d in installments],
    orientation="h",
    marker=dict(color="#1d2333", line=dict(width=0)),
    showlegend=False, hoverinfo="skip",
))

# Progress bars
for i, inst in enumerate(installments):
    fig_timeline.add_trace(go.Bar(
        x=[inst["month_num"]],
        y=[inst["label"]],
        orientation="h",
        marker=dict(color=colors_bar[i], line=dict(width=0)),
        text=[f"  {inst['pct']}% by {inst['date']}"],
        textposition="inside",
        insidetextanchor="start",
        textfont=dict(size=12, color="#f0f4ff"),
        showlegend=False,
        hovertemplate=f"<b>{inst['label']}</b><br>{inst['pct']}% due by {inst['date']}<extra></extra>",
    ))

fig_timeline.update_layout(
    **PLOTLY_LAYOUT,
    barmode="overlay",
    height=260,
    xaxis=dict(
        range=[0, 13],
        showgrid=False,
        tickvals=list(range(1, 13)),
        ticktext=["Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar"],
        color="#5a6a85",
    ),
    yaxis=dict(showgrid=False, autorange="reversed"),
)
st.plotly_chart(fig_timeline, use_container_width=True)

st.markdown("""
<p style="color:#5a6a85;font-size:12px;margin-top:-.5rem;">
    Advance tax applies when estimated annual tax liability &gt; Rs. 10,000.
    Salaried individuals fully covered by TDS are generally exempt.
</p>
""", unsafe_allow_html=True)

# ── Deadline table ────────────────────────────────────────────────────────────
deadlines_df = pd.DataFrame([
    {"Installment": "1st",  "Due Date": "15 June 2025",      "Min % of Tax Due": "15%"},
    {"Installment": "2nd",  "Due Date": "15 September 2025", "Min % of Tax Due": "45%"},
    {"Installment": "3rd",  "Due Date": "15 December 2025",  "Min % of Tax Due": "75%"},
    {"Installment": "4th",  "Due Date": "15 March 2026",     "Min % of Tax Due": "100%"},
])
st.table(deadlines_df.set_index("Installment"))

# ══════════════════════════════════════════════════════════════════════════════
# 2 — Penalty sections
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<hr style='border-color:#252d3d;margin:1.5rem 0;'>", unsafe_allow_html=True)
st.markdown(section_header("Interest Penalties", "Sections 234B and 234C"),
            unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(card("""
    <div style="color:#00e676;font-weight:700;font-size:13px;margin-bottom:.6rem;">
        Section 234B — Default in Advance Tax
    </div>
    <p style="color:#9aaac4;font-size:13px;margin:0 0 .6rem 0;">
        Applies when less than 90% of assessed tax is paid by 31 March
        through advance tax and TDS combined.
    </p>
    <p style="color:#9aaac4;font-size:13px;margin:0 0 .5rem 0;">
        <b style="color:#f0f4ff;">Rate:</b> 1% per month on the shortfall.
    </p>
    <code style="font-size:11px;background:#0f1117;padding:.4rem .7rem;
                 border-radius:6px;display:block;color:#00e676;">
        Interest = 1% × Shortfall × Months
    </code>
    """), unsafe_allow_html=True)

with col2:
    st.markdown(card("""
    <div style="color:#00e676;font-weight:700;font-size:13px;margin-bottom:.6rem;">
        Section 234C — Deferred Installments
    </div>
    <p style="color:#9aaac4;font-size:13px;margin:0 0 .6rem 0;">
        Applies when each installment falls short of the required cumulative
        percentage.
    </p>
    <p style="color:#9aaac4;font-size:13px;margin:0 0 .5rem 0;">
        <b style="color:#f0f4ff;">Rate:</b> 1% per month for 3 months on the shortfall
        (last installment: 1 month).
    </p>
    <code style="font-size:11px;background:#0f1117;padding:.4rem .7rem;
                 border-radius:6px;display:block;color:#00e676;">
        Interest = 1% × Shortfall × 3 months
    </code>
    """), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 3 — New Regime savings
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<hr style='border-color:#252d3d;margin:1.5rem 0;'>", unsafe_allow_html=True)
st.markdown(section_header("Tax Saving Under New Regime — FY 2026",
    "Valid avenues under the new regime"), unsafe_allow_html=True)

savings = pd.DataFrame([
    {"Option": "Standard Deduction",     "Section": "16(ia)",    "Benefit": "Rs. 75,000 deduction from gross salary",           "Eligible For": "Salaried only"},
    {"Option": "Employer NPS",           "Section": "80CCD(2)",  "Benefit": "Up to 14% of basic (govt) / 10% (others)",        "Eligible For": "Salaried with employer NPS"},
    {"Option": "Agniveer Corpus Fund",   "Section": "80CCH",     "Benefit": "Full deduction on contribution",                   "Eligible For": "Agniveer scheme"},
    {"Option": "Family Pension",         "Section": "57(iia)",   "Benefit": "Lower of Rs. 25,000 or 1/3rd of pension",         "Eligible For": "Family pension recipients"},
    {"Option": "Section 87A Rebate",     "Section": "87A",       "Benefit": "Full rebate up to Rs. 60,000 (income ≤ 12L)",     "Eligible For": "All individuals (new regime)"},
])
st.table(savings.set_index("Option"))

st.info("Note: 80C, 80D, HRA, and home loan interest (Sec 24) are NOT available under the new regime.")

# ══════════════════════════════════════════════════════════════════════════════
# 4 — GST
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<hr style='border-color:#252d3d;margin:1.5rem 0;'>", unsafe_allow_html=True)
st.markdown(section_header("GST — Registration Thresholds & Rate Slabs"),
            unsafe_allow_html=True)

g1, g2 = st.columns(2)
with g1:
    st.markdown("**Mandatory Registration**")
    thresholds = pd.DataFrame([
        {"Business Type": "Goods — general states",       "Threshold": "Rs. 40 Lakh"},
        {"Business Type": "Goods — special category",     "Threshold": "Rs. 20 Lakh"},
        {"Business Type": "Services — all states",        "Threshold": "Rs. 20 Lakh"},
        {"Business Type": "Inter-state supply",           "Threshold": "Mandatory"},
        {"Business Type": "E-commerce operators",         "Threshold": "Mandatory"},
    ])
    st.table(thresholds.set_index("Business Type"))

with g2:
    st.markdown("**GST Rate Slabs**")
    gst_slabs = pd.DataFrame([
        {"Rate": "0%",  "Applicable To": "Grains, milk, eggs, fresh vegetables"},
        {"Rate": "5%",  "Applicable To": "Packaged food, footwear < Rs. 1,000"},
        {"Rate": "12%", "Applicable To": "Processed food, computers"},
        {"Rate": "18%", "Applicable To": "Most services, IT, AC restaurants"},
        {"Rate": "28%", "Applicable To": "Luxury items, tobacco, automobiles"},
    ])
    st.table(gst_slabs.set_index("Rate"))

# ══════════════════════════════════════════════════════════════════════════════
# 5 — ITR Form Selector
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<hr style='border-color:#252d3d;margin:1.5rem 0;'>", unsafe_allow_html=True)
st.markdown(section_header("ITR Form Selection Guide"), unsafe_allow_html=True)

itr_forms = pd.DataFrame([
    {"ITR Form": "ITR-1 (Sahaj)",  "Who Should File": "Salaried, one house property, income ≤ Rs. 50L"},
    {"ITR Form": "ITR-2",          "Who Should File": "Capital gains, foreign income, multiple house properties"},
    {"ITR Form": "ITR-3",          "Who Should File": "Business or professional income (proprietorship)"},
    {"ITR Form": "ITR-4 (Sugam)",  "Who Should File": "Presumptive income u/s 44AD, 44ADA, 44AE"},
    {"ITR Form": "ITR-5",          "Who Should File": "Partnership firms, LLPs"},
    {"ITR Form": "ITR-6",          "Who Should File": "Companies (non-section 11 exemption)"},
])
st.table(itr_forms.set_index("ITR Form"))

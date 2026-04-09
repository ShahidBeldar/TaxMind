import streamlit as st
import pandas as pd
import io
import plotly.graph_objects as go
import plotly.express as px
from utils.i18n import t
from utils.tax import calculate_tax, slab_breakdown, format_inr
from utils.theme import inject_theme, page_title, stat_card, section_header

# ── Auth guard ────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()

inject_theme()

# ── Plotly dark template ──────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#9aaac4", size=12),
    margin=dict(l=8, r=8, t=36, b=8),
    legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0),
)

# ── PDF export ────────────────────────────────────────────────────────────────
def build_pdf(result: dict, slabs: list[dict], employment_type: str) -> bytes:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                    Paragraph, Spacer)
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("TaxMind AI", styles["Title"]))
    elements.append(Paragraph("Tax Computation Summary — FY 2026 (New Regime)", styles["Heading2"]))
    elements.append(Spacer(1, 0.4*cm))
    elements.append(Paragraph(f"Employment Type: {employment_type}", styles["Normal"]))
    elements.append(Spacer(1, 0.4*cm))

    summary_data = [
        ["Description", "Amount (Rs.)"],
        ["Gross Income",          f"{result['gross_income']:,.0f}"],
        ["Standard Deduction",    f"{result['standard_deduction']:,.0f}"],
        ["Taxable Income",        f"{result['taxable_income']:,.0f}"],
        ["Tax Before Rebate",     f"{result['tax_before_rebate']:,.0f}"],
        ["Rebate u/s 87A",        f"({result['rebate_87a']:,.0f})"],
        ["Tax After Rebate",      f"{result['tax_after_rebate']:,.0f}"],
        ["Health & Education Cess (4%)", f"{result['cess']:,.0f}"],
        ["Total Tax Payable",     f"{result['total_tax_payable']:,.0f}"],
    ]
    tbl = Table(summary_data, colWidths=[10*cm, 6*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#171c27")),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN",        (1, 0), (1, -1), "RIGHT"),
        ("FONTNAME",     (0, -1), (-1, -1), "Helvetica-Bold"),
    ]))
    elements.append(tbl)
    elements.append(Spacer(1, 0.6*cm))
    elements.append(Paragraph("Slab-wise Breakdown", styles["Heading3"]))
    elements.append(Spacer(1, 0.2*cm))

    slab_data = [["Slab", "Rate", "Income in Slab (Rs.)", "Tax (Rs.)"]]
    for row in slabs:
        slab_data.append([
            row["Slab"], row["Rate"],
            f"{row['Income in Slab (Rs.)']:,.0f}",
            f"{row['Tax (Rs.)']:,.0f}",
        ])
    slab_tbl = Table(slab_data, colWidths=[7*cm, 2*cm, 4*cm, 3*cm])
    slab_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#171c27")),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN",        (1, 0), (-1, -1), "RIGHT"),
    ]))
    elements.append(slab_tbl)
    doc.build(elements)
    return buffer.getvalue()


# ── Page ──────────────────────────────────────────────────────────────────────
st.markdown(page_title("📊", "Tax Dashboard",
    f"Employment: {st.session_state.get('employment_type','Salaried')} · "
    f"Regime: {'New' if st.session_state.get('preferred_regime','new') == 'new' else 'Old'}"),
    unsafe_allow_html=True)

employment_type  = st.session_state.get("employment_type", "Salaried") or "Salaried"
preferred_regime = st.session_state.get("preferred_regime", "new") or "new"

col_in, col_btn = st.columns([3, 1])
with col_in:
    gross_income = st.number_input(
        t("gross_income_label"),
        min_value=0, max_value=100_000_000, value=0, step=10_000, format="%d",
    )
with col_btn:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    calc_clicked = st.button(t("calculate_btn"), use_container_width=True)

# ── Results ───────────────────────────────────────────────────────────────────
if calc_clicked and gross_income > 0:
    result = calculate_tax(gross_income, employment_type, regime="new")
    slabs  = slab_breakdown(result["taxable_income"])

    # ── Top KPI strip ─────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    kpis = [
        ("Gross Income",    format_inr(result["gross_income"]),    "Before deductions",    "var(--text-md)"),
        ("Taxable Income",  format_inr(result["taxable_income"]),  "After std. deduction", "var(--amber)"),
        ("Tax Payable",     format_inr(result["total_tax_payable"]),"Incl. 4% cess",       "var(--red)"),
        ("Effective Rate",
         f"{(result['total_tax_payable']/gross_income*100):.1f}%",
         "of gross income", "var(--green)"),
    ]
    for col, (lbl, val, sub, accent) in zip([k1, k2, k3, k4], kpis):
        with col:
            st.markdown(stat_card(lbl, val, sub, accent), unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # ── Two-column: Donut + Slab bar ─────────────────────────────────────────
    ch1, ch2 = st.columns(2)

    with ch1:
        st.markdown(section_header("Tax Composition", "How your tax breaks down"),
                    unsafe_allow_html=True)
        donut_labels = ["Take-Home Income", "Tax After Rebate", "Cess"]
        donut_values = [
            result["gross_income"] - result["total_tax_payable"],
            result["tax_after_rebate"],
            result["cess"],
        ]
        donut_colors = ["#00e676", "#ff5252", "#ffab40"]
        fig_donut = go.Figure(go.Pie(
            labels=donut_labels, values=donut_values,
            hole=.62,
            marker=dict(colors=donut_colors,
                        line=dict(color="#0f1117", width=3)),
            textinfo="percent",
            textfont=dict(size=13, color="#f0f4ff"),
            hovertemplate="<b>%{label}</b><br>Rs. %{value:,.0f}<extra></extra>",
        ))
        fig_donut.update_layout(
            **PLOTLY_LAYOUT,
            showlegend=True,
            legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center",
                        font=dict(size=11, color="#9aaac4")),
            annotations=[dict(
                text=f"Rs.<br><b>{result['total_tax_payable']:,.0f}</b>",
                x=0.5, y=0.5, font=dict(size=14, color="#f0f4ff"), showarrow=False,
            )],
            height=300,
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with ch2:
        st.markdown(section_header("Slab-wise Tax", "Tax computed per income bracket"),
                    unsafe_allow_html=True)
        if slabs:
            slab_df = pd.DataFrame(slabs)
            short_labels = [s.split(" to ")[-1].replace("Above ", ">").replace("Up to ", "≤")
                            for s in slab_df["Slab"]]
            fig_slab = go.Figure(go.Bar(
                x=short_labels,
                y=slab_df["Tax (Rs.)"],
                marker=dict(
                    color=slab_df["Tax (Rs.)"],
                    colorscale=[[0, "#1d3a2a"], [1, "#00e676"]],
                    showscale=False,
                    line=dict(width=0),
                ),
                text=[f"Rs.{v:,.0f}" for v in slab_df["Tax (Rs.)"]],
                textposition="outside",
                textfont=dict(size=10, color="#9aaac4"),
                hovertemplate="<b>%{x}</b><br>Tax: Rs. %{y:,.0f}<extra></extra>",
            ))
            fig_slab.update_layout(
                **PLOTLY_LAYOUT,
                height=300,
                xaxis=dict(showgrid=False, tickfont=dict(size=10)),
                yaxis=dict(showgrid=True, gridcolor="#252d3d", tickformat=","),
            )
            st.plotly_chart(fig_slab, use_container_width=True)

    # ── Detailed breakdown table ──────────────────────────────────────────────
    st.markdown(section_header("Full Breakdown"), unsafe_allow_html=True)
    summary_rows = {
        t("gross_income"):      format_inr(result["gross_income"]),
        t("standard_deduction"): format_inr(result["standard_deduction"]),
        t("taxable_income"):    format_inr(result["taxable_income"]),
        t("tax_before_rebate"): format_inr(result["tax_before_rebate"]),
        t("rebate_87a"):        f"({format_inr(result['rebate_87a'])})",
        t("tax_after_rebate"):  format_inr(result["tax_after_rebate"]),
        t("cess"):              format_inr(result["cess"]),
        t("total_tax_payable"): format_inr(result["total_tax_payable"]),
    }
    summary_df = pd.DataFrame(list(summary_rows.items()), columns=["Description", "Amount"])
    st.table(summary_df.set_index("Description"))

    # ── Slab table ────────────────────────────────────────────────────────────
    if slabs:
        st.markdown(section_header("Slab Breakdown"), unsafe_allow_html=True)
        st.table(pd.DataFrame(slabs).set_index("Slab"))

    # ── Exports ───────────────────────────────────────────────────────────────
    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
    col_pdf, col_csv, _ = st.columns([1, 1, 2])
    with col_pdf:
        pdf_bytes = build_pdf(result, slabs, employment_type)
        st.download_button(label=t("export_pdf"), data=pdf_bytes,
                           file_name="taxmind_computation_fy2026.pdf",
                           mime="application/pdf", use_container_width=True)
    with col_csv:
        csv_df    = pd.DataFrame(list(summary_rows.items()), columns=["Description", "Amount"])
        csv_bytes = csv_df.to_csv(index=False).encode("utf-8")
        st.download_button(label=t("export_csv"), data=csv_bytes,
                           file_name="taxmind_computation_fy2026.csv",
                           mime="text/csv", use_container_width=True)

elif calc_clicked and gross_income == 0:
    st.warning("Please enter a gross income greater than zero.")
else:
    # Empty-state hint
    st.markdown("""
    <div style="
        background:#171c27;border:1px dashed #252d3d;border-radius:16px;
        padding:2.5rem;text-align:center;margin-top:1rem;
    ">
        <div style="font-size:2rem;margin-bottom:.6rem;">📥</div>
        <div style="font-family:'Syne',sans-serif;font-weight:700;color:#f0f4ff;font-size:1rem;">
            Enter your gross income above
        </div>
        <p style="color:#5a6a85;font-size:13px;margin:.4rem 0 0 0;">
            Get an instant slab-wise breakdown with charts and PDF export.
        </p>
    </div>
    """, unsafe_allow_html=True)

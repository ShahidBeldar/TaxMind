import streamlit as st
import pandas as pd
import io
import plotly.graph_objects as go
from utils.i18n import t
from utils.tax import calculate_tax, slab_breakdown, format_inr
from utils.theme import inject_theme, page_title, stat_card, section_header
from utils.sidebar import render_sidebar

# ── Auth guard ────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()

inject_theme()
render_sidebar()

# ── Plotly dark template ──────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#8899b8", size=12),
    margin=dict(l=8, r=8, t=40, b=8),
    legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0, font=dict(size=11)),
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
        ["Gross Income",                   f"{result['gross_income']:,.0f}"],
        ["Standard Deduction",             f"{result['standard_deduction']:,.0f}"],
        ["Taxable Income",                 f"{result['taxable_income']:,.0f}"],
        ["Tax Before Rebate",              f"{result['tax_before_rebate']:,.0f}"],
        ["Rebate u/s 87A",                 f"({result['rebate_87a']:,.0f})"],
        ["Tax After Rebate",               f"{result['tax_after_rebate']:,.0f}"],
        ["Health & Education Cess (4%)",   f"{result['cess']:,.0f}"],
        ["Total Tax Payable",              f"{result['total_tax_payable']:,.0f}"],
    ]
    tbl = Table(summary_data, colWidths=[10*cm, 6*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  colors.HexColor("#111827")),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        ("GRID",           (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN",          (1, 0), (1, -1),  "RIGHT"),
        ("FONTNAME",       (0, -1), (-1, -1),"Helvetica-Bold"),
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
        ("BACKGROUND",     (0, 0), (-1, 0),  colors.HexColor("#111827")),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        ("GRID",           (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN",          (1, 0), (-1, -1), "RIGHT"),
    ]))
    elements.append(slab_tbl)
    doc.build(elements)
    return buffer.getvalue()


# ── Page ──────────────────────────────────────────────────────────────────────
employment_type  = st.session_state.get("employment_type", "Salaried") or "Salaried"
preferred_regime = st.session_state.get("preferred_regime", "new") or "new"

st.markdown(page_title("📊", "Tax Dashboard",
    f"Employment: {employment_type} · Regime: {'New' if preferred_regime == 'new' else 'Old'} · FY 2026"),
    unsafe_allow_html=True)

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

    # ── KPI strip ─────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    eff_rate = result['total_tax_payable'] / gross_income * 100 if gross_income else 0
    kpis = [
        ("Gross Income",   format_inr(result["gross_income"]),      "Before deductions",     "var(--text-md)"),
        ("Taxable Income", format_inr(result["taxable_income"]),    "After std. deduction",  "var(--amber)"),
        ("Tax Payable",    format_inr(result["total_tax_payable"]), "Incl. 4% cess",         "var(--red)"),
        ("Effective Rate", f"{eff_rate:.1f}%",                      "Of gross income",        "var(--green)"),
    ]
    for col, (lbl, val, sub, accent) in zip([k1, k2, k3, k4], kpis):
        with col:
            st.markdown(stat_card(lbl, val, sub, accent), unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # ── Chart row 1: Donut + Waterfall ────────────────────────────────────────
    ch1, ch2 = st.columns(2)

    with ch1:
        st.markdown(section_header("Tax Composition", "How your income is split"), unsafe_allow_html=True)
        take_home = result["gross_income"] - result["total_tax_payable"]
        labels  = ["Take-Home", "Tax (after rebate)", "Cess"]
        values  = [take_home, result["tax_after_rebate"], result["cess"]]
        colours = ["#00e676", "#ff5252", "#ffab40"]

        fig_donut = go.Figure(go.Pie(
            labels=labels, values=values,
            hole=.65,
            marker=dict(colors=colours, line=dict(color="#0b0f1a", width=3)),
            textinfo="percent",
            textfont=dict(size=12, color="#edf2ff", family="DM Mono"),
            hovertemplate="<b>%{label}</b><br>Rs. %{value:,.0f}  (%{percent})<extra></extra>",
        ))
        fig_donut.update_layout(
            **PLOTLY_LAYOUT,
            showlegend=True,
            height=300,
            legend=dict(orientation="h", y=-0.08, x=0.5, xanchor="center"),
            annotations=[dict(
                text=f"<b>Rs. {result['total_tax_payable']:,.0f}</b><br><span style='font-size:11px'>total tax</span>",
                x=0.5, y=0.5,
                font=dict(size=13, color="#edf2ff", family="DM Mono"),
                showarrow=False,
            )],
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with ch2:
        st.markdown(section_header("Income Waterfall", "From gross to take-home"), unsafe_allow_html=True)
        wf_labels  = ["Gross Income", "Std. Deduction", "Taxable Income", "Tax + Cess", "Take-Home"]
        wf_values  = [
            result["gross_income"],
            -result["standard_deduction"],
            0,  # placeholder (measure)
            -result["total_tax_payable"],
            0,
        ]
        wf_measure = ["absolute", "relative", "total", "relative", "total"]
        wf_text    = [
            format_inr(result["gross_income"]),
            f"−{format_inr(result['standard_deduction'])}",
            format_inr(result["taxable_income"]),
            f"−{format_inr(result['total_tax_payable'])}",
            format_inr(take_home),
        ]
        fig_wf = go.Figure(go.Waterfall(
            orientation="v",
            measure=wf_measure,
            x=wf_labels,
            y=wf_values,
            text=wf_text,
            textposition="outside",
            textfont=dict(size=10, color="#8899b8", family="DM Mono"),
            connector=dict(line=dict(color="#273347", width=1, dash="dot")),
            increasing=dict(marker=dict(color="#00e676", line=dict(width=0))),
            decreasing=dict(marker=dict(color="#ff5252", line=dict(width=0))),
            totals=dict(marker=dict(color="#40c4ff", line=dict(width=0))),
            hovertemplate="<b>%{x}</b><br>Rs. %{y:,.0f}<extra></extra>",
        ))
        fig_wf.update_layout(
            **PLOTLY_LAYOUT, height=300,
            xaxis=dict(showgrid=False, tickfont=dict(size=10)),
            yaxis=dict(showgrid=True, gridcolor="#1e2a3d", tickformat=","),
            showlegend=False,
        )
        st.plotly_chart(fig_wf, use_container_width=True)

    # ── Chart row 2: Slab bar + Effective rate gauge ──────────────────────────
    ch3, ch4 = st.columns(2)

    with ch3:
        st.markdown(section_header("Slab-wise Tax", "Tax computed per income bracket"), unsafe_allow_html=True)
        if slabs:
            slab_df = pd.DataFrame(slabs)
            short_labels = [
                s.split(" to ")[-1].replace("Above ", ">").replace("Up to ", "≤")
                for s in slab_df["Slab"]
            ]
            non_zero = slab_df["Tax (Rs.)"] > 0
            bar_colors = ["#00e676" if nz else "#1e2a3d" for nz in non_zero]

            fig_slab = go.Figure(go.Bar(
                x=short_labels,
                y=slab_df["Tax (Rs.)"],
                marker=dict(color=bar_colors, line=dict(width=0), cornerradius=4),
                text=[f"Rs.{v:,.0f}" if v > 0 else "" for v in slab_df["Tax (Rs.)"]],
                textposition="outside",
                textfont=dict(size=10, color="#8899b8", family="DM Mono"),
                hovertemplate="<b>%{x}</b><br>Tax: Rs. %{y:,.0f}<extra></extra>",
            ))
            fig_slab.update_layout(
                **PLOTLY_LAYOUT, height=280,
                xaxis=dict(showgrid=False, tickfont=dict(size=10)),
                yaxis=dict(showgrid=True, gridcolor="#1e2a3d", tickformat=","),
            )
            st.plotly_chart(fig_slab, use_container_width=True)

    with ch4:
        st.markdown(section_header("Effective Tax Rate", "Visual gauge vs. top marginal rate"), unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=eff_rate,
            number=dict(suffix="%", font=dict(size=28, color="#edf2ff", family="DM Mono")),
            delta=dict(reference=30, valueformat=".1f",
                       increasing=dict(color="#ff5252"),
                       decreasing=dict(color="#00e676")),
            gauge=dict(
                axis=dict(range=[0, 40], tickwidth=1, tickcolor="#273347",
                          tickfont=dict(size=10, color="#4a5a72")),
                bar=dict(color="#00e676", thickness=0.22),
                bgcolor="rgba(0,0,0,0)",
                borderwidth=0,
                steps=[
                    dict(range=[0, 5],  color="#0d2018"),
                    dict(range=[5, 15], color="#112a1e"),
                    dict(range=[15, 25],color="#1a2e1a"),
                    dict(range=[25, 40],color="#2a1a1a"),
                ],
                threshold=dict(line=dict(color="#ffab40", width=2), thickness=0.75, value=30),
            ),
            title=dict(text="Eff. Rate vs 30% marginal", font=dict(size=11, color="#4a5a72")),
        ))
        fig_gauge.update_layout(**PLOTLY_LAYOUT, height=280)
        st.plotly_chart(fig_gauge, use_container_width=True)

    # ── Full breakdown table ──────────────────────────────────────────────────
    st.markdown(section_header("Full Breakdown"), unsafe_allow_html=True)
    summary_rows = {
        t("gross_income"):       format_inr(result["gross_income"]),
        t("standard_deduction"): format_inr(result["standard_deduction"]),
        t("taxable_income"):     format_inr(result["taxable_income"]),
        t("tax_before_rebate"):  format_inr(result["tax_before_rebate"]),
        t("rebate_87a"):         f"({format_inr(result['rebate_87a'])})",
        t("tax_after_rebate"):   format_inr(result["tax_after_rebate"]),
        t("cess"):               format_inr(result["cess"]),
        t("total_tax_payable"):  format_inr(result["total_tax_payable"]),
    }
    summary_df = pd.DataFrame(list(summary_rows.items()), columns=["Description", "Amount"])
    st.table(summary_df.set_index("Description"))

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
    st.markdown("""
    <div style="
        background:#111827;border:1px dashed #1e2a3d;border-radius:16px;
        padding:3rem;text-align:center;margin-top:1rem;
    ">
        <div style="font-size:2rem;margin-bottom:.6rem;">📥</div>
        <div style="font-family:'Syne',sans-serif;font-weight:700;color:#edf2ff;font-size:1rem;">
            Enter your gross income above
        </div>
        <p style="color:#4a5a72;font-size:13px;margin:.4rem 0 0 0;">
            Get an instant slab-wise breakdown with waterfall, gauge, and PDF export.
        </p>
    </div>
    """, unsafe_allow_html=True)

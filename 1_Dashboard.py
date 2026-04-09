import streamlit as st
import pandas as pd
import io
from utils.i18n import t
from utils.tax import calculate_tax, slab_breakdown, format_inr

# ---------------------------------------------------------------------------
# Auth guard
# ---------------------------------------------------------------------------
if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()

# ---------------------------------------------------------------------------
# PDF export helper
# ---------------------------------------------------------------------------
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
        ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
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
            row["Slab"],
            row["Rate"],
            f"{row['Income in Slab (Rs.)']:,.0f}",
            f"{row['Tax (Rs.)']:,.0f}",
        ])

    slab_tbl = Table(slab_data, colWidths=[7*cm, 2*cm, 4*cm, 3*cm])
    slab_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN",        (1, 0), (-1, -1), "RIGHT"),
    ]))
    elements.append(slab_tbl)

    doc.build(elements)
    return buffer.getvalue()


# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------
st.title(t("dashboard_title"))
st.write("---")

employment_type  = st.session_state.get("employment_type", "Salaried") or "Salaried"
preferred_regime = st.session_state.get("preferred_regime", "new") or "new"

st.caption(
    f"Employment: {employment_type}  |  "
    f"Regime: {'New' if preferred_regime == 'new' else 'Old'} Regime"
)

gross_income = st.number_input(
    t("gross_income_label"),
    min_value=0,
    max_value=100_000_000,
    value=0,
    step=10_000,
    format="%d",
)

calc_clicked = st.button(t("calculate_btn"), use_container_width=True)

if calc_clicked and gross_income > 0:
    result = calculate_tax(gross_income, employment_type, regime="new")
    slabs  = slab_breakdown(result["taxable_income"])

    st.write("")
    st.subheader(t("tax_breakdown"))

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

    summary_df = pd.DataFrame(
        list(summary_rows.items()),
        columns=["Description", "Amount"]
    )
    st.table(summary_df.set_index("Description"))

    if slabs:
        st.write("")
        st.subheader(t("slab_breakdown"))
        slab_df = pd.DataFrame(slabs)
        st.table(slab_df.set_index("Slab"))

    # Export buttons
    st.write("")
    col_pdf, col_csv = st.columns(2)

    with col_pdf:
        pdf_bytes = build_pdf(result, slabs, employment_type)
        st.download_button(
            label=t("export_pdf"),
            data=pdf_bytes,
            file_name="taxmind_computation_fy2026.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    with col_csv:
        csv_df = pd.DataFrame(list(summary_rows.items()), columns=["Description", "Amount"])
        csv_bytes = csv_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=t("export_csv"),
            data=csv_bytes,
            file_name="taxmind_computation_fy2026.csv",
            mime="text/csv",
            use_container_width=True,
        )

elif calc_clicked and gross_income == 0:
    st.warning("Please enter a gross income greater than zero.")

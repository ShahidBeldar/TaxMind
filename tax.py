# Tax engine for FY 2026 — New Regime only
# All amounts in Indian Rupees (INR)

STANDARD_DEDUCTION_SALARIED = 75_000

NEW_REGIME_SLABS = [
    (400_000,  0.00),
    (800_000,  0.05),
    (1_200_000, 0.10),
    (1_600_000, 0.15),
    (2_000_000, 0.20),
    (2_400_000, 0.25),
    (float("inf"), 0.30),
]

REBATE_87A_INCOME_LIMIT = 1_200_000
REBATE_87A_MAX          = 60_000
CESS_RATE               = 0.04


def _compute_slab_tax(taxable_income: float) -> float:
    """Compute tax before rebate using the new regime slabs."""
    tax = 0.0
    previous_limit = 0

    for slab_limit, rate in NEW_REGIME_SLABS:
        if taxable_income <= previous_limit:
            break
        slab_top    = min(taxable_income, slab_limit)
        slab_income = slab_top - previous_limit
        tax        += slab_income * rate
        previous_limit = slab_limit

    return tax


def calculate_tax(gross_income: float,
                  employment_type: str,
                  regime: str = "new") -> dict:
    """
    Compute full tax liability for FY 2026.

    Parameters
    ----------
    gross_income     : annual gross income in INR
    employment_type  : "Salaried" | "Self-Employed" | "Business"
    regime           : "new" (old regime not implemented in this version)

    Returns
    -------
    dict with keys:
        gross_income, standard_deduction, taxable_income,
        tax_before_rebate, rebate_87a, tax_after_rebate,
        cess, total_tax_payable
    """
    gross_income = max(0.0, float(gross_income))

    # Standard deduction applies only to salaried employees under new regime
    if employment_type == "Salaried":
        standard_deduction = min(STANDARD_DEDUCTION_SALARIED, gross_income)
    else:
        standard_deduction = 0.0

    taxable_income = max(0.0, gross_income - standard_deduction)

    tax_before_rebate = _compute_slab_tax(taxable_income)

    # Section 87A rebate
    if taxable_income <= REBATE_87A_INCOME_LIMIT:
        rebate_87a = min(tax_before_rebate, REBATE_87A_MAX)
    else:
        rebate_87a = 0.0

    tax_after_rebate = max(0.0, tax_before_rebate - rebate_87a)

    # 4% health and education cess
    cess = tax_after_rebate * CESS_RATE

    total_tax_payable = tax_after_rebate + cess

    return {
        "gross_income":       gross_income,
        "standard_deduction": standard_deduction,
        "taxable_income":     taxable_income,
        "tax_before_rebate":  tax_before_rebate,
        "rebate_87a":         rebate_87a,
        "tax_after_rebate":   tax_after_rebate,
        "cess":               cess,
        "total_tax_payable":  total_tax_payable,
    }


def slab_breakdown(taxable_income: float) -> list[dict]:
    """
    Returns a per-slab breakdown for display in the dashboard.
    Each item: {slab_label, rate_pct, slab_income, tax}
    """
    rows = []
    previous_limit = 0
    slab_labels = [
        "Up to Rs. 4,00,000",
        "Rs. 4,00,001 to Rs. 8,00,000",
        "Rs. 8,00,001 to Rs. 12,00,000",
        "Rs. 12,00,001 to Rs. 16,00,000",
        "Rs. 16,00,001 to Rs. 20,00,000",
        "Rs. 20,00,001 to Rs. 24,00,000",
        "Above Rs. 24,00,000",
    ]

    for (slab_limit, rate), label in zip(NEW_REGIME_SLABS, slab_labels):
        if taxable_income <= previous_limit:
            break
        slab_top    = min(taxable_income, slab_limit)
        slab_income = slab_top - previous_limit
        tax         = slab_income * rate
        rows.append({
            "Slab":         label,
            "Rate":         f"{int(rate * 100)}%",
            "Income in Slab (Rs.)": slab_income,
            "Tax (Rs.)":    tax,
        })
        previous_limit = slab_limit

    return rows


def format_inr(amount: float) -> str:
    """Format a number as Indian currency string."""
    return f"Rs. {amount:,.0f}"

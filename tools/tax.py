def calculate_taxable_income(
    gross_income: float,
    deductions: float,
):
    return max(gross_income - deductions, 0.0)


def calculate_tax_saving(
    deduction_amount: float,
    applicable_tax_rate: float,
):
    return deduction_amount * (
        applicable_tax_rate / 100
    )


def calculate_post_tax_return(
    pre_tax_return: float,
    tax_rate: float,
):
    return pre_tax_return * (
        1 - tax_rate / 100
    )


def calculate_tax_impact(
    income: float,
    deductions: float,
    tax_rate: float,
):
    taxable_income = calculate_taxable_income(
        gross_income=income,
        deductions=deductions,
    )

    estimated_tax = taxable_income * (
        tax_rate / 100
    )

    return {
        "gross_income": income,
        "deductions": deductions,
        "taxable_income": taxable_income,
        "assumed_tax_rate": tax_rate,
        "estimated_tax": estimated_tax,
    }
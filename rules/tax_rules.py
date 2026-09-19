def check_taxable_income(
    gross_income: float,
    deductions: float,
):
    if gross_income <= 0:
        return {
            "rule": "income",
            "status": "critical",
            "message": "Gross income must be greater than zero.",
        }

    if deductions < 0:
        return {
            "rule": "deductions",
            "status": "attention",
            "message": "Deductions cannot be negative.",
        }

    if deductions > gross_income:
        return {
            "rule": "deductions",
            "status": "attention",
            "message": (
                "Deductions exceed gross income. "
                "Review the supplied assumptions."
            ),
        }

    return {
        "rule": "taxable_income",
        "status": "informational",
        "message": (
            "Taxable income will be calculated from "
            "the supplied income and deduction inputs."
        ),
    }


def check_tax_rate(tax_rate: float):
    if tax_rate < 0:
        return {
            "rule": "tax_rate",
            "status": "critical",
            "message": "Tax rate cannot be negative.",
        }

    if tax_rate > 100:
        return {
            "rule": "tax_rate",
            "status": "critical",
            "message": "Tax rate cannot exceed 100%.",
        }

    return {
        "rule": "tax_rate",
        "status": "informational",
        "message": (
            "The supplied tax rate is an assumption "
            "for this calculation."
        ),
    }


def check_tax_planning_impact(
    estimated_tax: float,
    gross_income: float,
):
    if gross_income <= 0:
        return {
            "rule": "tax_impact",
            "status": "attention",
            "message": "Cannot evaluate tax impact without income.",
        }

    tax_ratio = (
        estimated_tax / gross_income
    ) * 100

    return {
        "rule": "tax_impact",
        "status": "informational",
        "tax_to_income_percent": round(
            tax_ratio,
            2,
        ),
        "message": (
            "Tax impact has been calculated using "
            "the supplied assumptions."
        ),
    }


def evaluate_tax(
    gross_income: float,
    deductions: float,
    tax_rate: float,
    estimated_tax: float,
):
    return {
        "income": check_taxable_income(
            gross_income,
            deductions,
        ),

        "tax_rate": check_tax_rate(
            tax_rate,
        ),

        "tax_impact": check_tax_planning_impact(
            estimated_tax,
            gross_income,
        ),
    }
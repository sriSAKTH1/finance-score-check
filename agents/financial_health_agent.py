from typing import Any


def analyze_financial_health(
    financial_context: dict[str, Any],
    financial_health_data: dict[str, Any],
) -> dict[str, Any]:

    cashflow = financial_health_data.get(
        "cashflow",
        {}
    )

    debt = financial_health_data.get(
        "debt",
        {}
    )

    emergency = financial_health_data.get(
        "emergency_fund",
        {}
    )

    investments = financial_health_data.get(
        "investments",
        {}
    )

    insurance = financial_health_data.get(
        "insurance",
        {}
    )

    retirement = financial_health_data.get(
        "retirement",
        {}
    )

    tax = financial_health_data.get(
        "tax",
        {}
    )

    goals = financial_health_data.get(
        "goals",
        []
    )

    risk_profile = financial_health_data.get(
        "risk_profile",
        {}
    )

    findings = []

    # ==================================================
    # CASH FLOW
    # ==================================================

    monthly_income = cashflow.get(
        "monthly_income",
        0
    )

    monthly_expenses = cashflow.get(
        "monthly_expenses",
        0
    )

    monthly_cashflow = cashflow.get(
        "monthly_cashflow",
        0
    )

    savings_rate = cashflow.get(
        "savings_rate",
        0
    )

    net_worth = cashflow.get(
        "net_worth",
        0
    )

    if monthly_cashflow < 0:

        findings.append({
            "area": "Cash Flow",
            "status": "CRITICAL",
            "message": "Expenses are higher than income."
        })

    elif monthly_cashflow == 0:

        findings.append({
            "area": "Cash Flow",
            "status": "ATTENTION",
            "message": "There is no monthly surplus."
        })

    else:

        findings.append({
            "area": "Cash Flow",
            "status": "POSITIVE",
            "message": (
                f"Monthly income is ₹{monthly_income:,.0f}, "
                f"expenses are ₹{monthly_expenses:,.0f}, "
                f"leaving a surplus of "
                f"₹{monthly_cashflow:,.0f}."
            )
        })

    # ==================================================
    # SAVINGS
    # ==================================================

    if savings_rate < 10:

        findings.append({
            "area": "Savings",
            "status": "ATTENTION",
            "message": (
                f"Savings rate is "
                f"{savings_rate:.2f}%."
            )
        })

    else:

        findings.append({
            "area": "Savings",
            "status": "POSITIVE",
            "message": (
                f"Current savings rate is "
                f"{savings_rate:.2f}%."
            )
        })

    # ==================================================
    # DEBT
    # ==================================================

    debt_burden = debt.get(
        "debt_burden",
        0
    )

    existing_emi = debt.get(
        "existing_emi",
        0
    )

    if debt_burden >= 50:

        debt_status = "CRITICAL"

    elif debt_burden >= 40:

        debt_status = "ATTENTION"

    else:

        debt_status = "POSITIVE"

    findings.append({
        "area": "Debt",
        "status": debt_status,
        "message": (
            f"Existing EMI is ₹{existing_emi:,.0f} "
            f"and debt burden is "
            f"{debt_burden:.2f}%."
        )
    })

    # ==================================================
    # NET WORTH
    # ==================================================

    if net_worth < 0:

        findings.append({
            "area": "Net Worth",
            "status": "ATTENTION",
            "message": (
                f"Current net worth is "
                f"₹{net_worth:,.0f}."
            )
        })

    else:

        findings.append({
            "area": "Net Worth",
            "status": "POSITIVE",
            "message": (
                f"Current net worth is "
                f"₹{net_worth:,.0f}."
            )
        })

    # ==================================================
    # EMERGENCY FUND
    # ==================================================

    emergency_result = emergency.get(
        "result",
        {}
    )

    emergency_findings = emergency_result.get(
        "findings",
        []
    )

    for item in emergency_findings:

        status = item.get(
            "status",
            "informational"
        ).upper()

        if status == "INFORMATIONAL":
            status = "POSITIVE"

        findings.append({
            "area": "Emergency Fund",
            "status": status,
            "message": item.get(
                "finding",
                "Emergency fund evaluated."
            )
        })

    # ==================================================
    # INVESTMENTS
    # ==================================================

    investment_checks = [
        investments.get("risk_profile"),
        investments.get("investment_horizon"),
        investments.get("investment_concentration"),
        investments.get("goal_alignment"),
    ]

    for item in investment_checks:

        if not item:
            continue

        status = item.get(
            "status",
            "informational"
        ).upper()

        if status == "INFORMATIONAL":
            status = "POSITIVE"

        findings.append({
            "area": "Investments",
            "status": status,
            "message": item.get(
                "message",
                "Investment factor evaluated."
            )
        })

    # ==================================================
    # INSURANCE
    # ==================================================

    if isinstance(insurance, dict):

        for name, item in insurance.items():

            if not isinstance(item, dict):
                continue

            status = item.get(
                "status",
                "informational"
            ).upper()

            if status == "INFORMATIONAL":
                status = "POSITIVE"

            findings.append({
                "area": "Insurance",
                "status": status,
                "message": item.get(
                    "message",
                    "Insurance factor evaluated."
                )
            })

    # ==================================================
    # RETIREMENT
    # ==================================================

    if retirement:

        status = retirement.get(
            "status",
            "INFO"
        ).upper()

        if status == "INFO":
            status = "INFORMATIONAL"

        findings.append({
            "area": "Retirement",
            "status": status,
            "message": retirement.get(
                "message",
                "Retirement planning requires further assessment."
            )
        })

    else:

        findings.append({
            "area": "Retirement",
            "status": "INFORMATIONAL",
            "message": (
                "Retirement assessment requires "
                "retirement corpus assumptions."
            )
        })

    # ==================================================
    # TAX
    # ==================================================

    if tax:

        status = tax.get(
            "status",
            "INFO"
        ).upper()

        if status == "INFO":
            status = "INFORMATIONAL"

        findings.append({
            "area": "Tax",
            "status": status,
            "message": tax.get(
                "message",
                "Tax assessment requires additional information."
            )
        })

    # ==================================================
    # GOALS
    # ==================================================

    if goals:

        findings.append({
            "area": "Goals",
            "status": "INFORMATIONAL",
            "message": (
                f"{len(goals)} financial goal(s) "
                "are recorded."
            )
        })

    else:

        findings.append({
            "area": "Goals",
            "status": "ATTENTION",
            "message": (
                "No financial goals are currently recorded."
            )
        })

    # ==================================================
    # RISK PROFILE
    # ==================================================

    if risk_profile:

        category = (
            risk_profile.get("category")
            if isinstance(risk_profile, dict)
            else getattr(
                risk_profile,
                "category",
                "Unknown"
            )
        )

        findings.append({
            "area": "Risk Profile",
            "status": "INFORMATIONAL",
            "message": (
                f"Recorded risk profile: "
                f"{category}."
            )
        })

    # ==================================================
    # SUMMARY
    # ==================================================

    critical_count = sum(
        1
        for item in findings
        if item["status"] == "CRITICAL"
    )

    attention_count = sum(
        1
        for item in findings
        if item["status"] == "ATTENTION"
    )

    positive_count = sum(
        1
        for item in findings
        if item["status"] == "POSITIVE"
    )

    informational_count = sum(
        1
        for item in findings
        if item["status"] == "INFORMATIONAL"
    )

    if critical_count > 0:

        overall_status = "CRITICAL AREAS PRESENT"

    elif attention_count > 0:

        overall_status = "NEEDS ATTENTION"

    else:

        overall_status = "GENERALLY STABLE"

    return {

        "overall_status": overall_status,

        "summary": {
            "critical": critical_count,
            "attention": attention_count,
            "positive": positive_count,
            "informational": informational_count,
        },

        "metrics": {
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "monthly_cashflow": monthly_cashflow,
            "savings_rate": savings_rate,
            "net_worth": net_worth,
            "existing_emi": existing_emi,
            "debt_burden": debt_burden,
            "emergency_coverage_months":
                emergency.get(
                    "coverage_months"
                ),
        },

        "findings": findings,
    }


def build_financial_health_response(result: dict) -> str:

    metrics = result.get("metrics", {})
    findings = result.get("findings", [])

    lines = []

    lines.append(
        f"Overall financial status: "
        f"{result.get('overall_status', 'UNKNOWN')}"
    )

    lines.append("")

    # --------------------------------------------------
    # WHAT
    # --------------------------------------------------

    lines.append("WHAT")

    lines.append(
        f"• Monthly income: "
        f"₹{metrics.get('monthly_income', 0):,.0f}"
    )

    lines.append(
        f"• Monthly expenses: "
        f"₹{metrics.get('monthly_expenses', 0):,.0f}"
    )

    lines.append(
        f"• Monthly surplus: "
        f"₹{metrics.get('monthly_cashflow', 0):,.0f}"
    )

    lines.append(
        f"• Savings rate: "
        f"{metrics.get('savings_rate', 0):.2f}%"
    )

    lines.append(
        f"• Existing EMI: "
        f"₹{metrics.get('existing_emi', 0):,.0f}"
    )

    lines.append(
        f"• Debt burden: "
        f"{metrics.get('debt_burden', 0):.2f}%"
    )

    lines.append(
        f"• Net worth: "
        f"₹{metrics.get('net_worth', 0):,.0f}"
    )

    emergency_months = metrics.get(
        "emergency_coverage_months"
    )

    if emergency_months is not None:

        lines.append(
            f"• Emergency-fund coverage: "
            f"{emergency_months:.2f} months"
        )

    # --------------------------------------------------
    # WHY
    # --------------------------------------------------

    lines.append("")
    lines.append("WHY")

    attention_items = [
        item
        for item in findings
        if item.get("status") == "ATTENTION"
    ]

    critical_items = [
        item
        for item in findings
        if item.get("status") == "CRITICAL"
    ]

    if critical_items:

        for item in critical_items:

            lines.append(
                f"• {item['area']}: "
                f"{item['message']}"
            )

    elif attention_items:

        for item in attention_items:

            lines.append(
                f"• {item['area']}: "
                f"{item['message']}"
            )

    else:

        lines.append(
            "• No critical or attention areas "
            "were identified from the available data."
        )

    # --------------------------------------------------
    # POSITIVE AREAS
    # --------------------------------------------------

    lines.append("")
    lines.append("POSITIVE AREAS")

    positive_items = [
        item
        for item in findings
        if item.get("status") == "POSITIVE"
    ]

    for item in positive_items:

        lines.append(
            f"• {item['area']}: "
            f"{item['message']}"
        )

    # --------------------------------------------------
    # INFORMATION GAPS
    # --------------------------------------------------

    informational_items = [
        item
        for item in findings
        if item.get("status") == "INFORMATIONAL"
    ]

    if informational_items:

        lines.append("")
        lines.append("INFORMATION GAPS")

        for item in informational_items:

            lines.append(
                f"• {item['area']}: "
                f"{item['message']}"
            )

    # --------------------------------------------------
    # NEXT STEPS
    # --------------------------------------------------

    lines.append("")
    lines.append("WHAT TO IMPROVE")

    if attention_items or critical_items:

        for item in (
            critical_items + attention_items
        ):

            lines.append(
                f"• Review {item['area'].lower()} "
                "and assess whether changes are needed."
            )

    else:

        lines.append(
            "• Continue monitoring the current "
            "financial position."
        )

    lines.append(
        "• Complete the missing retirement and "
        "tax inputs for a more complete assessment."
    )

    return "\n".join(lines)
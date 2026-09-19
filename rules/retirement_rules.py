def check_retirement_horizon(years_to_retirement: int):
    if years_to_retirement <= 0:
        return {
            "rule": "retirement_horizon",
            "status": "critical",
            "message": "Retirement age is at or before the current age.",
        }

    if years_to_retirement < 5:
        status = "short_horizon"
    elif years_to_retirement <= 15:
        status = "medium_horizon"
    else:
        status = "long_horizon"

    return {
        "rule": "retirement_horizon",
        "status": "informational",
        "message": (
            f"Years to retirement classified as "
            f"{status}."
        ),
    }


def check_retirement_gap(
    required_corpus: float,
    projected_corpus: float,
):
    gap = max(
        required_corpus - projected_corpus,
        0.0,
    )

    if gap > 0:
        return {
            "rule": "retirement_corpus_gap",
            "status": "attention",
            "gap": gap,
            "message": (
                f"Projected retirement corpus is "
                f"below the calculated target by "
                f"₹{gap:,.2f} under the supplied assumptions."
            ),
        }

    return {
        "rule": "retirement_corpus_gap",
        "status": "informational",
        "gap": 0.0,
        "message": (
            "Projected corpus meets or exceeds "
            "the calculated target under the "
            "supplied assumptions."
        ),
    }


def check_retirement_assumptions(
    inflation_rate: float,
    expected_return: float,
):
    findings = []

    if inflation_rate < 0:
        findings.append({
            "rule": "inflation_assumption",
            "status": "attention",
            "message": "Inflation assumption cannot be negative.",
        })

    if expected_return < 0:
        findings.append({
            "rule": "return_assumption",
            "status": "attention",
            "message": "Expected return assumption is negative.",
        })

    if not findings:
        findings.append({
            "rule": "retirement_assumptions",
            "status": "informational",
            "message": (
                "Inflation and return are scenario "
                "assumptions and are not guaranteed."
            ),
        })

    return findings


def evaluate_retirement(
    years_to_retirement: int,
    required_corpus: float,
    projected_corpus: float,
    inflation_rate: float,
    expected_return: float,
):
    return {
        "retirement_horizon": check_retirement_horizon(
            years_to_retirement
        ),

        "retirement_gap": check_retirement_gap(
            required_corpus,
            projected_corpus,
        ),

        "assumptions": check_retirement_assumptions(
            inflation_rate,
            expected_return,
        ),
    }
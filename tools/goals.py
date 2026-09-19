def future_value(
    present_value: float,
    annual_return: float,
    years: int,
):
    """
    Calculate future value of an existing corpus.
    """

    rate = annual_return / 100

    return present_value * ((1 + rate) ** years)


def future_value_with_monthly_contribution(
    current_corpus: float,
    monthly_contribution: float,
    annual_return: float,
    years: int,
):
    """
    Calculate future value of an existing corpus
    plus monthly contributions.
    """

    months = years * 12
    monthly_rate = annual_return / 100 / 12

    corpus_growth = current_corpus * (
        (1 + annual_return / 100) ** years
    )

    if monthly_rate == 0:
        contribution_growth = monthly_contribution * months
    else:
        contribution_growth = monthly_contribution * (
            ((1 + monthly_rate) ** months - 1)
            / monthly_rate
        )

    return corpus_growth + contribution_growth


def required_future_value(
    current_goal_amount: float,
    inflation_rate: float,
    years: int,
):
    """
    Calculate the future amount required for a goal
    after accounting for inflation.
    """

    inflation = inflation_rate / 100

    return current_goal_amount * (
        (1 + inflation) ** years
    )


def required_monthly_contribution(
    target_amount: float,
    current_corpus: float,
    annual_return: float,
    years: int,
):
    """
    Calculate the approximate monthly contribution
    required to reach a target amount.
    """

    months = years * 12
    monthly_rate = annual_return / 100 / 12

    current_corpus_future_value = current_corpus * (
        (1 + annual_return / 100) ** years
    )

    remaining_target = (
        target_amount - current_corpus_future_value
    )

    if remaining_target <= 0:
        return 0.0

    if monthly_rate == 0:
        return remaining_target / months

    contribution = remaining_target * monthly_rate / (
        (1 + monthly_rate) ** months - 1
    )

    return contribution


def calculate_goal_gap(
    target_amount: float,
    projected_amount: float,
):
    """
    Calculate the difference between the target
    and projected corpus.
    """

    return max(target_amount - projected_amount, 0)
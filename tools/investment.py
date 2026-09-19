def calculate_future_value(
    current_amount: float,
    annual_return: float,
    years: int,
):
    """
    Calculate the future value of a current investment.
    """

    rate = annual_return / 100

    return current_amount * ((1 + rate) ** years)


def calculate_monthly_investment_future_value(
    monthly_investment: float,
    annual_return: float,
    years: int,
):
    """
    Calculate future value of regular monthly investments.
    """

    months = years * 12
    monthly_rate = annual_return / 100 / 12

    if monthly_rate == 0:
        return monthly_investment * months

    return monthly_investment * (
        ((1 + monthly_rate) ** months - 1)
        / monthly_rate
    )


def calculate_total_investment_value(
    current_amount: float,
    monthly_investment: float,
    annual_return: float,
    years: int,
):
    """
    Calculate projected value of current investment
    plus regular monthly investment.
    """

    current_value = calculate_future_value(
        current_amount,
        annual_return,
        years,
    )

    monthly_value = calculate_monthly_investment_future_value(
        monthly_investment,
        annual_return,
        years,
    )

    return current_value + monthly_value


def calculate_investment_gain(
    invested_amount: float,
    projected_value: float,
):
    """
    Calculate projected gain.
    """

    return projected_value - invested_amount
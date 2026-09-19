def calculate_years_to_retirement(
    current_age: int,
    retirement_age: int,
):
    return max(retirement_age - current_age, 0)


def calculate_future_expense(
    current_monthly_expense: float,
    inflation_rate: float,
    years: int,
):
    inflation = inflation_rate / 100

    return current_monthly_expense * (
        (1 + inflation) ** years
    )


def calculate_retirement_corpus(
    future_monthly_expense: float,
    years_in_retirement: int,
    annual_return: float,
):
    months = years_in_retirement * 12

    monthly_rate = annual_return / 100 / 12

    if monthly_rate == 0:
        return future_monthly_expense * months

    corpus = future_monthly_expense * (
        (1 - (1 + monthly_rate) ** (-months))
        / monthly_rate
    )

    return corpus


def calculate_future_value(
    current_amount: float,
    annual_return: float,
    years: int,
):
    return current_amount * (
        (1 + annual_return / 100) ** years
    )


def calculate_required_monthly_investment(
    target_corpus: float,
    current_corpus: float,
    annual_return: float,
    years: int,
):
    months = years * 12

    monthly_rate = annual_return / 100 / 12

    current_corpus_future_value = (
        calculate_future_value(
            current_corpus,
            annual_return,
            years,
        )
    )

    remaining_corpus = (
        target_corpus
        - current_corpus_future_value
    )

    if remaining_corpus <= 0:
        return 0.0

    if monthly_rate == 0:
        return remaining_corpus / months

    monthly_investment = (
        remaining_corpus
        * monthly_rate
        / (
            (1 + monthly_rate) ** months
            - 1
        )
    )

    return monthly_investment


def calculate_retirement_gap(
    required_corpus: float,
    projected_corpus: float,
):
    return max(
        required_corpus - projected_corpus,
        0.0,
    )
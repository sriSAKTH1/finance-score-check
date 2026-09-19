def calculate_insurance_gap(
    required_cover: float,
    existing_cover: float,
):
    """
    Calculate the difference between required and existing
    insurance coverage.
    """

    gap = required_cover - existing_cover

    return max(gap, 0.0)


def calculate_life_cover_multiple(
    annual_income: float,
    life_cover: float,
):
    """
    Calculate life cover as a multiple of annual income.
    """

    if annual_income <= 0:
        return 0.0

    return life_cover / annual_income


def calculate_health_cover_per_dependent(
    health_cover: float,
    dependents: int,
):
    """
    Calculate health cover available per dependent.

    This is only a descriptive calculation and does not
    determine whether coverage is adequate.
    """

    if dependents <= 0:
        return health_cover

    return health_cover / dependents


def calculate_total_insurance_cover(
    life_cover: float,
    health_cover: float,
):
    """
    Calculate total recorded insurance cover.
    """

    return life_cover + health_cover
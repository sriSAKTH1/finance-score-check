from pydantic import BaseModel, Field


class ScenarioInput(BaseModel):
    name: str

    # Investment / Goal
    monthly_investment: float | None = Field(
        default=None,
        ge=0
    )

    current_investment: float | None = Field(
        default=None,
        ge=0
    )

    # Common assumptions
    annual_return: float | None = None

    years: int | None = Field(
        default=None,
        gt=0
    )

    inflation_rate: float | None = None

    # Loan
    loan_amount: float | None = Field(
        default=None,
        ge=0
    )

    interest_rate: float | None = Field(
        default=None,
        ge=0
    )

    tenure_months: int | None = Field(
        default=None,
        gt=0
    )

    # Retirement
    retirement_age: int | None = Field(
        default=None,
        gt=0
    )


class ScenarioResult(BaseModel):
    scenario_name: str

    metrics: dict[str, float]

    assumptions: dict[str, float]


class ScenarioComparison(BaseModel):
    baseline: ScenarioResult

    scenario: ScenarioResult

    differences: dict[str, float]
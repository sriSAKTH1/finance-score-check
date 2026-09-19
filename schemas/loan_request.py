from pydantic import BaseModel, Field


class LoanRequest(BaseModel):
    loan_amount: float = Field(gt=0)
    interest_rate: float | None = Field(default=None, ge=0)
    tenure_months: int | None = Field(default=None, gt=0)
    purpose: str | None = None
from pydantic import BaseModel, Field
from typing import List


class Profile(BaseModel):
    name: str
    age: int = Field(ge=18)
    occupation: str
    marital_status: str
    dependents: int = Field(ge=0)


class Income(BaseModel):
    monthly_salary: float = Field(ge=0)
    other_income: float = Field(ge=0)


class Expenses(BaseModel):
    rent: float = Field(ge=0)
    food: float = Field(ge=0)
    transport: float = Field(ge=0)
    utilities: float = Field(ge=0)
    education: float = Field(ge=0)
    other: float = Field(ge=0)


class Loan(BaseModel):
    outstanding: float = Field(ge=0)
    emi: float = Field(ge=0)
    interest_rate: float = Field(ge=0)
    remaining_months: int = Field(ge=0)


class Liabilities(BaseModel):
    home_loan: Loan | None = None


class Assets(BaseModel):
    bank_savings: float = Field(ge=0)
    mutual_funds: float = Field(ge=0)
    gold: float = Field(ge=0)


class Insurance(BaseModel):
    health_cover: float = Field(ge=0)
    life_cover: float = Field(ge=0)


class Goal(BaseModel):
    name: str
    current_corpus: float = Field(ge=0)
    target_amount: float = Field(gt=0)
    years: int = Field(gt=0)
    monthly_contribution: float = Field(ge=0)


class RiskProfile(BaseModel):
    category: str


class FinancialProfile(BaseModel):
    user_id: str

    profile: Profile
    income: Income
    expenses: Expenses
    liabilities: Liabilities
    assets: Assets
    insurance: Insurance

    goals: List[Goal]

    risk_profile: RiskProfile
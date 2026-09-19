from scenarios.scenario_engine import (
    run_loan_scenario,
)


result = run_loan_scenario(
    user_id="demo_user_001",

    loan_amount=50_000,

    interest_rate=12,

    tenure_months=24,

    current_monthly_cashflow=35_000,

    scenario_name="Take ₹50,000 Loan",
)


print("\nLOAN SCENARIO TEST")
print("==================")

print("\nBASELINE")
print(result.baseline.model_dump())

print("\nSCENARIO")
print(result.scenario.model_dump())

print("\nDIFFERENCES")
print(result.differences)
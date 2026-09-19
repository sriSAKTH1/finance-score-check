from rules.investment_rules import (
    check_risk_profile,
    check_investment_horizon,
    check_investment_concentration,
    check_goal_alignment,
)


print("INVESTMENT RULE TEST")
print("====================")

print(
    check_risk_profile("Moderate")
)

print(
    check_investment_horizon(10)
)

print(
    check_investment_concentration(
        total_investments=500000,
        largest_investment=250000,
    )
)

print(
    check_goal_alignment(
        investment_horizon=10,
        goal_horizon=12,
    )
)
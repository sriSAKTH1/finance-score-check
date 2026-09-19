from tools.goals import (
    future_value,
    future_value_with_monthly_contribution,
    required_future_value,
    required_monthly_contribution,
    calculate_goal_gap,
)


print("\nFINSOURCE GOAL TOOLS")
print("============================")


current_corpus = 400000
target_amount = 2000000
monthly_contribution = 5000
years = 12


print("\nCURRENT CORPUS")
print(current_corpus)


future_corpus = future_value(
    present_value=current_corpus,
    annual_return=10,
    years=years,
)

print("\nFuture value of current corpus:")
print(round(future_corpus, 2))


projected_corpus = future_value_with_monthly_contribution(
    current_corpus=current_corpus,
    monthly_contribution=monthly_contribution,
    annual_return=10,
    years=years,
)

print("\nProjected corpus with monthly contribution:")
print(round(projected_corpus, 2))


inflation_adjusted_target = required_future_value(
    current_goal_amount=target_amount,
    inflation_rate=6,
    years=years,
)

print("\nInflation-adjusted target:")
print(round(inflation_adjusted_target, 2))


required_sip = required_monthly_contribution(
    target_amount=target_amount,
    current_corpus=current_corpus,
    annual_return=10,
    years=years,
)

print("\nRequired monthly contribution:")
print(round(required_sip, 2))


gap = calculate_goal_gap(
    target_amount=target_amount,
    projected_amount=projected_corpus,
)

print("\nGoal gap:")
print(round(gap, 2))
from tools.retirement import (
    calculate_years_to_retirement,
    calculate_future_expense,
    calculate_retirement_corpus,
    calculate_future_value,
    calculate_required_monthly_investment,
    calculate_retirement_gap,
)


current_age = 28
retirement_age = 55

current_monthly_expense = 45_000
inflation_rate = 6
years_in_retirement = 25

current_corpus = 500_000
annual_return = 10


years_to_retirement = calculate_years_to_retirement(
    current_age=current_age,
    retirement_age=retirement_age,
)


future_expense = calculate_future_expense(
    current_monthly_expense=current_monthly_expense,
    inflation_rate=inflation_rate,
    years=years_to_retirement,
)


retirement_corpus = calculate_retirement_corpus(
    future_monthly_expense=future_expense,
    years_in_retirement=years_in_retirement,
    annual_return=annual_return,
)


future_current_corpus = calculate_future_value(
    current_amount=current_corpus,
    annual_return=annual_return,
    years=years_to_retirement,
)


required_monthly_investment = (
    calculate_required_monthly_investment(
        target_corpus=retirement_corpus,
        current_corpus=current_corpus,
        annual_return=annual_return,
        years=years_to_retirement,
    )
)


gap = calculate_retirement_gap(
    required_corpus=retirement_corpus,
    projected_corpus=future_current_corpus,
)


print("\nRETIREMENT TOOL TEST")
print("====================")

print(
    f"Years to retirement: "
    f"{years_to_retirement}"
)

print(
    f"Future monthly expense: "
    f"₹{future_expense:,.2f}"
)

print(
    f"Required retirement corpus: "
    f"₹{retirement_corpus:,.2f}"
)

print(
    f"Future value of current corpus: "
    f"₹{future_current_corpus:,.2f}"
)

print(
    f"Required monthly investment: "
    f"₹{required_monthly_investment:,.2f}"
)

print(
    f"Retirement corpus gap: "
    f"₹{gap:,.2f}"
)
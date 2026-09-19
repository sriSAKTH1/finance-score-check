from tools.investment import (
    calculate_future_value,
    calculate_monthly_investment_future_value,
    calculate_total_investment_value,
)


current_value = calculate_future_value(
    current_amount=250000,
    annual_return=10,
    years=10,
)

monthly_value = calculate_monthly_investment_future_value(
    monthly_investment=10000,
    annual_return=10,
    years=10,
)

total_value = calculate_total_investment_value(
    current_amount=250000,
    monthly_investment=10000,
    annual_return=10,
    years=10,
)


print("INVESTMENT TOOL TEST")
print("====================")
print(f"Current investment future value: ₹{current_value:,.2f}")
print(f"Monthly investment future value: ₹{monthly_value:,.2f}")
print(f"Total projected value: ₹{total_value:,.2f}")
from tools.cashflow import (
    calculate_total_income,
    calculate_total_expenses,
    calculate_monthly_cashflow,
    calculate_savings_rate,
    calculate_net_worth,
)


USER_ID = "demo_user_001"


print("FINANCIAL CALCULATIONS")
print("======================")

income = calculate_total_income(USER_ID)
expenses = calculate_total_expenses(USER_ID)
cashflow = calculate_monthly_cashflow(USER_ID)
savings_rate = calculate_savings_rate(USER_ID)
net_worth = calculate_net_worth(USER_ID)


print(f"Total Income      : ₹{income:,.2f}")
print(f"Total Expenses    : ₹{expenses:,.2f}")
print(f"Monthly Surplus   : ₹{cashflow:,.2f}")
print(f"Savings Rate      : {savings_rate:.2f}%")
print(f"Net Worth         : ₹{net_worth:,.2f}")
from agents.cashflow_agent import analyze_cashflow


result = analyze_cashflow(
    user_id="demo_user_001",
    user_message="Am I saving enough?"
)


print("\nFINSOURCE CASH FLOW AGENT")
print("============================")

print("\nCALCULATED DATA")
print("----------------------------")

calculations = result["analysis"]["calculations"]

print("Monthly Income:",
      calculations["total_income"])

print("Monthly Expenses:",
      calculations["total_expenses"])

print("Monthly Cash Flow:",
      calculations["monthly_cashflow"])

print("Savings Rate:",
      calculations["savings_rate"])

print("Net Worth:",
      calculations["net_worth"])


print("\nAI ANALYSIS")
print("----------------------------")

print(result["response"])
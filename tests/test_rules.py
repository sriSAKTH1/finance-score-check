from rules.rule_engine import analyze_financial_rules


USER_ID = "demo_user_001"


result = analyze_financial_rules(USER_ID)


print("FINANCIAL RULE ANALYSIS")
print("=======================")


print("\nCASH FLOW")
print("---------")

print(
    f"Income: ₹{result['cashflow']['income']:,.2f}"
)

print(
    f"Expenses: ₹{result['cashflow']['expenses']:,.2f}"
)

print(
    f"Cashflow: ₹{result['cashflow']['cashflow']:,.2f}"
)

print(
    f"Savings Rate: "
    f"{result['cashflow']['savings_rate']:.2f}%"
)


print("\nDEBT")
print("----")

print(
    f"Existing EMI: "
    f"₹{result['debt']['existing_emi']:,.2f}"
)

print(
    f"Debt Burden: "
    f"{result['debt']['debt_burden']:.2f}%"
)


print("\nEMERGENCY FUND")
print("--------------")

print(
    f"Emergency Savings: "
    f"₹{result['emergency_fund']['emergency_savings']:,.2f}"
)

print(
    f"Coverage: "
    f"{result['emergency_fund']['coverage_months']:.2f} months"
)


print("\nFINDINGS")
print("--------")

for category in result.values():

    for finding in category["findings"]:

        print(
            f"[{finding['status'].upper()}] "
            f"{finding['finding']}"
        )
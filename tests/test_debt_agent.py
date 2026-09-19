from agents.debt_agent import analyze_debt


USER_ID = "demo_user_001"


result = analyze_debt(
    user_id=USER_ID,

    user_message=(
        "Can I take a ₹50,000 loan at 12% "
        "for 24 months?"
    ),

    loan_amount=50000,

    interest_rate=12,

    tenure_months=24,
)


print("\nFINSOURCE DEBT AGENT")
print("====================")

print("\nCALCULATED DATA")
print("----------------")

analysis = result["analysis"]

loan = analysis["loan"]

print(
    f"Loan Amount: "
    f"₹{loan['amount']:,.2f}"
)

print(
    f"Interest Rate: "
    f"{loan['interest_rate']}%"
)

print(
    f"Tenure: "
    f"{loan['tenure_months']} months"
)

print(
    f"EMI: "
    f"₹{loan['emi']:,.2f}"
)

print(
    f"Total Interest: "
    f"₹{loan['total_interest']:,.2f}"
)

print(
    f"Total Repayment: "
    f"₹{loan['total_repayment']:,.2f}"
)


print("\nAI ANALYSIS")
print("-----------")

print(result["response"])
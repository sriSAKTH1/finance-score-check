from agents.tax_agent import analyze_tax


result = analyze_tax(
    user_id="demo_user_001",

    user_message=(
        "How does tax affect my savings "
        "and investment returns?"
    ),

    gross_income=1_200_000,
    deductions=150_000,
    tax_rate=20,
    deduction_amount=150_000,
    pre_tax_return=10,
)


print("\nTAX AGENT TEST")
print("==============")

print("\nANALYSIS")
print(result["analysis"])

print("\nRESPONSE")
print(result["response"])
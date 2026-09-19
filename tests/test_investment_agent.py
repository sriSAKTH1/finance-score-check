from agents.investment_agent import analyze_investment


result = analyze_investment(
    user_id="demo_user_001",
    user_message=(
        "I have ₹2,50,000 invested and can invest "
        "₹10,000 every month for 10 years."
    ),
    current_investment=250000,
    monthly_investment=10000,
    years=10,
    assumed_return=10,
    risk_category="Moderate",
)


print("\nINVESTMENT AGENT TEST")
print("====================")

print("\nANALYSIS")
print(result["analysis"])

print("\nRESPONSE")
print(result["response"])
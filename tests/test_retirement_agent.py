from agents.retirement_agent import analyze_retirement


result = analyze_retirement(
    user_id="demo_user_001",

    user_message=(
        "How much do I need for retirement "
        "and how much should I invest?"
    ),

    current_age=28,
    retirement_age=55,

    current_monthly_expense=45_000,

    inflation_rate=6,

    years_in_retirement=25,

    current_corpus=500_000,

    expected_return=10,
)


print("\nRETIREMENT AGENT TEST")
print("=====================")

print("\nANALYSIS")
print(result["analysis"])

print("\nRESPONSE")
print(result["response"])
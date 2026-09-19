from agents.scenario_agent import (
    extract_number,
    extract_percentage,
    extract_months,
    extract_years,
)

print("=" * 60)
print("SCENARIO PARSER TEST")
print("=" * 60)

tests = [
    "What if I take a loan of 100000?",
    "What if I reduce the interest rate to 10%?",
    "What if I increase the tenure to 36 months?",
    "What if I invest ₹15000?",
    "What if I invest 1 lakh?",
]

for message in tests:

    print("\nMESSAGE:")
    print(message)

    print("Amount:", extract_number(message))
    print("Rate:", extract_percentage(message))
    print("Months:", extract_months(message))
    print("Years:", extract_years(message))
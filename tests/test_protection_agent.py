from agents.protection_agent import analyze_protection


result = analyze_protection(
    user_id="demo_user_001",
    user_message=(
        "Do I have enough insurance for my family?"
    ),
    required_life_cover=3_000_000,
    existing_life_cover=1_000_000,
    health_cover=500_000,
    dependents=2,
    annual_income=80_000 * 12,
)


print("\nPROTECTION AGENT TEST")
print("=====================")

print("\nANALYSIS")
print(result["analysis"])

print("\nRESPONSE")
print(result["response"])
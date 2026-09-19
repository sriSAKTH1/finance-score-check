from rules.insurance_rules import evaluate_insurance


result = evaluate_insurance(
    required_life_cover=3_000_000,
    existing_life_cover=1_000_000,
    health_cover=500_000,
    dependents=2,
)

print("\nINSURANCE RULE TEST")
print("===================")

for name, finding in result.items():
    print(f"\n{name}")
    print(f"Status : {finding['status']}")
    print(f"Message: {finding['message']}")
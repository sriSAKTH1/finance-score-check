from rules.tax_rules import evaluate_tax


result = evaluate_tax(
    gross_income=1_200_000,
    deductions=150_000,
    tax_rate=20,
    estimated_tax=210_000,
)


print("\nTAX RULE TEST")
print("=============")

for name, finding in result.items():

    print(f"\n{name}")

    print(
        f"Status : {finding['status']}"
    )

    print(
        f"Message: {finding['message']}"
    )

    if "tax_to_income_percent" in finding:
        print(
            f"Tax / Income: "
            f"{finding['tax_to_income_percent']}%"
        )
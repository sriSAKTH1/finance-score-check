from rules.retirement_rules import evaluate_retirement


result = evaluate_retirement(
    years_to_retirement=27,
    required_corpus=10_000_000,
    projected_corpus=7_500_000,
    inflation_rate=6,
    expected_return=10,
)


print("\nRETIREMENT RULE TEST")
print("====================")

for name, finding in result.items():

    print(f"\n{name}")

    if isinstance(finding, list):

        for item in finding:
            print(
                f"Status : {item['status']}"
            )
            print(
                f"Message: {item['message']}"
            )

    else:

        print(
            f"Status : {finding['status']}"
        )

        print(
            f"Message: {finding['message']}"
        )
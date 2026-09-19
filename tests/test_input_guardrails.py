from guardrails.input_guardrails import (
    validate_financial_inputs,
)


tests = [
    (
        "VALID INVESTMENT",
        {
            "monthly_investment": 10000,
            "annual_return": 10,
            "years": 10,
        },
        True,
    ),
    (
        "NEGATIVE INVESTMENT",
        {
            "monthly_investment": -10000,
            "annual_return": 10,
            "years": 10,
        },
        False,
    ),
    (
        "ZERO YEARS",
        {
            "monthly_investment": 10000,
            "annual_return": 10,
            "years": 0,
        },
        False,
    ),
    (
        "NEGATIVE INFLATION",
        {
            "monthly_investment": 10000,
            "annual_return": 10,
            "inflation_rate": -5,
            "years": 10,
        },
        False,
    ),
    (
        "VALID LOAN",
        {
            "loan_amount": 100000,
            "interest_rate": 12,
            "tenure_months": 24,
        },
        True,
    ),
]


passed = 0
failed = 0

for name, inputs, expected in tests:

    result = validate_financial_inputs(inputs)

    actual = result["valid"]

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    print("INPUT:", inputs)
    print("VALID:", actual)
    print("ERRORS:", result["errors"])

    if actual == expected:
        print("RESULT: PASS")
        passed += 1
    else:
        print("RESULT: FAIL")
        failed += 1


print("\n" + "=" * 60)
print("INPUT GUARDRAIL SUMMARY")
print("=" * 60)

print("Total :", passed + failed)
print("Passed:", passed)
print("Failed:", failed)

if failed == 0:
    print("\nALL INPUT GUARDRAIL TESTS PASSED")
else:
    print("\nINPUT GUARDRAIL TESTS NEED REVIEW")
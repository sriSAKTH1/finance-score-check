from guardrails.assumption_guardrails import (
    evaluate_assumptions,
)


tests = [
    (
        "NORMAL RETURN",
        {
            "annual_return": 10,
        },
        0,
    ),
    (
        "HIGH RETURN",
        {
            "annual_return": 20,
        },
        1,
    ),
    (
        "EXTREME RETURN",
        {
            "annual_return": 100,
        },
        1,
    ),
    (
        "HIGH INTEREST",
        {
            "interest_rate": 25,
        },
        1,
    ),
    (
        "EXTREME INTEREST",
        {
            "interest_rate": 50,
        },
        1,
    ),
    (
        "HIGH INFLATION",
        {
            "inflation_rate": 20,
        },
        1,
    ),
]


passed = 0
failed = 0

for name, assumptions, expected_warnings in tests:

    result = evaluate_assumptions(assumptions)

    actual_warnings = len(result["warnings"])

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    print("ASSUMPTIONS:", assumptions)
    print("WARNINGS:", actual_warnings)

    for warning in result["warnings"]:
        print("⚠️", warning)

    if actual_warnings == expected_warnings:
        print("RESULT: PASS")
        passed += 1
    else:
        print("RESULT: FAIL")
        failed += 1


print("\n" + "=" * 60)
print("ASSUMPTION GUARDRAIL SUMMARY")
print("=" * 60)

print("Total :", passed + failed)
print("Passed:", passed)
print("Failed:", failed)

if failed == 0:
    print("\nALL ASSUMPTION GUARDRAIL TESTS PASSED")
else:
    print("\nASSUMPTION GUARDRAIL TESTS NEED REVIEW")
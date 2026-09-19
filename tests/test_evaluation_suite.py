import os

os.environ["FINAI_TEST_MODE"] = "1"

from graph.workflow import app


USER_ID = "demo_user_001"


def run_test(name, session_id, message, expected_intent):
    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    result = app.invoke({
        "user_id": USER_ID,
        "session_id": session_id,
        "user_message": message,
    })

    actual_intent = result.get("intent")
    errors = result.get("errors")

    print("Question:")
    print(message)

    print("\nExpected intent:")
    print(expected_intent)

    print("Actual intent:")
    print(actual_intent)

    print("Errors:")
    print(errors)

    passed = (
        actual_intent == expected_intent
        and errors in (None, [])
    )

    print("\nRESULT:")
    print("PASS" if passed else "FAIL")

    return passed, result


def main():

    tests = [
        (
            "TEST 1 - Debt",
            "eval-debt-001",
            "Can I take a loan of ₹50000?",
            "DEBT",
        ),
        (
            "TEST 2 - Cash Flow",
            "eval-cashflow-001",
            "How much money do I save every month?",
            "CASHFLOW",
        ),
        (
            "TEST 3 - Goal",
            "eval-goal-001",
            "Will I have enough money for my child's education?",
            "GOAL",
        ),
        (
            "TEST 4 - Investment",
            "eval-investment-001",
            "Should I invest my money?",
            "INVESTMENT",
        ),
        (
            "TEST 5 - Insurance",
            "eval-insurance-001",
            "Do I have enough insurance?",
            "INSURANCE",
        ),
        (
            "TEST 6 - Retirement",
            "eval-retirement-001",
            "Will I have enough money for retirement?",
            "RETIREMENT",
        ),
        (
            "TEST 7 - Tax",
            "eval-tax-001",
            "How can I reduce my tax?",
            "TAX",
        ),
        (
            "TEST 8 - Scenario",
            "eval-scenario-001",
            "What if I invest ₹15000?",
            "SCENARIO",
        ),
        (
            "TEST 9 - Financial Health",
            "eval-health-001",
            "How is my financial health?",
            "FINANCIAL_HEALTH",
        ),
    ]

    passed = 0
    failed = 0

    for test in tests:

        name, session_id, message, expected = test

        success, _ = run_test(
            name,
            session_id,
            message,
            expected,
        )

        if success:
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    print(f"Total : {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed == 0:
        print("\nALL BASIC EVALUATION TESTS PASSED")
    else:
        print("\nSOME EVALUATION TESTS FAILED")


if __name__ == "__main__":
    main()
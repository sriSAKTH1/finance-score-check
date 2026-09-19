import os

os.environ["FINAI_TEST_MODE"] = "1"
os.environ["FINAI_STRICT_INPUT_TEST_MODE"] = "1"

from graph.workflow import app


USER_ID = "demo_user_001"


def run_test(name, session_id, message, expected_missing):

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    print("USER:")
    print(message)

    result = app.invoke({
        "user_id": USER_ID,
        "session_id": session_id,
        "user_message": message,
    })

    print("\nINTENT:")
    print(result.get("intent"))

    print("\nMISSING INFORMATION:")
    print(result.get("missing_information"))

    print("\nFINAL RESPONSE:")
    print(result.get("final_response"))

    missing = result.get("missing_information", [])

    for field in expected_missing:
        assert field in missing, (
            f"Expected missing field '{field}' "
            f"but got {missing}"
        )

    print("\nRESULT: PASS")

    return result


def main():

    passed = 0
    failed = 0

    # ================================================================
    # TEST 1
    # Loan amount only
    # ================================================================

    try:

        run_test(
            "TEST 1 - Missing Interest Rate and Tenure",
            "missing-data-001",
            "Can I take a loan of ₹50000?",
            [
                "interest rate",
                "loan tenure",
            ],
        )

        passed += 1

    except Exception as e:

        print("\nRESULT: FAIL")
        print("Error:", e)

        failed += 1


    # ================================================================
    # TEST 2
    # Loan amount + interest rate
    # ================================================================

    try:

        run_test(
            "TEST 2 - Missing Tenure",
            "missing-data-002",
            "Can I take a loan of ₹100000 at 10% interest?",
            [
                "loan tenure",
            ],
        )

        passed += 1

    except Exception as e:

        print("\nRESULT: FAIL")
        print("Error:", e)

        failed += 1


    # ================================================================
    # TEST 3
    # Loan amount + tenure
    # ================================================================

    try:

        run_test(
            "TEST 3 - Missing Interest Rate",
            "missing-data-003",
            "Can I take a loan of ₹100000 for 36 months?",
            [
                "interest rate",
            ],
        )

        passed += 1

    except Exception as e:

        print("\nRESULT: FAIL")
        print("Error:", e)

        failed += 1


    # ================================================================
    # SUMMARY
    # ================================================================

    print("\n" + "=" * 70)
    print("MISSING DATA EVALUATION SUMMARY")
    print("=" * 70)

    print("Total :", 3)
    print("Passed:", passed)
    print("Failed:", failed)

    if failed == 0:

        print("\nALL MISSING DATA TESTS PASSED")

    else:

        print("\nSOME MISSING DATA TESTS FAILED")


if __name__ == "__main__":
    main()
from graph.workflow import app


USER_ID = "demo_user_001"
SESSION_ID = "eval-memory-001"


def run_test(message):
    print("\n" + "-" * 70)
    print("USER:", message)

    result = app.invoke({
        "user_id": USER_ID,
        "session_id": SESSION_ID,
        "user_message": message,
    })

    print("INTENT:", result.get("intent"))
    print("ERRORS:", result.get("errors"))

    if result.get("scenario_results"):
        scenario = result["scenario_results"][-1]
        print("SCENARIO:")
        print(scenario)

    return result


def get_assumptions(result):
    scenario = result["scenario_results"][-1]
    return scenario["scenario"]["assumptions"]


def main():

    print("=" * 70)
    print("SCENARIO + CONVERSATION MEMORY EVALUATION")
    print("=" * 70)

    # ================================================================
    # TEST 1
    # ================================================================

    result1 = run_test(
        "What if I take a loan of 100000?"
    )

    assert result1["intent"] == "SCENARIO"
    assert not result1.get("errors")

    assumptions1 = get_assumptions(result1)

    print("\nTEST 1 ASSUMPTIONS:")
    print(assumptions1)

    assert assumptions1["loan_amount"] == 100000
    assert assumptions1["interest_rate"] == 12
    assert assumptions1["tenure_months"] == 24

    print("TEST 1: PASS")


    # ================================================================
    # TEST 2
    # Change interest rate only
    # ================================================================

    result2 = run_test(
        "What if I reduce the interest rate to 10%?"
    )

    assert result2["intent"] == "SCENARIO"
    assert not result2.get("errors")

    assumptions2 = get_assumptions(result2)

    print("\nTEST 2 ASSUMPTIONS:")
    print(assumptions2)

    # Loan amount must be remembered
    assert assumptions2["loan_amount"] == 100000

    # Interest rate must change
    assert assumptions2["interest_rate"] == 10

    # Tenure must be remembered
    assert assumptions2["tenure_months"] == 24

    print("TEST 2: PASS")


    # ================================================================
    # TEST 3
    # Change tenure only
    # ================================================================

    result3 = run_test(
        "What if I increase the tenure to 36 months?"
    )

    assert result3["intent"] == "SCENARIO"
    assert not result3.get("errors")

    assumptions3 = get_assumptions(result3)

    print("\nTEST 3 ASSUMPTIONS:")
    print(assumptions3)

    # Loan amount must still be remembered
    assert assumptions3["loan_amount"] == 100000

    # Interest rate must still be remembered
    assert assumptions3["interest_rate"] == 10

    # Tenure must change
    assert assumptions3["tenure_months"] == 36

    print("TEST 3: PASS")


    # ================================================================
    # FINAL RESULT
    # ================================================================

    print("\n" + "=" * 70)
    print("SCENARIO MEMORY EVALUATION SUMMARY")
    print("=" * 70)

    print("Test 1 - Initial scenario      : PASS")
    print("Test 2 - Remember + change rate: PASS")
    print("Test 3 - Remember + change term: PASS")

    print("\nALL SCENARIO MEMORY TESTS PASSED")


if __name__ == "__main__":
    main()
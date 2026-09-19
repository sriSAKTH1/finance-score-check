import os

os.environ["FINAI_TEST_MODE"] = "1"
os.environ["FINAI_STRICT_INPUT_TEST_MODE"] = "1"

from agents.loan_parser import LoanRequest


def run_invalid_loan(
    name,
    loan_amount,
    interest_rate,
    tenure_months,
):

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    print("Loan amount   :", loan_amount)
    print("Interest rate :", interest_rate)
    print("Tenure        :", tenure_months)

    try:

        LoanRequest(
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            tenure_months=tenure_months,
        )

        print("\nRESULT: FAIL")
        print("Invalid input was accepted.")

        return False

    except Exception as e:

        print("\nValidation correctly rejected input.")
        print("Error type:", type(e).__name__)

        print("\nRESULT: PASS")

        return True


def main():

    tests = [

        (
            "TEST 1 - Zero Loan Amount",
            0,
            12,
            24,
        ),

        (
            "TEST 2 - Negative Loan Amount",
            -50000,
            12,
            24,
        ),

        (
            "TEST 3 - Negative Interest Rate",
            100000,
            -5,
            24,
        ),

        (
            "TEST 4 - Zero Tenure",
            100000,
            12,
            0,
        ),

        (
            "TEST 5 - Negative Tenure",
            100000,
            12,
            -12,
        ),
    ]

    passed = 0
    failed = 0

    for (
        name,
        loan_amount,
        interest_rate,
        tenure_months,
    ) in tests:

        try:

            success = run_invalid_loan(
                name,
                loan_amount,
                interest_rate,
                tenure_months,
            )

            if success:
                passed += 1
            else:
                failed += 1

        except Exception as e:

            print("\nUnexpected error:", e)

            failed += 1

    print("\n" + "=" * 70)
    print("INVALID INPUT EVALUATION SUMMARY")
    print("=" * 70)

    print("Total :", len(tests))
    print("Passed:", passed)
    print("Failed:", failed)

    if failed == 0:

        print("\nALL INVALID INPUT TESTS PASSED")

    else:

        print("\nSOME INVALID INPUT TESTS FAILED")


if __name__ == "__main__":
    main()
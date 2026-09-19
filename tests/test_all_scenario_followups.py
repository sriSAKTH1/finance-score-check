from graph.workflow import app


# ============================================================
# HELPER
# ============================================================

def run_test(
    session_id,
    first_message,
    second_message,
):

    print("\n")
    print("=" * 60)
    print("SESSION:", session_id)
    print("=" * 60)

    # --------------------------------------------------------
    # FIRST MESSAGE
    # --------------------------------------------------------

    first_result = app.invoke({
        "session_id": session_id,
        "user_id": "demo_user_001",
        "user_message": first_message,
    })

    print("\nFIRST:")
    print(first_message)

    print("\nINTENT:")
    print(first_result.get("intent"))

    print("\nSCENARIO:")
    print(first_result.get("scenario_results"))

    # --------------------------------------------------------
    # SECOND MESSAGE
    # --------------------------------------------------------

    second_result = app.invoke({
        "session_id": session_id,
        "user_id": "demo_user_001",
        "user_message": second_message,
    })

    print("\nSECOND:")
    print(second_message)

    print("\nINTENT:")
    print(second_result.get("intent"))

    print("\nPREVIOUS SCENARIO:")
    print(second_result.get("last_scenario"))

    print("\nNEW SCENARIO:")
    print(second_result.get("scenario_results"))

    print("\nERRORS:")
    print(second_result.get("errors"))


# ============================================================
# INVESTMENT
# ============================================================

run_test(
    "investment-followup-001",

    "What if I invest 10000?",

    "What if I increase it to 15000?",
)


# ============================================================
# GOAL
# ============================================================

run_test(
    "goal-followup-001",

    "What if I increase my goal investment to 10000?",

    "What if I increase it to 15000?",
)


# ============================================================
# LOAN
# ============================================================

run_test(
    "loan-followup-001",

    "What if I take a loan of 50000?",

    "What if I change it to 100000?",
)


# ============================================================
# RETIREMENT
# ============================================================

run_test(
    "retirement-followup-001",

    "What if I retire at 50?",

    "What if I change it to 55?",
)
from graph.workflow import app


def run(session_id, message):

    result = app.invoke({
        "user_id": "demo_user_001",
        "session_id": session_id,
        "user_message": message,
    })

    print("\n" + "=" * 60)
    print(message)
    print("=" * 60)

    print("INTENT:")
    print(result.get("intent"))

    print("SCENARIO:")
    print(result.get("scenario_results"))

    print("ERRORS:")
    print(result.get("errors"))


# ============================================================
# LOAN MULTI-PARAMETER TEST
# ============================================================

session = "multi-loan-001"

run(
    session,
    "What if I take a loan of 100000?"
)

run(
    session,
    "What if I reduce the interest rate to 10%?"
)

run(
    session,
    "What if I increase the tenure to 36 months?"
)

import os

os.environ["FINAI_TEST_MODE"] = "1"
os.environ["FINAI_STRICT_INPUT_TEST_MODE"] = "1"

from graph.workflow import app


tests = [
    "What if I take a loan of ₹100000 at 50% for 12 months?",
    "What if I invest ₹10000 every month with 100% annual return for 10 years?",
]

for message in tests:

    print("\n" + "=" * 70)
    print("MESSAGE:", message)
    print("=" * 70)

    result = app.invoke({
        "user_id": "demo_user_001",
        "session_id": "debug-safety",
        "user_message": message,
    })

    print("\nINTENT:")
    print(result.get("intent"))

    print("\nSCENARIO TYPE:")
    print(result.get("scenario_type"))

    print("\nLAST SCENARIO:")
    print(result.get("last_scenario"))

    print("\nSCENARIO RESULTS:")
    print(result.get("scenario_results"))

    print("\nANALYSIS:")
    print(result.get("analysis"))

    print("\nFINAL RESPONSE:")
    print(repr(result.get("final_response")))

    print("\nERRORS:")
    print(result.get("errors"))
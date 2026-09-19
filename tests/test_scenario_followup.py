from graph.workflow import app


SESSION_ID = "scenario-followup-001"


# ============================================================
# FIRST QUESTION
# ============================================================

first_state = {
    "session_id": SESSION_ID,
    "user_id": "demo_user_001",

    "user_message":
        "What if I invest 10000?",
}


first_result = app.invoke(
    first_state
)


print("\nFIRST QUESTION")
print("==============")

print(
    first_result.get("intent")
)

print(
    first_result.get("scenario_results")
)


# ============================================================
# SECOND QUESTION
# ============================================================

second_state = {
    "session_id": SESSION_ID,
    "user_id": "demo_user_001",

    "user_message":
        "What if I increase it to 15000?",
}


second_result = app.invoke(
    second_state
)


print("\nSECOND QUESTION")
print("===============")

print(
    second_result.get("intent")
)

print("\nPREVIOUS SCENARIO")

print(
    second_result.get("last_scenario")
)

print("\nNEW SCENARIO")

print(
    second_result.get("scenario_results")
)

print("\nERRORS")

print(
    second_result.get("errors")
)
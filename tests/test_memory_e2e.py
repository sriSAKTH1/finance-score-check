from graph.workflow import app


SESSION_ID = "memory-e2e-001"


# ============================================================
# FIRST MESSAGE
# ============================================================

first_state = {
    "session_id": SESSION_ID,
    "user_id": "demo_user_001",
    "user_message": "What if I invest 10000?",
}

first_result = app.invoke(first_state)

print("\nFIRST REQUEST")
print("=============")

print("Intent:")
print(first_result.get("intent"))

print("Scenario:")
print(first_result.get("scenario_results"))

print("Errors:")
print(first_result.get("errors"))


# ============================================================
# SECOND MESSAGE
# ============================================================

second_state = {
    "session_id": SESSION_ID,
    "user_id": "demo_user_001",
    "user_message": "What if I increase it to 15000?",
}

second_result = app.invoke(second_state)

print("\nSECOND REQUEST")
print("==============")

print("Intent:")
print(second_result.get("intent"))

print("Previous intent:")
print(second_result.get("last_intent"))

print("Previous scenario:")
print(second_result.get("last_scenario"))

print("Scenario:")
print(second_result.get("scenario_results"))

print("Errors:")
print(second_result.get("errors"))


print("\nMEMORY E2E TEST COMPLETED")
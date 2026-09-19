from graph.workflow import build_workflow


workflow = build_workflow()


initial_state = {
    "user_id": "demo_user_001",
    "user_message": "Can I take a 50000 rupee loan?"
}


result = workflow.invoke(initial_state)


print("FINSOURCE WORKFLOW")
print("==================")

print("User:", result["user_id"])

print(
    "Intent:",
    result["intent"]
)

print(
    "Monthly Income:",
    result["financial_context"]
    ["income"]["monthly_salary"]
)

print(
    "Risk Profile:",
    result["financial_context"]
    ["risk_profile"]["category"]
)
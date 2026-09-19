from graph.workflow import build_workflow


workflow = build_workflow()


result = workflow.invoke(
    {
        "user_id": "demo_user_001",
        "user_message": "Can I take a ₹50,000 loan at 12% for 24 months?"
    }
)


print("\nFINSOURCE END-TO-END")
print("============================")

print("\nINTENT")
print(result.get("intent"))

print("\nLOAN REQUEST")
print(result.get("loan_request"))

print("\nFINAL RESPONSE")
print(result.get("final_response"))
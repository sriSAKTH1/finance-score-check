from graph.workflow import build_workflow


workflow = build_workflow()


result = workflow.invoke(
    {
        "user_id": "demo_user_001",
        "user_message": (
            "I have ₹4 lakh for my child's education. "
            "Is it enough?"
        )
    }
)


print("\nFINSOURCE GOAL END-TO-END")
print("============================")

print("\nINTENT")
print(result.get("intent"))

print("\nFINAL RESPONSE")
print(result.get("final_response"))
from graph.workflow import build_workflow


workflow = build_workflow()


result = workflow.invoke(
    {
        "user_id": "demo_user_001",
        "user_message": (
            "Do I have enough life insurance and "
            "health insurance for my family?"
        ),
    }
)


print("\nFINSOURCE PROTECTION END-TO-END")
print("================================")

print("\nINTENT")
print(result.get("intent"))

print("\nFINAL RESPONSE")
print(result.get("final_response"))
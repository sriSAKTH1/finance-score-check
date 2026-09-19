from graph.workflow import build_workflow


workflow = build_workflow()


result = workflow.invoke(
    {
        "user_id": "demo_user_001",
        "user_message": (
            "How does tax affect my savings "
            "and investment returns?"
        ),
    }
)


print("\nFINSOURCE TAX END-TO-END")
print("========================")

print("\nINTENT")
print(result.get("intent"))

print("\nFINAL RESPONSE")
print(result.get("final_response"))
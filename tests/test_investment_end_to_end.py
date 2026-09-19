from graph.workflow import build_workflow


workflow = build_workflow()


result = workflow.invoke(
    {
        "user_id": "demo_user_001",
        "user_message": (
            "I have ₹2,50,000 invested and can invest "
            "₹10,000 every month for 10 years."
        ),
    }
)


print("\nFINSOURCE INVESTMENT END-TO-END")
print("===============================")

print("\nINTENT")
print(result.get("intent"))

print("\nFINAL RESPONSE")
print(result.get("final_response"))
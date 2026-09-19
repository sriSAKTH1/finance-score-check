from graph.workflow import app


print("=" * 60)
print("FINANCIAL HEALTH WORKFLOW TEST")
print("=" * 60)

result = app.invoke({
    "user_id": "demo_user_001",
    "session_id": "financial-health-001",
    "user_message": "How is my financial health?",
})

print("\nINTENT:")
print(result.get("intent"))

print("\nFINANCIAL HEALTH:")
print(result.get("financial_health"))

print("\nFINAL RESPONSE:")
print(result.get("final_response"))

print("\nERRORS:")
print(result.get("errors"))
from graph.financial_health_nodes import collect_financial_health_data


state = {
    "user_id": "demo_user_001"
}

result = collect_financial_health_data(state)

print("=" * 60)
print("FINANCIAL HEALTH DATA")
print("=" * 60)

print(result)
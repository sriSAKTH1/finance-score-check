from agents.financial_health_agent import analyze_financial_health
from graph.financial_health_nodes import collect_financial_health_data


state = {
    "user_id": "demo_user_001"
}

collected = collect_financial_health_data(state)

result = analyze_financial_health(
    financial_context={},
    financial_health_data=collected["financial_health_data"],
)

print("=" * 60)
print("FINANCIAL HEALTH ANALYSIS")
print("=" * 60)

print("\nOverall Status:")
print(result["overall_status"])

print("\nSummary:")
print(result["summary"])

print("\nMetrics:")
print(result["metrics"])

print("\nFindings:")

for finding in result["findings"]:
    print(
        f"- {finding['area']}: "
        f"{finding['status']} → "
        f"{finding['message']}"
    )
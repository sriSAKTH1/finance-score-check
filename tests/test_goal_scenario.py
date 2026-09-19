from scenarios.scenario_engine import run_goal_scenario
from schemas.scenario import ScenarioInput


scenario = ScenarioInput(
    name="Increase Monthly Investment",
    monthly_investment=10_000,
    annual_return=10,
    years=12,
)

result = run_goal_scenario(
    current_corpus=400_000,
    monthly_contribution=5_000,
    target_amount=2_000_000,
    annual_return=10,
    inflation_rate=6,
    years=12,
    scenario=scenario,
)

print("\nGOAL SCENARIO TEST")
print("===================")

print("\nBASELINE")
print(result.baseline)

print("\nSCENARIO")
print(result.scenario)

print("\nDIFFERENCES")
print(result.differences)
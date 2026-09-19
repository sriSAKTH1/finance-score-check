from scenarios.scenario_engine import run_retirement_scenario
from schemas.scenario import ScenarioInput


scenario = ScenarioInput(
    name="Retire Earlier At 50",
    retirement_age=50,
    annual_return=10,
)

result = run_retirement_scenario(
    current_age=28,
    retirement_age=55,
    current_monthly_expense=45_000,
    inflation_rate=6,
    years_in_retirement=25,
    current_corpus=500_000,
    annual_return=10,
    scenario=scenario,
)


print("\nRETIREMENT SCENARIO TEST")
print("========================")

print("\nBASELINE")
print(result.baseline)

print("\nSCENARIO")
print(result.scenario)

print("\nDIFFERENCES")
print(result.differences)
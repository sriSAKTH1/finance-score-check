from schemas.scenario import ScenarioInput

from scenarios.scenario_engine import (
    run_investment_scenario,
)


scenario = ScenarioInput(
    name="Increase Monthly Investment",

    monthly_investment=15_000,

    annual_return=10,

    years=10,
)


result = run_investment_scenario(
    current_investment=250_000,
    monthly_investment=10_000,
    annual_return=10,
    years=10,
    scenario=scenario,
)


print("\nSCENARIO ENGINE TEST")
print("====================")

print("\nBASELINE")

print(
    result.baseline.model_dump()
)


print("\nSCENARIO")

print(
    result.scenario.model_dump()
)


print("\nDIFFERENCES")

print(
    result.differences
)
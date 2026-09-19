from schemas.scenario import ScenarioResult

from scenarios.comparator import (
    compare_scenarios,
)


baseline = ScenarioResult(
    scenario_name="Baseline",
    metrics={
        "projected_value": 2_000_000,
        "total_contributions": 1_450_000,
    },
    assumptions={
        "annual_return": 10,
        "years": 10,
    },
)


scenario = ScenarioResult(
    scenario_name="Higher Monthly Investment",
    metrics={
        "projected_value": 2_700_000,
        "total_contributions": 2_050_000,
    },
    assumptions={
        "annual_return": 10,
        "years": 10,
    },
)


result = compare_scenarios(
    baseline=baseline,
    scenario=scenario,
)


print("\nSCENARIO COMPARATOR TEST")
print("========================")

print("\nBASELINE")
print(result.baseline.model_dump())

print("\nSCENARIO")
print(result.scenario.model_dump())

print("\nDIFFERENCES")
print(result.differences)
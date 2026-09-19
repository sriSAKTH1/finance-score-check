from schemas.scenario import (
    ScenarioResult,
    ScenarioComparison,
)


def compare_scenarios(
    baseline: ScenarioResult,
    scenario: ScenarioResult,
):
    """
    Compare baseline and alternative scenario metrics.

    Only metrics present in both scenarios are compared.
    """

    differences = {}

    common_metrics = set(
        baseline.metrics.keys()
    ).intersection(
        scenario.metrics.keys()
    )

    for metric in common_metrics:

        baseline_value = baseline.metrics[metric]
        scenario_value = scenario.metrics[metric]

        differences[metric] = (
            scenario_value - baseline_value
        )

    return ScenarioComparison(
        baseline=baseline,
        scenario=scenario,
        differences=differences,
    )
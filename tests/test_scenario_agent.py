import os

import pytest

from agents.scenario_agent import analyze_investment_scenario


@pytest.mark.skipif(
    os.getenv("SCENARIO_TEST_MODE", "false").lower() != "true",
    reason="Scenario agent live Gemini test disabled",
)
def test_investment_scenario():

    result = analyze_investment_scenario(
        "What if I increase my monthly investment to 15000?"
    )

    assert result is not None
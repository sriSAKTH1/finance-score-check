from agents.goal_agent import analyze_goal


result = analyze_goal(
    user_id="demo_user_001",
    user_message="I have ₹4 lakh for my child's education. Is it enough?",
    goal_name="Child Education",
    current_corpus=400000,
    target_amount=2000000,
    years=12,
    monthly_contribution=5000,
)


print("\nFINSOURCE GOAL AGENT")
print("============================")

print("\nGOAL")
print("----------------------------")

goal = result["analysis"]["goal"]

print("Goal:", goal["name"])
print("Current Corpus:", goal["current_corpus"])
print("Target Amount:", goal["target_amount"])
print("Years:", goal["years"])
print("Monthly Contribution:", goal["monthly_contribution"])


print("\nCALCULATED DATA")
print("----------------------------")

calculations = result["analysis"]["calculations"]

print(
    "Future Value of Current Corpus:",
    round(
        calculations["current_corpus_future_value"],
        2
    )
)

print(
    "Projected Corpus:",
    round(
        calculations["projected_corpus"],
        2
    )
)

print(
    "Inflation Adjusted Target:",
    round(
        calculations["inflation_adjusted_target"],
        2
    )
)

print(
    "Required Monthly Contribution:",
    round(
        calculations["required_monthly_contribution_nominal"],
        2
    )
)

print(
    "Nominal Goal Gap:",
    round(
        calculations["nominal_goal_gap"],
        2
    )
)


print("\nAI ANALYSIS")
print("----------------------------")

print(result["response"])
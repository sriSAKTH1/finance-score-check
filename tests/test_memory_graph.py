from graph.state import FinancialState

from graph.memory_nodes import (
    load_conversation_memory,
    save_conversation_memory,
    conversation_memory,
)


# ============================================================
# FIRST MESSAGE
# ============================================================

state: FinancialState = {
    "session_id": "memory-demo-001",
    "user_id": "demo_user_001",
    "user_message": "What if I invest 10000?",
    "intent": "SCENARIO",
    "scenario_results": [
        {
            "type": "investment",
            "monthly_investment": 10000,
        }
    ],
    "final_response": "Scenario calculated.",
}


# ============================================================
# SAVE
# ============================================================

save_conversation_memory(state)


# ============================================================
# LOAD
# ============================================================

loaded_state = load_conversation_memory(
    {
        "session_id": "memory-demo-001",
        "user_id": "demo_user_001",
        "user_message": "What if I increase it?",
    }
)


# ============================================================
# OUTPUT
# ============================================================

print("\nGRAPH MEMORY TEST")
print("=================")

print("\nCONVERSATION HISTORY:")
print(
    loaded_state["conversation_history"]
)

print("\nLAST INTENT:")
print(
    loaded_state["last_intent"]
)

print("\nLAST SCENARIO:")
print(
    loaded_state["last_scenario"]
)


print("\nMEMORY GRAPH TEST PASSED")
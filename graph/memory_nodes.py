from memory.conversation_memory import ConversationMemory

from graph.state import FinancialState


# ============================================================
# GLOBAL MEMORY INSTANCE
# ============================================================

conversation_memory = ConversationMemory()


# ============================================================
# LOAD MEMORY
# ============================================================

def load_conversation_memory(
    state: FinancialState,
):
    """
    Load previous conversation information
    into the current LangGraph state.
    """

    session_id = state.get(
        "session_id",
        state.get(
            "user_id",
            "default-session",
        ),
    )

    messages = conversation_memory.get_messages(
        session_id
    )

    last_intent = conversation_memory.get_last_intent(
        session_id
    )

    last_scenario = conversation_memory.get_last_scenario(
        session_id
    )

    scenario_type = None

    if last_scenario:

        scenario_type = last_scenario.get(
            "type"
        )

    return {
        "conversation_history": messages,
        "last_intent": last_intent,
        "last_scenario": last_scenario,
        "scenario_type": scenario_type,
    }


# ============================================================
# SAVE MEMORY
# ============================================================

def save_conversation_memory(
    state: FinancialState,
):
    """
    Save current conversation information.
    """

    session_id = state.get(
        "session_id",
        state.get(
            "user_id",
            "default-session",
        ),
    )

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    user_message = state.get(
        "user_message"
    )

    if user_message:

        conversation_memory.add_message(
            session_id=session_id,
            role="user",
            content=user_message,
        )

    # --------------------------------------------------------
    # INTENT
    # --------------------------------------------------------

    intent = state.get(
        "intent"
    )

    if intent:

        conversation_memory.set_last_intent(
            session_id=session_id,
            intent=intent,
        )

    # --------------------------------------------------------
    # SCENARIO
    # --------------------------------------------------------

    scenario_results = state.get(
        "scenario_results",
        []
    )

    if scenario_results:

        latest_scenario = scenario_results[-1]

        conversation_memory.set_last_scenario(
            session_id=session_id,
            scenario=latest_scenario,
        )

    # --------------------------------------------------------
    # AI RESPONSE
    # --------------------------------------------------------

    final_response = state.get(
        "final_response"
    )

    if final_response:

        conversation_memory.add_message(
            session_id=session_id,
            role="assistant",
            content=final_response,
        )

    return {}
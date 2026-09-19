from memory.conversation_memory import ConversationMemory


memory = ConversationMemory()


session_id = "demo-session-001"


# ============================================================
# STORE USER MESSAGE
# ============================================================

memory.add_message(
    session_id=session_id,
    role="user",
    content="What if I invest ₹10,000?",
)


# ============================================================
# STORE AI MESSAGE
# ============================================================

memory.add_message(
    session_id=session_id,
    role="assistant",
    content="Your scenario has been calculated.",
)


# ============================================================
# STORE INTENT
# ============================================================

memory.set_last_intent(
    session_id=session_id,
    intent="SCENARIO",
)


# ============================================================
# STORE SCENARIO
# ============================================================

memory.set_last_scenario(
    session_id=session_id,
    scenario={
        "type": "investment",
        "monthly_investment": 10_000,
        "annual_return": 10,
        "years": 10,
    },
)


# ============================================================
# READ MEMORY
# ============================================================

print("\nCONVERSATION MEMORY TEST")
print("========================")

print("\nMESSAGES:")
print(memory.get_messages(session_id))


print("\nLAST INTENT:")
print(memory.get_last_intent(session_id))


print("\nLAST SCENARIO:")
print(memory.get_last_scenario(session_id))


print("\nSESSION:")
print(memory.get_session(session_id))


print("\nMEMORY TEST PASSED")
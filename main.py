from graph.workflow import graph


USER_ID = "demo_user_001"
SESSION_ID = "terminal-session-001"


def run_agent(user_message: str, conversation_history: list[dict]):

    state = {
        "user_id": USER_ID,
        "session_id": SESSION_ID,
        "user_message": user_message,
        "conversation_history": conversation_history,
    }

    result = graph.invoke(state)

    response = result.get("final_response")

    if not response:
        print("\nDEBUG: Agent returned no final response")
        print("DEBUG errors:", result.get("errors"))
        print("DEBUG intent:", result.get("intent"))
        print("DEBUG tool_results:", result.get("tool_results"))
        print("DEBUG rule_findings:", result.get("rule_findings"))
        print("DEBUG rag_results:", result.get("rag_results"))

        response = "I could not generate a response."

    return result, response


def main():

    print("=" * 60)
    print("              FinSource AI Agent")
    print("=" * 60)

    print("\nType 'exit' to quit.")
    print("Type 'clear' to start a new conversation.\n")

    conversation_history = []

    while True:

        user_message = input("You: ").strip()

        if not user_message:
            continue

        if user_message.lower() == "exit":
            print("\nFinSource: Goodbye!")
            break

        if user_message.lower() == "clear":

            conversation_history = []

            print("\nFinSource: Conversation cleared.\n")
            continue

        try:

            result, response = run_agent(
                user_message,
                conversation_history,
            )

            print("\nFinSource:")
            print(response)
            print()

            # Store the conversation
            conversation_history.append(
                {
                    "role": "user",
                    "content": user_message,
                }
            )

            conversation_history.append(
                {
                    "role": "assistant",
                    "content": response,
                }
            )

        except Exception as exc:

            print("\nFinSource: An error occurred.")
            print(f"Error: {exc}\n")


if __name__ == "__main__":
    main()
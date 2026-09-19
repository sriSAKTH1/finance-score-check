from typing import Any


class ConversationMemory:
    """
    Simple in-memory conversation store.

    This version is for development/testing.
    Later it can be replaced with Redis,
    PostgreSQL, or Supabase persistence.
    """

    def __init__(self):
        self.sessions: dict[str, dict[str, Any]] = {}

    # ========================================================
    # CREATE / GET SESSION
    # ========================================================

    def get_session(self, session_id: str) -> dict[str, Any]:
        """
        Get an existing session.

        If the session does not exist, create it.
        """

        if session_id not in self.sessions:

            self.sessions[session_id] = {
                "messages": [],
                "last_intent": None,
                "last_scenario": None,
                "financial_context": {},
            }

        return self.sessions[session_id]

    # ========================================================
    # ADD MESSAGE
    # ========================================================

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ):
        """
        Store a conversation message.
        """

        session = self.get_session(session_id)

        session["messages"].append(
            {
                "role": role,
                "content": content,
            }
        )

    # ========================================================
    # GET MESSAGES
    # ========================================================

    def get_messages(
        self,
        session_id: str,
    ) -> list[dict[str, str]]:
        """
        Return conversation messages.
        """

        session = self.get_session(session_id)

        return session["messages"]

    # ========================================================
    # LAST INTENT
    # ========================================================

    def set_last_intent(
        self,
        session_id: str,
        intent: str,
    ):
        """
        Store the most recent user intent.
        """

        session = self.get_session(session_id)

        session["last_intent"] = intent

    def get_last_intent(
        self,
        session_id: str,
    ) -> str | None:
        """
        Return the most recent intent.
        """

        session = self.get_session(session_id)

        return session["last_intent"]

    # ========================================================
    # LAST SCENARIO
    # ========================================================

    def set_last_scenario(
        self,
        session_id: str,
        scenario: dict[str, Any],
    ):
        """
        Store the most recent scenario.
        """

        session = self.get_session(session_id)

        session["last_scenario"] = scenario

    def get_last_scenario(
        self,
        session_id: str,
    ) -> dict[str, Any] | None:
        """
        Return the most recent scenario.
        """

        session = self.get_session(session_id)

        return session["last_scenario"]

    # ========================================================
    # FINANCIAL CONTEXT
    # ========================================================

    def set_financial_context(
        self,
        session_id: str,
        context: dict[str, Any],
    ):
        """
        Store financial context for the session.
        """

        session = self.get_session(session_id)

        session["financial_context"] = context

    def get_financial_context(
        self,
        session_id: str,
    ) -> dict[str, Any]:
        """
        Return stored financial context.
        """

        session = self.get_session(session_id)

        return session["financial_context"]

    # ========================================================
    # CLEAR SESSION
    # ========================================================

    def clear_session(
        self,
        session_id: str,
    ):
        """
        Delete a conversation session.
        """

        if session_id in self.sessions:
            del self.sessions[session_id]
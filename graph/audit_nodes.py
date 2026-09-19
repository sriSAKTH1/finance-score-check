from typing import Any

from audit.audit_logger import log_audit_event

from graph.state import FinancialState


def audit_request_node(
    state: FinancialState,
) -> dict[str, Any]:

    user_id = state.get(
        "user_id",
        "unknown",
    )

    session_id = state.get(
        "session_id",
        "unknown",
    )

    log_audit_event(
        user_id=user_id,
        session_id=session_id,
        event_type="REQUEST_RECEIVED",
        data={
            "intent": state.get("intent"),
        },
    )

    return {}


def audit_intent_node(
    state: FinancialState,
) -> dict[str, Any]:

    log_audit_event(
        user_id=state.get(
            "user_id",
            "unknown",
        ),
        session_id=state.get(
            "session_id",
            "unknown",
        ),
        event_type="INTENT_DETECTED",
        data={
            "intent": state.get("intent"),
        },
    )

    return {}


def audit_context_node(
    state: FinancialState,
) -> dict[str, Any]:

    context = state.get(
        "financial_context",
        {},
    )

    log_audit_event(
        user_id=state.get(
            "user_id",
            "unknown",
        ),
        session_id=state.get(
            "session_id",
            "unknown",
        ),
        event_type="FINANCIAL_CONTEXT_LOADED",
        data={
            "fields_available": list(
                context.keys()
            ),
        },
    )

    return {}


def audit_agent_node(
    state: FinancialState,
) -> dict[str, Any]:

    log_audit_event(
        user_id=state.get(
            "user_id",
            "unknown",
        ),
        session_id=state.get(
            "session_id",
            "unknown",
        ),
        event_type="AGENT_SELECTED",
        data={
            "intent": state.get("intent"),
            "scenario_type": state.get(
                "scenario_type"
            ),
        },
    )

    return {}


def audit_response_node(
    state: FinancialState,
) -> dict[str, Any]:

    response = state.get(
        "final_response"
    )

    log_audit_event(
        user_id=state.get(
            "user_id",
            "unknown",
        ),
        session_id=state.get(
            "session_id",
            "unknown",
        ),
        event_type="RESPONSE_GENERATED",
        data={
            "response_generated": response is not None,
            "response_length": (
                len(response)
                if response
                else 0
            ),
            "errors": state.get(
                "errors",
                [],
            ),
        },
    )

    log_audit_event(
        user_id=state.get(
            "user_id",
            "unknown",
        ),
        session_id=state.get(
            "session_id",
            "unknown",
        ),
        event_type="RESPONSE_AUDITED",
        data={
            "response_generated": response is not None,
            "response_length": (
                len(response)
                if response
                else 0
            ),
            "errors": state.get(
                "errors",
                [],
            ),
        },
    )

    return {}
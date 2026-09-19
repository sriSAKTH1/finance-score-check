from collections import Counter
from typing import Any

from audit.audit_reader import read_audit_events


def get_total_requests() -> int:
    """Return the total number of requests received."""

    events = read_audit_events()

    return sum(
        1
        for event in events
        if event.get("event_type") == "REQUEST_RECEIVED"
    )


def get_intent_counts() -> dict[str, int]:
    """Return the number of requests for each detected intent."""

    events = read_audit_events()

    intents = Counter()

    for event in events:
        if event.get("event_type") == "INTENT_DETECTED":
            intent = event.get("data", {}).get("intent")

            if intent:
                intents[intent] += 1

    return dict(intents)


def get_agent_counts() -> dict[str, int]:
    """Return the number of times each agent was selected."""

    events = read_audit_events()

    agents = Counter()

    for event in events:
        if event.get("event_type") == "AGENT_SELECTED":
            agent = event.get("data", {}).get("intent")

            if agent:
                agents[agent] += 1

    return dict(agents)


def get_tool_success_rate() -> float:
    """Return successful tool executions as a percentage."""

    events = read_audit_events()

    tool_events = [
        event
        for event in events
        if event.get("event_type") == "TOOL_EXECUTED"
    ]

    if not tool_events:
        return 0.0

    successful = sum(
        1
        for event in tool_events
        if event.get("data", {}).get("success") is True
    )

    return round(
        (successful / len(tool_events)) * 100,
        2,
    )


def get_rule_results() -> dict[str, int]:
    """Return rule evaluation result counts."""

    events = read_audit_events()

    results = Counter()

    for event in events:
        if event.get("event_type") == "RULE_EVALUATED":
            result = event.get("data", {}).get("result")

            if result:
                results[result] += 1

    return dict(results)


def get_rag_usage() -> int:
    """Return the number of RAG retrieval events."""

    events = read_audit_events()

    return sum(
        1
        for event in events
        if event.get("event_type") == "RAG_RETRIEVED"
    )


def get_error_count() -> int:
    """Return the number of audit events containing errors."""

    events = read_audit_events()

    count = 0

    for event in events:
        data: dict[str, Any] = event.get("data", {})

        errors = data.get("errors")

        if errors:
            count += 1

    return count
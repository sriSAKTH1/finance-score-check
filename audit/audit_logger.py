from datetime import datetime
from typing import Any
import json
from pathlib import Path


AUDIT_DIR = Path("data/audit")
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

AUDIT_FILE = AUDIT_DIR / "audit_log.jsonl"


def create_audit_event(
    user_id: str,
    session_id: str,
    event_type: str,
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create one audit event.
    """

    return {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "session_id": session_id,
        "event_type": event_type,
        "data": data or {},
    }


def log_audit_event(
    user_id: str,
    session_id: str,
    event_type: str,
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create and persist an audit event.
    """

    event = create_audit_event(
        user_id=user_id,
        session_id=session_id,
        event_type=event_type,
        data=data,
    )

    with open(
        AUDIT_FILE,
        "a",
        encoding="utf-8",
    ) as file:

        file.write(
            json.dumps(
                event,
                ensure_ascii=False,
                default=str,
            )
            + "\n"
        )

    return event


def log_tool_event(
    user_id: str,
    session_id: str,
    tool_name: str,
    success: bool,
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Log execution of a financial calculation/tool."""

    event_data = {
        "tool": tool_name,
        "success": success,
    }

    if data:
        event_data.update(data)

    return log_audit_event(
        user_id=user_id,
        session_id=session_id,
        event_type="TOOL_EXECUTED",
        data=event_data,
    )


def log_rule_event(
    user_id: str,
    session_id: str,
    rule_name: str,
    result: str,
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Log evaluation of a financial rule."""

    event_data = {
        "rule": rule_name,
        "result": result,
    }

    if data:
        event_data.update(data)

    return log_audit_event(
        user_id=user_id,
        session_id=session_id,
        event_type="RULE_EVALUATED",
        data=event_data,
    )


def log_rag_event(
    user_id: str,
    session_id: str,
    query: str,
    sources: list[str],
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Log NISM/RAG retrieval activity."""

    event_data = {
        "query": query,
        "sources": sources,
    }

    if data:
        event_data.update(data)

    return log_audit_event(
        user_id=user_id,
        session_id=session_id,
        event_type="RAG_RETRIEVED",
        data=event_data,
    )
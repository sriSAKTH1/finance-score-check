from typing import Any, Callable

from audit.audit_logger import log_tool_event


def execute_with_audit(
    tool: Callable,
    tool_name: str,
    user_id: str,
    session_id: str,
    *args: Any,
    **kwargs: Any,
) -> Any:
    """
    Execute a financial tool and automatically create an audit event.
    """

    try:
        result = tool(*args, **kwargs)

        log_tool_event(
            user_id=user_id,
            session_id=session_id,
            tool_name=tool_name,
            success=True,
        )

        return result

    except Exception as exc:

        log_tool_event(
            user_id=user_id,
            session_id=session_id,
            tool_name=tool_name,
            success=False,
            data={
                "error": str(exc),
            },
        )

        raise
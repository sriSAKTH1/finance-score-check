from audit.audit_logger import (
    create_audit_event,
    log_audit_event,
)
from audit.audit_reader import (
    read_audit_events,
    get_session_events,
)


def test_create_audit_event():

    event = create_audit_event(
        user_id="demo_user_001",
        session_id="test-session",
        event_type="intent_detected",
        data={
            "intent": "LOAN"
        },
    )

    assert event["user_id"] == "demo_user_001"
    assert event["session_id"] == "test-session"
    assert event["event_type"] == "intent_detected"
    assert event["data"]["intent"] == "LOAN"
    assert "timestamp" in event


def test_log_audit_event():

    event = log_audit_event(
        user_id="demo_user_001",
        session_id="audit-test-session",
        event_type="test_event",
        data={
            "value": 123
        },
    )

    assert event["event_type"] == "test_event"


def test_read_audit_events():

    log_audit_event(
        user_id="demo_user_001",
        session_id="read-test-session",
        event_type="test_event",
        data={
            "value": "hello"
        },
    )

    events = read_audit_events()

    assert len(events) > 0


def test_get_session_events():

    session_id = "specific-session"

    log_audit_event(
        user_id="demo_user_001",
        session_id=session_id,
        event_type="intent_detected",
        data={
            "intent": "INVESTMENT"
        },
    )

    events = get_session_events(
        session_id
    )

    assert len(events) >= 1
    assert events[-1]["event_type"] == "intent_detected"
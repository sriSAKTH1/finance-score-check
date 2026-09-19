from audit.tool_audit import execute_with_audit


def test_successful_tool():

    def fake_tool(value):
        return value * 2

    result = execute_with_audit(
        fake_tool,
        "fake_tool",
        "demo_user_001",
        "audit_test_001",
        10,
    )

    assert result == 20


def test_failed_tool():

    def failing_tool():
        raise ValueError("Test failure")

    try:
        execute_with_audit(
            failing_tool,
            "failing_tool",
            "demo_user_001",
            "audit_test_002",
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")
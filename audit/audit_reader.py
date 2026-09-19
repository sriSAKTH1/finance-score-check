import json
from pathlib import Path


AUDIT_FILE = Path("data/audit/audit_log.jsonl")


def read_audit_events() -> list[dict]:
    """
    Read all audit events.
    """

    if not AUDIT_FILE.exists():
        return []

    events = []

    with open(
        AUDIT_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            try:
                events.append(
                    json.loads(line)
                )
            except json.JSONDecodeError:
                continue

    return events


def get_session_events(
    session_id: str,
) -> list[dict]:

    events = read_audit_events()

    return [
        event
        for event in events
        if event.get("session_id") == session_id
    ]
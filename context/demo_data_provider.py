import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_user(user_id: str) -> dict:
    file_path = DATA_DIR / f"{user_id}.json"

    if not file_path.exists():
        raise FileNotFoundError(
            f"No financial data found for user: {user_id}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
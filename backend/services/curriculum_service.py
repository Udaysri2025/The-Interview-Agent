import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "curriculum.json"


def load_curriculum():
    """Load the supplied 31-day cohort curriculum."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Curriculum data not found: {DATA_FILE}"
        )

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_all_days():
    """Return curriculum days."""
    data = load_curriculum()

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in ("days", "curriculum", "modules", "data"):
            if key in data and isinstance(data[key], list):
                return data[key]

    return [data]


def get_day(day_number):
    """Find a specific curriculum day."""
    days = get_all_days()

    for day in days:
        if not isinstance(day, dict):
            continue

        possible_numbers = [
            day.get("day"),
            day.get("day_number"),
            day.get("dayNumber"),
        ]

        if day_number in possible_numbers or str(day_number) in [
            str(value) for value in possible_numbers
        ]:
            return day

    return None

import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "candidates.json"


def load_candidates():
    """Load all candidate profiles from the hackathon JSON."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Candidate data not found: {DATA_FILE}"
        )

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_all_candidates():
    """Return all candidate profiles."""
    data = load_candidates()

    if isinstance(data, dict) and "candidates" in data:
        return data["candidates"]

    if isinstance(data, list):
        return data

    return []


def get_candidate(candidate_id: str):
    """Find a candidate using the member.id field."""
    candidates = get_all_candidates()

    for candidate in candidates:
        member = candidate.get("member", {})

        if member.get("id") == candidate_id:
            return candidate

    return None

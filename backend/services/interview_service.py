import uuid


sessions = {}


def create_session(candidate_id, candidate, analysis):

    session_id = str(uuid.uuid4())

    sessions[session_id] = {
        "session_id": session_id,
        "candidate_id": candidate_id,
        "candidate": candidate,
        "analysis": analysis,
        "history": [],
        "question_number": 0,
        "completed": False,
        "feedback": None
    }

    return sessions[session_id]


def get_session(session_id):

    return sessions.get(session_id)

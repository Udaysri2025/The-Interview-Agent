from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from services.candidate_service import (
    get_all_candidates,
    get_candidate
)

from services.curriculum_service import (
    get_all_days,
    get_day
)

from agents.candidate_analyzer import analyze_candidate

from agents.interview_agent import (
    generate_question,
    generate_feedback
)

from services.interview_service import (
    create_session,
    get_session
)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI Interview Agent",
    version="1.0.0",
    description="Adaptive AI Interview Agent for the AI Cohort"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
async def root():
    return {
        "status": "running",
        "message": "AI Interview Agent API"
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


# ============================================================
# CANDIDATES
# ============================================================

@app.get("/candidates")
async def candidates():

    all_candidates = get_all_candidates()

    return {
        "count": len(all_candidates),
        "candidates": all_candidates
    }


@app.get("/candidates/{candidate_id}")
async def candidate(candidate_id: str):

    result = get_candidate(candidate_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return result


# ============================================================
# CANDIDATE ANALYSIS
# ============================================================

@app.post("/candidates/{candidate_id}/analyze")
async def analyze(candidate_id: str):

    candidate_data = get_candidate(candidate_id)

    if candidate_data is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    analysis = analyze_candidate(candidate_data)

    return {
        "candidate_id": candidate_id,
        "analysis": analysis
    }


# ============================================================
# CURRICULUM
# ============================================================

@app.get("/curriculum")
async def curriculum():

    all_days = get_all_days()

    return {
        "count": len(all_days),
        "days": all_days
    }


@app.get("/curriculum/day/{day_number}")
async def curriculum_day(day_number: int):

    result = get_day(day_number)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Curriculum day not found"
        )

    return result


# ============================================================
# START INTERVIEW
# ============================================================

@app.post("/interview/start/{candidate_id}")
async def start_interview(candidate_id: str):

    # --------------------------------------------------------
    # Load candidate
    # --------------------------------------------------------

    candidate_data = get_candidate(candidate_id)

    if candidate_data is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    # --------------------------------------------------------
    # Analyze candidate
    # --------------------------------------------------------

    analysis = analyze_candidate(candidate_data)

    # --------------------------------------------------------
    # Create interview session
    # --------------------------------------------------------

    session = create_session(
        candidate_id,
        candidate_data,
        analysis
    )

    # --------------------------------------------------------
    # Generate first question
    # --------------------------------------------------------

    question = generate_question(
        candidate_data,
        get_all_days(),
        analysis,
        [],
        1
    )

    # --------------------------------------------------------
    # Store question number
    # --------------------------------------------------------

    session["question_number"] = 1

    session["history"].append({
        "question_number": 1,
        "question": question
    })

    # --------------------------------------------------------
    # Return session
    # --------------------------------------------------------

    return {
        "session_id": session["session_id"],
        "candidate_id": candidate_id,
        "question_number": 1,
        "completed": False,
        "question": question
    }


# ============================================================
# SUBMIT INTERVIEW ANSWER
# ============================================================

@app.post("/interview/{session_id}/answer")
async def answer_interview(
    session_id: str,
    answer: dict
):

    # --------------------------------------------------------
    # Get session
    # --------------------------------------------------------

    session = get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found"
        )

    # --------------------------------------------------------
    # Check completion
    # --------------------------------------------------------

    if session["completed"]:
        raise HTTPException(
            status_code=400,
            detail="Interview already completed"
        )

    # --------------------------------------------------------
    # Validate answer
    # --------------------------------------------------------

    candidate_answer = answer.get("answer", "").strip()

    if not candidate_answer:
        raise HTTPException(
            status_code=400,
            detail="Answer cannot be empty"
        )

    # --------------------------------------------------------
    # Store answer for current question
    # --------------------------------------------------------

    history = session["history"]

    history[-1]["answer"] = candidate_answer

    # --------------------------------------------------------
    # Determine next question
    # --------------------------------------------------------

    current_number = session["question_number"]
    next_number = current_number + 1

    # ========================================================
    # INTERVIEW COMPLETE
    # ========================================================

    if next_number > 8:

        try:

            feedback = generate_feedback(
                session["candidate"],
                history
            )

        except Exception as e:

            print(
                f"Feedback generation failed: {str(e)}"
            )

            raise HTTPException(
                status_code=500,
                detail=(
                    "Interview completed, but AI feedback "
                    "could not be generated. Please try again."
                )
            )

        # ----------------------------------------------------
        # Mark session completed
        # ----------------------------------------------------

        session["completed"] = True

        session["feedback"] = feedback

        session["question_number"] = 8

        # ----------------------------------------------------
        # Return final interview result
        # ----------------------------------------------------

        return {
            "completed": True,
            "session_id": session_id,
            "candidate_id": session["candidate_id"],
            "question_number": 8,
            "total_questions": 8,
            "feedback": feedback
        }

    # ========================================================
    # GENERATE NEXT QUESTION
    # ========================================================

    try:

        question = generate_question(
            session["candidate"],
            get_all_days(),
            session["analysis"],
            history,
            next_number
        )

    except Exception as e:

        print(
            f"Question generation failed: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to generate the next interview question. "
                "Please try again."
            )
        )

    # --------------------------------------------------------
    # Update session
    # --------------------------------------------------------

    session["question_number"] = next_number

    history.append({
        "question_number": next_number,
        "question": question
    })

    # --------------------------------------------------------
    # Return next question
    # --------------------------------------------------------

    return {
        "completed": False,
        "session_id": session_id,
        "candidate_id": session["candidate_id"],
        "question_number": next_number,
        "total_questions": 8,
        "question": question
    }


# ============================================================
# INTERVIEW STATUS
# ============================================================

@app.get("/interview/{session_id}")
async def interview_status(session_id: str):

    session = get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found"
        )

    return {
        "session_id": session_id,
        "candidate_id": session["candidate_id"],
        "question_number": session["question_number"],
        "total_questions": 8,
        "completed": session["completed"],
        "history": session["history"],
        "feedback": session.get("feedback")
    }
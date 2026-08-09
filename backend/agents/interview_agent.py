import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


# ============================================================
# GROQ CLIENT
# ============================================================

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "llama-3.1-8b-instant"


# ============================================================
# JSON CLEANER
# ============================================================

def clean_json_response(content: str) -> dict:
    """
    Safely extract JSON from an LLM response.

    Handles:
    - Pure JSON
    - ```json ... ```
    - ``` ... ```
    - Text before/after JSON
    """

    if not content:
        raise ValueError("Empty model response.")

    content = content.strip()

    # Remove markdown code fences
    content = re.sub(
        r"```json\s*",
        "",
        content,
        flags=re.IGNORECASE
    )

    content = re.sub(
        r"```\s*",
        "",
        content
    )

    content = content.strip()

    # First attempt: response is already valid JSON
    try:
        return json.loads(content)

    except json.JSONDecodeError:
        pass

    # Find the first JSON object
    start = content.find("{")
    end = content.rfind("}")

    if start != -1 and end != -1 and end > start:

        json_text = content[start:end + 1]

        try:
            return json.loads(json_text)

        except json.JSONDecodeError as e:

            raise ValueError(
                f"Could not parse JSON from model response:\n{content}"
            ) from e

    raise ValueError(
        f"Model did not return a JSON object:\n{content}"
    )


# ============================================================
# INTERVIEWER SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are a senior AI engineering technical interviewer.

Conduct a realistic adaptive interview for a candidate who
completed an AI engineering cohort.

Your goal is to assess:
- Technical understanding
- Engineering reasoning
- Practical application
- System design
- Debugging ability
- Communication

QUESTION RULES:

1. Ask meaningful technical questions.
2. Prefer practical, scenario-based and engineering questions.
3. Analyze previous answers before creating the next question.
4. Ask follow-ups when an answer is incomplete, vague, incorrect,
   contradictory, or especially interesting.
5. Increase difficulty when the candidate performs strongly.
6. Decrease or redirect difficulty when the candidate struggles.
7. Never repeat a previously asked question.
8. Connect questions to previous answers when useful.
9. Do not treat every question as an isolated interaction.

CURRICULUM:

- The interview must cover at least 4 different curriculum days.
- Questions 1-4 should prioritize different curriculum days.
- Avoid repeating a curriculum day unless a follow-up is justified.
- Prefer completed and relevant curriculum topics.
- Do not claim the candidate completed a topic that was skipped.

INTERVIEW STRUCTURE:

- Minimum 8 questions.
- Early questions: foundational understanding.
- Middle questions: practical application and engineering decisions.
- Later questions: system design, trade-offs, debugging and scenarios.

Avoid:
- Generic textbook questions
- Pure memorization
- Repetitive questions
- Irrelevant questions

Prefer:
- Why would you choose X instead of Y?
- How would you design this?
- What would happen if...?
- How would you debug this?
- What trade-offs would you consider?
- How would you scale this system?

Return ONLY a JSON object.

Use exactly:

{
    "question": "...",
    "question_type": "core | follow_up | scenario",
    "curriculum_day": 0,
    "topic": "...",
    "difficulty": "easy | medium | hard",
    "reason": "..."
}

Do not write explanations outside JSON.
Do not use Markdown code fences.
"""


# ============================================================
# HELPER: SAFE JSON STRING
# ============================================================

def compact_json(data) -> str:
    """
    Convert Python data to compact JSON to reduce token usage.
    """

    return json.dumps(
        data,
        ensure_ascii=False,
        separators=(",", ":")
    )


# ============================================================
# HELPER: COMPACT TEXT
# ============================================================

def limit_text(value, max_chars: int) -> str:
    """
    Safely convert a value to text and limit its size.
    """

    if value is None:
        return ""

    if isinstance(value, str):
        return value[:max_chars]

    return compact_json(value)[:max_chars]


# ============================================================
# QUESTION GENERATOR
# ============================================================

def generate_question(
    candidate: dict,
    curriculum: list,
    analysis: dict,
    history: list,
    question_number: int
):

    # --------------------------------------------------------
    # Find curriculum days already used
    # --------------------------------------------------------

    used_days = []

    for item in history:

        question_data = item.get("question", {})

        if isinstance(question_data, dict):

            day = question_data.get("curriculum_day")

            if day is not None and day not in used_days:
                used_days.append(day)

    remaining_days = [
        day
        for day in range(1, 32)
        if day not in used_days
    ]

    # --------------------------------------------------------
    # Curriculum coverage instruction
    # --------------------------------------------------------

    if question_number <= 4:

        coverage_instruction = (
            f"This is interview question {question_number}. "
            f"The interview must cover at least 4 different "
            f"curriculum days. "
            f"Previously used days: {used_days}. "
            f"Prefer an unused relevant curriculum day. "
            f"Available unused days: {remaining_days[:15]}. "
            f"Prioritize completed, relevant and technically "
            f"meaningful topics."
        )

    else:

        coverage_instruction = (
            f"Previously covered curriculum days: {used_days}. "
            f"The interview must contain at least 4 different "
            f"curriculum days. "
            f"Adaptive follow-ups are allowed when justified. "
            f"Avoid unnecessary repetition."
        )

    # --------------------------------------------------------
    # COMPACT CANDIDATE DATA
    # --------------------------------------------------------

    candidate_summary = {}

    if isinstance(candidate, dict):

        # Keep only useful candidate information.
        for key in [
            "name",
            "jobRole",
            "role",
            "skills",
            "completedMissions",
            "completed_missions",
            "skippedTopics",
            "skipped_topics",
            "signals",
            "member"
        ]:

            if key in candidate:

                value = candidate[key]

                if isinstance(value, str):
                    value = value[:700]

                elif isinstance(value, list):
                    value = value[:15]

                elif isinstance(value, dict):
                    value = compact_json(value)[:1000]

                candidate_summary[key] = value

    candidate_text = compact_json(candidate_summary)

    # Absolute safety limit
    candidate_text = candidate_text[:1800]

    # --------------------------------------------------------
    # COMPACT ANALYSIS
    # --------------------------------------------------------

    analysis_summary = {}

    if isinstance(analysis, dict):

        for key, value in analysis.items():

            if isinstance(value, str):
                analysis_summary[key] = value[:500]

            elif isinstance(value, list):
                analysis_summary[key] = value[:10]

            else:
                analysis_summary[key] = value

    analysis_text = compact_json(analysis_summary)

    # Absolute safety limit
    analysis_text = analysis_text[:1400]

    # --------------------------------------------------------
    # COMPACT INTERVIEW HISTORY
    # --------------------------------------------------------
    #
    # Only recent questions and answers are needed.
    # Sending the complete interview every time was causing
    # the Groq request to exceed the TPM limit.
    # --------------------------------------------------------

    compact_history = []

    # Only last 3 interactions
    recent_history = history[-3:]

    for item in recent_history:

        question_data = item.get("question", {})
        answer_data = item.get("answer", "")

        if isinstance(question_data, dict):

            compact_question = {
                "question": limit_text(
                    question_data.get("question", ""),
                    450
                ),
                "type": question_data.get(
                    "question_type",
                    ""
                ),
                "day": question_data.get(
                    "curriculum_day"
                ),
                "topic": limit_text(
                    question_data.get("topic", ""),
                    150
                ),
                "difficulty": question_data.get(
                    "difficulty",
                    ""
                )
            }

        else:

            compact_question = limit_text(
                question_data,
                450
            )

        compact_history.append(
            {
                "question": compact_question,
                "answer": limit_text(
                    answer_data,
                    700
                )
            }
        )

    # --------------------------------------------------------
    # COMPACT CURRICULUM
    # --------------------------------------------------------

    compact_curriculum = []

    if isinstance(curriculum, list):

        for item in curriculum:

            if isinstance(item, dict):

                compact_item = {}

                # Preserve useful fields only
                for key in [
                    "day",
                    "curriculum_day",
                    "topic",
                    "title",
                    "name",
                    "topics"
                ]:

                    if key in item:

                        value = item[key]

                        if isinstance(value, str):
                            value = value[:180]

                        elif isinstance(value, list):
                            value = value[:8]

                        compact_item[key] = value

                if compact_item:
                    compact_curriculum.append(
                        compact_item
                    )

            else:

                compact_curriculum.append(
                    limit_text(item, 180)
                )

    # Maximum 15 curriculum entries
    compact_curriculum = compact_curriculum[:15]

    # --------------------------------------------------------
    # FINAL COMPACT CONTEXT
    # --------------------------------------------------------

    context = {
        "question_number": question_number,
        "candidate": candidate_text,
        "analysis": analysis_text,
        "recent_history": compact_history,
        "curriculum": compact_curriculum,
        "coverage": coverage_instruction
    }

    user_prompt = compact_json(context)

    # --------------------------------------------------------
    # EXTRA SAFETY LIMIT
    # --------------------------------------------------------
    #
    # Keep the user prompt comfortably below the Groq limit.
    #
    # The previous implementation could send 6,000+ tokens.
    # This version intentionally keeps the request much smaller.
    # --------------------------------------------------------

    user_prompt = user_prompt[:9000]

    # --------------------------------------------------------
    # GROQ REQUEST
    # --------------------------------------------------------

    try:

        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.3,

            # The generated JSON is very small.
            max_tokens=300,

            response_format={
                "type": "json_object"
            },

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

    except Exception as e:

        error_message = str(e)

        if "413" in error_message or "TPM" in error_message:

            raise RuntimeError(
                "Groq request was too large. "
                "The interview context has exceeded the "
                "model token-per-minute limit. "
                "Please try again."
            ) from e

        if "429" in error_message:

            raise RuntimeError(
                "Groq rate limit reached. "
                "Please wait before continuing the interview."
            ) from e

        raise

    # --------------------------------------------------------
    # GET MODEL RESPONSE
    # --------------------------------------------------------

    content = response.choices[0].message.content

    if not content:
        raise ValueError(
            "Model returned an empty response."
        )

    # --------------------------------------------------------
    # PARSE JSON
    # --------------------------------------------------------

    question = clean_json_response(content)

    # --------------------------------------------------------
    # VALIDATE FIELDS
    # --------------------------------------------------------

    required_fields = [
        "question",
        "question_type",
        "curriculum_day",
        "topic",
        "difficulty",
        "reason"
    ]

    for field in required_fields:

        if field not in question:

            raise ValueError(
                f"Generated question is missing field: {field}"
            )

    # --------------------------------------------------------
    # Validate question type
    # --------------------------------------------------------

    valid_question_types = [
        "core",
        "follow_up",
        "scenario"
    ]

    if question["question_type"] not in valid_question_types:

        question["question_type"] = "core"

    # --------------------------------------------------------
    # Validate difficulty
    # --------------------------------------------------------

    valid_difficulties = [
        "easy",
        "medium",
        "hard"
    ]

    if question["difficulty"] not in valid_difficulties:

        question["difficulty"] = "medium"

    # --------------------------------------------------------
    # Validate curriculum day
    # --------------------------------------------------------

    try:

        question["curriculum_day"] = int(
            question["curriculum_day"]
        )

    except (TypeError, ValueError):

        question["curriculum_day"] = (
            remaining_days[0]
            if question_number <= 4
            and remaining_days
            else 1
        )

    return question


# ============================================================
# FEEDBACK PROMPT
# ============================================================

FEEDBACK_PROMPT = """
You are a senior technical interviewer.

Review the technical interview and candidate information.

Evaluate ONLY what is supported by the interview.

Evaluate:
- Technical understanding
- Depth of reasoning
- Engineering decisions
- Practical system-design thinking
- Problem-solving ability
- Communication
- Strong areas
- Weak areas
- Topics for improvement

Scores must be between 0 and 100.

Feedback must be specific and actionable.

Avoid generic statements such as:
"Practice more."

Instead explain:
- What the candidate did well
- What is missing
- What should be improved
- Why it matters technically

Return ONLY JSON.

Use exactly:

{
    "overall_score": 0,
    "technical_score": 0,
    "reasoning_score": 0,
    "communication_score": 0,
    "strengths": [],
    "weaknesses": [],
    "recommended_topics": [],
    "final_feedback": ""
}

Do not write explanations outside JSON.
Do not use Markdown code fences.
"""


# ============================================================
# FEEDBACK GENERATOR
# ============================================================

def generate_feedback(candidate, history):

    # --------------------------------------------------------
    # Compact candidate
    # --------------------------------------------------------

    candidate_summary = {}

    if isinstance(candidate, dict):

        for key in [
            "name",
            "jobRole",
            "role",
            "skills",
            "signals",
            "member"
        ]:

            if key in candidate:

                value = candidate[key]

                if isinstance(value, str):
                    value = value[:500]

                elif isinstance(value, list):
                    value = value[:10]

                elif isinstance(value, dict):
                    value = compact_json(value)[:700]

                candidate_summary[key] = value

    # --------------------------------------------------------
    # Compact interview history
    # --------------------------------------------------------

    compact_history = []

    for item in history:

        question_data = item.get(
            "question",
            {}
        )

        answer_data = item.get(
            "answer",
            ""
        )

        if isinstance(question_data, dict):

            compact_question = {
                "question": limit_text(
                    question_data.get(
                        "question",
                        ""
                    ),
                    600
                ),
                "day": question_data.get(
                    "curriculum_day"
                ),
                "topic": limit_text(
                    question_data.get(
                        "topic",
                        ""
                    ),
                    150
                ),
                "difficulty": question_data.get(
                    "difficulty",
                    ""
                )
            }

        else:

            compact_question = limit_text(
                question_data,
                600
            )

        compact_history.append(
            {
                "question": compact_question,
                "answer": limit_text(
                    answer_data,
                    1000
                )
            }
        )

    payload = {
        "candidate": candidate_summary,
        "interview": compact_history
    }

    user_prompt = compact_json(payload)

    # --------------------------------------------------------
    # Feedback request
    # --------------------------------------------------------

    try:

        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.2,

            max_tokens=500,

            response_format={
                "type": "json_object"
            },

            messages=[
                {
                    "role": "system",
                    "content": FEEDBACK_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

    except Exception as e:

        error_message = str(e)

        if "413" in error_message or "TPM" in error_message:

            raise RuntimeError(
                "Groq feedback request was too large. "
                "Please reduce the interview history."
            ) from e

        if "429" in error_message:

            raise RuntimeError(
                "Groq rate limit reached while generating "
                "feedback. Please wait and try again."
            ) from e

        raise

    # --------------------------------------------------------
    # Get response
    # --------------------------------------------------------

    content = response.choices[0].message.content

    if not content:

        raise ValueError(
            "Model returned an empty feedback response."
        )

    # --------------------------------------------------------
    # Parse JSON
    # --------------------------------------------------------

    feedback = clean_json_response(content)

    # --------------------------------------------------------
    # Validate feedback structure
    # --------------------------------------------------------

    required_fields = [
        "overall_score",
        "technical_score",
        "reasoning_score",
        "communication_score",
        "strengths",
        "weaknesses",
        "recommended_topics",
        "final_feedback"
    ]

    for field in required_fields:

        if field not in feedback:

            raise ValueError(
                f"Generated feedback is missing field: {field}"
            )

    return feedback
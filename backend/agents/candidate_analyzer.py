import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "llama-3.3-70b-versatile"


SYSTEM_PROMPT = """
You are an expert technical interview preparation analyst.

Analyze a candidate's learning journey from an AI engineering cohort.

Use ONLY the candidate data provided.

Identify:
1. Completed topics
2. Strong areas
3. Weak or uncertain areas
4. Skipped topics
5. Important learning signals
6. Recommended interview difficulty

Return ONLY valid JSON:

{
  "completed_topics": [],
  "strong_areas": [],
  "weak_areas": [],
  "skipped_topics": [],
  "learning_signals": [],
  "recommended_difficulty": "Easy | Medium | Hard",
  "analysis_summary": ""
}
"""


def analyze_candidate(candidate: dict) -> dict:

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": json.dumps(
                    candidate,
                    indent=2,
                    ensure_ascii=False
                )
            }
        ]
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    try:
        return json.loads(content)

    except json.JSONDecodeError:
        return {
            "completed_topics": [],
            "strong_areas": [],
            "weak_areas": [],
            "skipped_topics": [],
            "learning_signals": [],
            "recommended_difficulty": "Medium",
            "analysis_summary": content
        }

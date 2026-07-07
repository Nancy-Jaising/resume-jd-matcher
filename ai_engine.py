import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# NOTE: if this model name 404s, run list_available_models() below
# to see what's live on your API key, and swap it in.
MODEL_NAME = "gemini-2.5-flash"

ANALYZE_PROMPT = """You are an ATS-style resume screener.
Compare the RESUME against the JOB DESCRIPTION below.

Respond ONLY with a valid JSON object, no markdown fences, no preamble. Schema:
{{
  "score": <integer 0-100>,
  "matched": [<short strings, skills/requirements the resume satisfies>],
  "missing": [<short strings, requirements the resume does NOT show>],
  "explanation": "<4-6 sentences, plain language, explaining why the score is what it is, what matched, and what's missing>"
}}

RESUME:
{resume}

JOB DESCRIPTION:
{jd}
"""


def list_available_models():
    """Helper: run this once if MODEL_NAME throws a 404."""
    return [m.name for m in genai.list_models() if "generateContent" in m.supported_generation_methods]


def analyze_match(resume_text: str, jd_text: str) -> dict:
    model = genai.GenerativeModel(MODEL_NAME)
    prompt = ANALYZE_PROMPT.format(resume=resume_text, jd=jd_text)
    response = model.generate_content(prompt)
    raw = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def chat_reply(history: list, user_msg: str, resume_text: str, jd_text: str, result: dict = None) -> str:
    """history: list of {'role': 'user'/'model', 'parts': [text]}"""
    score_context = ""
    if result:
        score_context = (
            f"\n\nIMPORTANT — the official match score has already been calculated as "
            f"{result['score']}/100. If the user asks about their score, always state exactly "
            f"{result['score']}/100 — do NOT recalculate or estimate a different number.\n"
            f"Matched skills: {', '.join(result.get('matched', []))}\n"
            f"Missing skills: {', '.join(result.get('missing', []))}\n"
            f"Explanation on file: {result.get('explanation', '')}"
        )

    model = genai.GenerativeModel(
        MODEL_NAME,
        system_instruction=(
            "You are Scanline's assistant. You help the candidate understand "
            "their resume-vs-JD match. Use the resume and JD context below when relevant. "
            "Be concise, direct, and practical."
            f"\n\nRESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{jd_text}"
            f"{score_context}"
        ),
    )
    chat = model.start_chat(history=history)
    response = chat.send_message(user_msg)
    return response.text
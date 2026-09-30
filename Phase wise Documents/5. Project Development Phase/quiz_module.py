import json
import re
from typing import Any

from gemini_client import generate_text
from models import QuizQuestion


QUIZ_SCHEMA_INSTRUCTION = """
Return ONLY a JSON array containing exactly 3 objects.

Each object must have:
- question: string
- options: array of exactly 4 strings
- correct_answer: string that exactly matches one option
- explanation: short string explaining the answer

Do not use Markdown code fences.
Do not add text before or after the JSON.
"""


def clean_json_block(text: str) -> str:
    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    return text.strip()


def _validate(raw: Any) -> list[QuizQuestion]:
    if not isinstance(raw, list) or len(raw) != 3:
        raise ValueError(
            "Quiz response must contain exactly 3 questions."
        )

    questions: list[QuizQuestion] = []

    for item in raw:
        question = QuizQuestion.model_validate(item)

        if question.correct_answer not in question.options:
            raise ValueError(
                "correct_answer must match one of the options."
            )

        questions.append(question)

    return questions


def generate_quiz(passage: str) -> list[QuizQuestion]:
    prompt = (
        QUIZ_SCHEMA_INSTRUCTION
        + """
Create three meaningful multiple-choice questions
from the following educational topic or passage.

Keep the distractors plausible but incorrect.

Topic or passage:
"""
        + passage
    )

    response = generate_text(
        prompt,
        system_instruction=(
            "You generate reliable educational MCQs "
            "and must follow the requested JSON format exactly."
        ),
        temperature=0.3,
    )

    cleaned = clean_json_block(response)

    try:
        raw = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Gemini returned invalid quiz JSON: {exc}"
        ) from exc

    return _validate(raw)
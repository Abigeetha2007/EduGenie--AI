import json
import re

from gemini_client import generate_text


def clean_json_block(text: str) -> str:

    text = text.strip()

    # Remove Markdown JSON block
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


def generate_quiz(text: str):

    prompt = f"""
Create exactly 3 multiple-choice questions
from the educational text below.

Each question must have exactly 4 options.

Return ONLY valid JSON.

Use exactly this format:

[
    {{
        "question": "Question text",
        "options": [
            "Option A",
            "Option B",
            "Option C",
            "Option D"
        ],
        "answer": "Correct option",
        "explanation": "Short explanation"
    }}
]

Rules:

- Exactly 3 questions
- Exactly 4 options per question
- The answer must match one of the options
- Questions must come from the provided text
- Do not include Markdown
- Do not include extra text

Educational text:

{text}
"""

    try:

        response = generate_text(prompt)

        cleaned_response = clean_json_block(
            response
        )

        quiz = json.loads(
            cleaned_response
        )

        # Validate list
        if not isinstance(quiz, list):
            raise ValueError(
                "Quiz response is not a list."
            )

        # Validate exactly 3 questions
        if len(quiz) != 3:
            raise ValueError(
                "Quiz must contain exactly 3 questions."
            )

        # Validate each question
        for question in quiz:

            if "question" not in question:
                raise ValueError(
                    "Question field is missing."
                )

            if "options" not in question:
                raise ValueError(
                    "Options field is missing."
                )

            if "answer" not in question:
                raise ValueError(
                    "Answer field is missing."
                )

            if len(question["options"]) != 4:
                raise ValueError(
                    "Each question must contain 4 options."
                )

            if question["answer"] not in question["options"]:
                raise ValueError(
                    "Correct answer is not one of the options."
                )

        return quiz

    except Exception as error:

        return {
            "error": f"Quiz generation failed: {error}"
        }
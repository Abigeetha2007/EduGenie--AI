from config import settings
from gemini_client import generate_text


def _gemini_explanation(topic: str) -> str:
    return generate_text(
        f"""
Explain this educational topic:

{topic}

Use simple language for a beginner.

Include:
1. Short definition
2. Key points
3. One easy example
4. One-line recap
""",
        system_instruction=(
            "You are EduGenie, a patient educational tutor. "
            "Prioritize clarity and correctness."
        ),
        temperature=0.2,
    )


def _local_explanation(topic: str) -> str:
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation mode requires optional dependencies. "
            "Install requirements-local.txt or use "
            "EXPLANATION_PROVIDER=gemini."
        ) from exc

    generator = pipeline(
        "text2text-generation",
        model=settings.local_explanation_model
    )

    prompt = (
        "Explain this topic simply for a beginner. "
        "Give a definition, 3 key points, one example, "
        "and a short recap: "
        + topic
    )

    output = generator(
        prompt,
        max_new_tokens=220,
        do_sample=False
    )

    return output[0]["generated_text"].strip()


def explain_topic(topic: str) -> str:
    if settings.explanation_provider == "local":
        return _local_explanation(topic)

    return _gemini_explanation(topic)
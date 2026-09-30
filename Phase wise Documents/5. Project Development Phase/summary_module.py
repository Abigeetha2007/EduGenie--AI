from gemini_client import generate_text


def summarize_text(text: str) -> str:
    return generate_text(
        """
Summarize the following educational text.

Preserve:
- important facts
- names
- relationships
- important conclusions

Use simple English.
Use bullet points where useful.

Text:

"""
        + text,
        system_instruction=(
            "You are EduGenie, an educational "
            "summarization assistant."
        ),
        temperature=0.2,
    )
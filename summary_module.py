from gemini_client import generate_text


def summarize_text(text: str) -> str:

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following educational text.

Requirements:

- Keep the important information.
- Remove unnecessary repetition.
- Use simple English.
- Make it useful for quick revision.
- Use bullet points where appropriate.
- Do not add information that is not present in the original text.

Text:

{text}
"""

    try:

        result = generate_text(prompt)

        return result

    except Exception as error:

        return f"Unable to summarize the text: {error}"
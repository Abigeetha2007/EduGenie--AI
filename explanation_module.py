from gemini_client import generate_text


def explain_topic(topic: str) -> str:

    prompt = f"""
You are EduGenie, a beginner-friendly educational assistant.

Explain this topic in very simple language.

Topic:

{topic}

Follow this structure:

1. Simple definition
2. Main idea
3. How it works
4. Simple example
5. Important points

Keep the explanation easy for a student to understand.
"""

    try:

        result = generate_text(prompt)

        return result

    except Exception as error:

        return f"Unable to explain the topic: {error}"
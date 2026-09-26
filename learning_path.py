from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:

    prompt = f"""
You are EduGenie, a personalized learning assistant.

Create a complete learning path for:

{topic}

Organize the learning path into:

1. Beginner level
2. Intermediate level
3. Advanced level
4. Practice activities
5. Project ideas
6. Recommended resources
7. Suggested timeline

Explain what the student should learn at each stage.

Keep the plan practical and easy to follow.
"""

    try:

        result = generate_text(prompt)

        return result

    except Exception as error:

        return f"Unable to create learning path: {error}"
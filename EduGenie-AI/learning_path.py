from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
Create a personalized learning path for:

{topic}

Use this structure:

1. Beginner foundations
2. Intermediate concepts
3. Advanced concepts
4. Suggested timeline
5. Practice ideas
6. Mini project ideas
7. Useful resource types

Make the plan realistic for a college student.

Use simple English.

Do not fabricate URLs.
"""

    return generate_text(
        prompt,
        system_instruction=(
            "You are EduGenie, a learning-path designer. "
            "Adapt the plan to a beginner unless another "
            "level is specified."
        ),
        temperature=0.4,
    )
from gemini_client import generate_text


def answer_question(question: str) -> str:

    prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the student's question clearly and accurately.

Use:
- Simple English
- Short explanations
- Important points
- Examples when useful

Do not invent information.

Student question:

{question}
"""

    try:

        result = generate_text(prompt)

        return result

    except Exception as error:

        return f"Unable to get answer from Gemini: {error}"
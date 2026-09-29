from gemini_client import generate_text


def answer_question(question: str) -> str:
    return generate_text(
        question,
        system_instruction=(
            "You are EduGenie, an academic question-answering "
            "assistant. Answer directly, accurately, and concisely. "
            "For educational questions, explain the reasoning briefly "
            "instead of giving only the final answer."
        ),
        temperature=0.2,
    )
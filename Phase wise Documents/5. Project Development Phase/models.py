from typing import List

from pydantic import BaseModel, Field, field_validator

from config import settings


class AIRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="Topic, question, or educational text",
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Input cannot be empty")

        if len(value) > settings.max_input_chars:
            raise ValueError(
                f"Input is too long. Maximum is "
                f"{settings.max_input_chars} characters."
            )

        return value


class AIResponse(BaseModel):
    result: str


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(
        min_length=4,
        max_length=4
    )
    correct_answer: str
    explanation: str = ""


class QuizResponse(BaseModel):
    quiz: List[QuizQuestion] = Field(
        min_length=3,
        max_length=3
    )


class HealthResponse(BaseModel):
    status: str
    gemini_configured: bool
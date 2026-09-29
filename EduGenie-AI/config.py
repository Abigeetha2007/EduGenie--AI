from functools import lru_cache
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Settings(BaseModel):
    app_name: str = Field(default="EduGenie")
    gemini_api_key: str = Field(default="")
    gemini_model: str = Field(default="gemini-3.8-flash")
    explanation_provider: str = Field(default="gemini")
    local_explanation_model: str = Field(
        default="MBZUAI/LaMini-Flan-T5-783M"
    )
    max_input_chars: int = Field(default=20000, ge=1000, le=100000)


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "EduGenie"),
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        gemini_model=os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        ),
        explanation_provider=os.getenv(
            "EXPLANATION_PROVIDER",
            "gemini"
        ).lower(),
        local_explanation_model=os.getenv(
            "LOCAL_EXPLANATION_MODEL",
            "MBZUAI/LaMini-Flan-T5-783M",
        ),
        max_input_chars=int(
            os.getenv("MAX_INPUT_CHARS", "20000")
        ),
    )


settings = get_settings()
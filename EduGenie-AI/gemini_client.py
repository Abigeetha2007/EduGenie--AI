from functools import lru_cache
import time

from config import settings


class GeminiNotConfiguredError(RuntimeError):
    pass


@lru_cache
def get_client():
    if not settings.gemini_api_key:
        raise GeminiNotConfiguredError(
            "GEMINI_API_KEY is not configured. "
            "Create a .env file and add your Gemini API key."
        )

    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError(
            "google-genai is not installed. "
            "Run: pip install -r requirements.txt"
        ) from exc

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.3,
) -> str:

    client = get_client()

    max_attempts = 4

    for attempt in range(max_attempts):

        try:
            from google.genai import types

            config_kwargs = {
                "temperature": temperature,
                "max_output_tokens": 2048,
            }

            if system_instruction:
                config_kwargs["system_instruction"] = (
                    system_instruction
                )

            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    **config_kwargs
                ),
            )

            text = (response.text or "").strip()

            if not text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return text

        except Exception as exc:

            error_text = str(exc)

            is_temporary_error = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            )

            if is_temporary_error and attempt < max_attempts - 1:

                wait_seconds = 2 ** attempt

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_seconds} seconds..."
                )

                time.sleep(wait_seconds)

                continue

            raise RuntimeError(
                f"Gemini request failed: {exc}"
            ) from exc

    raise RuntimeError(
        "Gemini request failed after multiple attempts."
    )
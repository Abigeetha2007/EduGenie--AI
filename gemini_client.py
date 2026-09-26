import os

from dotenv import load_dotenv
from google import genai


# Load variables from .env
load_dotenv()


# Gemini model
MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)


# Create Gemini client
def get_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add your Gemini API key to the .env file."
        )

    client = genai.Client(
        api_key=api_key
    )

    return client


# Generate response
def generate_text(prompt: str) -> str:

    client = get_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()
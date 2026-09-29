from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from models import (
    AIRequest,
    AIResponse,
    HealthResponse,
    QuizResponse,
)
from explanation_module import explain_topic
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    version="1.0.0",
    description=(
        "AI-powered educational assistant with "
        "Q&A, explanations, quizzes, summaries, "
        "and learning paths."
    ),
)


app.mount(
    "/static",
    StaticFiles(
        directory=BASE_DIR / "static"
    ),
    name="static",
)


templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.app_name,
        },
    )


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        gemini_configured=bool(
            settings.gemini_api_key
        ),
    )


@app.post("/qa", response_model=AIResponse)
def qa(payload: AIRequest):
    return AIResponse(
        result=answer_question(payload.text)
    )


@app.post("/explain", response_model=AIResponse)
def explain(payload: AIRequest):
    return AIResponse(
        result=explain_topic(payload.text)
    )


@app.post("/summarize", response_model=AIResponse)
def summarize(payload: AIRequest):
    return AIResponse(
        result=summarize_text(payload.text)
    )


@app.post(
    "/learn/recommendations",
    response_model=AIResponse,
)
def learning_recommendations(
    payload: AIRequest
):
    return AIResponse(
        result=get_learning_recommendations(
            payload.text
        )
    )


@app.post(
    "/quiz",
    response_model=QuizResponse,
)
def quiz(payload: AIRequest):
    return QuizResponse(
        quiz=generate_quiz(payload.text)
    )
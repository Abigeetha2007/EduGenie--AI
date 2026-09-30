from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


def test_homepage():
    response = client.get("/")

    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_validation_rejects_empty_input():
    response = client.post(
        "/qa",
        json={"text": "   "}
    )

    assert response.status_code == 422


def test_quiz_validation(monkeypatch):

    def fake_quiz(_):

        return [
            {
                "question": "What is 2 + 2?",
                "options": [
                    "3",
                    "4",
                    "5",
                    "6"
                ],
                "correct_answer": "4",
                "explanation":
                    "Adding two and two gives four."
            }
        ] * 3


    monkeypatch.setattr(
        main,
        "generate_quiz",
        fake_quiz
    )


    response = client.post(
        "/quiz",
        json={
            "text": "Basic arithmetic"
        }
    )


    assert response.status_code == 200
    assert len(response.json()["quiz"]) == 3
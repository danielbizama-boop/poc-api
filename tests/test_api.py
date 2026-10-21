from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)
FLOR = {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_predict_ok():
    r = client.post("/v1/predict", json=FLOR)
    assert r.status_code == 200
    assert 0 <= r.json()["probabilidad"] <= 1


def test_predict_invalido():
    r = client.post("/v1/predict", json={**FLOR, "sepal_length": -1})
    assert r.status_code == 422

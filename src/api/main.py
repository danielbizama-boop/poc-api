# src/api/main.py
from pathlib import Path

import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field

MODEL_VERSION = "2.0.0"
MODEL_PATH = Path(__file__).resolve().parents[1] / "model.joblib"

app = FastAPI(title="API de predicción", version=MODEL_VERSION)
model = joblib.load(MODEL_PATH)  # se carga una sola vez al iniciar


class Flor(BaseModel):
    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)


class Prediccion(BaseModel):
    clase: int
    probabilidad: float
    version_modelo: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version_modelo": MODEL_VERSION}


@app.post("/v1/predict", response_model=Prediccion)
def predict(x: Flor) -> Prediccion:
    fila = [[x.sepal_length, x.sepal_width, x.petal_length, x.petal_width]]
    proba = model.predict_proba(fila)[0]
    clase = int(proba.argmax())
    return Prediccion(clase=clase, probabilidad=float(proba[clase]), version_modelo=MODEL_VERSION)

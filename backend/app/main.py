from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
import numpy as np


# Create the FastAPI application FIRST
app = FastAPI(
    title="SeismoBuild AI API",
    description="ML-based concrete strength prediction system",
    version="1.0.0"
)


# Add CORS middleware AFTER creating app
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Find the backend folder
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "concrete_strength_model.pkl"
)

print("\n========== MODEL DEBUG ==========")
print("BASE_DIR:", BASE_DIR)
print("MODEL_PATH:", MODEL_PATH)
print("MODEL EXISTS:", os.path.exists(MODEL_PATH))
print("=================================\n")


# Load the ML model
model = None

try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("SUCCESS: ML model loaded successfully!")
    else:
        print("ERROR: Model file does not exist at the expected path.")
except Exception as e:
    print("ERROR loading model:", repr(e))


class ConcreteInput(BaseModel):
    cement: float
    slag: float
    fly_ash: float
    water: float
    superplasticizer: float
    coarse_aggregate: float
    fine_aggregate: float
    age: float


@app.get("/")
def home():
    return {
        "message": "Welcome to SeismoBuild AI API",
        "status": "Backend is running successfully"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


@app.post("/api/concrete/predict")
def predict_concrete_strength(data: ConcreteInput):

    if model is None:
        raise HTTPException(
            status_code=503,
            detail="ML model is not available. Please train the model first."
        )

    features = np.array([[
        data.cement,
        data.slag,
        data.fly_ash,
        data.water,
        data.superplasticizer,
        data.coarse_aggregate,
        data.fine_aggregate,
        data.age
    ]])

    prediction = model.predict(features)[0]

    return {
        "predicted_strength_mpa": round(float(prediction), 2),
        "message": "Concrete compressive strength predicted successfully"
    }
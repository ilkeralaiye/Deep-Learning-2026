from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import torch
import os

from model import load_model, CROP_LABELS

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = FastAPI(title="Crop Recommendation API", version="1.0.0")

# Load model once at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), "crop_model.pth")

try:
    model = load_model(MODEL_PATH)
    print(f"[OK] Model loaded successfully from {MODEL_PATH}")
except FileNotFoundError:
    model = None
    print(f"[WARNING] Model file not found at {MODEL_PATH}. Place 'crop_model.pth' in the project root.")


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class PredictRequest(BaseModel):
    nitrogen: float = Field(..., ge=0, le=200, description="Nitrogen content (N)")
    phosphorus: float = Field(..., ge=0, le=200, description="Phosphorus content (P)")
    potassium: float = Field(..., ge=0, le=200, description="Potassium content (K)")
    temperature: float = Field(..., ge=-10, le=60, description="Temperature in °C")
    humidity: float = Field(..., ge=0, le=100, description="Relative humidity (%)")
    ph_value: float = Field(..., ge=0, le=14, description="Soil pH value")
    rainfall: float = Field(..., ge=0, le=500, description="Annual rainfall (mm)")


class PredictResponse(BaseModel):
    crop: str
    confidence: float
    probabilities: dict[str, float]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please place 'crop_model.pth' in the project root and restart the server."
        )

    features = torch.tensor(
        [[req.nitrogen, req.phosphorus, req.potassium,
          req.temperature, req.humidity, req.ph_value, req.rainfall]],
        dtype=torch.float32
    )

    with torch.inference_mode():
        logits = model(features)
        probs = torch.softmax(logits, dim=1).squeeze()  # shape: (22,)

    predicted_idx = probs.argmax().item()
    predicted_crop = CROP_LABELS[predicted_idx]
    confidence = float(probs[predicted_idx]) * 100

    probabilities = {
        CROP_LABELS[i]: round(float(probs[i]) * 100, 2)
        for i in range(len(CROP_LABELS))
    }

    return PredictResponse(
        crop=predicted_crop,
        confidence=round(confidence, 2),
        probabilities=probabilities
    )


# ---------------------------------------------------------------------------
# Serve static frontend
# ---------------------------------------------------------------------------
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def root():
    return FileResponse(os.path.join(static_dir, "index.html"))

import os
import torch
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel, Field
from model import IrisClassifier

# ── App setup ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Iris Classifier API",
    description="PyTorch tabanlı Iris çiçek sınıflandırma modeli",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ── Model yükleme ────────────────────────────────────────────────────────────
MODEL_PATH = "iris_model.pth"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = IrisClassifier().to(device)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model dosyası bulunamadı: '{MODEL_PATH}'. "
        "Lütfen eğitilmiş modelin state_dict'ini bu dosya adıyla kaydedin:\n"
        "  torch.save(model.state_dict(), 'iris_model.pth')"
    )

model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()
print(f"[OK] Model yuklendi: {MODEL_PATH} (device={device})")

CLASS_NAMES = ["Setosa", "Versicolor", "Virginica"]

# ── Schemas ──────────────────────────────────────────────────────────────────
class IrisFeatures(BaseModel):
    sepal_length: float = Field(..., ge=4.0, le=8.0, example=5.1,
                                description="Çanak yaprak uzunluğu (cm)")
    sepal_width:  float = Field(..., ge=2.0, le=5.0, example=3.5,
                                description="Çanak yaprak genişliği (cm)")
    petal_length: float = Field(..., ge=1.0, le=7.0, example=1.4,
                                description="Taç yaprak uzunluğu (cm)")
    petal_width:  float = Field(..., ge=0.1, le=2.6, example=0.2,
                                description="Taç yaprak genişliği (cm)")


class PredictionResponse(BaseModel):
    predicted_class: str
    class_index: int
    confidence: float
    probabilities: list[float]


# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict", response_model=PredictionResponse, summary="Iris türü tahmini")
async def predict(features: IrisFeatures):
    """
    Verilen 4 özelliğe göre iris çiçeğinin türünü tahmin eder.
    """
    try:
        x = torch.tensor(
            [[features.sepal_length, features.sepal_width,
              features.petal_length, features.petal_width]],
            dtype=torch.float32,
        ).to(device)

        with torch.inference_mode():
            logits = model(x)
            probs  = torch.softmax(logits, dim=1).squeeze()

        class_idx   = probs.argmax().item()
        confidence  = probs[class_idx].item()
        prob_list   = probs.cpu().tolist()

        return PredictionResponse(
            predicted_class=CLASS_NAMES[class_idx],
            class_index=class_idx,
            confidence=confidence,
            probabilities=prob_list,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tahmin hatası: {str(e)}")


@app.get("/health", summary="Sağlık kontrolü")
async def health():
    return {
        "status": "ok",
        "model": MODEL_PATH,
        "device": str(device),
        "classes": CLASS_NAMES,
    }

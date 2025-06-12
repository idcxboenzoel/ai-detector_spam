from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import re

# 🔄 Inisialisasi FastAPI
app = FastAPI()

# ✅ Model input
class EmailInput(BaseModel):
    text: str

# 🧠 Load model dan vectorizer
model_path = os.path.join(os.path.dirname(__file__), "model.joblib")
vec_path = os.path.join(os.path.dirname(__file__), "vectorizer.joblib")

try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)
except Exception as e:
    raise RuntimeError(f"Gagal memuat model/vectorizer: {e}")

# 🧼 Preprocessing
def bersihkan(teks: str) -> str:
    teks = re.sub(r'\W+', ' ', teks)  # hapus tanda baca
    teks = re.sub(r'\d+', '', teks)   # hapus angka
    return teks.lower().strip()

# 🔍 Endpoint prediksi
@app.post("/predict")
def predict(data: EmailInput):
    if not data.text:
        raise HTTPException(status_code=400, detail="Teks tidak boleh kosong")

    teks_bersih = bersihkan(data.text)
    vector = vectorizer.transform([teks_bersih])
    prediksi = model.predict(vector)

    return {
        "input": data.text,
        "label": "SPAM" if prediksi[0] == 1 else "HAM"
    }

# 🌐 Root endpoint
@app.get("/")
def root():
    return {"message": "🚀 FastAPI Spam Detector Aktif"}

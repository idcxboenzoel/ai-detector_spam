from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from spam_detector.spam_classifier import classify_text
from fastapi.responses import FileResponse
import csv
import os
import chardet
import pandas as pd

router = APIRouter()
templates = Jinja2Templates(directory="webapp/templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "prediction": None
    })

@router.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    contents = await file.read()

    # Deteksi encoding
    detected = chardet.detect(contents)
    encoding = detected.get("encoding") or "utf-8"

    try:
        text_lines = contents.decode(encoding).splitlines()
    except UnicodeDecodeError:
        try:
            text_lines = contents.decode("ISO-8859-1").splitlines()
            encoding = "ISO-8859-1 (fallback)"
        except Exception:
            text_lines = contents.decode("utf-8", errors="ignore").splitlines()
            encoding = "utf-8 (ignore errors)"
            return {"message": f"File berhasil dibaca dengan encoding: {encoding}", "data": text_lines}

    text_lines = [line for line in text_lines if line.strip()]
    result = [classify_text(line) for line in text_lines]

    if len(text_lines) != len(result):
        return {"message": f"Panjang baris ({len(text_lines)}) tidak cocok dengan hasil prediksi ({len(result)})"}

    df = pd.DataFrame({"Text": text_lines, "Prediction": result})
    df.to_csv("log_prediksi.csv", index=False)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "multi_result": zip(text_lines, result)
    })

@router.get("/download")
async def download_log():
    file_path = "log_prediksi.csv"
    if not os.path.exists(file_path):
        return {"message": "Belum ada prediksi yang disimpan."}
    return FileResponse(path=file_path, filename="log_prediksi.csv", media_type='text/csv')

@router.post("/predict", response_class=HTMLResponse)
def predict(request: Request, message: str = Form(...)):
    prediction = classify_text(message)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "prediction": prediction,
        "message": message
    })
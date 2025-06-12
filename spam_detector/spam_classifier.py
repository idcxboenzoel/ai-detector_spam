import re
from spam_detector.model_loader import model, vectorizer

def bersihkan(teks):
    teks = re.sub(r'\W+', ' ', teks)
    teks = re.sub(r'\d+', '', teks)
    teks = teks.lower().strip()
    return teks

def classify_text(teks: str) -> str:
    teks_bersih = bersihkan(teks)
    vektorisasi = vectorizer.transform([teks_bersih])
    hasil = model.predict(vektorisasi)
    return "SPAM" if hasil[0] == 1 else "HAM"

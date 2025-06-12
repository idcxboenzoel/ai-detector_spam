
# Spam Detector CLI 🛑📧

Alat pendeteksi spam berbasis Machine Learning (Naive Bayes) untuk email/SMS, dapat dijalankan langsung dari terminal.

![PyPI](https://img.shields.io/pypi/v/spam-detector-cli)
![Python](https://img.shields.io/pypi/pyversions/spam-detector-cli)

---

## ✨ Fitur

- Deteksi SPAM / HAM berbasis Naive Bayes
- Preprocessing teks otomatis
- Logging hasil ke CSV
- Deteksi batch dari file
- Command-line interface interaktif

---

## 🔧 Instalasi

```bash
pip install spam-detector-cli
```

---

## 🚀 Cara Pakai

Setelah terinstal, jalankan:

```bash
spam-detector
```

Lalu:

- Ketik email untuk dideteksi
- Perintah `stats` → statistik SPAM/HAM
- Perintah `clear` → bersihkan log
- Perintah `predictfile nama_file.txt` → deteksi banyak email
- Perintah `exit` → keluar
- `--help` atau `-h` → panduan CLI

---

## 📂 Struktur Log

Hasil disimpan ke:

```
log_prediksi.csv
```

Dengan format:

| teks | hasil |
|------|-------|
| "contoh email spam" | SPAM |
| "halo teman lama"   | HAM  |

---

## 📦 Dataset

Menggunakan dataset publik dari UCI Spam Collection.

---

## 🧠 Model

- **Vectorizer**: TfidfVectorizer
- **Model**: Multinomial Naive Bayes
- Akurasi rata-rata ~95%

---

## 🛠 Pengembangan Lokal

Clone dan jalankan:

```bash
git clone https://github.com/username/spam-detector-cli
cd spam-detector-cli
pip install -e .
spam-detector
```

---

## 📝 Lisensi

Proyek ini berlisensi MIT. Silakan gunakan dan kontribusi!

---

## ✉️ Kontak

Dikembangkan oleh [Nama Kamu](mailto:email@domain.com)

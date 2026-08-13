# ================================================================
# ASUMSI struktur project backend (SESUAIKAN kalau beda):
#   backend/requirements.txt
#   backend/run.py         <- entry point Flask, punya variabel `app` hasil create_app()
#   backend/app/           <- source code (routes, services, models, dst)
#   backend/config.py      <- Flask config classes (config_by_name), sesuai
#                              import "from config import config_by_name" di __init__.py
# ================================================================
FROM python:3.11-slim

WORKDIR /app

# Dependency sistem:
# - libgl1, libglib2.0-0 : WAJIB untuk OpenCV (cv2) -- tanpa ini import cv2
#   akan error "ImportError: libGL.so.1: cannot open shared object file"
# (libpq-dev/gcc TIDAK dibutuhkan karena requirements.txt pakai
# psycopg2-binary, yang sudah precompiled -- tidak perlu compile dari source)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt DULU, sebelum copy source code -- supaya layer
# Docker ini ke-cache dan tidak install ulang semua dependency tiap kali
# cuma ada perubahan kode (bukan perubahan requirements.txt).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Model CLIP otomatis terunduh saat clip_handler.py pertama kali di-import
# (CLIPModel.from_pretrained). Uncomment 3 baris di bawah untuk 'bake'
# model ke dalam image saat build -- startup container jadi lebih cepat,
# tapi image jadi lebih besar (~350MB tambahan). Sesuaikan nama model
# dengan CLIP_MODEL_NAME di settings kamu.
# RUN python -c "from transformers import CLIPModel, CLIPProcessor; \
#     CLIPModel.from_pretrained('openai/clip-vit-base-patch32'); \
#     CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')"

COPY . .

EXPOSE 5000

# Gunicorn untuk production (bukan flask dev server / app.run()).
# --timeout 120 sengaja dilebihkan dari default 30 detik, karena request
# cek video (ekstraksi frame + CLIP + Groq berkali-kali) bisa makan waktu
# cukup lama -- worker timeout default akan mematikan request itu paksa.
# 'run:app' asumsi run.py punya variabel `app`, ganti kalau beda.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "run:app"]

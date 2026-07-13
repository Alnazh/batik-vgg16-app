# ============================================================
# Dockerfile
# Digunakan untuk membangun image container aplikasi Batik AI
# Classifier, supaya bisa dijalankan konsisten di server manapun
# (Render, Railway, VPS, dll) tanpa masalah perbedaan environment.
# ============================================================

FROM python:3.11-slim

# Supaya log Python langsung tampil di terminal, tidak ditahan oleh buffer
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependensi sistem yang dibutuhkan Pillow & TensorFlow
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements dulu agar layer cache Docker lebih optimal
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh source code aplikasi
COPY . .

# Port yang dipakai gunicorn saat container berjalan
EXPOSE 5000

# Jalankan aplikasi dengan gunicorn (production WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]

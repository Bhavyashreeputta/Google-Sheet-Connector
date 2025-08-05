FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python deps first (build cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code (including service_account.json for hardcoded auth)
COPY . .

# Cloud Run listens on $PORT; we bind to 8080 which matches the default
EXPOSE 8080

# Gunicorn: 2 workers, threaded to keep it simple
CMD ["gunicorn", "-w", "2", "-k", "gthread", "--threads", "8", "-b", "0.0.0.0:8080", "app:app"]

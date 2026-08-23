# Production Dockerfile for Google Cloud Run (FastAPI Backend)
FROM python:3.11-slim

# Prevent Python from buffering stdout and writing .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Google Cloud Run dynamically injects the PORT environment variable (default: 8080)
EXPOSE 8080

# Run with uvicorn listening on 0.0.0.0 and $PORT
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}

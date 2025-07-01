# Use a minimal base image
FROM python:3.11-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE -> Prevents .pyc files — cleaner containers
# PYTHONUNBUFFERED -> Ensures real-time logs in Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a working directory
WORKDIR /app

# Install system dependencies (if any are needed by requirements.txt, e.g., psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application folders and files
COPY backend/app ./app
COPY .env .
COPY dataset ./dataset

# Expose FastAPI port
EXPOSE 8000

# Use uvicorn to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

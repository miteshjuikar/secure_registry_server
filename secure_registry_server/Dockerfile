FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# PostgreSQL client only
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Cache Python dependencies (CI/CD optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

EXPOSE 10000

# Run migrations + collectstatic + start server (all at runtime with env vars)
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn secure_registry_server.wsgi:application \
    --bind 0.0.0.0:10000 \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --log-level info

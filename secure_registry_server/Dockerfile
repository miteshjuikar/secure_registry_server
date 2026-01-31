FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Minimal PostgreSQL client only
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Cache dependencies (CI/CD speed)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Only collectstatic at build time (no DB needed)
RUN python manage.py collectstatic --noinput

EXPOSE 10000

# Run migrations THEN start server (key fix)
CMD python manage.py migrate --noinput && \
    gunicorn secure_registry_server.wsgi:application \
    --bind 0.0.0.0:10000 \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --log-level info

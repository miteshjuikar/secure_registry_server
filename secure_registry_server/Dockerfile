FROM python:3.12-slim

# Prevent Python from writing .pyc files & buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install only runtime PostgreSQL deps (no gcc needed)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy & install Python deps first (CI/CD cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Fix auth_user table issue - RUN MIGRATIONS AT BUILD TIME
RUN python manage.py collectstatic --noinput && \
    python manage.py makemigrations --noinput && \
    python manage.py migrate --noinput

# Expose Render port
EXPOSE 10000

# Production Gunicorn
CMD ["gunicorn", "secure_registry_server.wsgi:application", \
     "--bind", "0.0.0.0:10000", \
     "--workers=2", \
     "--threads=4", \
     "--timeout=120", \
     "--log-level=info"]

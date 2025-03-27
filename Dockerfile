FROM python:3.9.21-slim

WORKDIR /app

# Install system dependencies (minimal requirements for SQLite)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=web_sac.settings_docker

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Create directory for SQLite database
RUN mkdir -p /app/db

# Copy project
COPY . .

# Set permissions for the database directory
RUN chmod 777 /app/db

# Collect static files
RUN python manage.py collectstatic --noinput

# Run as non-root user for better security
RUN useradd -m appuser
USER appuser

# Set entry point
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web_sac.wsgi:application"] 
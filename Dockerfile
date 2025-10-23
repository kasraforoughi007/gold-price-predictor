FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer logs
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/

# Installing system dependencies
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    tzdata \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    python3-dev \
    ca-certificates \
    curl \
 && update-ca-certificates \
 && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
 && rm -rf /var/lib/apt/lists/*

# Installing Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copying project files
COPY . /app/

# Checking if Yahoo Finance blocks us or not
RUN curl -I https://query1.finance.yahoo.com/v7/finance/download/GLD || echo "⚠️ Warning: Yahoo Finance not reachable during build."

# accesing to postgres-db servers on port 5432 and if it succeeded , it will run migrations and our main forecast script ( gold_prediction.py ) then the django app
CMD ["sh", "-c", "until nc -z postgres-db 5432; do echo 'Waiting for db ...'; sleep 2; done && \
python manage.py migrate && \
python gold_app/code/gold_prediction.py && \
gunicorn myproject.wsgi:application --bind 0.0.0.0:8000"]

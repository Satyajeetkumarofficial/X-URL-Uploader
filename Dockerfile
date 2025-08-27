FROM python:3.11-slim

# Install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Run both bot + dummy healthcheck server
CMD ["sh", "-c", "python3 healthcheck.py & python3 -m Bot"]

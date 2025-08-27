FROM python:3.10-slim

# Install system deps
RUN apt-get update && apt-get install -y \
    ffmpeg wget unzip \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy project
COPY . /app

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Run both bot + dummy healthcheck server
CMD ["sh", "-c", "python3 healthcheck.py & python3 -m Bot"]

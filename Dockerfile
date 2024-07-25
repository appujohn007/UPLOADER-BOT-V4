FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY needs.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r needs.txt

COPY . .

CMD ["python", "bot.py"]

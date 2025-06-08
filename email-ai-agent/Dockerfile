FROM python:3.11-slim-bullseye
WORKDIR /app
COPY . .
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends tesseract-ocr && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:$PORT", "src.web.app:app"]
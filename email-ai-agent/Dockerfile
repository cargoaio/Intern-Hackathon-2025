FROM python:3.11-slim

# Install Tesseract and system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set tesseract path as an environment variable
ENV TESSERACT_PATH=/usr/bin/tesseract

# Expose port
EXPOSE 8000

# Command to run the app
# CMD ["gunicorn", "src.web.app:app"]
CMD ["sh", "-c", "gunicorn src.web.app:app --bind 0.0.0.0:${PORT}"]


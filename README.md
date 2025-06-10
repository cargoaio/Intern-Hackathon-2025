---

# AI Email Processing System 📧✨

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)
![Groq](https://img.shields.io/badge/Groq-API-orange)
![License](https://img.shields.io/badge/license-MIT-blue)



[![Website](https://img.shields.io/website?url=https://intern-hackathon-2025.onrender.com/&style=for-the-badge)](https://intern-hackathon-2025.onrender.com/)

## 🚀 Live Demo

Check out the live application: [AI Email Processor](https://intern-hackathon-2025.onrender.com/)

## Preview

<div align="center">
  <img src="https://drive.google.com/file/d/1v4kUv0bdQu1qIx6m32LzzIdGGcaE79RY/view?usp=sharing" alt="AI Email Processor Preview" width="600px">
</div>

An end-to-end email processing pipeline featuring AI-powered summarization, advanced attachment parsing, and multi-format support.

## 🌟 Key Features

- **Multi-Format Email Parsing**
  - Native `.eml` and Outlook `.msg` support
  - Metadata extraction (From/To/Subject/Date)
  - MIME-aware body parsing

- **AI Summarization**
  - Groq API integration (Llama 3 70B model)
  - Structured prompt engineering
  - Rate-limited API calls

- **Smart Attachment Processing**
  - PDF text extraction (PyPDF2)
  - Word document parsing (python-docx)
  - Image OCR (Tesseract)
  - Graceful fallback handling

- **RESTful API**
  - File upload endpoint
  - Batch processing
  - JSON results API

## 🏗️ Architecture Overview

```mermaid
graph TB
    A[Email File Upload] --> B[Email Parser]
    B --> C{Email Type}
    C -->|.eml| D[EML Parser]
    C -->|.msg| E[MSG Parser]
    D --> F[Extract Metadata]
    E --> F
    F --> G[Extract Body Content]
    G --> H[Extract Attachments]
    H --> I{Attachment Type}
    I -->|PDF| J[PDF Text Extractor]
    I -->|DOCX| K[Word Document Parser]
    I -->|Image| L[OCR Text Extraction]
    I -->|Other| M[Base64 Storage]
    J --> N[Compile Email Data]
    K --> N
    L --> N
    M --> N
    N --> O[AI Summarizer]
    O --> P[Groq API Call]
    P --> Q[Generate Summary]
    Q --> R[JSON Response]
    R --> S[Web Interface Display]
    
    style A fill:
    style O fill:#c63939
    style P fill:
    style Q fill:
    style R fill:
    style S fill:
```

## 📂 Core Components

### `email_parser.py`
```python
def parse_email(email_path):
    """
    Windows-friendly MIME parser with:
    - Multi-part email handling
    - Attachment extraction
    - Error-resilient decoding
    """
```

### `summarizer.py`
```python
class EmailSummarizer:
    """
    Groq-powered AI summarizer featuring:
    - Rate-limited API calls (1/sec)
    - Structured prompt engineering
    - Error handling with retries
    """
```

### `document_processor.py`
```python
def process_attachment(attachment):
    """
    Universal attachment processor with:
    - File type detection
    - PDF/DOCX/Image handling
    - Cascading fallback logic
    """
```

### `app.py`
```python
@app.route('/api/process')
def process_email():
    """
    Orchestrates the full pipeline:
    1. Email parsing
    2. Attachment processing
    3. AI summarization
    4. Result storage
    """
```

## 🔌 API Endpoints

| Endpoint             | Method | Description                   |
|----------------------|--------|-------------------------------|
| `/upload`            | POST   | Accepts .eml/.msg files       |
| `/api/process`       | POST   | Triggers email processing     |
| `/api/results/<id>`  | GET    | Retrieves processed results   |
| `/api/save-summary`  | POST   | Saves edited summaries        |

## 🚀 Deployment Guide

### Prerequisites
- Groq API key
- Tesseract OCR installed
- Python 3.8+

```bash
# Installation
git clone https://github.com/KaranKumar2326/Intern-Hackathon-2025.git
cd Intern-Hackathon-2025
cd email-ai-agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configuration
echo "GROQ_API_KEY=your_key_here" > .env
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env

Otherwise set above keys manually in .env file.

# Running
python src\web\app.py
```

### Docker Setup

```dockerfile
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


```

## 📊 Sample API Response

```json
{
  "processing_timestamp": "2023-11-15T12:34:56",
  "email": {
    "from": "sender@example.com",
    "subject": "Quarterly Report",
    "date": "Thu, 16 Nov 2023 09:00:00 +0000"
  },
  "summary": {
    "content": "The email discusses Q3 results...",
    "model": "meta-llama/llama-3-70b",
    "status": "success"
  },
  "attachments": [
    {
      "filename": "report.pdf",
      "type": "pdf",
      "text": "Extracted PDF content..."
    }
  ]
}
```

## 🛠️ Development Notes

### Attachment Processing Logic

1. **Primary Detection**:
    ```python
    if filename.endswith('.pdf'):
        return _process_pdf(payload)
    ```
2. **Content Sniffing**:
    ```python
    if payload.startswith(b'%PDF'):
        return _process_pdf(payload)
    ```
3. **Fallback**:
    ```python
    return {
        "type": "unknown",
        "error": "Unprocessable format"
    }
    ```

### Groq API Integration

```python
payload = {
    "model": "meta-llama/llama-3-70b",
    "messages": [
        {"role": "system", "content": "You are an email summarization expert"},
        {"role": "user", "content": formatted_prompt}
    ],
    "temperature": 0.3,
    "max_tokens": 300
}
```

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Maintainer:**  
Karan Kumar ([karanyadav3775@gmail.com](mailto:karanyadav3775@gmail.com))

---

import os
import requests
import time
import logging
from typing import Dict, Any
from dotenv import load_dotenv

class EmailSummarizer:
    def __init__(self):
        """Initialize Groq API client"""
        load_dotenv()
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")

        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"
        self.last_call_time = 0
        self.min_call_interval = 1  # 1 second between calls

    def generate_summary(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary using Groq API"""
        current_time = time.time()
        elapsed = current_time - self.last_call_time
        if elapsed < self.min_call_interval:
            time.sleep(self.min_call_interval - elapsed)

        try:
            prompt = self._build_prompt(email_data)

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that summarizes emails concisely."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 300  # slightly raised for flexibility
            }

            response = requests.post(self.endpoint, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            self.last_call_time = time.time()
            return {
                "summary": result["choices"][0]["message"]["content"],
                "model": self.model,
                "status": "success"
            }

        except Exception as e:
            logging.error(f"Summary generation failed: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }

    def _build_prompt(self, email_data: Dict[str, Any]) -> str:
        """Build prompt for summarization"""
        return f"""Summarize this email concisely (100 words max):

From: {email_data['email']['from']}
Subject: {email_data['email']['subject']}
Date: {email_data['email']['date']}

Body:
{email_data['body'][:2000]}

Attachments:
{email_data['attachments']}

Key points to extract:
1. Main purpose
2. Action items
3. Important details
4. Numerical data
5. Summary of attachments (if any)
"""

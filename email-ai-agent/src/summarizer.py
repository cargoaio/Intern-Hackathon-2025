import os
from dotenv import load_dotenv
from openai import OpenAI
import time
import logging
from typing import Dict, Any

class EmailSummarizer:
    def __init__(self):
        """Initialize with proper API key validation"""
        load_dotenv()
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        try:
            self.client = OpenAI(api_key=self.api_key)
            self.model = "gpt-3.5-turbo"
            self.last_call_time = 0
            self.min_call_interval = 1  # 1 second between calls for OpenAI
        except Exception as e:
            logging.error(f"Failed to initialize OpenAI client: {str(e)}")
            raise

    def generate_summary(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary with robust error handling"""
        if not hasattr(self, 'client'):
            return {
                "error": "OpenAI client not initialized",
                "status": "failed"
            }

        current_time = time.time()
        elapsed = current_time - self.last_call_time
        
        # Enforce rate limiting
        if elapsed < self.min_call_interval:
            time.sleep(self.min_call_interval - elapsed)

        try:
            prompt = self._build_prompt(email_data)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes emails concisely."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            self.last_call_time = time.time()
            return {
                "summary": response.choices[0].message.content,
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
        """Build efficient prompt"""
        return f"""Summarize this email concisely (100 words max):

From: {email_data['email']['from']}
Subject: {email_data['email']['subject']}
Date: {email_data['email']['date']}

Body:
{email_data['body'][:2000]}


Attachments:
# include attachment data
{email_data['attachments']}

Key points to extract:
1. Main purpose
2. Action items
3. Important details
4. Numerical data
5. Summary of attachments (if any)  """

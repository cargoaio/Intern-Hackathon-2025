import email
from email import policy
from pathlib import Path
import json

def parse_email(email_path):
    """Windows-friendly email parser"""
    email_path = Path(email_path)
    with open(email_path, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=policy.default)
    
    metadata = {
        'from': msg['from'],
        'to': msg['to'],
        'subject': msg['subject'],
        'date': msg['date']
    }
    
    body = ""
    attachments = []
    
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            body = part.get_payload(decode=True).decode(errors='ignore')
        elif part.get_filename():
            attachments.append({
                'filename': part.get_filename(),
                'content_type': part.get_content_type(),
                'payload': part.get_payload(decode=True)
            })
    
    return {
        'metadata': metadata,
        'body': body,
        'attachments': attachments,
        'source_file': email_path.name,
        'id': email_path.stem  # Added ID for web interface
    }

def get_emails():
    """Get all emails from the emails directory"""
    emails_dir = Path(__file__).parent.parent / "emails"
    emails = []
    
    for eml_file in emails_dir.glob("*.eml"):
        parsed = parse_email(eml_file)
        emails.append({
            'id': eml_file.stem,
            'subject': parsed['metadata']['subject'],
            'sender': parsed['metadata']['from'],
            'date': parsed['metadata']['date'],
            'preview': parsed['body'][:100] + '...' if parsed['body'] else ''
        })
    
    return emails

def get_email(email_id):
    """Get single email by ID (filename without extension)"""
    email_path = Path(__file__).parent.parent / "emails" / f"{email_id}.eml"
    if not email_path.exists():
        return None
    
    parsed = parse_email(email_path)
    return {
        'id': email_id,
        'subject': parsed['metadata']['subject'],
        'sender': parsed['metadata']['from'],
        'date': parsed['metadata']['date'],
        'body': parsed['body'],
        'attachments': parsed['attachments']
    }

if __name__ == "__main__":
    print(json.dumps(get_emails(), indent=2))
    print(json.dumps(get_email("test1"), indent=2))
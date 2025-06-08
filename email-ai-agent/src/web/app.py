import sys
from pathlib import Path
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
import json
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from extract_msg import Message  

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Now import your modules
from email_parser import parse_email
from summarizer import EmailSummarizer
from document_processor import process_attachment

app = Flask(__name__)


# Configure paths and allowed extensions
BASE_DIR = Path(__file__).resolve().parents[2]
print(f"Base directory: {BASE_DIR}")
EMAILS_DIR = BASE_DIR / "emails"
OUTPUT_DIR = BASE_DIR / "output"
ALLOWED_EXTENSIONS = {'eml', 'msg'}

# Ensure directories exist
EMAILS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(EMAILS_DIR / filename)
        flash('File successfully uploaded')
        return redirect(url_for('index'))
    
    flash('Invalid file type. Only .eml and .msg files allowed')
    return redirect(url_for('index'))

@app.route('/api/emails')
def get_available_emails():
    """List all available .eml files"""
    emails = []
    for eml_file in EMAILS_DIR.glob("*.*"):
        if eml_file.suffix.lower() in ('.eml', '.msg'):
            emails.append({
                'id': eml_file.stem,
                'filename': eml_file.name,
                'path': str(eml_file),
                'size': f"{os.path.getsize(eml_file) / 1024:.1f} KB",
                'upload_time': datetime.fromtimestamp(
                    os.path.getmtime(eml_file)
                ).strftime('%Y-%m-%d %H:%M:%S')
            })
    return jsonify(sorted(emails, key=lambda x: x['upload_time'], reverse=True))



@app.route('/api/process', methods=['POST'])
def process_email():
    """Process selected email (.eml or .msg) and generate summary"""
    email_id = request.json.get('email_id')
    
    # Try both .eml and .msg
    eml_file = EMAILS_DIR / f"{email_id}.eml"
    msg_file = EMAILS_DIR / f"{email_id}.msg"
    
    if eml_file.exists():
        email_data = parse_email(eml_file)
    elif msg_file.exists():
        email_data = parse_msg_email(msg_file)  # new function
    else:
        return jsonify({'error': 'Email not found'}), 404
    
    # Process attachments
    processed_attachments = []
    for att in email_data['attachments']:
        processed = process_attachment(att)
        processed_attachments.append(processed)
    
    # Generate summary
    summarizer = EmailSummarizer()
    summary = summarizer.generate_summary({
        'email': email_data['metadata'],
        'body': email_data['body'],
        'attachments': processed_attachments
    })
    
    # Prepare result
    result = {
        'processing_timestamp': datetime.now().isoformat(),
        'email': email_data['metadata'],
        'body': email_data['body'],
        'attachments': processed_attachments,
        'summary': summary,
        'source_file': email_data['source_file']
    }
    
    # Save to output
    output_file = OUTPUT_DIR / f"{email_id}.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    return jsonify(result)


from extract_msg import Message

def parse_msg_email(file_path):
    """Parses .msg (Outlook) email files"""
    msg = Message(str(file_path))
    msg_subject = msg.subject or "No subject"
    msg_sender = msg.sender or "Unknown"
    msg_to = msg.to or "Unknown"
    msg_date = msg.date or "Unknown"
    msg_body = msg.body or ""

    if isinstance(msg_date, datetime):
        msg_date = msg_date.isoformat()

    # Extract attachments
    attachments = []
    for att in msg.attachments:
        attachments.append({
            'filename': att.longFilename or att.shortFilename or "unknown",
            'data': att.data,
            'type': 'unknown'  # You can add MIME detection here
        })

    return {
        'metadata': {
            'from': msg_sender,
            'to': msg_to,
            'subject': msg_subject,
            'date': msg_date
        },
        'body': msg_body,
        'attachments': attachments,
        'source_file': str(file_path)
    }


@app.route('/api/results/<email_id>')
def get_result(email_id):
    """Get processing results if available"""
    json_file = OUTPUT_DIR / f"{email_id}.json"
    if json_file.exists():
        with open(json_file, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({'status': 'not processed'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
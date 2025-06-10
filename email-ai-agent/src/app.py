from email_parser import parse_email
from document_processor import process_attachment
from summarizer import EmailSummarizer 
from pathlib import Path
import json
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_processor.log'),
        logging.StreamHandler()
    ]
)

def process_emails(input_dir="emails", output_dir="output"):
    """Process emails from input directory and save summarized results"""
    try:
        # Initialize components with error handling
        try:
            summarizer = EmailSummarizer()
        except Exception as init_error:
            logging.error(f"Failed to initialize summarizer: {init_error}")
            return

        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        # Validate directories
        if not input_path.exists():
            logging.error(f"Input directory not found: {input_path}")
            return
            
        output_path.mkdir(exist_ok=True, parents=True)
        
        # Process each email file
        processed_count = 0
        start_time = time.time()
        
        for email_file in input_path.glob("*.eml"):
            file_start_time = time.time()
            try:
                logging.info(f"Processing {email_file.name}")
                
                # Parse email with validation
                try:
                    email_data = parse_email(email_file)
                    if not all(k in email_data for k in ['metadata', 'body', 'attachments']):
                        raise ValueError("Invalid email data structure")
                except Exception as parse_error:
                    logging.error(f"Failed to parse {email_file.name}: {parse_error}")
                    continue
                
                # Process attachments with error handling
                processed_attachments = []
                for att in email_data['attachments']:
                    try:
                        processed = process_attachment(att)
                        processed_attachments.append(processed)
                    except Exception as att_error:
                        logging.warning(f"Failed to process attachment in {email_file.name}: {att_error}")
                        processed_attachments.append({
                            'error': str(att_error),
                            'original_filename': att.get('filename', 'unknown')
                        })
                
                # Generate summary with rate limiting
                summary = None
                try:
                    summary = summarizer.generate_summary({
                        'email': email_data['metadata'],
                        'body': email_data['body'],
                        'attachments': processed_attachments
                    })
                except Exception as summary_error:
                    logging.error(f"Summary failed for {email_file.name}: {summary_error}")
                    summary = {
                        'error': str(summary_error),
                        'status': 'failed'
                    }
                
                # Prepare and save result
                result = {
                    'processing_timestamp': datetime.now().isoformat(),
                    'email': email_data['metadata'],
                    'body': email_data['body'],
                    'attachments': processed_attachments,
                    'summary': summary,
                    'source_file': str(email_file.name)
                }
                
                output_file = output_path / f"{email_file.stem}.json"
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)
                    processed_count += 1
                except IOError as io_error:
                    logging.error(f"Failed to save {output_file}: {io_error}")
                
                # Adaptive rate limiting
                processing_time = time.time() - file_start_time
                delay = max(1.0 - processing_time, 0)  # Minimum 1s between emails
                time.sleep(delay)
                
            except Exception as e:
                logging.error(f"Unexpected error processing {email_file.name}: {e}")
                continue
        
        # Final report
        total_time = time.time() - start_time
        logging.info(
            f"Processing complete. {processed_count} emails processed in {total_time:.2f} seconds. "
            f"Average {total_time/max(1, processed_count):.2f} sec/email."
        )
        
    except Exception as global_error:
        logging.critical(f"Fatal error in email processing: {global_error}")

if __name__ == "__main__":
    process_emails()
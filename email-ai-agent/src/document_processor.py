import io
import PyPDF2
from docx import Document
import pytesseract
from PIL import Image
import logging

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def process_attachment(attachment):
    """Process email attachments with maximum reliability"""
    filename = attachment.get('filename', 'unnamed').lower()
    payload = attachment['payload']
    
    try:
        # First try to detect by filename
        if filename.endswith('.pdf') or filename.endswith('.pdf'):
            return _process_pdf(payload, filename)
        elif filename.endswith(('.docx', '.doc')):
            return _process_docx(payload, filename)
        elif filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
            return _process_image(payload, filename)
        
        # Fallback to content detection
        if payload.startswith(b'%PDF'):
            return _process_pdf(payload, filename)
        
        # Try as image (will fail gracefully if not an image)
        image_result = _process_image(payload, filename)
        if image_result['type'] != 'image_error':
            return image_result
            
        # Final fallback
        return {
            'type': 'unknown',
            'filename': filename,
            'text': '',
            'error': 'Could not determine file type'
        }
        
    except Exception as e:
        logger.error(f"Failed to process {filename}: {str(e)}")
        return {
            'type': 'error',
            'filename': filename,
            'text': f"Processing failed: {str(e)}"
        }

def _process_pdf(data, filename):
    """Extract text from PDF with error handling"""
    try:
        text = ""
        with io.BytesIO(data) as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return {
            'type': 'pdf',
            'filename': filename,
            'text': text.strip(),
            'pages': len(reader.pages)
        }
    except Exception as e:
        return {
            'type': 'pdf_error',
            'filename': filename,
            'text': f"PDF processing failed: {str(e)}"
        }

def _process_docx(data, filename):
    """Extract text from Word documents"""
    try:
        doc = Document(io.BytesIO(data))
        return {
            'type': 'docx',
            'filename': filename,
            'text': "\n".join(para.text for para in doc.paragraphs)
        }
    except Exception as e:
        return {
            'type': 'docx_error',
            'filename': filename,
            'text': f"DOCX processing failed: {str(e)}"
        }

def _process_image(data, filename):
    """Process image with OCR (text detection only)"""
    try:
        # Attempt to open image
        try:
            with Image.open(io.BytesIO(data)) as img:
                # Convert to RGB if needed
                if img.mode in ('RGBA', 'P', 'LA'):
                    img = img.convert('RGB')
                
                # Get basic info
                info = {
                    'format': img.format,
                    'dimensions': f"{img.width}x{img.height}",
                    'mode': img.mode
                }
                
                # Attempt OCR (text detection)
                try:
                    text = pytesseract.image_to_string(img)
                    print(text)
                    return {
                        'type': 'image',
                        'filename': filename,
                        'text': text.strip(),
                        'info': info
                    }
                except pytesseract.TesseractError as te:
                    return {
                        'type': 'image',
                        'filename': filename,
                        'text': '',
                        'info': info,
                        'error': f"OCR failed: {str(te)}"
                    }
                    
        except Image.UnidentifiedImageError:
            # Not a recognizable image format
            return {
                'type': 'image_error',
                'filename': filename,
                'text': 'Unrecognized image format'
            }
            
    except Exception as e:
        return {
            'type': 'image_error',
            'filename': filename,
            'text': f"Image processing failed: {str(e)}"
        }

import fitz  # PyMuPDF
from docx import Document
import pytesseract
from PIL import Image
from io import BytesIO
import hashlib
from app.core.config import TESSERACT_CMD

# Set the path to tesseract executable if not in PATH
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts text from a PDF file using PyMuPDF."""
    text = ""
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text.strip() or "Warning: No text detected in PDF"
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extracts text from a DOCX file using python-docx."""
    try:
        doc = Document(BytesIO(file_bytes))
        full_text = [para.text for para in doc.paragraphs]
        return "\n".join(full_text).strip() or "Warning: No text detected in DOCX"
    except Exception as e:
        return f"Error extracting DOCX: {str(e)}"


def extract_text_from_image(file_bytes: bytes) -> str:
    """Extracts text from an image using Tesseract OCR."""
    try:
        img = Image.open(BytesIO(file_bytes))
        text = pytesseract.image_to_string(img)
        return text.strip() or "Warning: No text detected in image"
    except pytesseract.TesseractNotFoundError:
        return "Error: Tesseract is not installed or not in PATH"
    except Exception as e:
        return f"Error extracting Image (OCR): {str(e)}"


def extract_text(file_bytes: bytes, filename: str, content_type: str) -> str:
    """Dispatches to the correct extraction function based on file extension or content type."""
    filename = filename.lower()
    
    if filename.endswith(".pdf") or content_type == "application/pdf":
        return extract_text_from_pdf(file_bytes)
    
    elif filename.endswith(".docx") or content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file_bytes)
    
    elif filename.endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp")) or content_type.startswith("image/"):
        return extract_text_from_image(file_bytes)
    
    elif filename.endswith(".txt") or content_type == "text/plain":
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                return file_bytes.decode("latin-1")
            except Exception:
                return "Error: Could not decode text file."
    
    else:
        return "Unsupported file type"


def process_file(file_bytes: bytes, filename: str, content_type: str) -> dict:
    """
    Processes a file and returns extracted text and file hash.
    """
    text = extract_text(file_bytes, filename, content_type)
    
    # Compute SHA-256 hash for duplicate checking
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    
    return {"text": text, "file_hash": file_hash}

import fitz
from app.services.file_processor import extract_text_from_pdf
import io

def create_test_pdf():
    """Creates a simple text-based PDF for testing."""
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "This is a test PDF for the Evidence Collection System.")
    page.insert_text((50, 70), "It contains multiple lines of text.")
    pdf_bytes = doc.write()
    doc.close()
    return pdf_bytes

def test_extraction():
    print("Testing PDF extraction...")
    pdf_bytes = create_test_pdf()
    text = extract_text_from_pdf(pdf_bytes)
    print(f"Extracted text:\n---\n{text}\n---")
    
    if "Evidence Collection System" in text:
        print("[SUCCESS] Text extraction test passed!")
    else:
        print("[FAILURE] Text extraction test failed!")

if __name__ == "__main__":
    test_extraction()

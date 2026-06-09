cat > extraction/utils.py << 'EOF'
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file page by page"""
    document = fitz.open(pdf_path)
    full_text = ""
    
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        full_text += page.get_text()
    
    document.close()
    return full_text

def clean_text(text):
    """Basic text cleaning"""
    text = text.replace('\n', ' ')
    text = ' '.join(text.split())
    return text.strip()
EOF
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file using PyPDF2.
    
    Args:
        file_path (str): Path to the PDF file.
    
    Returns:
        str: Extracted text from the PDF.
    
    Raises:
        ValueError: If the file is not a PDF.
    """
    if not file_path.lower().endswith('.pdf'):
        raise ValueError("Only PDF files are supported")
    
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:  # Ensure text extraction succeeded
            text += page_text + "\n"  # Add newline between pages
    
    return text.strip()
from PyPDF2 import PdfReader


def read_pdf(file_path):
    """Extract selectable text from a PDF file."""
    reader = PdfReader(file_path)
    extracted_text = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            extracted_text.append(page_text)
    text = "\n".join(extracted_text).strip()
    if not text:
        raise ValueError(
            "No selectable text was found. "
            "Scanned PDFs need OCR before upload."
        )
    return text

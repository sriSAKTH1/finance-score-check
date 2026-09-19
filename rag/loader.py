from pathlib import Path
from pypdf import PdfReader


def load_pdf(pdf_path: str, source_name: str) -> list[dict]:
    """
    Extract text page-by-page from a PDF.
    """

    reader = PdfReader(pdf_path)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        if not text.strip():
            continue

        documents.append({
            "text": text,
            "metadata": {
                "source": source_name,
                "page": page_number
            }
        })

    return documents
# utils/extractor.py

import fitz  # PyMuPDF
from typing import Union

def extract_text_from_pdf(contents: Union[bytes, str]) -> str:
    """
    Extracts text from a PDF file (passed as bytes).
    Returns clean concatenated text from all pages.
    """
    doc = fitz.open(stream=contents, filetype="pdf")
    text = "\n".join([page.get_text() for page in doc])
    return text

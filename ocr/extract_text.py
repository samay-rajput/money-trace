import pdfplumber
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path



def extract_with_pdfplumber(pdf_path: str) -> str:
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


def extract_with_pymupdf(pdf_path: str) -> str:
    text = ""

    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text() + "\n"

    return text


def extract_with_ocr(pdf_path: str) -> str:
    text = ""

    pages = convert_from_path(pdf_path, dpi=300)
    for page in pages:
        text += pytesseract.image_to_string(page) + "\n"

    return text


def extract_text(pdf_path: str) -> str:
    text = extract_with_pdfplumber(pdf_path)

    if len(text.strip()) > 500:
        return text

    text = extract_with_pymupdf(pdf_path)
    if len(text.strip()) > 500:
        return text

    return extract_with_ocr(pdf_path)


if __name__ == "__main__":
    pdf_path = "../pdfs/sample_statement.pdf"
    raw_text = extract_with_pdfplumber(pdf_path)
    print(raw_text)



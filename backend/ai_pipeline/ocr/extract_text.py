import pdfplumber
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path

from PIL import Image 


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


def extract_from_pdf(pdf_path: str) -> str:
    text = extract_with_pdfplumber(pdf_path)

    if len(text.strip()) > 500:
        return text

    text = extract_with_pymupdf(pdf_path)
    if len(text.strip()) > 500:
        return text

    return extract_with_ocr(pdf_path)


def extract_from_image(image_path: str) -> str:
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text


import os

def extract_text_auto(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        return extract_from_pdf(path)   # existing PDF pipeline
    else:
        return extract_from_image(path)  # direct OCR


if __name__ == "__main__":
    pdf_path = "../../../sample_pdfs/sample_image.jpeg"
    raw_text = extract_text_auto(pdf_path)
    print(raw_text)
import pytesseract
from PIL import Image
from docx import Document
import pdfplumber
from pdf2image import convert_from_path

def ocr_image(image_path: str, lang:str = "vie+eng") -> str:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang=lang)
    return text


def extract_docx(docx_path: str) -> str:
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


def extract_pdf(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    if not text.strip():
        images = convert_from_path(pdf_path)
        for image in images:
            page_text = pytesseract.image_to_string(image, lang="vie+eng")
            text += page_text + "\n"
    return text
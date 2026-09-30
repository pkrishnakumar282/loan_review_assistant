import os
import fitz
import pytesseract

from PIL import Image


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF.

    Uses normal PDF text extraction first.
    If a page contains little/no text, OCR is attempted.
    """

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        text = page.get_text("text").strip()

        # OCR fallback for scanned pages
        if len(text) < 30:

            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            try:
                text = pytesseract.image_to_string(image)
            except Exception:
                text = ""

        pages.append({
            "page": page_number,
            "text": text,
            "source": os.path.basename(pdf_path)
        })

    document.close()

    return pages
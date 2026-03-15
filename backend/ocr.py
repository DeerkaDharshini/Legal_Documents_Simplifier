import easyocr
import cv2
import numpy as np
from PIL import Image
from pdf2image import convert_from_bytes
import io

# Initialize OCR reader
reader = easyocr.Reader(['en'], gpu=False)


def preprocess_image(image):
    """
    Improve image quality for better OCR accuracy
    """

    # Convert PIL image to OpenCV format
    img = np.array(image)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Noise removal
    denoise = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)

    # Increase contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(denoise)

    # Thresholding (important for old docs)
    thresh = cv2.adaptiveThreshold(
        contrast,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return thresh


def extract_text_from_image(image):
    """
    OCR for image files
    """

    processed = preprocess_image(image)

    results = reader.readtext(processed)

    text = " ".join([res[1] for res in results])

    return text


def extract_text_from_pdf(pdf_bytes):
    """
    OCR for scanned PDFs
    """

    images = convert_from_bytes(
    pdf_bytes,
    poppler_path=r"c:\Users\Admin\Downloads\Release-24.02.0-0\poppler-24.02.0\Library\bin"
)

    full_text = ""

    for image in images:
        processed = preprocess_image(image)

        results = reader.readtext(processed)

        page_text = " ".join([res[1] for res in results])

        full_text += page_text + "\n"

    return full_text
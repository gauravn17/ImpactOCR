# ocr/handwriting.py
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
import cv2
import pytesseract
import numpy as np
from typing import Tuple


def extract_handwritten_text(
    image_path: str,
    roi: Tuple[int, int, int, int],
    lang: str = "eng"
) -> str:
    """
    Extract handwritten text from a specific region of an image using Tesseract OCR.

    Parameters
    ----------
    image_path : str
        Path to the input image.
    roi : Tuple[int, int, int, int]
        Region of interest defined as (x, y, width, height).
        This should correspond to the handwritten name/ID area.
    lang : str
        Language model for Tesseract OCR.

    Returns
    -------
    str
        Extracted text (cleaned).
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image from path: {image_path}")

    x, y, w, h = roi
    cropped = image[y:y + h, x:x + w]

    # Convert to grayscale
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    # Light thresholding to improve handwriting contrast
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Tesseract configuration for handwriting
    config = (
        "--oem 1 "          # LSTM OCR engine
        "--psm 7 "          # Single text line
        "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz "
    )

    text = pytesseract.image_to_string(
        thresh,
        lang=lang,
        config=config
    )

    return text.strip()

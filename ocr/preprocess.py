# ocr/preprocess.py
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
import cv2
import numpy as np


def preprocess_image(image_path: str) -> np.ndarray:
    """
    Load and preprocess an image for OCR and MCQ bubble detection.

    Pipeline:
    1. Load image from disk
    2. Convert to grayscale
    3. Apply Gaussian blur to reduce noise
    4. Apply adaptive thresholding to handle uneven lighting

    Parameters
    ----------
    image_path : str
        Path to the input image file.

    Returns
    -------
    np.ndarray
        Binary (thresholded) image suitable for downstream processing.
    """
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image from path: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Reduce high-frequency noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive thresholding (robust to lighting variation)
    binary = cv2.adaptiveThreshold(
        blurred,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=11,
        C=2
    )

    return binary

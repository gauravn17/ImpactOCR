import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
import cv2
import numpy as np
from typing import List, Dict


def detect_mcq_answers(
    binary_image: np.ndarray,
    choices_per_question: int = 4,
    fill_threshold: float = 0.5
) -> List[Dict]:
    """
    Detect filled MCQ bubbles from a preprocessed binary image.

    Parameters
    ----------
    binary_image : np.ndarray
        Binary image (white = filled regions).
    choices_per_question : int
        Number of answer options per question (default 4).
    fill_threshold : float
        Minimum fill ratio to consider a bubble filled.

    Returns
    -------
    List[Dict]
        One dict per question:
        {
            "question": int,
            "selected_option": str | None,
            "confidence": float
        }
    """

    # 1. Find contours
    contours, _ = cv2.findContours(
        binary_image,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    bubble_contours = []

    # 2. Filter contours that look like bubbles
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        aspect_ratio = w / float(h)

        # Heuristics for circular-ish bubbles
        if (
            15 < w < 60 and
            15 < h < 60 and
            0.8 < aspect_ratio < 1.2 and
            area > 200
        ):
            bubble_contours.append(cnt)

    if not bubble_contours:
        return []

    # 3. Sort top-to-bottom, then left-to-right
    bubble_contours = sorted(
        bubble_contours,
        key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0])
    )

    option_labels = [chr(ord("A") + i) for i in range(choices_per_question)]
    results = []

    # 4. Process bubbles in question-sized groups
    for i in range(0, len(bubble_contours), choices_per_question):
        group = bubble_contours[i:i + choices_per_question]

        if len(group) != choices_per_question:
            continue

        fill_ratios = []

        for cnt in group:
            mask = np.zeros(binary_image.shape, dtype="uint8")
            cv2.drawContours(mask, [cnt], -1, 255, -1)

            total_pixels = cv2.countNonZero(mask)
            filled_pixels = cv2.countNonZero(
                cv2.bitwise_and(binary_image, binary_image, mask=mask)
            )

            fill_ratio = (
                filled_pixels / float(total_pixels)
                if total_pixels > 0 else 0.0
            )

            fill_ratios.append(fill_ratio)

        max_fill = max(fill_ratios)
        selected_index = fill_ratios.index(max_fill)

        if max_fill >= fill_threshold:
            selected_option = option_labels[selected_index]
        else:
            selected_option = None

        results.append({
            "question": len(results) + 1,
            "selected_option": selected_option,
            "confidence": round(max_fill, 2)
        })

    return results

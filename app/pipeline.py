# app/pipeline.py

import sys
from pathlib import Path

# Ensure repo root is on PYTHONPATH (Streamlit Cloud)
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
from typing import Dict, List, Tuple
import pandas as pd

from ocr.preprocess import preprocess_image
from ocr.mcq_detector import detect_mcq_answers
from ocr.handwriting import extract_handwritten_text


def run_assessment_pipeline(
    image_path: str,
    answer_key: List[str],
    name_roi: Tuple[int, int, int, int],
) -> Dict:
    """
    Run the full OCR-based assessment pipeline on a single answer sheet.

    Parameters
    ----------
    image_path : str
        Path to the scanned answer sheet image.
    answer_key : List[str]
        Correct answers in order (e.g., ["A", "C", "B", ...]).
    name_roi : Tuple[int, int, int, int]
        ROI for handwritten name (x, y, w, h).

    Returns
    -------
    Dict
        Structured results including student name, answers, and score.
    """

    # 1. Extract student name
    student_name = extract_handwritten_text(
        image_path=image_path,
        roi=name_roi
    )

    # 2. Preprocess image for MCQ detection
    binary_image = preprocess_image(image_path)

    # 3. Detect MCQ answers
    detected_answers = detect_mcq_answers(binary_image)

    # 4. Grade answers
    graded = []
    total_correct = 0

    for idx, detected in enumerate(detected_answers):
        correct_answer = answer_key[idx] if idx < len(answer_key) else None
        selected = detected["selected_option"]

        is_correct = selected == correct_answer
        if is_correct:
            total_correct += 1

        graded.append({
            "question": idx + 1,
            "selected": selected,
            "correct": correct_answer,
            "is_correct": is_correct,
            "confidence": detected["confidence"]
        })

    score_percent = round(
        (total_correct / len(answer_key)) * 100, 2
    ) if answer_key else 0.0

    return {
        "student_name": student_name,
        "total_correct": total_correct,
        "total_questions": len(answer_key),
        "score_percent": score_percent,
        "details": graded
    }


def results_to_dataframe(results: Dict) -> pd.DataFrame:
    """
    Convert detailed results to a Pandas DataFrame.

    Parameters
    ----------
    results : Dict
        Output from run_assessment_pipeline.

    Returns
    -------
    pd.DataFrame
        Per-question grading table.
    """
    return pd.DataFrame(results["details"])

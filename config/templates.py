# config/templates.py

"""
Answer sheet templates.

Each template defines fixed regions for:
- handwritten name
- (optionally) MCQ region
- number of choices per question

Teachers never see these values.
"""

TEMPLATES = {
    "Class 8 – Midterm MCQ (2025)": {
        "name_roi": (100, 50, 600, 120),
        "choices_per_question": 4
    },

    # Example future template
    # "Class 10 – Unit Test": {
    #     "name_roi": (90, 40, 580, 110),
    #     "choices_per_question": 4
    # }
}

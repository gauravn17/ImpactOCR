# ImpactOCR

Try it live at : https://impactocr.streamlit.app/

-Offline OCR-based assessment platform that digitizes and grades paper-based MCQ tests, enabling baseline and endline impact analysis in low-connectivity environments.

-Designed for NGOs, schools, and education programs where internet access is unreliable, AssessAI converts scanned answer sheets into structured, sponsor-ready analytic-s.

<img width="1710" height="1107" alt="Screenshot 2026-01-29 at 12 37 51 PM" src="https://github.com/user-attachments/assets/1b3f21a4-8165-490c-b2c7-306671a35495" />

---

## 🎯 Problem

Many education programs rely on **paper-based assessments** due to limited internet access.  
Manually grading these tests is slow, error-prone, and makes it difficult to quantify learning impact for sponsors.

AssessAI solves this by automating:
- MCQ grading
- Student-level scoring
- Baseline vs endline improvement analysis

—all **offline**.

---

## 🧠 System Architecture
Scanned Answer Sheets
↓
Image Preprocessing (OpenCV)
	•	grayscale
	•	noise reduction
	•	adaptive thresholding
↓
MCQ Detection (Contours + Pixel Density)
↓
Handwritten Name OCR (ROI-based, Tesseract)
↓
Grading Engine
↓
Analytics Layer
	•	student scores
	•	baseline vs endline comparison
↓
CSV / Excel Outputs

---

## ✨ Key Features

- Offline-first OCR pipeline
- Deterministic MCQ bubble detection (no ML required)
- ROI-based handwritten name extraction
- Confidence scoring per detected answer
- Sponsor-ready analytics and exports

---

## 📁 Project Structure
ImpactOCR/
├── app/              # Pipeline orchestration
├── ocr/              # Preprocessing, MCQ detection, OCR
├── analytics/        # Aggregation and impact metrics
├── data/             # Sample inputs/outputs
├── README.md
├── requirements.txt

---

## 📊 Outputs

- Student-level scores (CSV / Excel)
- Question-level correctness
- Baseline vs endline improvement metrics

---

## 🔮 Future Improvements

- Support for multiple answer sheet templates
- PaddleOCR integration for noisier handwriting
- Dashboard-based visual analytics
- Batch processing for large-scale deployments

---

## 👤 Author

Built by **Gaurav Nair** as a portfolio project demonstrating applied computer vision, OCR systems, and impact-focused analytics.

# ImpactOCR  
**Offline OCR-Based Assessment & Impact Analysis Platform**

🔗 **Live Demo:** https://impactocr.streamlit.app/

ImpactOCR is an **offline-first OCR grading system** that digitizes and grades paper-based MCQ assessments, enabling **baseline vs endline impact analysis** in low-connectivity environments.

Designed for **NGOs, schools, and education programs** where internet access is unreliable, ImpactOCR converts scanned answer sheets into **structured, sponsor-ready analytics**—without requiring cloud connectivity or ML-heavy infrastructure.

---

## 🎯 Problem

Many education programs operate in regions with **limited or no internet access**, forcing assessments to remain paper-based.

This creates three major challenges:
- Manual grading is **slow and error-prone**
- Student performance data is **hard to aggregate**
- Demonstrating **measurable learning impact** to sponsors is difficult

---

## 💡 Solution

ImpactOCR automates the entire assessment pipeline:

- MCQ bubble detection and grading  
- Handwritten student name extraction  
- Student-level scoring  
- Baseline vs endline improvement analysis  

All while remaining **fully offline**.

---

## 🧠 System Architecture
Scanned Answer Sheets
↓
Image Preprocessing (OpenCV)
• Grayscale conversion
• Noise reduction
• Adaptive thresholding
↓
MCQ Detection
• Contour detection
• Pixel density analysis
↓
Handwritten Name OCR
• ROI-based extraction
• Tesseract OCR
↓
Grading Engine
↓
Analytics Layer
• Student-level scores
• Baseline vs endline comparison
↓
CSV / Excel Outputs

---

## ✨ Key Features

- **Offline-first OCR pipeline** (no internet dependency)
- **Deterministic MCQ detection** using classical computer vision (no ML required)
- **ROI-based handwritten name extraction**
- **Confidence scoring** per detected answer
- **Sponsor-ready analytics and exports** (CSV / Excel)

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Computer Vision:** OpenCV  
- **OCR:** Tesseract  
- **Data Processing:** Pandas  
- **UI:** Streamlit  

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

- Student-level score reports  
- Question-level correctness tables  
- Baseline vs endline improvement metrics  
- Exportable CSV / Excel files for sponsor reporting

---

## 🔮 Future Improvements

- Support for multiple answer sheet templates  
- PaddleOCR integration for noisier handwriting  
- Interactive dashboard-based visual analytics  
- Batch processing for large-scale deployments  

---

## 📌 Use Cases

- NGO education impact studies  
- Baseline vs endline assessments  
- Low-connectivity or offline school environments  
- Sponsor and donor impact reporting  

---

## 🧠 Why ImpactOCR?

ImpactOCR focuses on **reliability, explainability, and real-world constraints**:
- No dependency on cloud APIs
- Deterministic, auditable grading logic
- Designed for constrained environments where automation matters most

---
## 🧠 How Computer Vision, OCR, and AI/ML Are Used

ImpactOCR combines **classical computer vision**, **OCR**, and **lightweight AI-inspired decision logic** to deliver a reliable, fully offline grading system. Rather than relying on large ML models or cloud APIs, the system prioritizes **determinism, explainability, and robustness** in constrained environments.

---

### 📸 Computer Vision (OpenCV)

Computer vision is the backbone of the grading pipeline and is used extensively for **image normalization and MCQ detection**.

#### Image Preprocessing
Scanned answer sheets often suffer from uneven lighting, shadows, and camera noise. ImpactOCR applies a series of preprocessing steps to standardize inputs:

- Grayscale conversion to remove color variance  
- Gaussian blurring for noise reduction  
- Adaptive thresholding to handle variable lighting conditions  

These steps ensure that downstream detection remains stable across different scanners and mobile cameras.

#### MCQ Bubble Detection
Rather than using a trained ML classifier, ImpactOCR uses **deterministic computer vision techniques** for explainability and offline reliability:

- Contour detection to locate potential answer bubbles  
- Area and shape filtering to eliminate false positives  
- Pixel density analysis within each bubble to determine whether it is filled  

This approach:
- Requires **no training data**
- Produces **auditable grading logic**
- Works consistently across deployments

Each detected answer is also assigned a **confidence score** based on fill density and contour stability.

---

### ✍️ OCR with Tesseract (Handwritten Name Extraction)

Optical Character Recognition is used specifically for **handwritten student name extraction**, which presents a very different challenge from MCQ detection.

#### ROI-Based OCR Strategy
Instead of applying OCR to the entire page, ImpactOCR:
- Identifies a fixed **Region of Interest (ROI)** where names are expected  
- Crops and preprocesses only that region  
- Applies binarization and contrast normalization  

This targeted approach significantly improves OCR accuracy on noisy handwriting.

#### Tesseract OCR
Tesseract is used for:
- Converting handwritten or semi-structured text into machine-readable strings  
- Handling variations in pen pressure, stroke width, and writing style  

While handwriting OCR is inherently noisy, the ROI-based strategy and preprocessing steps improve robustness without introducing heavy ML dependencies.

---

### 🤖 AI / ML-Inspired Logic (Without Heavy Models)

Although ImpactOCR does not rely on large neural networks, it incorporates **AI/ML-inspired decision logic** throughout the pipeline:

- Heuristic scoring functions mimic classification confidence  
- Rule-based validation replaces opaque ML predictions  
- Deterministic grading logic ensures reproducibility  

This design choice reflects real-world NGO constraints:
- No GPU availability
- Limited or no internet access
- Need for explainable results for audits and sponsors

The result is a system that behaves like an AI pipeline, but with **lower operational risk and higher transparency**.

---

### 📊 Analytics & Impact Measurement

After grading, results are passed into an analytics layer that:
- Aggregates student-level scores  
- Computes question-level correctness distributions  
- Compares baseline vs endline performance  

These outputs enable **quantitative impact analysis**, allowing organizations to demonstrate learning gains using real data rather than anecdotal evidence.

---

### 🧩 Why This Approach Works

| Challenge | Design Choice |
|---------|--------------|
Offline environments | No cloud APIs, no heavy ML |
Limited data | Deterministic CV over trained models |
Sponsor accountability | Explainable grading logic |
Scalability | Lightweight batch processing |

ImpactOCR shows how **computer vision + OCR + pragmatic AI design** can outperform over-engineered ML systems in real-world, constrained settings.

## 👤 Author

Built by **Gaurav Nair** as a portfolio project demonstrating applied computer vision, OCR systems, and impact-focused analytics.

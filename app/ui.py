# app/ui.py

import sys
from pathlib import Path

# Ensure repo root is on PYTHONPATH (Streamlit Cloud fix)
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import pandas as pd
import tempfile
import os

from app.pipeline import run_assessment_pipeline
from analytics.metrics import aggregate_results, compute_summary_metrics
from config.templates import TEMPLATES


# --------------------------------------------------
# Page setup
# --------------------------------------------------
st.set_page_config(page_title="ImpactOCR", layout="centered")

st.title("📄 ImpactOCR")
st.subheader("Offline OCR-based MCQ Assessment Platform")

st.markdown(
    "Upload scanned answer sheets and an answer key to automatically grade "
    "paper-based MCQ tests."
)

# --------------------------------------------------
# 1. Select Answer Sheet Template
# --------------------------------------------------
st.header("1️⃣ Select Answer Sheet Format")

template_name = st.selectbox(
    "Answer sheet template",
    options=list(TEMPLATES.keys())
)

template = TEMPLATES[template_name]
name_roi = template["name_roi"]
choices_per_question = template.get("choices_per_question", 4)

st.info(
    f"Using template **{template_name}**.\n\n"
    "Handwritten name region and MCQ layout are automatically applied."
)

# --------------------------------------------------
# 2. Upload Answer Key
# --------------------------------------------------
st.header("2️⃣ Upload Answer Key")

answer_key_file = st.file_uploader(
    "Answer key (CSV with one column)",
    type=["csv"]
)

answer_key = None
if answer_key_file:
    answer_key = pd.read_csv(answer_key_file).iloc[:, 0].tolist()
    st.success(f"Loaded answer key with {len(answer_key)} questions.")

# --------------------------------------------------
# 3. Upload Answer Sheets
# --------------------------------------------------
st.header("3️⃣ Upload Answer Sheets")

uploaded_files = st.file_uploader(
    "Scanned answer sheet images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# --------------------------------------------------
# 4. Run Processing
# --------------------------------------------------
st.header("4️⃣ Run Assessment")

if st.button("🚀 Process Assessments"):

    if not answer_key:
        st.error("Please upload an answer key.")
        st.stop()

    if not uploaded_files:
        st.error("Please upload at least one answer sheet.")
        st.stop()

    results = []

    with st.spinner("Processing answer sheets..."):
        for uploaded in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(uploaded.read())
                tmp_path = tmp.name

            output = run_assessment_pipeline(
                image_path=tmp_path,
                answer_key=answer_key,
                name_roi=name_roi,
                choices_per_question=choices_per_question
            )

            results.append(output)
            os.unlink(tmp_path)

    # --------------------------------------------------
    # 5. Display Results
    # --------------------------------------------------
    df = aggregate_results(results)
    summary = compute_summary_metrics(df)

    st.success("Processing complete!")

    st.header("📊 Summary Metrics")
    st.json(summary)

    st.header("📋 Student Results")
    st.dataframe(df)

    st.download_button(
        label="⬇️ Download Results (CSV)",
        data=df.to_csv(index=False),
        file_name="assessment_results.csv",
        mime="text/csv"
    )

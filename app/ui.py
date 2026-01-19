# app/ui.py

import streamlit as st
import pandas as pd
import tempfile
import os

from .pipeline import run_assessment_pipeline
from analytics.metrics import aggregate_results, compute_summary_metrics

st.set_page_config(page_title="ImpactOCR", layout="centered")

st.title("📄 ImpactOCR")
st.subheader("Offline OCR-based MCQ Assessment Platform")

st.markdown(
    "Upload scanned answer sheets and an answer key to automatically grade paper-based MCQ tests."
)

# Upload answer key
st.header("1️⃣ Upload Answer Key")
answer_key_file = st.file_uploader("Answer key (CSV with one column)", type=["csv"])

answer_key = None
if answer_key_file:
    answer_key = pd.read_csv(answer_key_file).iloc[:, 0].tolist()
    st.success(f"Loaded answer key with {len(answer_key)} questions.")

# Upload answer sheets
st.header("2️⃣ Upload Answer Sheets")
uploaded_files = st.file_uploader(
    "Scanned answer sheet images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# ROI inputs
st.header("3️⃣ Handwritten Name Region (ROI)")
x = st.number_input("x", value=100)
y = st.number_input("y", value=50)
w = st.number_input("width", value=600)
h = st.number_input("height", value=120)

name_roi = (x, y, w, h)

# Run processing
if st.button("🚀 Process Assessments"):

    if not answer_key or not uploaded_files:
        st.error("Please upload both answer key and answer sheets.")
    else:
        results = []

        with st.spinner("Processing answer sheets..."):
            for uploaded in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    tmp.write(uploaded.read())
                    tmp_path = tmp.name

                output = run_assessment_pipeline(
                    image_path=tmp_path,
                    answer_key=answer_key,
                    name_roi=name_roi
                )

                results.append(output)
                os.unlink(tmp_path)

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

# app/ui.py

import sys
from pathlib import Path

# Add project root to PYTHONPATH (keep this for your setup)
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd
import tempfile
import os
import cv2
import numpy as np

from streamlit_drawable_canvas import st_canvas

from app.pipeline import run_assessment_pipeline
from analytics.metrics import aggregate_results, compute_summary_metrics


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
# 1. Upload Answer Key
# --------------------------------------------------
st.header("1️⃣ Upload Answer Key")

answer_key_file = st.file_uploader(
    "Answer key (CSV with one column)",
    type=["csv"]
)

answer_key = None
if answer_key_file:
    answer_key = pd.read_csv(answer_key_file).iloc[:, 0].tolist()
    st.success(f"Loaded answer key with {len(answer_key)} questions.")

# --------------------------------------------------
# 2. Upload Answer Sheets
# --------------------------------------------------
st.header("2️⃣ Upload Answer Sheets")

uploaded_files = st.file_uploader(
    "Scanned answer sheet images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# --------------------------------------------------
# 3. Select Handwritten Name ROI (visual)
# --------------------------------------------------
st.header("3️⃣ Select Handwritten Name Region")

name_roi = None

if uploaded_files:
    st.info(
        "Draw a rectangle over the **handwritten student name** on the image below. "
        "This only needs to be done once per answer sheet template."
    )

    # Load first uploaded image for ROI selection
    file_bytes = np.asarray(
        bytearray(uploaded_files[0].read()),
        dtype=np.uint8
    )
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    canvas = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=2,
        stroke_color="#FF0000",
        background_image=image_rgb,
        update_streamlit=True,
        height=image_rgb.shape[0],
        width=image_rgb.shape[1],
        drawing_mode="rect",
        key="roi_canvas",
    )

    if canvas.json_data and len(canvas.json_data["objects"]) > 0:
        rect = canvas.json_data["objects"][0]
        x = int(rect["left"])
        y = int(rect["top"])
        w = int(rect["width"])
        h = int(rect["height"])
        name_roi = (x, y, w, h)

        st.success(f"ROI selected: {name_roi}")

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

    if name_roi is None:
        st.error("Please draw a region around the handwritten name.")
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
                name_roi=name_roi
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

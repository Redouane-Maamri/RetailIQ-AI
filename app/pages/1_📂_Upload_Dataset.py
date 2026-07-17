import os
import tempfile

import pandas as pd
import streamlit as st
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
    
from etl.pipeline import run_pipeline
from etl.validate import generate_validation_report


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Upload Dataset",
    page_icon="📂",
    layout="wide"
)

# --------------------------------------------------
# Page Title
# --------------------------------------------------

st.title("📂 Upload Retail Dataset")
st.write("Upload your retail CSV dataset to start the ETL pipeline.")

# --------------------------------------------------
# File Upload
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

# --------------------------------------------------
# Process Uploaded File
# --------------------------------------------------

if uploaded_file is not None:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.success("✅ Dataset uploaded successfully!")

    st.write(f"**Dataset:** `{uploaded_file.name}`")

    # --------------------------------------------------
    # Dataset Preview
    # --------------------------------------------------

    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)

    # --------------------------------------------------
    # Dataset Information
    # --------------------------------------------------

    rows = df.shape[0]
    columns = df.shape[1]
    missing_values = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()
    memory_usage = df.memory_usage(deep=True).sum() / (1024 * 1024)

    st.subheader("📋 Dataset Information")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Rows", f"{rows:,}")

    with c2:
        st.metric("Columns", columns)

    with c3:
        st.metric("Missing Values", missing_values)

    c4, c5 = st.columns(2)

    with c4:
        st.metric("Duplicate Rows", duplicate_rows)

    with c5:
        st.metric("Memory Usage", f"{memory_usage:.2f} MB")

    # --------------------------------------------------
    # Dataset Validation
    # --------------------------------------------------

    st.subheader("✅ Dataset Validation")

    report = generate_validation_report(df)

    if report["status"] == "VALID":
        st.success("🟢 Dataset validation passed successfully!")
    else:
        st.error("🔴 Dataset validation failed!")

    # --------------------------------------------------
    # Validation Details
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.write(
            f"**Required Columns:** {'✅ PASS' if report['required_columns'] else '❌ FAIL'}"
        )
        st.write(f"**Duplicate Rows:** {report['duplicate_rows']}")

    with col2:
        st.write(
            f"**Dataset Empty:** {'❌ Yes' if report['empty_dataset'] else '✅ No'}"
        )
        st.write(f"**Status:** {report['status']}")

    # Missing Columns

    if report["missing_columns"]:
        st.warning("### Missing Columns")

        for column in report["missing_columns"]:
            st.write(f"- {column}")

    # Missing Values

    if report["missing_values"]:
        st.warning("### Missing Values")

        missing_df = pd.DataFrame(
            report["missing_values"].items(),
            columns=["Column", "Missing Values"]
        )

        st.dataframe(missing_df, use_container_width=True)

    # --------------------------------------------------
    # Run ETL Pipeline
    # --------------------------------------------------

    st.divider()

    st.subheader("⚙️ Run ETL Pipeline")

    st.write(
        "Execute the complete ETL pipeline to load the dataset into PostgreSQL."
    )

    # Only allow ETL if validation passed
    if report["status"] == "VALID":

        if st.button("🚀 Run ETL Pipeline", use_container_width=True):

            try:

                # Save uploaded file temporarily

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".csv"
                ) as tmp_file:

                    tmp_file.write(uploaded_file.getbuffer())
                    temp_file_path = tmp_file.name

                # Execute ETL

                with st.spinner("Running ETL Pipeline..."):

                    result = run_pipeline(temp_file_path)

                # Display result

                if result["status"] == "SUCCESS":
                    st.success(result["message"])
                    st.balloons()
                else:
                    st.error(result["message"])

            except Exception as e:
                st.error(f"ETL Pipeline Error: {e}")

            finally:

                if "temp_file_path" in locals() and os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

    else:
        st.warning(
            "⚠️ Fix the validation errors before running the ETL pipeline."
        )

# --------------------------------------------------
# No File Uploaded
# --------------------------------------------------

else:

    st.info("👆 Please upload a CSV dataset to continue.")
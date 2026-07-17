import os
import sys
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from etl.pipeline import run_pipeline
from etl.validate import generate_validation_report


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Upload Dataset",
    page_icon="📂",
    layout="wide"
)

# ==========================================================
# Title
# ==========================================================

st.title("📂 Upload Retail Dataset")

st.write(
    "Upload a retail CSV dataset to validate, clean and load it into PostgreSQL."
)

# ==========================================================
# Upload CSV
# ==========================================================

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

# ==========================================================
# No File Uploaded
# ==========================================================

if uploaded_file is None:

    st.info("👆 Please upload a CSV dataset.")

    st.stop()

# ==========================================================
# Read Dataset
# ==========================================================

df = pd.read_csv(uploaded_file)

st.success("Dataset uploaded successfully.")

st.write(f"**Dataset:** `{uploaded_file.name}`")

# ==========================================================
# Dataset Preview
# ==========================================================

st.subheader("📄 Dataset Preview")

st.dataframe(
    df.head(10),
    use_container_width=True
)

# ==========================================================
# Dataset Information
# ==========================================================

rows = len(df)

columns = len(df.columns)

missing_values = int(df.isnull().sum().sum())

duplicate_rows = int(df.duplicated().sum())

memory_usage = (
    df.memory_usage(deep=True).sum()
    / (1024 * 1024)
)

st.subheader("📊 Dataset Information")

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
    st.metric(
        "Memory Usage",
        f"{memory_usage:.2f} MB"
    )

# ==========================================================
# Validation
# ==========================================================

st.divider()

st.subheader("✅ Dataset Validation")

report = generate_validation_report(df)

# ==========================================================
# Validation Status
# ==========================================================

if report["status"] == "VALID":

    st.success("🟢 Dataset validation passed successfully.")

elif report["status"] == "VALID_WITH_WARNINGS":

    st.warning(
        "🟡 Dataset contains recoverable issues.\n\n"
        "The ETL pipeline will clean the dataset automatically."
    )

else:

    st.error(
        "🔴 Dataset validation failed.\n\n"
        "Please fix the critical errors before running the ETL pipeline."
    )

# ==========================================================
# Validation Summary
# ==========================================================

left, right = st.columns(2)

with left:

    st.write(
        f"**Required Columns:** {'✅ PASS' if report['required_columns'] else '❌ FAIL'}"
    )

    st.write(
        f"**Duplicate Rows:** {report['duplicate_rows']}"
    )

with right:

    st.write(
        f"**Dataset Empty:** {'❌ Yes' if report['empty_dataset'] else '✅ No'}"
    )

    st.write(
        f"**Status:** {report['status']}"
    )

# ==========================================================
# Missing Required Columns
# ==========================================================

if report["missing_columns"]:

    st.error("### ❌ Missing Required Columns")

    missing_columns_df = pd.DataFrame(
        report["missing_columns"],
        columns=["Missing Column"]
    )

    st.dataframe(
        missing_columns_df,
        use_container_width=True
    )

# ==========================================================
# Critical Missing Values
# ==========================================================

if report["critical_missing_values"]:

    st.error("### ❌ Critical Missing Values")

    critical_df = pd.DataFrame(
        report["critical_missing_values"].items(),
        columns=[
            "Column",
            "Missing Values"
        ]
    )

    st.dataframe(
        critical_df,
        use_container_width=True
    )

# ==========================================================
# Non Critical Missing Values
# ==========================================================

if report["non_critical_missing_values"]:

    st.warning("### ⚠️ Non-Critical Missing Values")

    warning_df = pd.DataFrame(
        report["non_critical_missing_values"].items(),
        columns=[
            "Column",
            "Missing Values"
        ]
    )

    st.dataframe(
        warning_df,
        use_container_width=True
    )

    st.info(
        "These values will be filled automatically during the Transformation phase."
    )

# ==========================================================
# Duplicate Rows
# ==========================================================

if report["duplicate_rows"] > 0:

    st.warning("### ⚠️ Duplicate Rows")

    st.write(
        f"**Duplicate Rows Found:** {report['duplicate_rows']}"
    )

    st.code(
        report["duplicate_indexes"]
    )

    st.info(
        "Duplicate rows will be removed automatically during the Transformation phase."
    )

# ==========================================================
# Run ETL Pipeline
# ==========================================================

st.divider()

st.subheader("⚙️ Run ETL Pipeline")

st.write(
    """
Execute the complete ETL pipeline.

The pipeline will:

- Validate the dataset
- Clean duplicate rows
- Fill non-critical missing values
- Transform the dataset
- Load data into PostgreSQL
"""
)

# ==========================================================
# Enable Button
# ==========================================================

can_run_etl = report["status"] in [
    "VALID",
    "VALID_WITH_WARNINGS"
]

if can_run_etl:

    if st.button(
        "🚀 Run ETL Pipeline",
        use_container_width=True
    ):

        try:

            # --------------------------------------------------
            # Save uploaded dataset temporarily
            # --------------------------------------------------

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".csv"
            ) as tmp_file:

                tmp_file.write(
                    uploaded_file.getbuffer()
                )

                temp_file_path = tmp_file.name

            # --------------------------------------------------
            # Execute ETL
            # --------------------------------------------------

            with st.spinner(
                "Running RetailIQ AI ETL Pipeline..."
            ):

                result = run_pipeline(
                    temp_file_path
                )

            # --------------------------------------------------
            # Success
            # --------------------------------------------------

            if result["status"] == "SUCCESS":

                st.success(result["message"])

                st.divider()

                st.subheader("🧹 Cleaning Summary")

                transformation_report = result[
                    "transformation_report"
                ]

                duplicate_report = transformation_report[
                    "duplicate_report"
                ]

                filling_report = transformation_report[
                    "filling_report"
                ]

                # ------------------------------
                # Duplicate Report
                # ------------------------------

                st.success(
                    f"Duplicate Rows Removed: {duplicate_report['duplicates_removed']}"
                )

                if duplicate_report[
                    "duplicate_indexes"
                ]:

                    st.write(
                        "Duplicate Row Indexes"
                    )

                    st.code(
                        duplicate_report[
                            "duplicate_indexes"
                        ]
                    )

                # ------------------------------
                # Filled Missing Values
                # ------------------------------

                if filling_report:

                    st.write(
                        "Filled Missing Values"
                    )

                    filling_df = pd.DataFrame([
                        {
                            "Column": column,
                            "Filled Values": info["filled"],
                            "Default Value": info["default_value"]
                        }

                        for column, info
                        in filling_report.items()

                    ])

                    st.dataframe(
                        filling_df,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No missing values required automatic filling."
                    )

                st.divider()

                st.success(
                    "🎉 Dataset successfully loaded into PostgreSQL."
                )

                st.balloons()

            # --------------------------------------------------
            # Failed
            # --------------------------------------------------

            else:

                st.error(result["message"])

        except Exception as e:

            st.error(
                f"ETL Pipeline Error:\n\n{e}"
            )

        finally:

            if (
                "temp_file_path" in locals()
                and os.path.exists(temp_file_path)
            ):

                os.remove(temp_file_path)

# ==========================================================
# Invalid Dataset
# ==========================================================

else:

    st.error(
        """
❌ The dataset contains critical validation errors.

Please fix:

- Missing required columns
- Critical missing values

before running the ETL pipeline.
"""
    )
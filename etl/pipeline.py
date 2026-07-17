from etl.extract import extract_data
from etl.validate import generate_validation_report
from etl.transform import transform_data
from etl.load import load_data


# ==========================================================
# RetailIQ AI - ETL Pipeline
# ==========================================================

def run_pipeline(file_path):
    """
    Execute the complete ETL pipeline.
    """

    print("=" * 70)
    print("               RetailIQ AI - ETL Pipeline")
    print("=" * 70)

    # ======================================================
    # 1. Extract
    # ======================================================

    print("\n[1/4] Extracting dataset...")

    df = extract_data(file_path)

    print("✅ Dataset extracted successfully.")

    # ======================================================
    # 2. Validate
    # ======================================================

    print("\n[2/4] Validating dataset...")

    validation_report = generate_validation_report(df)

    if validation_report["status"] == "INVALID":

        print("\n❌ Dataset validation failed.")

        return {
            "status": "FAILED",
            "message": "Dataset validation failed.",
            "validation_report": validation_report,
        }

    elif validation_report["status"] == "VALID_WITH_WARNINGS":

        print("\n⚠️ Validation completed with warnings.")
        print("The dataset will be cleaned during the transformation phase.")

    else:

        print("\n✅ Dataset validation passed.")

    # ======================================================
    # 3. Transform
    # ======================================================

    print("\n[3/4] Transforming dataset...")

    df, transformation_report = transform_data(df)

    print("✅ Transformation completed.")

    # ======================================================
    # 4. Load
    # ======================================================

    print("\n[4/4] Loading data into PostgreSQL...")

    try:

        load_data(df)

    except Exception as e:

        print("\n❌ Error while loading data.")

        print(type(e).__name__)

        print(e)

        return {
            "status": "FAILED",
            "message": str(e),
            "validation_report": validation_report,
            "transformation_report": transformation_report,
        }

    print("\n" + "=" * 70)
    print("🎉 ETL PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)

    return {

        "status": "SUCCESS",

        "message": "ETL pipeline completed successfully.",

        "validation_report": validation_report,

        "transformation_report": transformation_report,
    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    result = run_pipeline("data/raw/SuperStoreOrders.csv")

    print("\nFinal Result:\n")

    print(result)
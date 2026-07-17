from etl.extract import extract_data
from etl.validate import generate_validation_report
from etl.transform import transform_data
from etl.load import load_data


def run_pipeline(file_path):
    """
    Execute the complete ETL pipeline.
    """

    print("=" * 70)
    print("               RetailIQ AI - ETL Pipeline")
    print("=" * 70)

    # -------------------------
    # 1. Extract
    # -------------------------
    print("\n[1/4] Extracting dataset...")

    df = extract_data(file_path)

    # -------------------------
    # 2. Validate
    # -------------------------
    print("\n[2/4] Validating dataset...")

    report = generate_validation_report(df)
    print("=" * 60)
    print(report)
    print("=" * 60)

    if report["status"] != "VALID":
        print("\n❌ Dataset validation failed.")
        print(report)

        return {
            "status": "FAILED",
            "message": "Dataset validation failed.",
            "report": report
        }

    print("✅ Dataset validation passed.")

    # -------------------------
    # 3. Transform
    # -------------------------
    print("\n[3/4] Transforming dataset...")

    df = transform_data(df)

    print("✅ Transformation completed.")

    # -------------------------
    # 4. Load
    # -------------------------
    print("\n[4/4] Loading data into PostgreSQL...")

    try:
        load_data(df)
    except Exception as e:
        print("ERROR DURING LOAD:")
        print(type(e).__name__)
        print(e)
        
        
        return {
        "status": "FAILED",
        "message": str(e)
    }

    print("\n" + "=" * 70)
    print("🎉 ETL PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)

    return {
        "status": "SUCCESS",
        "message": "ETL pipeline completed successfully."
    }


if __name__ == "__main__":
    run_pipeline("data/raw/SuperStoreOrders.csv")
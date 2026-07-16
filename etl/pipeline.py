from etl.extract import extract_data
from etl.validate import generate_validation_report
from etl.transform import transform_data
from etl.load import load_data


def run_pipeline():
    """
    Execute the complete ETL pipeline.
    """

    print("=" * 70)
    print("               RetailIQ AI - ETL Pipeline")
    print("=" * 70)

    # -------------------------
    # Extract
    # -------------------------
    print("\n[1/4] Extracting dataset...")

    df = extract_data("data/raw/SuperStoreOrders.csv")

    # -------------------------
    # Validate
    # -------------------------
    print("\n[2/4] Validating dataset...")

    report = generate_validation_report(df)

    if report["status"] != "VALID":
        print("\n❌ Dataset validation failed.")
        return

    print("✅ Dataset validation passed.")

    # -------------------------
    # Transform
    # -------------------------
    print("\n[3/4] Transforming dataset...")

    df = transform_data(df)

    print("✅ Transformation completed.")

    # -------------------------
    # Load
    # -------------------------
    print("\n[4/4] Loading data into PostgreSQL...")

    load_data(df)

    print("\n" + "=" * 70)
    print("🎉 ETL PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()
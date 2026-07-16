import pandas as pd

# ==========================================================
# Required Dataset Columns
# ==========================================================

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "ship_date",
    "ship_mode",
    "customer_name",
    "segment",
    "state",
    "country",
    "market",
    "region",
    "product_id",
    "category",
    "sub_category",
    "product_name",
    "sales",
    "quantity",
    "discount",
    "profit",
    "shipping_cost",
    "order_priority",
    "year",
]


# ==========================================================
# Validation Functions
# ==========================================================

def check_required_columns(df: pd.DataFrame) -> list:
    """
    Check if all required columns exist.
    Returns a list of missing columns.
    """

    return [col for col in REQUIRED_COLUMNS if col not in df.columns]


def check_missing_values(df: pd.DataFrame) -> dict:
    """
    Returns only columns containing missing values.
    """

    missing = df.isnull().sum()

    return missing[missing > 0].to_dict()


def check_duplicate_rows(df: pd.DataFrame) -> int:
    """
    Count duplicate rows.
    """

    return int(df.duplicated().sum())


def check_empty_dataset(df: pd.DataFrame) -> bool:
    """
    Check whether the dataset is empty.
    """

    return df.empty


def generate_validation_report(df: pd.DataFrame) -> dict:
    """
    Generate a complete validation report.
    """

    missing_columns = check_required_columns(df)
    missing_values = check_missing_values(df)
    duplicate_rows = check_duplicate_rows(df)
    empty_dataset = check_empty_dataset(df)

    status = (
        len(missing_columns) == 0
        and len(missing_values) == 0
        and duplicate_rows == 0
        and not empty_dataset
    )

    report = {
        "rows": len(df),
        "columns": len(df.columns),
        "required_columns": len(missing_columns) == 0,
        "missing_columns": missing_columns,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "empty_dataset": empty_dataset,
        "status": "VALID" if status else "INVALID",
    }

    return report


# ==========================================================
# Display Validation Report
# ==========================================================

def print_validation_report(report: dict):
    """
    Print a professional validation report.
    """

    print("=" * 65)
    print("               RetailIQ AI - Validation Report")
    print("=" * 65)

    print(f"Rows                 : {report['rows']}")
    print(f"Columns              : {report['columns']}")

    print(
        f"Required Columns     : {'✅ PASS' if report['required_columns'] else '❌ FAIL'}"
    )

    print(
        f"Duplicate Rows       : {report['duplicate_rows']}"
    )

    print(
        f"Dataset Empty        : {'Yes' if report['empty_dataset'] else 'No'}"
    )

    if report["missing_columns"]:
        print("\nMissing Columns:")
        for column in report["missing_columns"]:
            print(f"   - {column}")

    if report["missing_values"]:
        print("\nMissing Values:")
        for column, count in report["missing_values"].items():
            print(f"   - {column}: {count}")

    print("\nStatus               :", end=" ")

    if report["status"] == "VALID":
        print("✅ VALID")
    else:
        print("❌ INVALID")

    print("=" * 65)


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    from extract import extract_data

    df = extract_data("data/raw/SuperStoreOrders.csv")

    report = generate_validation_report(df)

    print_validation_report(report)
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
# Critical Columns
# Missing values in these columns STOP the ETL pipeline.
# ==========================================================

CRITICAL_COLUMNS = [
    "order_id",
    "customer_name",
    "product_id",
    "sales",
    "quantity",
]

# ==========================================================
# Non-Critical Columns
# Missing values will be automatically handled
# during the Transform phase.
# ==========================================================

NON_CRITICAL_COLUMNS = [
    "ship_mode",
    "discount",
    "profit",
    "shipping_cost",
    "order_priority",
]

# ==========================================================
# Validation Functions
# ==========================================================

def check_required_columns(df: pd.DataFrame) -> list:
    """
    Check whether all required columns exist.
    """

    return [col for col in REQUIRED_COLUMNS if col not in df.columns]


def check_critical_missing_values(df: pd.DataFrame) -> dict:
    """
    Return missing values only for critical columns.
    """

    missing = {}

    for column in CRITICAL_COLUMNS:

        if column in df.columns:

            count = int(df[column].isnull().sum())

            if count > 0:
                missing[column] = count

    return missing


def check_non_critical_missing_values(df: pd.DataFrame) -> dict:
    """
    Return missing values only for non-critical columns.
    """

    missing = {}

    for column in NON_CRITICAL_COLUMNS:

        if column in df.columns:

            count = int(df[column].isnull().sum())

            if count > 0:
                missing[column] = count

    return missing


def check_duplicate_rows(df: pd.DataFrame) -> dict:
    """
    Count duplicate rows and return their indexes.
    """

    duplicate_indexes = df[df.duplicated()].index.tolist()

    return {
        "count": len(duplicate_indexes),
        "indexes": duplicate_indexes,
    }


def check_empty_dataset(df: pd.DataFrame) -> bool:
    """
    Check whether the dataset is empty.
    """

    return df.empty


# ==========================================================
# Validation Report
# ==========================================================

def generate_validation_report(df: pd.DataFrame) -> dict:
    """
    Generate a complete validation report.
    """

    missing_columns = check_required_columns(df)

    critical_missing_values = check_critical_missing_values(df)

    non_critical_missing_values = check_non_critical_missing_values(df)

    duplicate_report = check_duplicate_rows(df)

    empty_dataset = check_empty_dataset(df)

    # ------------------------------------------------------
    # Fatal Errors
    # ------------------------------------------------------

    has_fatal_errors = (
        len(missing_columns) > 0
        or len(critical_missing_values) > 0
        or empty_dataset
    )

    # ------------------------------------------------------
    # Warnings
    # ------------------------------------------------------

    has_warnings = (
        duplicate_report["count"] > 0
        or len(non_critical_missing_values) > 0
    )

    # ------------------------------------------------------
    # Validation Status
    # ------------------------------------------------------

    if has_fatal_errors:

        status = "INVALID"

    elif has_warnings:

        status = "VALID_WITH_WARNINGS"

    else:

        status = "VALID"

    # ------------------------------------------------------
    # Report
    # ------------------------------------------------------

    report = {

        "rows": len(df),

        "columns": len(df.columns),

        "required_columns": len(missing_columns) == 0,

        "missing_columns": missing_columns,

        "critical_missing_values": critical_missing_values,

        "non_critical_missing_values": non_critical_missing_values,

        "duplicate_rows": duplicate_report["count"],

        "duplicate_indexes": duplicate_report["indexes"],

        "empty_dataset": empty_dataset,

        "status": status,
    }

    return report


# ==========================================================
# Display Validation Report
# ==========================================================

def print_validation_report(report: dict):
    """
    Print a professional validation report.
    """

    print("=" * 70)
    print("              RetailIQ AI - Validation Report")
    print("=" * 70)

    print(f"Rows                 : {report['rows']}")
    print(f"Columns              : {report['columns']}")

    print(
        f"Required Columns     : {'✅ PASS' if report['required_columns'] else '❌ FAIL'}"
    )

    print(f"Duplicate Rows       : {report['duplicate_rows']}")

    print(
        f"Dataset Empty        : {'Yes' if report['empty_dataset'] else 'No'}"
    )

    # ------------------------------------------------------
    # Missing Required Columns
    # ------------------------------------------------------

    if report["missing_columns"]:

        print("\n❌ Missing Required Columns:")

        for column in report["missing_columns"]:

            print(f"   - {column}")

    # ------------------------------------------------------
    # Critical Missing Values
    # ------------------------------------------------------

    if report["critical_missing_values"]:

        print("\n❌ Critical Missing Values:")

        for column, count in report["critical_missing_values"].items():

            print(f"   - {column}: {count}")

    # ------------------------------------------------------
    # Non-Critical Missing Values
    # ------------------------------------------------------

    if report["non_critical_missing_values"]:

        print("\n⚠️ Non-Critical Missing Values:")

        for column, count in report["non_critical_missing_values"].items():

            print(f"   - {column}: {count}")

        print("   These values will be filled automatically during transformation.")

    # ------------------------------------------------------
    # Duplicate Rows
    # ------------------------------------------------------

    if report["duplicate_rows"] > 0:

        print("\n⚠️ Duplicate Rows Found:")

        print(f"   Total : {report['duplicate_rows']}")

        print(f"   Indexes : {report['duplicate_indexes']}")

        print("   These duplicate rows will be removed automatically during transformation.")

    # ------------------------------------------------------
    # Final Status
    # ------------------------------------------------------

    print("\nStatus               :", end=" ")

    if report["status"] == "VALID":

        print("✅ VALID")

    elif report["status"] == "VALID_WITH_WARNINGS":

        print("⚠️ VALID WITH WARNINGS")

    else:

        print("❌ INVALID")

    print("=" * 70)


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    from etl.extract import extract_data

    df = extract_data("data/raw/SuperStoreOrders.csv")

    report = generate_validation_report(df)

    print_validation_report(report)
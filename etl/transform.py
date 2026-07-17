import pandas as pd


# ==========================================================
# Standardize Column Names
# ==========================================================

def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert column names to lowercase and replace spaces with underscores.
    """

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


# ==========================================================
# Convert Date Columns
# ==========================================================

def convert_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert date columns to datetime format.
    """

    date_columns = [
        "order_date",
        "ship_date"
    ]

    for column in date_columns:

        if column in df.columns:

            df[column] = pd.to_datetime(
                df[column],
                dayfirst=True,
                errors="coerce"
            )

    return df


# ==========================================================
# Convert Numeric Columns
# ==========================================================

def convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert numeric columns to numeric types.
    """

    numeric_columns = [
        "sales",
        "quantity",
        "discount",
        "profit",
        "shipping_cost",
        "year"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


# ==========================================================
# Clean Text Columns
# ==========================================================

def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove leading and trailing spaces from text columns.
    """

    text_columns = df.select_dtypes(include="object").columns

    for column in text_columns:
        df[column] = df[column].str.strip()

    return df


# ==========================================================
# Remove Duplicate Rows
# ==========================================================

def remove_duplicate_rows(df: pd.DataFrame):
    """
    Remove duplicate rows and generate a report.
    """

    duplicate_indexes = df[df.duplicated()].index.tolist()

    duplicates_removed = len(duplicate_indexes)

    df = df.drop_duplicates()

    report = {
        "duplicates_removed": duplicates_removed,
        "duplicate_indexes": duplicate_indexes
    }

    return df, report


# ==========================================================
# Fill Non-Critical Missing Values
# ==========================================================

def fill_non_critical_missing_values(df: pd.DataFrame):
    """
    Fill missing values for non-critical columns.
    """

    report = {}

    default_values = {
        "ship_mode": "Unknown",
        "order_priority": "Medium",
        "discount": 0,
        "profit": 0,
        "shipping_cost": 0,
    }

    for column, default_value in default_values.items():

        if column in df.columns:

            missing_count = int(df[column].isnull().sum())

            if missing_count > 0:

                df[column] = df[column].fillna(default_value)

                report[column] = {
                    "filled": missing_count,
                    "default_value": default_value
                }

    return df, report


# ==========================================================
# Main Transformation Function
# ==========================================================

def transform_data(df: pd.DataFrame):
    """
    Execute all transformation steps.
    """

    df = standardize_column_names(df)

    df = convert_dates(df)

    df = convert_numeric_columns(df)

    df = clean_text_columns(df)

    df, duplicate_report = remove_duplicate_rows(df)

    df, filling_report = fill_non_critical_missing_values(df)

    transformation_report = {
        "duplicate_report": duplicate_report,
        "filling_report": filling_report
    }

    return df, transformation_report


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    from etl.extract import extract_data

    df = extract_data("data/raw/SuperStoreOrders.csv")

    transformed_df, report = transform_data(df)

    print("=" * 70)
    print("          RetailIQ AI - Transformation Report")
    print("=" * 70)

    print(f"Rows                 : {len(transformed_df)}")
    print(f"Columns              : {len(transformed_df.columns)}")

    print("\nCleaning Summary")
    print("-" * 70)

    print(
        f"Duplicate Rows Removed : {report['duplicate_report']['duplicates_removed']}"
    )

    if report["duplicate_report"]["duplicate_indexes"]:

        print(
            f"Duplicate Row Indexes : {report['duplicate_report']['duplicate_indexes']}"
        )

    if report["filling_report"]:

        print("\nFilled Missing Values:")

        for column, info in report["filling_report"].items():

            print(
                f"- {column}: {info['filled']} filled with '{info['default_value']}'"
            )

    else:

        print("\nNo missing values were filled.")

    print("\nData Types:\n")

    print(transformed_df.dtypes)

    print("\nFirst 5 Rows:\n")

    print(transformed_df.head())

    print("\nTransformation Status : SUCCESS ✅")

    print("=" * 70)
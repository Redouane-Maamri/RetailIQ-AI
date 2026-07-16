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

def remove_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows.
    """

    df = df.drop_duplicates()

    return df


# ==========================================================
# Main Transformation Function
# ==========================================================

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Execute all transformation steps.
    """

    df = standardize_column_names(df)
    df = convert_dates(df)
    df = convert_numeric_columns(df)
    df = clean_text_columns(df)
    df = remove_duplicate_rows(df)

    return df


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    from etl.extract import extract_data

    df = extract_data("data/raw/SuperStoreOrders.csv")

    transformed_df = transform_data(df)

    print("=" * 65)
    print("          RetailIQ AI - Transformation Report")
    print("=" * 65)

    print(f"Rows             : {len(transformed_df)}")
    print(f"Columns          : {len(transformed_df.columns)}")

    print("\nData Types:\n")
    print(transformed_df.dtypes)

    print("\nFirst 5 Rows:\n")
    print(transformed_df.head())

    print("\nTransformation Status : SUCCESS ✅")
    print("=" * 65)
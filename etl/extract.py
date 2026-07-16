import pandas as pd
from pathlib import Path


def extract_data(file_path: str) -> pd.DataFrame:
    """
    Read a CSV file and return a Pandas DataFrame.

    Parameters:
        file_path (str): Path to the CSV dataset.

    Returns:
        pd.DataFrame: Loaded dataset.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    df = pd.read_csv(path)

    return df


if __name__ == "__main__":

    dataset_path = "data/raw/SuperStoreOrders.csv"

    df = extract_data(dataset_path)

    print("=" * 60)
    print("RetailIQ AI - Extract Module")
    print("=" * 60)

    print(f"Rows      : {df.shape[0]}")
    print(f"Columns   : {df.shape[1]}")

    print("\nColumn Names:\n")
    print(df.columns.tolist())

    print("\nFirst 5 Rows:\n")
    print(df.head())
import os
import pandas as pd

# -----------------------------
# Paths
# -----------------------------
INPUT_FILE = "data/raw/SuperStoreOrders.csv"
OUTPUT_FOLDER = "data/testing"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------------
# Read original dataset
# -----------------------------
df = pd.read_csv(INPUT_FILE)

# Keep only first 20 rows
df = df.head(20)

# ======================================================
# 1. VALID DATASET
# ======================================================
valid_df = df.copy()

valid_df.to_csv(
    f"{OUTPUT_FOLDER}/01_valid_dataset.csv",
    index=False
)

# ======================================================
# 2. EXTRA COLUMNS
# ======================================================
extra_df = df.copy()

extra_df["supplier"] = "Dell"
extra_df["warehouse"] = "Warehouse A"
extra_df["currency"] = "USD"
extra_df["promotion_code"] = "PROMO10"

extra_df.to_csv(
    f"{OUTPUT_FOLDER}/02_extra_columns.csv",
    index=False
)

# ======================================================
# 3. DUPLICATE ROWS
# ======================================================
duplicate_df = df.copy()

duplicate_df = pd.concat(
    [
        duplicate_df,
        duplicate_df.iloc[[0]]
    ],
    ignore_index=True
)

duplicate_df.to_csv(
    f"{OUTPUT_FOLDER}/03_duplicate_rows.csv",
    index=False
)

# ======================================================
# 4. MISSING VALUES
# ======================================================
missing_values_df = df.copy()

missing_values_df.loc[0, "sales"] = None
missing_values_df.loc[2, "profit"] = None
missing_values_df.loc[4, "ship_mode"] = None

missing_values_df.to_csv(
    f"{OUTPUT_FOLDER}/04_missing_values.csv",
    index=False
)

# ======================================================
# 5. MISSING REQUIRED COLUMN
# ======================================================
missing_column_df = df.copy()

missing_column_df = missing_column_df.drop(
    columns=["shipping_cost"]
)

missing_column_df.to_csv(
    f"{OUTPUT_FOLDER}/05_missing_required_column.csv",
    index=False
)

print("=" * 60)
print("RetailIQ AI - Test Datasets Created")
print("=" * 60)

print("✅ 01_valid_dataset.csv")
print("✅ 02_extra_columns.csv")
print("✅ 03_duplicate_rows.csv")
print("✅ 04_missing_values.csv")
print("✅ 05_missing_required_column.csv")

print("\nLocation:")
print(OUTPUT_FOLDER)
import pandas as pd
from sqlalchemy import text

from database.connection import get_engine

def clear_database():
    """
    Remove existing data while respecting foreign key constraints.
    """

    engine = get_engine()

    with engine.begin() as connection:

        connection.execute(text('DELETE FROM "OrderItems";'))
        connection.execute(text('DELETE FROM "Orders";'))
        connection.execute(text('DELETE FROM "Products";'))
        connection.execute(text('DELETE FROM "Locations";'))
        connection.execute(text('DELETE FROM "Customers";'))

        connection.execute(text('ALTER SEQUENCE "Customers_customer_id_seq" RESTART WITH 1;'))
        connection.execute(text('ALTER SEQUENCE "Locations_location_id_seq" RESTART WITH 1;'))
        connection.execute(text('ALTER SEQUENCE "OrderItems_order_item_id_seq" RESTART WITH 1;'))

    print("Database cleaned successfully.")

def load_customers(df: pd.DataFrame):
    """
    Load unique customers and return a lookup dictionary.
    """

    engine = get_engine()

    customers = (
        df[
            [
                "customer_name",
                "segment"
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    customers.to_sql(
        "Customers",
        engine,
        if_exists="append",
        index=False
    )

    customers_db = pd.read_sql(
        'SELECT customer_id, customer_name FROM "Customers";',
        engine
    )

    customer_lookup = dict(
        zip(
            customers_db["customer_name"],
            customers_db["customer_id"]
        )
    )

    print(f"Customers Loaded : {len(customers)}")

    return customer_lookup

def load_locations(df: pd.DataFrame):
    """
    Load unique locations and return a lookup dictionary.
    """

    engine = get_engine()

    locations = (
        df[
            [
                "country",
                "state",
                "market",
                "region"
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    locations.to_sql(
        "Locations",
        engine,
        if_exists="append",
        index=False
    )

    locations_db = pd.read_sql(
        '''
        SELECT
            location_id,
            country,
            state,
            market,
            region
        FROM "Locations";
        ''',
        engine
    )

    location_lookup = {}

    for _, row in locations_db.iterrows():

        key = (
            row["country"],
            row["state"],
            row["market"],
            row["region"]
        )

        location_lookup[key] = row["location_id"]

    print(f"Locations Loaded : {len(locations)}")

    return location_lookup

def load_products(df: pd.DataFrame):
    """
    Load unique products into PostgreSQL.
    """

    engine = get_engine()

    products = (
        df[
            [
                "product_id",
                "product_name",
                "category",
                "sub_category"
            ]
        ]
        .drop_duplicates(subset=["product_id"])
        .reset_index(drop=True)
    )

    print(f"Original rows      : {len(df)}")
    print(f"Unique Product IDs : {df['product_id'].nunique()}")
    print(f"Products to insert : {len(products)}")

    products.to_sql(
        "Products",
        engine,
        if_exists="append",
        index=False
    )

    print(f"Products Loaded : {len(products)}")

def load_orders(
    df: pd.DataFrame,
    customer_lookup: dict,
    location_lookup: dict
):
    """
    Load Orders table using customer and location lookup dictionaries.
    """

    engine = get_engine()

    orders = df[
        [
            "order_id",
            "order_date",
            "ship_date",
            "ship_mode",
            "order_priority",
            "year",
            "customer_name",
            "country",
            "state",
            "market",
            "region"
        ]
    ].copy()

    # Map customer_id
    orders["customer_id"] = orders["customer_name"].map(customer_lookup)

    # Map location_id
    orders["location_id"] = orders.apply(
        lambda row: location_lookup[
            (
                row["country"],
                row["state"],
                row["market"],
                row["region"]
            )
        ],
        axis=1
    )

    # Keep only database columns
    orders = orders[
        [
            "order_id",
            "order_date",
            "ship_date",
            "ship_mode",
            "order_priority",
            "year",
            "customer_id",
            "location_id"
        ]
    ]

    # One order only once
    orders = orders.drop_duplicates(subset=["order_id"])

    print(f"Orders to insert : {len(orders)}")

    orders.to_sql(
        "Orders",
        engine,
        if_exists="append",
        index=False
    )

    print(f"Orders Loaded : {len(orders)}")

def load_order_items(df: pd.DataFrame):
    """
    Load OrderItems table.
    """

    engine = get_engine()

    order_items = df[
        [
            "order_id",
            "product_id",
            "quantity",
            "sales",
            "discount",
            "profit",
            "shipping_cost"
        ]
    ].copy()

    print(f"Order Items to insert : {len(order_items)}")

    order_items.to_sql(
        "OrderItems",
        engine,
        if_exists="append",
        index=False
    )

    print(f"Order Items Loaded : {len(order_items)}")

if __name__ == "__main__":

    from etl.extract import extract_data
    from etl.transform import transform_data

    df = extract_data("data/raw/SuperStoreOrders.csv")
    df = transform_data(df)

    clear_database()

customer_lookup = load_customers(df)

location_lookup = load_locations(df)

load_products(df)

load_orders(
    df,
    customer_lookup,
    location_lookup
)

load_order_items(df)

print()

print("Customer Lookup Example:")
print(list(customer_lookup.items())[:5])

print()

print("Location Lookup Example:")
print(list(location_lookup.items())[:5])
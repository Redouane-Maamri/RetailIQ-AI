import pandas as pd

from database.connection import get_engine


def load_dashboard_data():
    """
    Load the complete analytical dataset.
    """

    query = """
    SELECT
        o.order_id,
        o.order_date,
        o.ship_date,
        o.ship_mode,
        o.order_priority,
        o.year,

        c.customer_id,
        c.customer_name,
        c.segment,

        p.product_id,
        p.product_name,
        p.category,
        p.sub_category,

        l.country,
        l.state,
        l.market,
        l.region,

        oi.quantity,
        oi.sales,
        oi.discount,
        oi.profit,
        oi.shipping_cost

    FROM "Orders" o

    JOIN "Customers" c
        ON o.customer_id = c.customer_id

    JOIN "Locations" l
        ON o.location_id = l.location_id

    JOIN "OrderItems" oi
        ON o.order_id = oi.order_id

    JOIN "Products" p
        ON oi.product_id = p.product_id

    ORDER BY o.order_date;
    """

    df = pd.read_sql(query, get_engine())

    # Convert dates
    df["order_date"] = pd.to_datetime(df["order_date"].astype(str))
    df["ship_date"] = pd.to_datetime(df["ship_date"].astype(str))

    return df
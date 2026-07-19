import streamlit as st


def display_kpi_cards(df):
    """
    Display dashboard KPI cards.
    """

    total_sales = df["sales"].sum()
    total_profit = df["profit"].sum()
    total_orders = df["order_id"].nunique()
    total_customers = df["customer_id"].nunique()
    total_products = df["product_id"].nunique()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "💰 Total Sales",
            f"${total_sales:,.0f}"
        )

    with col2:
        st.metric(
            "📦 Orders",
            f"{total_orders:,}"
        )

    with col3:
        st.metric(
            "👥 Customers",
            f"{total_customers:,}"
        )

    with col4:
        st.metric(
            "📈 Profit",
            f"${total_profit:,.0f}"
        )

    with col5:
        st.metric(
            "🛒 Products",
            f"{total_products:,}"
        )
import streamlit as st
import plotly.express as px


def sales_by_category(df):
    """
    Display total sales by category.
    """

    category_sales = (
        df.groupby("category", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=True)
    )

    fig = px.bar(
        category_sales,
        x="sales",
        y="category",
        orientation="h",
        text_auto=".2s",
        color="sales",
        color_continuous_scale="Blues",
        title="💰 Sales by Category"
    )

    fig.update_layout(
        template="plotly_dark",
        height=420,
        coloraxis_showscale=False,
        xaxis_title="Sales ($)",
        yaxis_title=""
    )

    st.plotly_chart(fig, use_container_width=True)

def profit_by_category(df):
    """
    Display total profit by category.
    """

    category_profit = (
        df.groupby("category", as_index=False)["profit"]
        .sum()
        .sort_values("profit", ascending=True)
    )

    fig = px.bar(
        category_profit,
        x="profit",
        y="category",
        orientation="h",
        text_auto=".2s",
        color="profit",
        color_continuous_scale="Greens",
        title="📈 Profit by Category"
    )

    fig.update_layout(
        template="plotly_dark",
        height=420,
        coloraxis_showscale=False,
        xaxis_title="Profit ($)",
        yaxis_title=""
    )

    st.plotly_chart(fig, use_container_width=True)
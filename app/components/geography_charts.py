import streamlit as st
import plotly.express as px


def sales_by_region(df):
    """
    Display total sales by region.
    """

    region_sales = (
        df.groupby("region", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    fig = px.bar(
        region_sales,
        x="region",
        y="sales",
        text_auto=".2s",
        color="sales",
        color_continuous_scale="Blues",
        title="🌍 Sales by Region"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        coloraxis_showscale=False,
        xaxis_title="Region",
        yaxis_title="Sales ($)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


def sales_by_market(df):
    """
    Display total sales by market.
    """

    market_sales = (
        df.groupby("market", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    fig = px.bar(
        market_sales,
        x="market",
        y="sales",
        text_auto=".2s",
        color="sales",
        color_continuous_scale="Viridis",
        title="🌎 Sales by Market"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        coloraxis_showscale=False,
        xaxis_title="Market",
        yaxis_title="Sales ($)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
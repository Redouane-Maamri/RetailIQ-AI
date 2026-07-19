import streamlit as st
import plotly.express as px


def top_products_sales(df):
    """
    Display the Top 10 Products by Sales.
    """

    top_products = (
        df.groupby("product_name", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top_products,
        x="sales",
        y="product_name",
        orientation="h",
        text_auto=".2s",
        color="sales",
        color_continuous_scale="Blues",
        title="🏆 Top 10 Products by Sales"
    )

    fig.update_layout(
        template="plotly_dark",
        height=520,
        coloraxis_showscale=False,
        xaxis_title="Sales ($)",
        yaxis_title=""
    )

    fig.update_yaxes(categoryorder="total ascending")

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
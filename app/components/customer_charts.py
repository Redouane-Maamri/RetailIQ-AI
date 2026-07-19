import streamlit as st
import plotly.express as px


def top_customers_sales(df):
    """
    Display the Top 10 Customers by Sales.
    """

    top_customers = (
        df.groupby("customer_name", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top_customers,
        x="sales",
        y="customer_name",
        orientation="h",
        text_auto=".2s",
        color="sales",
        color_continuous_scale="Purples",
        title="👥 Top 10 Customers by Sales"
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
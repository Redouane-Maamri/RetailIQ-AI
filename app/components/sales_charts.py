import pandas as pd
import plotly.express as px
import streamlit as st


def monthly_sales_chart(df):

    monthly_sales = (
        df.assign(month=df["order_date"].dt.to_period("M").astype(str))
          .groupby("month", as_index=False)["sales"]
          .sum()
    )

    fig = px.line(
        monthly_sales,
        x="month",
        y="sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Month",
        yaxis_title="Sales ($)",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)
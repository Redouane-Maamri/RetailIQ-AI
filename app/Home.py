import streamlit as st

st.set_page_config(
    page_title="RetailIQ AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 RetailIQ AI")
st.subheader("Intelligent Retail Analytics Platform")

st.markdown("---")

st.write("""
Welcome to **RetailIQ AI**, an intelligent platform for retail data analysis.

This application allows you to:

- 📂 Upload a retail dataset
- ⚙️ Execute the ETL pipeline
- 🗄️ Store cleaned data in PostgreSQL
- 📊 Explore interactive dashboards
- 🤖 Generate AI-powered insights
""")
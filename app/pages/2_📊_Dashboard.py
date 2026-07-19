import streamlit as st

from pathlib import Path
import sys

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.queries import load_dashboard_data
from components.kpi_cards import display_kpi_cards
from components.filters import dashboard_filters
from components.sales_charts import monthly_sales_chart
from components.category_charts import (
    sales_by_category,
    profit_by_category
)
from components.product_charts import top_products_sales
from components.customer_charts import top_customers_sales
from components.geography_charts import (
    sales_by_region,
    sales_by_market
)

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 RetailIQ AI Dashboard")

# Load data
df = load_dashboard_data()

df = load_dashboard_data()

df = dashboard_filters(df)

# KPI Cards
display_kpi_cards(df)

st.divider()

# Monthly Sales Chart
monthly_sales_chart(df)

st.divider()

col1, col2 = st.columns(2)

with col1:
    sales_by_category(df)

with col2:
    profit_by_category(df)

st.divider()

col1, col2 = st.columns(2)

with col1:
    top_products_sales(df)

with col2:
    top_customers_sales(df)

st.divider()

col1, col2 = st.columns(2)

with col1:
    sales_by_region(df)

with col2:
    sales_by_market(df)

# # Temporary table
# st.dataframe(df, use_container_width=True)

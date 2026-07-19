import streamlit as st

from pathlib import Path
import sys

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.queries import load_dashboard_data
from components.kpi_cards import display_kpi_cards

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 RetailIQ AI Dashboard")

# Load data
df = load_dashboard_data()

# Display KPI cards
display_kpi_cards(df)

st.divider()

# Display table (temporary)
st.dataframe(df, use_container_width=True)
import streamlit as st


def dashboard_filters(df):
    """
    Professional sidebar filters for RetailIQ AI.
    Returns the filtered dataframe.
    """

    filtered_df = df.copy()

    # =====================================================
    # SIDEBAR HEADER
    # =====================================================

    st.sidebar.title("🔎 Filters")
    st.sidebar.caption("Filter the dashboard to explore your retail data.")
    st.sidebar.divider()

    # =====================================================
    # BUSINESS FILTERS
    # =====================================================

    st.sidebar.subheader("Business")

    # ---------- Year ----------
    years = sorted(
        filtered_df["order_date"]
        .dt.year
        .dropna()
        .astype(int)
        .unique()
    )

    selected_year = st.sidebar.selectbox(
        "📅 Year",
        ["All"] + years
    )

    if selected_year != "All":
        filtered_df = filtered_df[
            filtered_df["order_date"].dt.year == selected_year
        ]

    # ---------- Market ----------
    markets = sorted(filtered_df["market"].dropna().unique())

    selected_market = st.sidebar.selectbox(
        "🌍 Market",
        ["All"] + markets
    )

    if selected_market != "All":
        filtered_df = filtered_df[
            filtered_df["market"] == selected_market
        ]

    # ---------- Region ----------
    regions = sorted(filtered_df["region"].dropna().unique())

    selected_region = st.sidebar.selectbox(
        "📍 Region",
        ["All"] + regions
    )

    if selected_region != "All":
        filtered_df = filtered_df[
            filtered_df["region"] == selected_region
        ]

    st.sidebar.divider()

    # =====================================================
    # CUSTOMER FILTERS
    # =====================================================

    st.sidebar.subheader("Customer")

    segments = sorted(filtered_df["segment"].dropna().unique())

    selected_segment = st.sidebar.selectbox(
        "👥 Segment",
        ["All"] + segments
    )

    if selected_segment != "All":
        filtered_df = filtered_df[
            filtered_df["segment"] == selected_segment
        ]

    st.sidebar.divider()

    # =====================================================
    # PRODUCT FILTERS
    # =====================================================

    st.sidebar.subheader("Product")

    categories = sorted(filtered_df["category"].dropna().unique())

    selected_category = st.sidebar.selectbox(
        "📦 Category",
        ["All"] + categories
    )

    if selected_category != "All":
        filtered_df = filtered_df[
            filtered_df["category"] == selected_category
        ]

    st.sidebar.divider()

    # =====================================================
    # DATASET SUMMARY
    # =====================================================

    st.sidebar.subheader("📊 Dataset")

    col1, col2 = st.sidebar.columns(2)

    col1.metric("Rows", f"{len(filtered_df):,}")

    col2.metric(
        "Orders",
        f"{filtered_df['order_id'].nunique():,}"
    )

    col1, col2 = st.sidebar.columns(2)

    col1.metric(
        "Customers",
        f"{filtered_df['customer_name'].nunique():,}"
    )

    col2.metric(
        "Products",
        f"{filtered_df['product_name'].nunique():,}"
    )

    st.sidebar.divider()

    # =====================================================
    # RESET BUTTON
    # =====================================================

    if st.sidebar.button(
        "🗑 Reset Filters",
        use_container_width=True
    ):
        st.rerun()

    return filtered_df
import streamlit as st
import pandas as pd
import plotly.express as px

from analytics.filters import get_filter_options

from analytics.filtered_analytics import (
    get_filtered_kpis,
    get_filtered_monthly_sales,
    get_filtered_category_sales,
    get_filtered_top_products,
    get_filtered_top_customers
)

from analytics.inventory import (
    get_inventory_status,
    get_low_stock_products
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="BizPulse AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PREMIUM DARK THEME
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #080D18;
    color: #F5F7FF;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

section[data-testid="stSidebar"] {
    background-color: #070B14;
    border-right: 1px solid #202A40;
}

section[data-testid="stSidebar"] * {
    color: #E8ECF8;
}

h1 {
    color: #FFFFFF !important;
    font-weight: 750 !important;
}

h2, h3 {
    color: #F5F7FF !important;
}

div[data-testid="metric-container"] {
    background-color: #11192C;
    border: 1px solid #263452;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.25);
    min-height: 120px;
}

div[data-testid="metric-container"] label {
    color: #8995AF !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 28px !important;
    font-weight: 750 !important;
    white-space: nowrap !important;
}

.secondary-box {
    background-color: #0F1729;
    border: 1px solid #202B44;
    border-radius: 14px;
    padding: 16px;
    text-align: center;
    min-height: 85px;
}

.secondary-title {
    color: #7F8BA6;
    font-size: 12px;
    font-weight: 600;
}

.secondary-value {
    color: #F5F7FF;
    font-size: 22px;
    font-weight: 700;
    margin-top: 7px;
}

.footer {
    text-align: center;
    color: #59657F;
    font-size: 12px;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# RESET FILTER FUNCTION
# ============================================================

def reset_filters():

    st.session_state["category_filter"] = "All Categories"

    st.session_state["city_filter"] = "All Cities"

    st.session_state["product_filter"] = "All Products"

    st.session_state["date_filter"] = (
        st.session_state["min_date"],
        st.session_state["max_date"]
    )


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.title("🚀 BizPulse AI")

    st.caption(
        "Business Intelligence Platform"
    )

    st.divider()

    page = st.radio(
        "Navigate",
        [
            "🏠 Executive Overview",
            "📈 Sales Analytics",
            "🏆 Product Analytics",
            "👥 Customer Intelligence",
            "📦 Inventory Intelligence",
            "🤖 AI Insights"
        ]
    )

    st.divider()

    st.caption(
        "BizPulse AI v1.0"
    )


# ============================================================
# LOAD FILTER OPTIONS
# ============================================================

filter_options = get_filter_options()


# ============================================================
# PREPARE DATE VALUES
# ============================================================

min_date = pd.to_datetime(
    filter_options["min_date"]
).date()

max_date = pd.to_datetime(
    filter_options["max_date"]
).date()


# Store dates for reset callback
st.session_state["min_date"] = min_date
st.session_state["max_date"] = max_date


# ============================================================
# INITIALIZE FILTER SESSION STATE
# ============================================================

if "category_filter" not in st.session_state:

    st.session_state["category_filter"] = "All Categories"


if "city_filter" not in st.session_state:

    st.session_state["city_filter"] = "All Cities"


if "product_filter" not in st.session_state:

    st.session_state["product_filter"] = "All Products"


if "date_filter" not in st.session_state:

    st.session_state["date_filter"] = (
        min_date,
        max_date
    )


# ============================================================
# DASHBOARD FILTERS
# ============================================================

with st.sidebar:

    st.markdown("### 🔎 Dashboard Filters")

    st.caption(
        "Change filters to update your business analytics."
    )


    # --------------------------------------------------------
    # DATE FILTER
    # --------------------------------------------------------

    selected_dates = st.date_input(
        "📅 Order Date Range",
        min_value=min_date,
        max_value=max_date,
        key="date_filter"
    )


    if isinstance(
        selected_dates,
        tuple
    ) and len(selected_dates) == 2:

        start_date = selected_dates[0]

        end_date = selected_dates[1]

    else:

        start_date = min_date

        end_date = max_date


    # --------------------------------------------------------
    # CATEGORY FILTER
    # --------------------------------------------------------

    selected_category = st.selectbox(
        "👗 Category",
        [
            "All Categories"
        ] +
        filter_options["categories"],
        key="category_filter"
    )


    # --------------------------------------------------------
    # CITY FILTER
    # --------------------------------------------------------

    selected_city = st.selectbox(
        "📍 Customer City",
        [
            "All Cities"
        ] +
        filter_options["cities"],
        key="city_filter"
    )


    # --------------------------------------------------------
    # PRODUCT FILTER
    # --------------------------------------------------------

    selected_product = st.selectbox(
        "🛍️ Product",
        [
            "All Products"
        ] +
        filter_options["products"],
        key="product_filter"
    )


    st.divider()


    # --------------------------------------------------------
    # RESET BUTTON
    # --------------------------------------------------------

    st.button(
        "🔄 Reset Filters",
        use_container_width=True,
        on_click=reset_filters
    )


# ============================================================
# FILTERED KPI DATA
# ============================================================

kpis = get_filtered_kpis(
    start_date=start_date,
    end_date=end_date,
    category=selected_category,
    city=selected_city,
    product=selected_product
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "🏠 Executive Overview":

    st.title(
        "Good evening, Maria 👋"
    )

    st.write(
        "Here's what's happening with your business based on your selected filters."
    )

    st.divider()


    # ========================================================
    # PRIMARY KPIs
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "💰 Total Revenue",
            f"${kpis['revenue']:,.0f}"
        )

    with col2:

        st.metric(
            "🤑 Total Profit",
            f"${kpis['profit']:,.0f}"
        )

    with col3:

        st.metric(
            "📊 Profit Margin",
            f"{kpis['profit_margin']:.1f}%"
        )

    with col4:

        st.metric(
            "🛒 Total Orders",
            f"{kpis['orders']:,}"
        )


    st.write("")


    # ========================================================
    # SECONDARY KPIs
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    secondary_data = [

        (
            col1,
            "👥 Customers",
            f"{kpis['customers']:,}"
        ),

        (
            col2,
            "📦 Units Sold",
            f"{kpis['units_sold']:,}"
        ),

        (
            col3,
            "🛍️ Avg Order Value",
            f"${kpis['average_order_value']:,.2f}"
        ),

        (
            col4,
            "💵 Total Cost",
            f"${kpis['cost']:,.0f}"
        )

    ]


    for column, title, value in secondary_data:

        with column:

            st.markdown(
                f"""
                <div class="secondary-box">

                <div class="secondary-title">
                {title}
                </div>

                <div class="secondary-value">
                {value}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    st.write("")


    # ========================================================
    # ACTIVE FILTERS
    # ========================================================

    st.subheader(
        "🔎 Active Filters"
    )

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)


    with filter_col1:

        st.caption("📅 Date Range")

        st.write(
            f"{start_date} → {end_date}"
        )


    with filter_col2:

        st.caption("👗 Category")

        st.write(
            selected_category
        )


    with filter_col3:

        st.caption("📍 City")

        st.write(
            selected_city
        )


    with filter_col4:

        st.caption("🛍️ Product")

        st.write(
            selected_product
        )


    st.divider()


    # ========================================================
    # REVENUE OVERVIEW
    # ========================================================

    st.subheader(
        "📈 Revenue Overview"
    )


    monthly_sales = get_filtered_monthly_sales(
        start_date=start_date,
        end_date=end_date,
        category=selected_category,
        city=selected_city,
        product=selected_product
    )


    if monthly_sales:

        sales_df = pd.DataFrame(
            monthly_sales,
            columns=[
                "Month",
                "Revenue"
            ]
        )


        fig = px.area(
            sales_df,
            x="Month",
            y="Revenue",
            title="Filtered Monthly Revenue"
        )


        fig.update_layout(
            paper_bgcolor="#0F1729",
            plot_bgcolor="#0F1729",
            font_color="#AAB5CC"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No revenue data found for the selected filters."
        )


    st.divider()


    # ========================================================
    # TOP PRODUCTS
    # ========================================================

    st.subheader(
        "🏆 Top Performing Products"
    )


    top_products = get_filtered_top_products(
        limit=5,
        start_date=start_date,
        end_date=end_date,
        category=selected_category,
        city=selected_city,
        product=selected_product
    )


    if top_products:

        products_df = pd.DataFrame(
            top_products,
            columns=[
                "Product",
                "Category",
                "Units Sold",
                "Revenue",
                "Profit"
            ]
        )


        st.dataframe(
            products_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No products found for the selected filters."
        )


# ============================================================
# SALES ANALYTICS
# ============================================================

elif page == "📈 Sales Analytics":

    st.title(
        "📈 Sales Analytics"
    )

    st.write(
        "Understand revenue trends and category performance."
    )

    st.divider()


    monthly_sales = get_filtered_monthly_sales(
        start_date,
        end_date,
        selected_category,
        selected_city,
        selected_product
    )


    if monthly_sales:

        sales_df = pd.DataFrame(
            monthly_sales,
            columns=[
                "Month",
                "Revenue"
            ]
        )


        st.subheader(
            "📈 Revenue Trend"
        )


        fig = px.area(
            sales_df,
            x="Month",
            y="Revenue"
        )


        fig.update_layout(
            paper_bgcolor="#0F1729",
            plot_bgcolor="#0F1729",
            font_color="#AAB5CC"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    category_sales = get_filtered_category_sales(
        start_date,
        end_date,
        selected_category,
        selected_city,
        selected_product
    )


    if category_sales:

        category_df = pd.DataFrame(
            category_sales,
            columns=[
                "Category",
                "Revenue"
            ]
        )


        st.subheader(
            "💰 Revenue by Category"
        )


        fig = px.bar(
            category_df,
            x="Category",
            y="Revenue"
        )


        fig.update_layout(
            paper_bgcolor="#0F1729",
            plot_bgcolor="#0F1729",
            font_color="#AAB5CC"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No sales data found for the selected filters."
        )


# ============================================================
# PRODUCT ANALYTICS
# ============================================================

elif page == "🏆 Product Analytics":

    st.title(
        "🏆 Product Analytics"
    )

    st.write(
        "Discover your best-performing and most profitable products."
    )

    st.divider()


    top_products = get_filtered_top_products(
        limit=10,
        start_date=start_date,
        end_date=end_date,
        category=selected_category,
        city=selected_city,
        product=selected_product
    )


    if top_products:

        products_df = pd.DataFrame(
            top_products,
            columns=[
                "Product",
                "Category",
                "Units Sold",
                "Revenue",
                "Profit"
            ]
        )


        st.subheader(
            "🏆 Top Products"
        )


        st.dataframe(
            products_df,
            use_container_width=True,
            hide_index=True
        )


        fig = px.bar(
            products_df,
            x="Product",
            y="Profit",
            title="Product Profit Performance"
        )


        fig.update_layout(
            paper_bgcolor="#0F1729",
            plot_bgcolor="#0F1729",
            font_color="#AAB5CC"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No product data found for the selected filters."
        )


# ============================================================
# CUSTOMER INTELLIGENCE
# ============================================================

elif page == "👥 Customer Intelligence":

    st.title(
        "👥 Customer Intelligence"
    )

    st.write(
        "Understand your most valuable customers."
    )

    st.divider()


    top_customers = get_filtered_top_customers(
        limit=10,
        start_date=start_date,
        end_date=end_date,
        category=selected_category,
        city=selected_city,
        product=selected_product
    )


    if top_customers:

        customer_df = pd.DataFrame(
            top_customers,
            columns=[
                "First Name",
                "Last Name",
                "City",
                "Orders",
                "Total Spent"
            ]
        )


        st.subheader(
            "💎 Top Customers"
        )


        st.dataframe(
            customer_df,
            use_container_width=True,
            hide_index=True
        )


        fig = px.bar(
            customer_df,
            x="First Name",
            y="Total Spent",
            title="Top Customers by Spending"
        )


        fig.update_layout(
            paper_bgcolor="#0F1729",
            plot_bgcolor="#0F1729",
            font_color="#AAB5CC"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No customer data found for the selected filters."
        )


# ============================================================
# INVENTORY INTELLIGENCE
# ============================================================

elif page == "📦 Inventory Intelligence":

    st.title(
        "📦 Inventory Intelligence"
    )

    st.write(
        "Monitor stock levels and identify inventory risks."
    )

    st.divider()


    try:

        inventory = get_inventory_status()

        low_stock = get_low_stock_products()


        if inventory:

            inventory_df = pd.DataFrame(
                inventory,
                columns=[
                    "Product ID",
                    "Product Name",
                    "Category",
                    "Stock Quantity",
                    "Reorder Level",
                    "Price",
                    "Cost Price",
                    "Last Restock Date"
                ]
            )


            total_stock = int(
                inventory_df[
                    "Stock Quantity"
                ].sum()
            )


            inventory_cost_value = (
                inventory_df[
                    "Stock Quantity"
                ]
                *
                inventory_df[
                    "Cost Price"
                ]
            ).sum()


            low_stock_count = len(
                low_stock
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "📦 Total Stock Units",
                    f"{total_stock:,}"
                )


            with col2:

                st.metric(
                    "💰 Inventory Cost Value",
                    f"${inventory_cost_value:,.2f}"
                )


            with col3:

                st.metric(
                    "⚠️ Low Stock Products",
                    f"{low_stock_count:,}"
                )


            st.divider()


            st.subheader(
                "⚠️ Stock Alerts"
            )


            if low_stock:

                st.warning(
                    f"{len(low_stock)} products "
                    f"are at or below their reorder level."
                )


                low_stock_df = pd.DataFrame(
                    low_stock,
                    columns=[
                        "Product ID",
                        "Product Name",
                        "Category",
                        "Stock Quantity",
                        "Reorder Level",
                        "Price",
                        "Cost Price",
                        "Last Restock Date"
                    ]
                )


                st.dataframe(
                    low_stock_df,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.success(
                    "🟢 Inventory looks healthy. "
                    "No products currently require immediate restocking."
                )


            st.divider()


            st.subheader(
                "📋 Complete Inventory"
            )


            st.dataframe(
                inventory_df,
                use_container_width=True,
                hide_index=True
            )


            st.divider()


            st.subheader(
                "📊 Stock Levels"
            )


            fig = px.bar(
                inventory_df,
                x="Product Name",
                y="Stock Quantity",
                hover_data=[
                    "Category",
                    "Reorder Level",
                    "Price",
                    "Cost Price"
                ]
            )


            fig.update_layout(
                paper_bgcolor="#0F1729",
                plot_bgcolor="#0F1729",
                font_color="#AAB5CC"
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


        else:

            st.info(
                "No inventory records found."
            )


    except Exception as error:

        st.error(
            "Inventory data could not be loaded."
        )

        st.caption(
            f"Technical details: {error}"
        )


# ============================================================
# AI INSIGHTS
# ============================================================

elif page == "🤖 AI Insights":

    st.title(
        "🤖 BizPulse AI Analyst"
    )

    st.write(
        "Your automated business intelligence assistant."
    )

    st.divider()


    st.subheader(
        "🧠 Filtered Business Performance Summary"
    )


    st.info(
        f"Based on your selected filters, your business generated "
        f"${kpis['revenue']:,.2f} in revenue and "
        f"${kpis['profit']:,.2f} in profit. "
        f"Your current profit margin is "
        f"{kpis['profit_margin']:.2f}%."
    )


    st.subheader(
        "💡 Recommended Actions"
    )


    col1, col2 = st.columns(2)


    with col1:

        if kpis["profit_margin"] >= 40:

            st.success(
                "🏆 Strong profitability. "
                "Consider scaling your best-performing products."
            )

        elif kpis["profit_margin"] >= 20:

            st.info(
                "📊 Healthy profitability. "
                "Look for opportunities to optimize costs."
            )

        else:

            st.warning(
                "⚠️ Profitability needs attention. "
                "Review pricing and product costs."
            )


        st.info(
            "💰 Monitor product costs and pricing "
            "to protect your profit margins."
        )


    with col2:

        try:

            low_stock = get_low_stock_products()

            if low_stock:

                st.warning(
                    f"📦 {len(low_stock)} products need restocking attention."
                )

            else:

                st.success(
                    "📦 Inventory levels look healthy."
                )

        except Exception:

            st.warning(
                "Inventory information is currently unavailable."
            )


        st.info(
            "👥 Build loyalty strategies around your "
            "highest-value and repeat customers."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🚀 BizPulse AI • Intelligent Business Analytics Platform
    </div>
    """,
    unsafe_allow_html=True
)
"""
app.py
------
Supplementary Interactive Web Dashboard for local browser exploration.
Built with Streamlit and Plotly/Altair.

NOTE: This is a supplementary local demonstration interface and does NOT replace
the primary Power BI Desktop implementation detailed in powerbi/powerbi_dashboard_guide.md.
"""

import os
import streamlit as st
import pandas as pd
import altair as alt

# Page Configuration
st.set_page_config(
    page_title="Retail Sales Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
    .kpi-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Supplementary Disclaimer Banner
st.info("ℹ️ **Supplementary Interactive Viewer:** This Streamlit app provides an immediate interactive browser preview. For the enterprise Power BI model, DAX measures, and dashboard guide, see the `powerbi/` folder.")

DATA_PATH = "data/processed/retail_sales_cleaned.csv"

@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error(f"Cleaned dataset not found at `{DATA_PATH}`. Please run `python src/clean_data.py` first.")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Year_Month"] = df["Order Date"].dt.strftime("%Y-%m")
    df["Month_Name"] = df["Order Date"].dt.strftime("%b %Y")
    return df

df_raw = load_data()

# Sidebar Interactive Filters
st.sidebar.header("🔍 Filter Transactions")

# Date Filter
min_date = df_raw["Order Date"].min().date()
max_date = df_raw["Order Date"].max().date()
date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Region Filter
all_regions = sorted(df_raw["Region"].unique())
selected_regions = st.sidebar.multiselect("Select Regions", options=all_regions, default=all_regions)

# Category Filter
all_categories = sorted(df_raw["Category"].unique())
selected_categories = st.sidebar.multiselect("Select Categories", options=all_categories, default=all_categories)

# Apply Filters
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_d, end_d = date_range
    mask = (
        (df_raw["Order Date"].dt.date >= start_d) &
        (df_raw["Order Date"].dt.date <= end_d) &
        (df_raw["Region"].isin(selected_regions)) &
        (df_raw["Category"].isin(selected_categories))
    )
else:
    mask = (
        (df_raw["Region"].isin(selected_regions)) &
        (df_raw["Category"].isin(selected_categories))
    )

df_filtered = df_raw[mask].copy()

# Header
st.markdown("<div class='main-title'>Retail Sales Analytics Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Executive performance visibility, order basket analytics, regional share, and category mix (Calendar Year 2025)</div>", unsafe_allow_html=True)

if df_filtered.empty:
    st.warning("No records match the current filter selection. Please adjust your filters.")
    st.stop()

# -------------------------------------------------------------
# Top KPI Cards
# -------------------------------------------------------------
total_revenue = df_filtered["Sales Amount"].sum()
unique_orders = df_filtered["Order ID"].nunique()
aov = total_revenue / unique_orders if unique_orders > 0 else 0.0
total_quantity = df_filtered["Quantity"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Total Sales Revenue</div>
        <div class='kpi-value'>₹{total_revenue:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Unique Orders</div>
        <div class='kpi-value'>{unique_orders:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Average Order Value (AOV)</div>
        <div class='kpi-value'>₹{aov:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Total Units Sold</div>
        <div class='kpi-value'>{total_quantity:,}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# -------------------------------------------------------------
# Row 1 Charts: Monthly Trend & Top 5 Products
# -------------------------------------------------------------
chart_col1, chart_col2 = st.columns([1.2, 1])

with chart_col1:
    st.subheader("📈 Monthly Revenue Trend")
    monthly_trend = df_filtered.groupby("Year_Month").agg(
        Revenue=("Sales Amount", "sum"),
        Orders=("Order ID", "nunique")
    ).reset_index().sort_values(by="Year_Month")

    bar_chart = alt.Chart(monthly_trend).mark_bar(color="#2563EB", cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
        x=alt.X("Year_Month:N", title="Year-Month", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("Revenue:Q", title="Revenue (INR ₹)"),
        tooltip=[
            alt.Tooltip("Year_Month:N", title="Month"),
            alt.Tooltip("Revenue:Q", format=",.2f", title="Revenue (₹)"),
            alt.Tooltip("Orders:Q", title="Orders")
        ]
    ).properties(height=340)
    st.altair_chart(bar_chart, use_container_width=True)

with chart_col2:
    st.subheader("🏆 Top 5 Products by Revenue")
    top_prods = df_filtered.groupby("Product Name")["Sales Amount"].sum().reset_index()
    top_prods = top_prods.sort_values(by="Sales Amount", ascending=False).head(5)

    prod_chart = alt.Chart(top_prods).mark_bar(color="#0D9488", cornerRadiusTopRight=4, cornerRadiusBottomRight=4).encode(
        y=alt.Y("Product Name:N", sort="-x", title=None),
        x=alt.X("Sales Amount:Q", title="Sales Revenue (INR ₹)"),
        tooltip=[
            alt.Tooltip("Product Name:N"),
            alt.Tooltip("Sales Amount:Q", format=",.2f", title="Revenue (₹)")
        ]
    ).properties(height=340)
    st.altair_chart(prod_chart, use_container_width=True)

# -------------------------------------------------------------
# Row 2 Charts: Regional Distribution & Category Mix
# -------------------------------------------------------------
chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.subheader("🗺️ Revenue by Region")
    reg_summary = df_filtered.groupby("Region").agg(
        Revenue=("Sales Amount", "sum"),
        Orders=("Order ID", "nunique")
    ).reset_index().sort_values(by="Revenue", ascending=False)

    reg_chart = alt.Chart(reg_summary).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
        x=alt.X("Region:N", title="Region", sort="-y"),
        y=alt.Y("Revenue:Q", title="Revenue (INR ₹)"),
        color=alt.Color("Region:N", legend=None),
        tooltip=[
            alt.Tooltip("Region:N"),
            alt.Tooltip("Revenue:Q", format=",.2f", title="Revenue (₹)"),
            alt.Tooltip("Orders:Q", title="Orders")
        ]
    ).properties(height=300)
    st.altair_chart(reg_chart, use_container_width=True)

with chart_col4:
    st.subheader("📦 Revenue by Product Category")
    cat_summary = df_filtered.groupby("Category")["Sales Amount"].sum().reset_index()

    cat_chart = alt.Chart(cat_summary).mark_arc(innerRadius=60).encode(
        theta=alt.Theta("Sales Amount:Q", title="Revenue"),
        color=alt.Color("Category:N", title="Category"),
        tooltip=[
            alt.Tooltip("Category:N"),
            alt.Tooltip("Sales Amount:Q", format=",.2f", title="Revenue (₹)")
        ]
    ).properties(height=300)
    st.altair_chart(cat_chart, use_container_width=True)

# -------------------------------------------------------------
# Data Table Inspector & Export
# -------------------------------------------------------------
with st.expander("📋 View Cleaned Transactions Data Table"):
    display_cols = ["Order ID", "Order Date", "Product ID", "Product Name", "Category", "Region", "Quantity", "Unit Price", "Sales Amount"]
    st.dataframe(
        df_filtered[display_cols].sort_values(by=["Order Date", "Order ID"], ascending=[False, True]),
        use_container_width=True,
        hide_index=True
    )
    csv_bytes = df_filtered[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="filtered_retail_sales.csv",
        mime="text/csv"
    )

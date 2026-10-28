"""
generate_data.py
----------------
Generates a realistic synthetic retail sales dataset with realistic real-world
data quality anomalies (missing values, whitespace, case inconsistencies,
exact duplicates, and multi-item orders) to demonstrate end-to-end data
cleaning, SQL querying, and Power BI visualization workflows.

Currency: Indian Rupee (INR - ₹)
Random Seed: 42 (Reproducible)
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_retail_sales_dataset(
    num_rows: int = 1500,
    seed: int = 42,
    output_csv_path: str = "data/raw/retail_sales_raw.csv",
    output_excel_path: str = "data/raw/retail_sales_raw.xlsx"
) -> pd.DataFrame:
    """
    Generates synthetic retail transactions spanning 2025 with controlled imperfections.
    """
    random.seed(seed)
    np.random.seed(seed)

    # Product catalog with fixed base prices in INR (₹)
    catalog = [
        # Electronics
        ("PROD-EL-01", "Wireless Ergonomic Mouse", "Electronics", 1299.0),
        ("PROD-EL-02", "RGB Mechanical Gaming Keyboard", "Electronics", 3499.0),
        ("PROD-EL-03", "Portable Bluetooth Speaker", "Electronics", 2199.0),
        ("PROD-EL-04", "7-in-1 USB-C Hub Adapter", "Electronics", 1799.0),
        ("PROD-EL-05", "Noise Cancelling Headphones", "Electronics", 5999.0),
        ("PROD-EL-06", "Smart Fitness Watch", "Electronics", 3999.0),
        ("PROD-EL-07", "Full HD 1080p Webcam", "Electronics", 2499.0),
        ("PROD-EL-08", "1TB High-Speed External SSD", "Electronics", 7499.0),
        
        # Home & Kitchen
        ("PROD-HK-01", "Stainless Steel Insulated Bottle", "Home & Kitchen", 799.0),
        ("PROD-HK-02", "Digital Air Fryer 4.5L", "Home & Kitchen", 4899.0),
        ("PROD-HK-03", "1.8L Stainless Electric Kettle", "Home & Kitchen", 1199.0),
        ("PROD-HK-04", "3-Piece Non-Stick Cookware Set", "Home & Kitchen", 2899.0),
        ("PROD-HK-05", "Ceramic Coffee Mug (Set of 4)", "Home & Kitchen", 649.0),
        ("PROD-HK-06", "500W High Speed Smoothie Blender", "Home & Kitchen", 2299.0),

        # Fashion & Apparel
        ("PROD-FA-01", "Organic Cotton Crewneck T-Shirt", "Fashion", 699.0),
        ("PROD-FA-02", "Slim Fit Denim Jeans", "Fashion", 1699.0),
        ("PROD-FA-03", "Fleece Zip-Up Hoodie", "Fashion", 1999.0),
        ("PROD-FA-04", "Breathable Mesh Running Shoes", "Fashion", 2799.0),
        ("PROD-FA-05", "Genuine Leather Reversible Belt", "Fashion", 899.0),

        # Office Supplies
        ("PROD-OS-01", "Dual-Sided PU Leather Desk Mat", "Office Supplies", 849.0),
        ("PROD-OS-02", "Premium Gel Pen Set (Pack of 12)", "Office Supplies", 399.0),
        ("PROD-OS-03", "A5 Hardcover Dotted Journal", "Office Supplies", 499.0),
        ("PROD-OS-04", "Ergonomic High-Back Mesh Chair", "Office Supplies", 8999.0),
        ("PROD-OS-05", "Architect LED Desk Lamp", "Office Supplies", 1499.0),

        # Beauty & Personal Care
        ("PROD-BP-01", "Hydrating Vitamin C Face Serum", "Beauty & Personal Care", 749.0),
        ("PROD-BP-02", "Sonic Rechargeable Electric Toothbrush", "Beauty & Personal Care", 1899.0),
        ("PROD-BP-03", "Salon Grade Ionic Hair Dryer", "Beauty & Personal Care", 2299.0),
        ("PROD-BP-04", "All-Natural Tea Tree Face Wash", "Beauty & Personal Care", 399.0),
        ("PROD-BP-05", "Complete Beard Grooming Kit", "Beauty & Personal Care", 1299.0),
    ]

    regions = ["North", "South", "East", "West", "Central"]
    # Regional weights reflecting major Indian retail markets
    region_weights = [0.28, 0.26, 0.16, 0.20, 0.10]

    # Generate dates across 2025 with slight seasonality (higher in Q4 festive season)
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    total_days = (end_date - start_date).days + 1

    # Weights per month (index 0 to 11) reflecting Indian retail festive spike (Oct, Nov, Dec)
    month_weights = [0.06, 0.06, 0.07, 0.08, 0.08, 0.07, 0.08, 0.09, 0.09, 0.13, 0.12, 0.07]

    records = []
    order_counter = 1001
    
    # We will generate multi-item orders (1 to 3 items per order)
    while len(records) < num_rows:
        order_id = f"ORD-2025-{order_counter}"
        order_counter += 1

        # Determine order month based on month_weights
        chosen_month = np.random.choice(range(1, 13), p=month_weights)
        # Select random day in chosen month
        if chosen_month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randint(1, 31)
        elif chosen_month in [4, 6, 9, 11]:
            day = random.randint(1, 30)
        else:
            day = random.randint(1, 28)
        order_date = datetime(2025, chosen_month, day)

        # Region for this order
        region = np.random.choice(regions, p=region_weights)

        # Number of distinct line items in this order
        num_items = np.random.choice([1, 2, 3, 4], p=[0.60, 0.26, 0.11, 0.03])
        # Pick distinct products
        selected_products = random.sample(catalog, min(num_items, len(catalog)))

        for prod_id, prod_name, category, unit_price in selected_products:
            # Quantity distribution (skewed towards 1-3, occasionally up to 6)
            qty = int(np.random.choice([1, 2, 3, 4, 5, 6], p=[0.55, 0.25, 0.10, 0.05, 0.03, 0.02]))
            sales_amount = round(qty * unit_price, 2)

            records.append({
                "Order ID": order_id,
                "Order Date": order_date.strftime("%Y-%m-%d"),
                "Product ID": prod_id,
                "Product Name": prod_name,
                "Category": category,
                "Region": region,
                "Quantity": qty,
                "Unit Price": unit_price,
                "Sales Amount": sales_amount
            })

            if len(records) >= num_rows:
                break

    df = pd.DataFrame(records)

    # -------------------------------------------------------------
    # Inject Realistic Imperfections / Data Quality Issues
    # -------------------------------------------------------------
    # 1. Trailing/leading spaces and casing in Category
    dirty_cat_indices = np.random.choice(df.index, size=int(0.04 * len(df)), replace=False)
    for idx in dirty_cat_indices:
        curr = df.loc[idx, "Category"]
        variations = [curr.upper(), curr.lower(), f"  {curr}  ", f"{curr.lower()} "]
        df.loc[idx, "Category"] = random.choice(variations)

    # 2. Whitespace and casing in Region
    dirty_reg_indices = np.random.choice(df.index, size=int(0.03 * len(df)), replace=False)
    for idx in dirty_reg_indices:
        curr = df.loc[idx, "Region"]
        variations = [f" {curr} ", curr.upper(), curr.lower()]
        df.loc[idx, "Region"] = random.choice(variations)

    # 3. Missing Sales Amount (Nulls, to be imputed via Quantity * Unit Price)
    missing_sales_indices = np.random.choice(df.index, size=int(0.03 * len(df)), replace=False)
    df.loc[missing_sales_indices, "Sales Amount"] = np.nan

    # 4. Inconsistent Sales Amount (mismatching Quantity * Unit Price due to data entry glitch)
    mismatch_indices = np.random.choice(df.index, size=8, replace=False)
    for idx in mismatch_indices:
        df.loc[idx, "Sales Amount"] = round(df.loc[idx, "Sales Amount"] * 0.90, 2)

    # 5. Missing Region (Nulls)
    missing_region_indices = np.random.choice(df.index, size=10, replace=False)
    df.loc[missing_region_indices, "Region"] = np.nan

    # 6. Inconsistent date formats (some dates as 'DD/MM/YYYY' or 'YYYY/MM/DD')
    date_format_indices = np.random.choice(df.index, size=int(0.05 * len(df)), replace=False)
    for idx in date_format_indices:
        d = datetime.strptime(str(df.loc[idx, "Order Date"]), "%Y-%m-%d")
        fmt = random.choice(["%d/%m/%Y", "%Y/%m/%d"])
        df.loc[idx, "Order Date"] = d.strftime(fmt)

    # 7. Exact duplicate rows (simulate duplicate sync / double-click submission)
    duplicate_indices = np.random.choice(df.index, size=15, replace=False)
    duplicate_rows = df.loc[duplicate_indices].copy()
    df = pd.concat([df, duplicate_rows], ignore_index=True)

    # 8. Negative or zero quantities/prices (anomalies to flag)
    anomaly_indices = np.random.choice(df.index, size=6, replace=False)
    df.loc[anomaly_indices[0], "Quantity"] = -1
    df.loc[anomaly_indices[1], "Quantity"] = 0
    df.loc[anomaly_indices[2], "Unit Price"] = -100.0
    df.loc[anomaly_indices[3], "Unit Price"] = 0.0

    # Ensure output directories exist
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    os.makedirs(os.path.dirname(output_excel_path), exist_ok=True)

    # Save CSV and Excel
    df.to_csv(output_csv_path, index=False)
    df.to_excel(output_excel_path, index=False, engine="openpyxl")

    print(f"[SUCCESS] Synthetic dataset generated:")
    print(f"  - Total raw rows: {len(df)}")
    print(f"  - Output CSV:   {output_csv_path}")
    print(f"  - Output Excel: {output_excel_path}")

    return df

if __name__ == "__main__":
    generate_retail_sales_dataset()

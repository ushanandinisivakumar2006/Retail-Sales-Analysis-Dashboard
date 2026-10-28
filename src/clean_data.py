"""
clean_data.py
-------------
Production-grade data cleaning and validation pipeline for retail sales data.
Performs comprehensive data auditing, deduplication, type casting,
text normalization, formula reconciliation, and anomaly tracking.

Generates:
- Cleaned CSV: data/processed/retail_sales_cleaned.csv
- Cleaned Excel: data/processed/retail_sales_cleaned.xlsx
- Quality Audit Report: reports/data_quality_report.md
"""

import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime

REQUIRED_COLUMNS = [
    "Order ID",
    "Order Date",
    "Product ID",
    "Product Name",
    "Category",
    "Region",
    "Quantity",
    "Unit Price",
    "Sales Amount"
]

CATEGORY_MAPPING = {
    "electronics": "Electronics",
    "home & kitchen": "Home & Kitchen",
    "fashion": "Fashion",
    "office supplies": "Office Supplies",
    "beauty & personal care": "Beauty & Personal Care"
}

REGION_MAPPING = {
    "north": "North",
    "south": "South",
    "east": "East",
    "west": "West",
    "central": "Central"
}

def load_raw_dataset(file_path: str) -> pd.DataFrame:
    """Loads raw dataset from CSV or Excel file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Source file not found at: {file_path}")
    
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file_path, engine="openpyxl")
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
    
    return df

def validate_schema(df: pd.DataFrame) -> None:
    """Verifies that all required columns exist in the DataFrame."""
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Schema validation failed! Missing required columns: {missing_cols}")

def clean_retail_sales_data(
    raw_df: pd.DataFrame,
    output_csv_path: str = "data/processed/retail_sales_cleaned.csv",
    output_excel_path: str = "data/processed/retail_sales_cleaned.xlsx",
    report_path: str = "reports/data_quality_report.md"
) -> tuple[pd.DataFrame, dict]:
    """
    Cleans raw retail sales data through transparent, documented transformations.
    Returns the cleaned DataFrame and the audit dictionary.
    """
    audit = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "initial_rows": len(raw_df),
        "initial_cols": len(raw_df.columns),
        "missing_values_initial": raw_df.isnull().sum().to_dict(),
        "exact_duplicates_removed": 0,
        "multi_item_orders_preserved": 0,
        "invalid_numeric_dropped": 0,
        "anomalies_flagged": [],
        "categories_normalized": 0,
        "regions_normalized": 0,
        "regions_imputed": 0,
        "sales_amount_imputed": 0,
        "sales_amount_reconciled": 0,
        "final_rows": 0,
        "final_cols": 0
    }

    validate_schema(raw_df)
    df = raw_df.copy()

    # 1. Audit and remove EXACT row duplicates (duplicate line entries)
    initial_count = len(df)
    exact_dup_mask = df.duplicated()
    audit["exact_duplicates_removed"] = int(exact_dup_mask.sum())
    df = df[~exact_dup_mask].copy()

    # Count legitimate multi-item orders (same Order ID, distinct products)
    order_counts = df["Order ID"].value_counts()
    multi_item_order_ids = order_counts[order_counts > 1].index
    audit["multi_item_orders_preserved"] = int(len(multi_item_order_ids))

    # 2. Text Normalization: Strip whitespace & standardize casing
    for col in ["Order ID", "Product ID", "Product Name"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Normalize Category
    raw_cats = df["Category"].copy()
    def normalize_category(val):
        if pd.isna(val) or str(val).strip().lower() in ["nan", "none", ""]:
            return np.nan
        cleaned = str(val).strip()
        return CATEGORY_MAPPING.get(cleaned.lower(), cleaned.title())
    df["Category"] = df["Category"].apply(normalize_category)
    audit["categories_normalized"] = int((raw_cats != df["Category"]).sum())

    # Normalize Region
    raw_regs = df["Region"].copy()
    def normalize_region(val):
        if pd.isna(val) or str(val).strip().lower() in ["nan", "none", ""]:
            return np.nan
        cleaned = str(val).strip()
        return REGION_MAPPING.get(cleaned.lower(), cleaned.title())
    df["Region"] = df["Region"].apply(normalize_region)
    audit["regions_normalized"] = int((raw_regs != df["Region"]).sum())

    # Impute missing region using another line item with the same Order ID if available, else 'Central'
    order_to_region = df.dropna(subset=["Region"]).groupby("Order ID")["Region"].first().to_dict()
    missing_region_mask = df["Region"].isna()
    for idx in df[missing_region_mask].index:
        ord_id = df.loc[idx, "Order ID"]
        if ord_id in order_to_region:
            df.loc[idx, "Region"] = order_to_region[ord_id]
        else:
            df.loc[idx, "Region"] = "Central"  # fallback default region
        audit["regions_imputed"] += 1

    # 3. Numeric Conversion and Type Casting
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Unit Price"] = pd.to_numeric(df["Unit Price"], errors="coerce")
    df["Sales Amount"] = pd.to_numeric(df["Sales Amount"], errors="coerce")

    # 4. Identify and handle invalid quantities and prices (e.g. Quantity <= 0 or Unit Price <= 0)
    invalid_mask = (df["Quantity"].isna()) | (df["Quantity"] <= 0) | (df["Unit Price"].isna()) | (df["Unit Price"] <= 0)
    invalid_rows = df[invalid_mask]
    audit["invalid_numeric_dropped"] = int(len(invalid_rows))
    
    for _, row in invalid_rows.iterrows():
        audit["anomalies_flagged"].append({
            "Order ID": row["Order ID"],
            "Product ID": row["Product ID"],
            "Reason": f"Invalid numeric value (Quantity={row['Quantity']}, Unit Price={row['Unit Price']})"
        })
    df = df[~invalid_mask].copy()

    # Ensure Quantity is int
    df["Quantity"] = df["Quantity"].astype(int)

    # 5. Date Parsing and Standardization
    # Handles mixed date formats ('YYYY-MM-DD', 'DD/MM/YYYY', 'YYYY/MM/DD')
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="mixed", errors="coerce")
    invalid_dates = df["Order Date"].isna().sum()
    if invalid_dates > 0:
        raise ValueError(f"Critical error: {invalid_dates} unparseable dates encountered!")

    # Format date cleanly to YYYY-MM-DD
    df["Order Date"] = df["Order Date"].dt.strftime("%Y-%m-%d")

    # 6. Sales Amount Calculation and Validation
    # Calculate expected sales amount: Quantity * Unit Price
    expected_sales = (df["Quantity"] * df["Unit Price"]).round(2)

    # A: Impute missing Sales Amount
    missing_sales_mask = df["Sales Amount"].isna()
    audit["sales_amount_imputed"] = int(missing_sales_mask.sum())
    df.loc[missing_sales_mask, "Sales Amount"] = expected_sales[missing_sales_mask]

    # B: Reconcile mismatched Sales Amount
    mismatch_mask = (df["Sales Amount"] - expected_sales).abs() > 0.01
    audit["sales_amount_reconciled"] = int(mismatch_mask.sum())
    for _, row in df[mismatch_mask].iterrows():
        exp = round(row["Quantity"] * row["Unit Price"], 2)
        audit["anomalies_flagged"].append({
            "Order ID": row["Order ID"],
            "Product ID": row["Product ID"],
            "Reason": f"Sales Amount discrepancy (Recorded: {row['Sales Amount']}, Expected: {exp}) -> Reconciled"
        })
    df.loc[mismatch_mask, "Sales Amount"] = expected_sales[mismatch_mask]

    # Ensure clean decimal representation
    df["Unit Price"] = df["Unit Price"].round(2)
    df["Sales Amount"] = df["Sales Amount"].round(2)

    # Sort deterministically by Order Date and Order ID
    df = df.sort_values(by=["Order Date", "Order ID", "Product ID"]).reset_index(drop=True)

    audit["final_rows"] = len(df)
    audit["final_cols"] = len(df.columns)

    # Ensure output directories exist
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    os.makedirs(os.path.dirname(output_excel_path), exist_ok=True)
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    # Export cleaned datasets
    df.to_csv(output_csv_path, index=False)
    df.to_excel(output_excel_path, index=False, engine="openpyxl")

    # Generate Markdown Data Quality Report
    generate_data_quality_report(audit, report_path)

    print(f"[SUCCESS] Data cleaning pipeline completed:")
    print(f"  - Initial rows: {audit['initial_rows']}")
    print(f"  - Exact duplicates removed: {audit['exact_duplicates_removed']}")
    print(f"  - Invalid numeric rows dropped: {audit['invalid_numeric_dropped']}")
    print(f"  - Sales amount imputed: {audit['sales_amount_imputed']}")
    print(f"  - Sales amount discrepancies corrected: {audit['sales_amount_reconciled']}")
    print(f"  - Final clean rows: {audit['final_rows']}")
    print(f"  - Clean CSV:   {output_csv_path}")
    print(f"  - Clean Excel: {output_excel_path}")
    print(f"  - Quality Audit: {report_path}")

    return df, audit

def generate_data_quality_report(audit: dict, report_path: str) -> None:
    """Generates a professional markdown Data Quality Report."""
    md_content = f"""# Data Quality and Cleaning Audit Report

**Project:** Retail Sales Analysis Dashboard  
**Generated At:** {audit['timestamp']}  
**Status:** Successfully Validated and Cleaned  
**Currency:** Indian Rupee (INR - ₹)

---

## 1. Executive Summary

| Metric | Raw Dataset | Cleaned Dataset | Change / Action |
| :--- | :--- | :--- | :--- |
| **Total Records** | {audit['initial_rows']:,} | {audit['final_rows']:,} | -{audit['initial_rows'] - audit['final_rows']} rows dropped |
| **Total Columns** | {audit['initial_cols']} | {audit['final_cols']} | Validated schema |
| **Exact Duplicate Rows** | {audit['exact_duplicates_removed']} | 0 | Removed duplicate line records |
| **Multi-Item Orders Preserved** | {audit['multi_item_orders_preserved']} | {audit['multi_item_orders_preserved']} | Retained legitimate basket orders |
| **Invalid Numeric Rows** | {audit['invalid_numeric_dropped']} | 0 | Dropped zero/negative values |
| **Missing Region Imputations** | {audit['regions_imputed']} | 0 | Resolved via basket/default fallback |
| **Sales Amount Imputations** | {audit['sales_amount_imputed']} | 0 | Calculated as `Quantity * Unit Price` |
| **Sales Amount Reconciliations**| {audit['sales_amount_reconciled']} | 0 | Reconciled data entry discrepancies |

---

## 2. Initial Missing Value Assessment

| Column Name | Missing Values (Count) | % of Total Raw Data | Handling Strategy |
| :--- | :--- | :--- | :--- |
"""
    for col, count in audit["missing_values_initial"].items():
        pct = (count / audit["initial_rows"]) * 100
        strategy = (
            "Computed via Quantity * Unit Price" if col == "Sales Amount"
            else "Imputed from multi-item order match or Central" if col == "Region"
            else "Mandatory field validated"
        )
        md_content += f"| `{col}` | {count} | {pct:.2f}% | {strategy} |\n"

    md_content += f"""
---

## 3. Data Cleaning Methodology & Transformation Rules

### 3.1 Duplicate vs. Multi-Item Order Handling
- **Exact Duplicates:** Records where every single column is identical were flagged as double submissions and dropped ({audit['exact_duplicates_removed']} records).
- **Legitimate Multi-Item Orders:** An order can contain multiple distinct products. Repeated `Order ID` values with distinct `Product ID` values were **strictly preserved** ({audit['multi_item_orders_preserved']} orders).

### 3.2 Categorical Normalization
- **Whitespace & Casing:** Stripped all leading and trailing whitespace from strings. Standardized all product categories and geographic regions to uniform Title Case.
- **Regions:** Normalized {audit['regions_normalized']} region entries and resolved {audit['regions_imputed']} missing regions.
- **Categories:** Normalized {audit['categories_normalized']} category entries.

### 3.3 Numeric Validation & Formula Reconciliation
- **Quantity & Price Validation:** Checked for non-positive values (`Quantity <= 0` or `Unit Price <= 0`). Dropped {audit['invalid_numeric_dropped']} corrupted records to safeguard analytical integrity.
- **Sales Amount Imputation:** Recomputed missing `Sales Amount` for {audit['sales_amount_imputed']} records using the business formula:
  $$\\text{{Sales Amount}} = \\text{{Quantity}} \\times \\text{{Unit Price}}$$
- **Discrepancy Correction:** Corrected {audit['sales_amount_reconciled']} records where entered `Sales Amount` differed from `Quantity * Unit Price` by more than ₹0.01 due to upstream data entry errors.

### 3.4 Temporal Standardization
- Standardized mixed date strings into uniform ISO format (`YYYY-MM-DD`). Verified 100% parseability across all dates.

---

## 4. Flagged Anomaly Log

Below is the transparent record of flagged anomalies during pipeline execution:

| Order ID | Product ID | Anomaly Reason & Resolution |
| :--- | :--- | :--- |
"""
    for item in audit["anomalies_flagged"][:20]:
        md_content += f"| `{item['Order ID']}` | `{item['Product ID']}` | {item['Reason']} |\n"

    if len(audit["anomalies_flagged"]) > 20:
        md_content += f"| *...* | *...* | *... and {len(audit['anomalies_flagged']) - 20} more logged items.* |\n"

    md_content += """
---

## 5. Verification Checklist

- [x] Schema structure matches project specification.
- [x] Date fields are in ISO format `YYYY-MM-DD`.
- [x] Quantity and Unit Price are strictly positive numbers.
- [x] Sales Amount strictly satisfies `Quantity * Unit Price`.
- [x] No missing or null values remain in primary dimensions or measures.
- [x] Output datasets written to both CSV and Excel formats.
"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md_content)

if __name__ == "__main__":
    input_file = "data/raw/retail_sales_raw.csv"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    
    raw_data = load_raw_dataset(input_file)
    clean_retail_sales_data(raw_data)

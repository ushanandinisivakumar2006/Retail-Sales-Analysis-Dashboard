"""
test_data_cleaning.py
---------------------
Unit tests for data cleaning logic:
- Sales amount calculations
- Missing value imputation and handling
- Exact duplicate removal
- Preservation of legitimate multi-item basket orders
- Removal of invalid negative/zero quantities and prices
- Normalization of category and region text
"""

import pytest
import numpy as np
import pandas as pd
from src.clean_data import clean_retail_sales_data, validate_schema

@pytest.fixture
def sample_raw_dataframe():
    """Provides a small, strictly controlled dataset with known anomalies."""
    data = [
        # Normal row 1
        {"Order ID": "ORD-101", "Order Date": "2025-01-10", "Product ID": "P1", "Product Name": "Widget A", "Category": "Electronics", "Region": "North", "Quantity": 2, "Unit Price": 500.0, "Sales Amount": 1000.0},
        # Multi-item basket item for same order (should be PRESERVED)
        {"Order ID": "ORD-101", "Order Date": "2025-01-10", "Product ID": "P2", "Product Name": "Gadget B", "Category": "  electronics  ", "Region": "north ", "Quantity": 1, "Unit Price": 1500.0, "Sales Amount": 1500.0},
        # Exact duplicate of row 1 (should be DROPPED)
        {"Order ID": "ORD-101", "Order Date": "2025-01-10", "Product ID": "P1", "Product Name": "Widget A", "Category": "Electronics", "Region": "North", "Quantity": 2, "Unit Price": 500.0, "Sales Amount": 1000.0},
        # Row with missing Sales Amount (should be IMPUTED as 3 * 200 = 600.0)
        {"Order ID": "ORD-102", "Order Date": "2025-01-15", "Product ID": "P3", "Product Name": "Item C", "Category": "home & kitchen", "Region": "South", "Quantity": 3, "Unit Price": 200.0, "Sales Amount": np.nan},
        # Row with mismatched Sales Amount (Recorded 800 instead of 4 * 250 = 1000, should be RECONCILED)
        {"Order ID": "ORD-103", "Order Date": "2025-02-01", "Product ID": "P4", "Product Name": "Item D", "Category": "Fashion", "Region": "West", "Quantity": 4, "Unit Price": 250.0, "Sales Amount": 800.0},
        # Row with invalid negative quantity (should be DROPPED)
        {"Order ID": "ORD-104", "Order Date": "2025-02-05", "Product ID": "P1", "Product Name": "Widget A", "Category": "Electronics", "Region": "East", "Quantity": -2, "Unit Price": 500.0, "Sales Amount": -1000.0},
        # Row with zero unit price (should be DROPPED)
        {"Order ID": "ORD-105", "Order Date": "2025-02-10", "Product ID": "P5", "Product Name": "Item E", "Category": "Office Supplies", "Region": "Central", "Quantity": 5, "Unit Price": 0.0, "Sales Amount": 0.0},
        # Row with missing Region (should be IMPUTED)
        {"Order ID": "ORD-106", "Order Date": "2025-03-01", "Product ID": "P2", "Product Name": "Gadget B", "Category": "Electronics", "Region": np.nan, "Quantity": 1, "Unit Price": 1500.0, "Sales Amount": 1500.0},
    ]
    return pd.DataFrame(data)

def test_schema_validation_success(sample_raw_dataframe):
    """Verifies schema validation succeeds when all required columns are present."""
    validate_schema(sample_raw_dataframe)

def test_schema_validation_failure():
    """Verifies schema validation raises ValueError when required column is missing."""
    invalid_df = pd.DataFrame({"Order ID": ["ORD-1"], "Quantity": [1]})
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_schema(invalid_df)

def test_exact_duplicate_detection(sample_raw_dataframe, tmp_path):
    """Verifies exact duplicate rows are detected and removed."""
    csv_out = str(tmp_path / "clean.csv")
    excel_out = str(tmp_path / "clean.xlsx")
    report_out = str(tmp_path / "report.md")

    clean_df, audit = clean_retail_sales_data(
        sample_raw_dataframe,
        output_csv_path=csv_out,
        output_excel_path=excel_out,
        report_path=report_out
    )
    assert audit["exact_duplicates_removed"] == 1

def test_multi_item_order_preservation(sample_raw_dataframe, tmp_path):
    """Verifies legitimate multi-item basket orders sharing an Order ID are preserved."""
    csv_out = str(tmp_path / "clean.csv")
    excel_out = str(tmp_path / "clean.xlsx")
    report_out = str(tmp_path / "report.md")

    clean_df, _ = clean_retail_sales_data(
        sample_raw_dataframe,
        output_csv_path=csv_out,
        output_excel_path=excel_out,
        report_path=report_out
    )
    ord_101_rows = clean_df[clean_df["Order ID"] == "ORD-101"]
    assert len(ord_101_rows) == 2
    assert set(ord_101_rows["Product ID"]) == {"P1", "P2"}

def test_missing_sales_amount_calculation(sample_raw_dataframe, tmp_path):
    """Verifies missing Sales Amount is accurately computed as Quantity * Unit Price."""
    csv_out = str(tmp_path / "clean.csv")
    excel_out = str(tmp_path / "clean.xlsx")
    report_out = str(tmp_path / "report.md")

    clean_df, audit = clean_retail_sales_data(
        sample_raw_dataframe,
        output_csv_path=csv_out,
        output_excel_path=excel_out,
        report_path=report_out
    )
    row_102 = clean_df[clean_df["Order ID"] == "ORD-102"].iloc[0]
    assert row_102["Sales Amount"] == 600.0  # 3 * 200.0
    assert audit["sales_amount_imputed"] == 1

def test_sales_amount_reconciliation(sample_raw_dataframe, tmp_path):
    """Verifies inconsistent Sales Amount is corrected to Quantity * Unit Price."""
    csv_out = str(tmp_path / "clean.csv")
    excel_out = str(tmp_path / "clean.xlsx")
    report_out = str(tmp_path / "report.md")

    clean_df, audit = clean_retail_sales_data(
        sample_raw_dataframe,
        output_csv_path=csv_out,
        output_excel_path=excel_out,
        report_path=report_out
    )
    row_103 = clean_df[clean_df["Order ID"] == "ORD-103"].iloc[0]
    assert row_103["Sales Amount"] == 1000.0  # 4 * 250.0
    assert audit["sales_amount_reconciled"] == 1

def test_invalid_numeric_filtering(sample_raw_dataframe, tmp_path):
    """Verifies non-positive quantities and prices are dropped from valid sales."""
    csv_out = str(tmp_path / "clean.csv")
    excel_out = str(tmp_path / "clean.xlsx")
    report_out = str(tmp_path / "report.md")

    clean_df, audit = clean_retail_sales_data(
        sample_raw_dataframe,
        output_csv_path=csv_out,
        output_excel_path=excel_out,
        report_path=report_out
    )
    assert audit["invalid_numeric_dropped"] == 2
    assert "ORD-104" not in clean_df["Order ID"].values
    assert "ORD-105" not in clean_df["Order ID"].values

def test_text_normalization(sample_raw_dataframe, tmp_path):
    """Verifies categories and regions are stripped and normalized to Title Case."""
    csv_out = str(tmp_path / "clean.csv")
    excel_out = str(tmp_path / "clean.xlsx")
    report_out = str(tmp_path / "report.md")

    clean_df, _ = clean_retail_sales_data(
        sample_raw_dataframe,
        output_csv_path=csv_out,
        output_excel_path=excel_out,
        report_path=report_out
    )
    categories = clean_df["Category"].tolist()
    regions = clean_df["Region"].tolist()

    assert "Electronics" in categories
    assert "Home & Kitchen" in categories
    assert all(r in ["North", "South", "East", "West", "Central"] for r in regions)

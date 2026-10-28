"""
test_sales_metrics.py
---------------------
Unit tests for sales business metrics using a small, deterministic,
known test dataset with manually precomputed ground-truth values.
"""

import pytest
import pandas as pd
from src.analyze_sales import calculate_metrics

@pytest.fixture
def benchmark_sales_df():
    """
    Creates a small, known dataset:
    Order 1: Jan 15, 2025 -> Prod A (Qty: 2, Price: 1000.0 => 2000.0) | North | Electronics
    Order 1: Jan 15, 2025 -> Prod B (Qty: 1, Price: 500.0  => 500.0)  | North | Electronics
    Order 2: Jan 20, 2025 -> Prod C (Qty: 3, Price: 200.0  => 600.0)  | South | Home & Kitchen
    Order 3: Feb 10, 2025 -> Prod A (Qty: 1, Price: 1000.0 => 1000.0) | West  | Electronics
    Order 4: Feb 15, 2025 -> Prod D (Qty: 4, Price: 100.0  => 400.0)  | North | Office Supplies
    Order 5: Feb 20, 2025 -> Prod E (Qty: 5, Price: 50.0   => 250.0)  | East  | Fashion
    Order 6: Mar 05, 2025 -> Prod F (Qty: 2, Price: 300.0  => 600.0)  | South | Fashion

    Summary Ground Truths:
    - Total Revenue = 2000 + 500 + 600 + 1000 + 400 + 250 + 600 = 5350.0
    - Total Orders = 6 (ORD-01, ORD-02, ORD-03, ORD-04, ORD-05, ORD-06)
    - Average Order Value (AOV) = 5350.0 / 6 = 891.67
    - Total Quantity = 2 + 1 + 3 + 1 + 4 + 5 + 2 = 18
    - Unique Products = 6 (Prod A, B, C, D, E, F)
    - Product Revenue:
        Prod A: 3000.0 (Qty: 3)
        Prod B: 500.0 (Qty: 1)
        Prod C: 600.0 (Qty: 3)
        Prod D: 400.0 (Qty: 4)
        Prod E: 250.0 (Qty: 5)
        Prod F: 600.0 (Qty: 2)
      Rank by Revenue:
        1: Prod A (3000.0)
        2: Prod C (600.0)
        3: Prod F (600.0)
        4: Prod B (500.0)
        5: Prod D (400.0)
      Rank by Quantity:
        1: Prod E (5)
        2: Prod D (4)
        3: Prod A (3)
        4: Prod C (3)
        5: Prod F (2)
    - Monthly Revenue:
        2025-01: 3100.0
        2025-02: 1650.0 (MoM Change = -1450.0, MoM Pct = -46.77%)
        2025-03: 600.0  (MoM Change = -1050.0, MoM Pct = -63.64%)
    """
    data = [
        {"Order ID": "ORD-01", "Order Date": "2025-01-15", "Product ID": "P-A", "Product Name": "Prod A", "Category": "Electronics", "Region": "North", "Quantity": 2, "Unit Price": 1000.0, "Sales Amount": 2000.0},
        {"Order ID": "ORD-01", "Order Date": "2025-01-15", "Product ID": "P-B", "Product Name": "Prod B", "Category": "Electronics", "Region": "North", "Quantity": 1, "Unit Price": 500.0,  "Sales Amount": 500.0},
        {"Order ID": "ORD-02", "Order Date": "2025-01-20", "Product ID": "P-C", "Product Name": "Prod C", "Category": "Home & Kitchen", "Region": "South", "Quantity": 3, "Unit Price": 200.0,  "Sales Amount": 600.0},
        {"Order ID": "ORD-03", "Order Date": "2025-02-10", "Product ID": "P-A", "Product Name": "Prod A", "Category": "Electronics", "Region": "West", "Quantity": 1, "Unit Price": 1000.0, "Sales Amount": 1000.0},
        {"Order ID": "ORD-04", "Order Date": "2025-02-15", "Product ID": "P-D", "Product Name": "Prod D", "Category": "Office Supplies", "Region": "North", "Quantity": 4, "Unit Price": 100.0,  "Sales Amount": 400.0},
        {"Order ID": "ORD-05", "Order Date": "2025-02-20", "Product ID": "P-E", "Product Name": "Prod E", "Category": "Fashion", "Region": "East", "Quantity": 5, "Unit Price": 50.0,   "Sales Amount": 250.0},
        {"Order ID": "ORD-06", "Order Date": "2025-03-05", "Product ID": "P-F", "Product Name": "Prod F", "Category": "Fashion", "Region": "South", "Quantity": 2, "Unit Price": 300.0,  "Sales Amount": 600.0},
    ]
    return pd.DataFrame(data)

def test_total_sales_revenue(benchmark_sales_df):
    metrics = calculate_metrics(benchmark_sales_df)
    assert metrics["total_revenue"] == 5350.0

def test_unique_order_count(benchmark_sales_df):
    metrics = calculate_metrics(benchmark_sales_df)
    assert metrics["unique_orders"] == 6

def test_average_order_value(benchmark_sales_df):
    metrics = calculate_metrics(benchmark_sales_df)
    # 5350.0 / 6 = 891.666... -> 891.67
    assert metrics["average_order_value"] == 891.67

def test_total_quantity_sold(benchmark_sales_df):
    metrics = calculate_metrics(benchmark_sales_df)
    assert metrics["total_quantity"] == 18

def test_unique_products_count(benchmark_sales_df):
    metrics = calculate_metrics(benchmark_sales_df)
    assert metrics["unique_products"] == 6

def test_top_five_revenue_ranking(benchmark_sales_df):
    metrics = calculate_metrics(benchmark_sales_df)
    top_5 = metrics["top_5_revenue"]
    assert len(top_5) == 5
    assert top_5.iloc[0]["Product Name"] == "Prod A"
    assert top_5.iloc[0]["revenue"] == 3000.0
    assert metrics["highest_revenue_product"]["name"] == "Prod A"

def test_top_five_quantity_ranking(benchmark_sales_df):
    metrics = calculate_metrics(benchmark_sales_df)
    top_5_qty = metrics["top_5_quantity"]
    assert len(top_5_qty) == 5
    assert top_5_qty.iloc[0]["Product Name"] == "Prod E"
    assert top_5_qty.iloc[0]["quantity"] == 5

def test_monthly_revenue_and_mom(benchmark_sales_df):
    metrics = calculate_metrics(benchmark_sales_df)
    monthly_df = metrics["monthly_summary"]
    assert len(monthly_df) == 3
    
    jan_row = monthly_df[monthly_df["Year_Month"] == "2025-01"].iloc[0]
    assert jan_row["monthly_revenue"] == 3100.0

    feb_row = monthly_df[monthly_df["Year_Month"] == "2025-02"].iloc[0]
    assert feb_row["monthly_revenue"] == 1650.0
    assert feb_row["mom_change_amt"] == -1450.0
    assert round(feb_row["mom_change_pct"], 2) == -46.77

    mar_row = monthly_df[monthly_df["Year_Month"] == "2025-03"].iloc[0]
    assert mar_row["monthly_revenue"] == 600.0
    assert mar_row["mom_change_amt"] == -1050.0
    assert round(mar_row["mom_change_pct"], 2) == -63.64

def test_best_and_worst_months(benchmark_sales_df):
    metrics = calculate_metrics(benchmark_sales_df)
    assert metrics["best_month"]["year_month"] == "2025-01"
    assert metrics["best_month"]["revenue"] == 3100.0
    assert metrics["worst_month"]["year_month"] == "2025-03"
    assert metrics["worst_month"]["revenue"] == 600.0

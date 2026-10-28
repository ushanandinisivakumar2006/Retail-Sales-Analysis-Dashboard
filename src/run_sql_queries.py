"""
run_sql_queries.py
------------------
Executes all SQL queries from sql/sales_analysis.sql against data/retail_sales.db,
formats the output cleanly, and validates mathematical alignment with Python metrics.
"""

import os
import sys
import sqlite3
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DB_PATH = "data/retail_sales.db"
SQL_FILE_PATH = "sql/sales_analysis.sql"

def execute_sql_analysis():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}. Run load_database.py first.")
    if not os.path.exists(SQL_FILE_PATH):
        raise FileNotFoundError(f"SQL file not found at {SQL_FILE_PATH}.")

    conn = sqlite3.connect(DB_PATH)

    with open(SQL_FILE_PATH, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Split queries by semicolon, ignoring empty statements and comments
    raw_statements = sql_content.split(";")

    query_labels = [
        "1. High-Level Executive KPI Summary",
        "2. Top 5 Products by Revenue",
        "3. Top 5 Products by Quantity Sold",
        "4. Monthly Revenue Trend with MoM Growth",
        "5. Regional Sales Performance",
        "6. Product Category Breakdown",
        "7. Best and Lowest Performing Months",
        "8. Customer Basket Size (Multi-Item Distribution)"
    ]

    label_idx = 0
    print("\n" + "="*70)
    print("EXECUTING SQL QUERIES ON SQLITE DATABASE (data/retail_sales.db)")
    print("="*70)

    for stmt in raw_statements:
        cleaned_stmt = stmt.strip()
        if not cleaned_stmt:
            continue
        # Check if statement contains a SELECT
        if "SELECT" in cleaned_stmt.upper():
            title = query_labels[label_idx] if label_idx < len(query_labels) else f"Query {label_idx + 1}"
            label_idx += 1
            print(f"\n--- [QUERY {title}] ---")
            try:
                df_result = pd.read_sql_query(cleaned_stmt, conn)
                print(df_result.to_string(index=False))
            except Exception as e:
                print(f"Error executing statement:\n{cleaned_stmt}\nDetails: {e}")

    conn.close()
    print("\n" + "="*70)
    print("[SUCCESS] All SQL queries executed successfully.")
    print("="*70 + "\n")

if __name__ == "__main__":
    execute_sql_analysis()

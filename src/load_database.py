"""
load_database.py
----------------
Loads the cleaned retail sales dataset into an embedded SQLite database (data/retail_sales.db)
with optimized schema design, indexes, and execution validation.
"""

import os
import sqlite3
import pandas as pd

DB_PATH = "data/retail_sales.db"
CSV_PATH = "data/processed/retail_sales_cleaned.csv"

def create_and_load_database(
    csv_path: str = CSV_PATH,
    db_path: str = DB_PATH
) -> sqlite3.Connection:
    """Creates SQLite schema and populates it with cleaned sales records."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Cleaned CSV not found at: {csv_path}")

    # Ensure target directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Read cleaned data
    df = pd.read_csv(csv_path)

    # Rename columns to standard SQL snake_case identifiers
    df_sql = df.rename(columns={
        "Order ID": "order_id",
        "Order Date": "order_date",
        "Product ID": "product_id",
        "Product Name": "product_name",
        "Category": "category",
        "Region": "region",
        "Quantity": "quantity",
        "Unit Price": "unit_price",
        "Sales Amount": "sales_amount"
    })

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table with explicit data types and primary composite constraints
    cursor.execute("DROP TABLE IF EXISTS sales;")
    cursor.execute("""
    CREATE TABLE sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT NOT NULL,
        order_date TEXT NOT NULL,
        product_id TEXT NOT NULL,
        product_name TEXT NOT NULL,
        category TEXT NOT NULL,
        region TEXT NOT NULL,
        quantity INTEGER NOT NULL CHECK(quantity > 0),
        unit_price REAL NOT NULL CHECK(unit_price > 0),
        sales_amount REAL NOT NULL CHECK(sales_amount > 0)
    );
    """)

    # Populate table
    df_sql.to_sql("sales", conn, if_exists="append", index=False)

    # Create indexes for high-frequency analytical queries
    cursor.execute("CREATE INDEX idx_sales_order_date ON sales(order_date);")
    cursor.execute("CREATE INDEX idx_sales_category ON sales(category);")
    cursor.execute("CREATE INDEX idx_sales_region ON sales(region);")
    cursor.execute("CREATE INDEX idx_sales_product_id ON sales(product_id);")

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM sales;")
    count = cursor.fetchone()[0]

    print(f"[SUCCESS] SQLite database successfully populated at: {db_path}")
    print(f"  - Table 'sales' created with {count} rows.")

    return conn

if __name__ == "__main__":
    conn = create_and_load_database()
    conn.close()

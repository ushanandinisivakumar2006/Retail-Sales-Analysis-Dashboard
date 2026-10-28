# Excel Retail Sales Analysis Guide

**Project Name:** Retail Sales Analysis Dashboard  
**Cleaned Dataset:** `data/processed/retail_sales_cleaned.xlsx` (or `.csv`)  
**Currency:** Indian Rupee (INR - ₹)  
**Target Audience:** Entry-Level Data Analysts / Financial & Business Modeling

---

## 1. Introduction

Microsoft Excel remains one of the most widely used tools in business analytics. This guide explains how to perform end-to-end data inspection, formula auditing, PivotTable modeling, and visual reporting using Excel, and how to verify calculations against Python and SQL outputs.

---

## 2. Opening and Inspecting the Dataset

1. Open `data/processed/retail_sales_cleaned.xlsx` in Excel.
2. Convert the data range to an **Excel Table**:
   - Click any cell within the data table (`A1:I1497`).
   - Press **Ctrl + T** (or go to **Insert** -> **Table**).
   - Ensure "My table has headers" is checked and click **OK**.
   - In the **Table Design** tab, rename the table to **`SalesTable`**.
3. **Inspect Column Headers and Types:**
   - Column A: `Order ID` (Text)
   - Column B: `Order Date` (Short Date `YYYY-MM-DD`)
   - Column C: `Product ID` (Text)
   - Column D: `Product Name` (Text)
   - Column E: `Category` (Text)
   - Column F: `Region` (Text)
   - Column G: `Quantity` (Number, integer)
   - Column H: `Unit Price` (Currency, `₹ #,##0.00`)
   - Column I: `Sales Amount` (Currency, `₹ #,##0.00`)

---

## 3. Core Excel Formulas & Reconciliation

To audit calculations directly in Excel:

### 3.1 Line Item Sales Amount Verification
Insert a test column in Column J named `Calculated_Sales`:
```excel
=[@Quantity] * [@[Unit Price]]
```
Add a verification formula in Column K named `Audit_Check`:
```excel
=IF(ROUND([@[Sales Amount]], 2) = ROUND([@Calculated_Sales], 2), "MATCH", "DISCREPANCY")
```
*Expected Result:* All 1,496 rows return `"MATCH"`.

### 3.2 High-Level Summary Formulas
In a separate summary sheet named `Executive_KPIs`, build these formulas:

| Metric | Excel Formula | Expected Output |
| :--- | :--- | :--- |
| **Total Sales Revenue** | `=SUM(SalesTable[Sales Amount])` | **₹6,406,050.00** |
| **Total Units Sold** | `=SUM(SalesTable[Quantity])` | **2,750** |
| **Total Order Rows** | `=COUNTA(SalesTable[Order ID])` | **1,496** |
| **Total Unique Orders** | `=COUNTA(UNIQUE(SalesTable[Order ID]))` | **945** |
| **Average Order Value (AOV)** | `=SUM(SalesTable[Sales Amount]) / COUNTA(UNIQUE(SalesTable[Order ID]))` | **₹6,778.89** |
| **Unique Products Count** | `=COUNTA(UNIQUE(SalesTable[Product ID]))` | **29** |

---

## 4. PivotTable Analysis Step-by-Step

### 4.1 PivotTable 1: Monthly Sales Trend
1. Click inside `SalesTable` -> Go to **Insert** -> **PivotTable**.
2. Select **New Worksheet**, name the sheet `Monthly_Analysis`.
3. In PivotTable Fields:
   - Drag `Order Date` to **Rows** (Excel will group into Years, Quarters, Months).
   - Drag `Sales Amount` to **Values** -> Summarize by **Sum** -> Format as Currency `₹ #,##0`.
   - Drag `Order ID` to **Values** -> Summarize by **Count** (or Distinct Count if Excel Data Model is enabled).
4. Add Month-over-Month calculation:
   - Drag `Sales Amount` to **Values** a second time.
   - Right-click the second column -> **Show Values As** -> **% Difference From...** -> Base field: `Order Date` -> Base item: `(previous)`.

*Verification:*
- Peak Month: **October 2025** (`₹759,650.00`)
- Lowest Month: **February 2025** (`₹237,934.00`)

---

### 4.2 PivotTable 2: Regional Sales Breakdown
1. In a new worksheet named `Regional_Analysis`, insert a PivotTable from `SalesTable`.
2. Fields:
   - Rows: `Region`
   - Values:
     * `Sum of Sales Amount` (Currency)
     * `Count of Order ID`
     * `Sum of Quantity`
     * `% of Column Total` (Show Values As -> `% of Column Total`)
3. Sort: Right-click any revenue value -> **Sort** -> **Sort Largest to Smallest**.

*Expected Breakdown:*
- North: ₹1,748,871.00 (27.30%)
- South: ₹1,376,303.00 (21.48%)
- West: ₹1,358,353.00 (21.20%)
- East: ₹1,161,092.00 (18.12%)
- Central: ₹761,431.00 (11.89%)

---

### 4.3 PivotTable 3: Category Performance
1. In a new worksheet named `Category_Analysis`, insert a PivotTable.
2. Fields:
   - Rows: `Category`
   - Values: `Sum of Sales Amount`, `Sum of Quantity`, `% of Column Total`
3. Sort Largest to Smallest.

*Expected Ranking:*
1. Electronics: ₹2,656,792.00 (41.47%)
2. Home & Kitchen: ₹1,229,368.00 (19.19%)
3. Office Supplies: ₹1,138,054.00 (17.77%)
4. Fashion: ₹796,696.00 (12.44%)
5. Beauty & Personal Care: ₹585,140.00 (9.13%)

---

### 4.4 PivotTable 4: Top 5 Products by Revenue
1. Fields:
   - Rows: `Product Name`
   - Values: `Sum of Sales Amount`
2. In the Row Labels dropdown, click **Value Filters** -> **Top 10...** -> Set to **Top 5** by `Sum of Sales Amount`.

*Expected Top 5 Products:*
1. Ergonomic High-Back Mesh Chair (₹809,910.00)
2. 1TB High-Speed External SSD (₹809,892.00)
3. Noise Cancelling Headphones (₹557,907.00)
4. Digital Air Fryer 4.5L (₹499,698.00)
5. Breathable Mesh Running Shoes (₹313,488.00)

---

## 5. Adding Slicers for Interactive Dashboarding

1. Select any PivotTable.
2. Navigate to **PivotTable Analyze** ribbon -> **Insert Slicer**.
3. Select **Region**, **Category**, and **Order Date**.
4. Right-click each slicer -> **Report Connections...** -> Check all PivotTables on all sheets.
5. Now, clicking any region (e.g., "North") instantly updates all PivotTables across the entire workbook.

---

## 6. Reconciliation Matrix: Excel vs. Python vs. SQL

| Business Metric | Excel Result | Python (`analyze_sales.py`) | SQL (`sales_analysis.sql`) | Status |
| :--- | :--- | :--- | :--- | :--- |
| Total Revenue | ₹6,406,050.00 | ₹6,406,050.00 | 6406050.00 | **100% Match** |
| Unique Orders | 945 | 945 | 945 | **100% Match** |
| Average Order Value | ₹6,778.89 | ₹6,778.89 | 6778.89 | **100% Match** |
| Total Units Sold | 2,750 | 2,750 | 2750 | **100% Match** |
| Unique Products | 29 | 29 | 29 | **100% Match** |
| Top Product Revenue | ₹809,910.00 | ₹809,910.00 | 809910.00 | **100% Match** |

# Power BI DAX Measures Reference Library

**Project:** Retail Sales Analysis Dashboard  
**Currency:** Indian Rupee (INR - ₹)  
**Model Table:** `Fact_Sales` (from `retail_sales_cleaned.csv`)  
**Calendar Table:** `Dim_Date`  
**Measures Table:** `_Measures` (Dedicated measure group table)

---

## 1. Calendar / Date Dimension DAX Table

To enable accurate time intelligence and chronological month sorting, create a dedicated Date table in Power BI:

```dax
Dim_Date = 
VAR MinDate = MIN('Fact_Sales'[Order Date])
VAR MaxDate = MAX('Fact_Sales'[Order Date])
RETURN
ADDCOLUMNS(
    CALENDAR(MinDate, MaxDate),
    "Year", YEAR([Date]),
    "Month Number", MONTH([Date]),
    "Month Name", FORMAT([Date], "mmm"),
    "Month Full Name", FORMAT([Date], "mmmm"),
    "Year Month", FORMAT([Date], "yyyy-mm"),
    "Month Year Display", FORMAT([Date], "mmm yyyy"),
    "MonthSort", YEAR([Date]) * 100 + MONTH([Date]),
    "Quarter", "Q" & FORMAT([Date], "q"),
    "Day of Week", FORMAT([Date], "dddd")
)
```

> [!IMPORTANT]
> **Sort Column Rule:** Select `Month Year Display` (or `Month Name`), go to the **Column Tools** ribbon tab, click **Sort by Column**, and select **`MonthSort`**. This prevents alphabetical sorting (e.g., April before January).

---

## 2. Core Business KPI Measures

Create these measures inside your `_Measures` table.

### 2.1 Total Sales Revenue (₹)
Calculates the total monetary value of all completed sales.

```dax
Total Sales = 
SUM('Fact_Sales'[Sales Amount])
```
* **Format:** Currency -> Custom format: `₹ #,##0` or `₹ #,##,##0`
* **Description:** Primary top-line revenue metric.

---

### 2.2 Total Unique Orders
Counts the number of distinct customer checkout transactions. Preserves multi-item order integrity.

```dax
Total Orders = 
DISTINCTCOUNT('Fact_Sales'[Order ID])
```
* **Format:** Whole Number -> `#,##0`
* **Description:** Number of unique order IDs.

---

### 2.3 Total Quantity Sold
Aggregates total physical units sold.

```dax
Total Quantity Sold = 
SUM('Fact_Sales'[Quantity])
```
* **Format:** Whole Number -> `#,##0`
* **Description:** Cumulative volume of units shipped.

---

### 2.4 Average Order Value (AOV)
Measures the average revenue generated per unique order.

```dax
Average Order Value = 
DIVIDE([Total Sales], [Total Orders], 0)
```
* **Format:** Currency -> Custom format: `₹ #,##0.00`
* **Description:** Total sales divided by distinct orders, using safe division with `0` fallback.

---

### 2.5 Active Product Count
Counts unique products sold within the filtered context.

```dax
Active Products = 
DISTINCTCOUNT('Fact_Sales'[Product ID])
```
* **Format:** Whole Number

---

## 3. Time Intelligence & Trend Measures

### 3.1 Previous Month Sales
Calculates sales revenue for the preceding calendar month.

```dax
Previous Month Sales = 
CALCULATE(
    [Total Sales],
    PREVIOUSMONTH('Dim_Date'[Date])
)
```
* **Format:** Currency (`₹ #,##0`)

---

### 3.2 Month-over-Month (MoM) Revenue Change (Amount)
Computes the net variance between the current month and the previous month.

```dax
MoM Sales Change = 
VAR CurrentSales = [Total Sales]
VAR PrevSales = [Previous Month Sales]
RETURN
IF(
    ISBLANK(PrevSales),
    BLANK(),
    CurrentSales - PrevSales
)
```
* **Format:** Currency (`+₹ #,##0;-₹ #,##0;₹ 0`)

---

### 3.3 Month-over-Month (MoM) Sales Growth Percentage
Percentage growth or contraction compared to the previous month.

```dax
MoM Sales Growth % = 
VAR CurrentSales = [Total Sales]
VAR PrevSales = [Previous Month Sales]
RETURN
DIVIDE(CurrentSales - PrevSales, PrevSales, BLANK())
```
* **Format:** Percentage (`+0.00%;-0.00%;0.00%`)

---

## 4. Ranking & Contribution Measures

### 4.1 Product Revenue Rank
Ranks products dynamically according to revenue within the filtered context.

```dax
Product Revenue Rank = 
RANKX(
    ALLSELECTED('Fact_Sales'[Product Name]),
    [Total Sales],
    ,
    DESC,
    Dense
)
```

---

### 4.2 Revenue Contribution Percentage (% of Total)
Calculates the proportion of total sales attributed to a selected region or category.

```dax
% Revenue Contribution = 
DIVIDE(
    [Total Sales],
    CALCULATE([Total Sales], ALLSELECTED('Fact_Sales')),
    0
)
```
* **Format:** Percentage (`0.0%`)

---

### 4.3 Average Items per Order (Basket Size)
Measures average line items attached to each transaction.

```dax
Average Items Per Order = 
DIVIDE([Total Quantity Sold], [Total Orders], 0)
```
* **Format:** Decimal Number (`0.0`)

---

## 5. Verification Checklist in Power BI

When verified against the benchmark cleaned dataset:
- `Total Sales` must equal **₹6,406,050.00**
- `Total Orders` must equal **945**
- `Average Order Value` must equal **₹6,778.89**
- `Total Quantity Sold` must equal **2,750**

-- ==============================================================================
-- Retail Sales Analysis - SQL Business Intelligence Queries
-- Database: SQLite 3 / ANSI SQL Compatible
-- Table: sales (order_id, order_date, product_id, product_name, category, 
--               region, quantity, unit_price, sales_amount)
-- Currency: Indian Rupee (INR - ₹)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. High-Level Executive KPI Summary
-- Calculates:
--   - Total Sales Revenue (₹)
--   - Distinct Order Count
--   - Total Quantity Sold
--   - Distinct Products Sold
--   - Average Order Value (AOV = Total Sales / Unique Orders)
-- ------------------------------------------------------------------------------
SELECT 
    ROUND(SUM(sales_amount), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_unique_orders,
    SUM(quantity) AS total_quantity_sold,
    COUNT(DISTINCT product_id) AS total_unique_products,
    ROUND(SUM(sales_amount) * 1.0 / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM sales;


-- ------------------------------------------------------------------------------
-- 2. Top 5 Products by Revenue
-- Ranks products by total sales generated and displays units sold and % revenue share.
-- ------------------------------------------------------------------------------
WITH total_sales_cte AS (
    SELECT SUM(sales_amount) AS grand_total FROM sales
)
SELECT 
    s.product_id,
    s.product_name,
    s.category,
    SUM(s.quantity) AS units_sold,
    ROUND(SUM(s.sales_amount), 2) AS total_revenue,
    ROUND((SUM(s.sales_amount) * 100.0) / (SELECT grand_total FROM total_sales_cte), 2) AS revenue_share_pct
FROM sales s
GROUP BY s.product_id, s.product_name, s.category
ORDER BY total_revenue DESC
LIMIT 5;


-- ------------------------------------------------------------------------------
-- 3. Top 5 Products by Quantity Sold
-- Identifies best-selling volume drivers.
-- ------------------------------------------------------------------------------
SELECT 
    product_id,
    product_name,
    category,
    SUM(quantity) AS total_quantity_sold,
    ROUND(SUM(sales_amount), 2) AS total_revenue
FROM sales
GROUP BY product_id, product_name, category
ORDER BY total_quantity_sold DESC
LIMIT 5;


-- ------------------------------------------------------------------------------
-- 4. Monthly Revenue Trend with Month-over-Month (MoM) Growth
-- Uses SQLite strftime to aggregate year-month and window function LAG()
-- to compute previous month revenue, absolute difference, and percentage growth.
-- ------------------------------------------------------------------------------
WITH monthly_sales AS (
    SELECT 
        strftime('%Y-%m', order_date) AS year_month,
        COUNT(DISTINCT order_id) AS monthly_orders,
        SUM(quantity) AS monthly_quantity,
        ROUND(SUM(sales_amount), 2) AS monthly_revenue
    FROM sales
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT 
    year_month,
    monthly_orders,
    monthly_quantity,
    monthly_revenue,
    LAG(monthly_revenue, 1) OVER (ORDER BY year_month) AS prev_month_revenue,
    ROUND(monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year_month), 2) AS mom_revenue_change,
    ROUND(
        (monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year_month)) * 100.0 / 
        LAG(monthly_revenue, 1) OVER (ORDER BY year_month), 
        2
    ) AS mom_growth_pct
FROM monthly_sales
ORDER BY year_month ASC;


-- ------------------------------------------------------------------------------
-- 5. Regional Sales Performance and Order Volume
-- Aggregates revenue, distinct orders, units sold, and average order value per region.
-- ------------------------------------------------------------------------------
WITH grand_total_cte AS (
    SELECT SUM(sales_amount) AS grand_total FROM sales
)
SELECT 
    region,
    COUNT(DISTINCT order_id) AS unique_orders,
    SUM(quantity) AS total_quantity_sold,
    ROUND(SUM(sales_amount), 2) AS regional_revenue,
    ROUND(SUM(sales_amount) * 1.0 / COUNT(DISTINCT order_id), 2) AS regional_aov,
    ROUND((SUM(sales_amount) * 100.0) / (SELECT grand_total FROM grand_total_cte), 2) AS revenue_contribution_pct
FROM sales
GROUP BY region
ORDER BY regional_revenue DESC;


-- ------------------------------------------------------------------------------
-- 6. Product Category Breakdown
-- Compares revenue, order volume, and revenue contribution across categories.
-- ------------------------------------------------------------------------------
WITH grand_total_cte AS (
    SELECT SUM(sales_amount) AS grand_total FROM sales
)
SELECT 
    category,
    COUNT(DISTINCT order_id) AS order_touchpoints,
    SUM(quantity) AS units_sold,
    ROUND(SUM(sales_amount), 2) AS category_revenue,
    ROUND((SUM(sales_amount) * 100.0) / (SELECT grand_total FROM grand_total_cte), 2) AS category_revenue_pct
FROM sales
GROUP BY category
ORDER BY category_revenue DESC;


-- ------------------------------------------------------------------------------
-- 7. Best-Performing and Lowest-Performing Months
-- Uses DENSE_RANK() / Subqueries to isolate peak and trough revenue months.
-- ------------------------------------------------------------------------------
WITH ranked_months AS (
    SELECT 
        strftime('%Y-%m', order_date) AS year_month,
        ROUND(SUM(sales_amount), 2) AS monthly_revenue,
        RANK() OVER (ORDER BY SUM(sales_amount) DESC) AS rank_desc,
        RANK() OVER (ORDER BY SUM(sales_amount) ASC) AS rank_asc
    FROM sales
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT 
    'Best Performing Month' AS performance_type,
    year_month,
    monthly_revenue
FROM ranked_months
WHERE rank_desc = 1

UNION ALL

SELECT 
    'Lowest Performing Month' AS performance_type,
    year_month,
    monthly_revenue
FROM ranked_months
WHERE rank_asc = 1;


-- ------------------------------------------------------------------------------
-- 8. Customer Basket Size (Items Per Order Distribution)
-- Analyzes cross-selling efficiency (multi-item orders vs single-item orders).
-- ------------------------------------------------------------------------------
WITH order_basket_size AS (
    SELECT 
        order_id,
        COUNT(product_id) AS line_items_count,
        SUM(quantity) AS total_units_in_order,
        SUM(sales_amount) AS total_order_value
    FROM sales
    GROUP BY order_id
)
SELECT 
    line_items_count,
    COUNT(*) AS order_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(DISTINCT order_id) FROM sales), 2) AS pct_of_total_orders,
    ROUND(AVG(total_order_value), 2) AS avg_order_basket_value
FROM order_basket_size
GROUP BY line_items_count
ORDER BY line_items_count ASC;

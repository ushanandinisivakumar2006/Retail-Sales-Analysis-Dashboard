# Executive Business Analysis Report: Retail Sales Performance

**Project Title:** Retail Sales Analysis Dashboard  
**Currency:** Indian Rupee (INR - ₹)  
**Dataset Nature:** Verified Synthetic Benchmark Dataset (1,496 clean transactions across calendar year 2025)  
**Analytical Scope:** Python, SQL, Excel, and Power BI Enterprise Model

---

## 1. Project Objective & Context

The objective of this retail analytics project is to provide executive leadership and category managers with granular, data-driven visibility into sales performance, consumer basket size, product mix, regional penetration, and seasonal revenue volatility.

> [!NOTE]
> **Dataset Transparency Notice:** This analysis is performed on a controlled synthetic retail dataset modeled with realistic commercial characteristics (multi-item orders, seasonal demand spikes, and geographic market weighting). While the conclusions demonstrate a complete enterprise analytics workflow, they reflect simulated transactional patterns and do not represent actual proprietary commercial records of any real corporation.

---

## 2. High-Level Performance KPIs

| Key Performance Indicator | Computed Metric | Business Context / Interpretation |
| :--- | :--- | :--- |
| **Total Gross Revenue** | **₹6,406,050.00** | Cumulative net billed value across all product categories. |
| **Total Unique Orders** | **945** | Distinct customer checkout events. |
| **Average Order Value (AOV)** | **₹6,778.89** | Average spend per customer order (`Total Revenue / Unique Orders`). |
| **Total Units Sold** | **2,750 units** | Physical volume shipped across 2025. |
| **Active Catalog Products** | **29 SKU items** | Distinct product lines with non-zero sales volume. |
| **Top Revenue Product** | **Ergonomic High-Back Mesh Chair** | Generated **₹809,910.00** (12.64% of total catalog revenue). |
| **Peak Sales Month** | **2025-10** | Recorded **₹759,650.00** across 133 orders (festive surge). |
| **Lowest Sales Month** | **2025-02** | Recorded **₹237,934.00** across 47 orders (post-holiday lull). |

---

## 3. Product Performance Analysis

### 3.1 Top 5 Products by Revenue
High-ticket electronics and premium home appliances drive disproportionate top-line revenue:

| Product ID | Product Name | Category | Units Sold | Total Revenue (₹) | % Revenue Share |
| :--- | :--- | :--- | :--- | :--- | :--- |
| PROD-OS-04 | **Ergonomic High-Back Mesh Chair** | Office Supplies | 90 | ₹809,910.00 | 12.64% |
| PROD-EL-08 | **1TB High-Speed External SSD** | Electronics | 108 | ₹809,892.00 | 12.64% |
| PROD-EL-05 | **Noise Cancelling Headphones** | Electronics | 93 | ₹557,907.00 | 8.71% |
| PROD-HK-02 | **Digital Air Fryer 4.5L** | Home & Kitchen | 102 | ₹499,698.00 | 7.80% |
| PROD-FA-04 | **Breathable Mesh Running Shoes** | Fashion | 112 | ₹313,488.00 | 4.89% |


### 3.2 Top 5 Products by Quantity Sold (Volume Leaders)
Affordable accessories, everyday office consumables, and kitchen essentials generate foot traffic and order basket depth:

| Product ID | Product Name | Category | Units Sold | Total Revenue (₹) |
| :--- | :--- | :--- | :--- | :--- |
| PROD-FA-01 | **Organic Cotton Crewneck T-Shirt** | Fashion | 137 | ₹95,763.00 |
| PROD-HK-06 | **500W High Speed Smoothie Blender** | Home & Kitchen | 122 | ₹280,478.00 |
| PROD-OS-03 | **A5 Hardcover Dotted Journal** | Office Supplies | 118 | ₹58,882.00 |
| PROD-EL-03 | **Portable Bluetooth Speaker** | Electronics | 115 | ₹252,885.00 |
| PROD-FA-04 | **Breathable Mesh Running Shoes** | Fashion | 112 | ₹313,488.00 |


---

## 4. Monthly Trend & Seasonality Analysis

The business exhibits distinct retail seasonality, characterized by stable baseline demand through Q1–Q3 followed by a dramatic revenue acceleration in Q4 coinciding with the Indian festive shopping season (Diwali, Dussehra, and year-end promotions).

| Year-Month | Orders | Units Sold | Monthly Revenue (₹) | MoM Change (₹) | MoM Growth (%) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 2025-01 | 48 | 161 | ₹340,639.00 | N/A | Baseline |
| 2025-02 | 47 | 116 | ₹237,934.00 | ₹-102,705.00 | -30.15% |
| 2025-03 | 79 | 226 | ₹609,624.00 | ₹+371,690.00 | +156.22% |
| 2025-04 | 70 | 207 | ₹538,093.00 | ₹-71,531.00 | -11.73% |
| 2025-05 | 81 | 263 | ₹645,987.00 | ₹+107,894.00 | +20.05% |
| 2025-06 | 74 | 212 | ₹461,888.00 | ₹-184,099.00 | -28.50% |
| 2025-07 | 78 | 212 | ₹520,088.00 | ₹+58,200.00 | +12.60% |
| 2025-08 | 90 | 258 | ₹607,042.00 | ₹+86,954.00 | +16.72% |
| 2025-09 | 85 | 254 | ₹560,746.00 | ₹-46,296.00 | -7.63% |
| 2025-10 | 133 | 350 | ₹759,650.00 | ₹+198,904.00 | +35.47% |
| 2025-11 | 103 | 306 | ₹733,594.00 | ₹-26,056.00 | -3.43% |
| 2025-12 | 60 | 185 | ₹390,765.00 | ₹-342,829.00 | -46.73% |


### Key Monthly Observations:
1. **Festive Spike (2025-10):** Revenue peaked at **₹759,650.00**, demonstrating the vital impact of high-intent festive campaigns.
2. **Post-Holiday Trough (2025-02):** Revenue dropped to **₹237,934.00**, illustrating consumer budget exhaustion following peak holiday spending.

---

## 5. Regional Sales Distribution

Regional sales performance reflects deliberate market penetration strategies across tier-1 and tier-2 urban corridors:

| Region | Unique Orders | Units Sold | Regional Revenue (₹) | Regional AOV (₹) | Revenue Contribution (%) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **North** | 271 | 829 | ₹1,748,871.00 | ₹6,453.40 | 27.30% |
| **South** | 226 | 597 | ₹1,376,303.00 | ₹6,089.84 | 21.48% |
| **West** | 174 | 547 | ₹1,358,353.00 | ₹7,806.63 | 21.20% |
| **East** | 178 | 508 | ₹1,161,092.00 | ₹6,522.99 | 18.12% |
| **Central** | 96 | 269 | ₹761,431.00 | ₹7,931.57 | 11.89% |


- **Leading Territories:** North and South regions represent the foundational core of business revenue, supported by higher digital adoption and dense logistics networks.
- **Growth Potential:** Central and East territories display solid average order values, signaling lucrative runway for fulfillment expansion.

---

## 6. Category Performance & Product Mix

| Category | Touchpoint Orders | Units Sold | Category Revenue (₹) | Revenue Contribution (%) |
| :--- | :--- | :--- | :--- | :--- |
| **Electronics** | 338 | 708 | ₹2,656,792.00 | 41.47% |
| **Home & Kitchen** | 301 | 582 | ₹1,229,368.00 | 19.19% |
| **Office Supplies** | 256 | 496 | ₹1,138,054.00 | 17.77% |
| **Fashion** | 239 | 504 | ₹796,696.00 | 12.44% |
| **Beauty & Personal Care** | 233 | 460 | ₹585,140.00 | 9.13% |


- **Electronics** serves as the primary revenue generator due to premium average selling prices (ASPs).
- **Home & Kitchen** and **Office Supplies** act as dependable volume drivers that encourage cross-category cart attachments.

---

## 7. Actionable Business Recommendations

1. **Strategic Bundle Promotions:**
   Combine high-volume accessories (e.g., *Dual-Sided Desk Mat* or *Wireless Mouse*) with premium anchor SKUs (e.g., *1TB External SSD* or *Ergonomic High-Back Mesh Chair*) at a 5-10% bundled discount to expand Average Order Value beyond ₹6,779.
2. **Q3 Pre-Festive Inventory Staging:**
   Given the sharp acceleration in October and November revenue, procurement and warehousing teams must stage safety stock for the top 5 revenue SKUs by mid-September to avoid stockouts during festive peaks.
3. **Geographic Growth Targeting:**
   Launch targeted localized digital marketing campaigns in the East and Central regions. Establishing localized micro-fulfillment hubs will shorten delivery SLAs and unlock incremental order velocity.
4. **Post-Holiday Re-Engagement (January–February):**
   Mitigate post-holiday demand troughs through customer loyalty reward redemptions, clearance flash events, and personalized replenishment reminders for consumable categories.

---

## 8. Dataset Scope and Limitations

1. **Synthetic Nature:** Generated with fixed base price models and controlled anomalies for analytical instruction.
2. **Omission of Taxes & Discounts:** The dataset tracks gross line-item sales amount (`Quantity * Unit Price`). Line-level coupon discounts, shipping surcharges, and GST slabs were not included in the raw feed.
3. **Returns and Refunds:** Cancelled orders and return merchandise authorizations (RMAs) were excluded during data hygiene filtering (`Quantity <= 0`).

---

*Report prepared and validated via Python analytics engine (`src/analyze_sales.py`).*

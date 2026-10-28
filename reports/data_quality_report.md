# Data Quality and Cleaning Audit Report

**Project:** Retail Sales Analysis Dashboard  
**Generated At:** 2026-10-28 19:35:10  
**Status:** Successfully Validated and Cleaned  
**Currency:** Indian Rupee (INR - ₹)

---

## 1. Executive Summary

| Metric | Raw Dataset | Cleaned Dataset | Change / Action |
| :--- | :--- | :--- | :--- |
| **Total Records** | 1,515 | 1,496 | -19 rows dropped |
| **Total Columns** | 9 | 9 | Validated schema |
| **Exact Duplicate Rows** | 15 | 0 | Removed duplicate line records |
| **Multi-Item Orders Preserved** | 381 | 381 | Retained legitimate basket orders |
| **Invalid Numeric Rows** | 4 | 0 | Dropped zero/negative values |
| **Missing Region Imputations** | 10 | 0 | Resolved via basket/default fallback |
| **Sales Amount Imputations** | 45 | 0 | Calculated as `Quantity * Unit Price` |
| **Sales Amount Reconciliations**| 8 | 0 | Reconciled data entry discrepancies |

---

## 2. Initial Missing Value Assessment

| Column Name | Missing Values (Count) | % of Total Raw Data | Handling Strategy |
| :--- | :--- | :--- | :--- |
| `Order ID` | 0 | 0.00% | Mandatory field validated |
| `Order Date` | 0 | 0.00% | Mandatory field validated |
| `Product ID` | 0 | 0.00% | Mandatory field validated |
| `Product Name` | 0 | 0.00% | Mandatory field validated |
| `Category` | 0 | 0.00% | Mandatory field validated |
| `Region` | 10 | 0.66% | Imputed from multi-item order match or Central |
| `Quantity` | 0 | 0.00% | Mandatory field validated |
| `Unit Price` | 0 | 0.00% | Mandatory field validated |
| `Sales Amount` | 46 | 3.04% | Computed via Quantity * Unit Price |

---

## 3. Data Cleaning Methodology & Transformation Rules

### 3.1 Duplicate vs. Multi-Item Order Handling
- **Exact Duplicates:** Records where every single column is identical were flagged as double submissions and dropped (15 records).
- **Legitimate Multi-Item Orders:** An order can contain multiple distinct products. Repeated `Order ID` values with distinct `Product ID` values were **strictly preserved** (381 orders).

### 3.2 Categorical Normalization
- **Whitespace & Casing:** Stripped all leading and trailing whitespace from strings. Standardized all product categories and geographic regions to uniform Title Case.
- **Regions:** Normalized 55 region entries and resolved 10 missing regions.
- **Categories:** Normalized 60 category entries.

### 3.3 Numeric Validation & Formula Reconciliation
- **Quantity & Price Validation:** Checked for non-positive values (`Quantity <= 0` or `Unit Price <= 0`). Dropped 4 corrupted records to safeguard analytical integrity.
- **Sales Amount Imputation:** Recomputed missing `Sales Amount` for 45 records using the business formula:
  $$\text{Sales Amount} = \text{Quantity} \times \text{Unit Price}$$
- **Discrepancy Correction:** Corrected 8 records where entered `Sales Amount` differed from `Quantity * Unit Price` by more than ₹0.01 due to upstream data entry errors.

### 3.4 Temporal Standardization
- Standardized mixed date strings into uniform ISO format (`YYYY-MM-DD`). Verified 100% parseability across all dates.

---

## 4. Flagged Anomaly Log

Below is the transparent record of flagged anomalies during pipeline execution:

| Order ID | Product ID | Anomaly Reason & Resolution |
| :--- | :--- | :--- |
| `ORD-2025-1184` | `PROD-OS-01` | Invalid numeric value (Quantity=-1, Unit Price=849.0) |
| `ORD-2025-1522` | `PROD-HK-05` | Invalid numeric value (Quantity=3, Unit Price=-100.0) |
| `ORD-2025-1611` | `PROD-EL-08` | Invalid numeric value (Quantity=2, Unit Price=0.0) |
| `ORD-2025-1919` | `PROD-OS-02` | Invalid numeric value (Quantity=0, Unit Price=399.0) |
| `ORD-2025-1010` | `PROD-EL-07` | Sales Amount discrepancy (Recorded: 4498.2, Expected: 4998.0) -> Reconciled |
| `ORD-2025-1078` | `PROD-FA-01` | Sales Amount discrepancy (Recorded: 1258.2, Expected: 1398.0) -> Reconciled |
| `ORD-2025-1182` | `PROD-FA-01` | Sales Amount discrepancy (Recorded: 629.1, Expected: 699.0) -> Reconciled |
| `ORD-2025-1238` | `PROD-HK-04` | Sales Amount discrepancy (Recorded: 7827.3, Expected: 8697.0) -> Reconciled |
| `ORD-2025-1459` | `PROD-EL-05` | Sales Amount discrepancy (Recorded: 5399.1, Expected: 5999.0) -> Reconciled |
| `ORD-2025-1545` | `PROD-HK-02` | Sales Amount discrepancy (Recorded: 13227.3, Expected: 14697.0) -> Reconciled |
| `ORD-2025-1715` | `PROD-BP-05` | Sales Amount discrepancy (Recorded: 1169.1, Expected: 1299.0) -> Reconciled |
| `ORD-2025-1785` | `PROD-BP-04` | Sales Amount discrepancy (Recorded: 718.2, Expected: 798.0) -> Reconciled |

---

## 5. Verification Checklist

- [x] Schema structure matches project specification.
- [x] Date fields are in ISO format `YYYY-MM-DD`.
- [x] Quantity and Unit Price are strictly positive numbers.
- [x] Sales Amount strictly satisfies `Quantity * Unit Price`.
- [x] No missing or null values remain in primary dimensions or measures.
- [x] Output datasets written to both CSV and Excel formats.

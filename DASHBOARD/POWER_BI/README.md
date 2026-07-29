# Power BI C-Suite Executive Financial & Risk Reporting Architecture

This document specifies the Data Modeling, DAX Measures, and Report Page Layout architecture for deploying the **Civil Infrastructure Construction Intelligence Engine** in Power BI Desktop / Power BI Service.

---

## 1. Data Architecture: Star Schema Model

The data model follows an enterprise Star Schema design to optimize DAX measure performance and enable seamless cross-filtering across civil project sites, vendors, and billing dates.

```text
               +-------------------+
               |   Dim_Projects    |
               +-------------------+
               | project_id (PK)   |
               | project_name      |
               | site_location     |
               | structure_type    |
               +---------+---------+
                         |
           +-------------+-------------+
           | 1                         | 1
           |                           |
           v *                         v *
+-------------------+       +-------------------+
|   Dim_WorkOrders  |       | Fact_PurchaseOrders|
+-------------------+       +-------------------+
| work_order_id(PK) |       | po_id (PK)        |
| project_id (FK)   |       | project_id (FK)   |
| total_contract_val|       | vendor_id (FK)    |
+---------+---------+       | total_po_value    |
          | 1               +---------+---------+
          |                           | *
          v *                         v 1
+-------------------+       +-------------------+
| Fact_TaxInvoices  |       |    Dim_Vendors    |
+-------------------+       +-------------------+
| invoice_id (PK)   |       | vendor_id (PK)    |
| work_order_id(FK) |       | vendor_name       |
| net_payable_amount|       | vendor_type       |
+-------------------+       +-------------------+
```

---

## 2. Core DAX Measures Specification

### Measure 1: Total Contract Value
```dax
Total Contract Value = 
SUM(Work_Orders[total_contract_value])
```

### Measure 2: Total Billed Amount (Invoiced)
```dax
Total Billed Amount = 
SUM(Tax_Invoices[net_payable_amount])
```

### Measure 3: Total Vendor PO Commitments
```dax
Total Vendor PO Commitments = 
SUM(Purchase_Orders[total_po_value])
```

### Measure 4: Subcontractor PO Commitment Ratio (%)
```dax
PO Commitment Ratio = 
DIVIDE(
    [Total Vendor PO Commitments],
    [Total Contract Value],
    0
)
```

### Measure 5: Progressive Milestone Billing Percentage (%)
```dax
Billing Percentage = 
DIVIDE(
    [Total Billed Amount],
    [Total Contract Value],
    0
)
```

### Measure 6: Vendor Overrun Risk Flag
```dax
Vendor Overrun Risk Flag = 
IF(
    [PO Commitment Ratio] >= 0.80,
    "HIGH RISK (>80%)",
    "NORMAL"
)
```

---

## 3. Power BI Dashboard Page Layout Guide

### Page 1: Executive C-Suite Overview
* **Top Header Slicer**: `Dim_Projects[project_name]` dropdown filter.
* **Top KPI Cards**: Total Contract Value, Total Billed Amount, PO Commitment Ratio.
* **Main Visual 1**: Clustered Column Chart comparing Contract Value vs Total Billed Amount by Project.
* **Main Visual 2**: Donut Chart showing Vendor PO Commitments grouped by `Dim_Vendors[vendor_type]` (Grouting, Storage Shed Fabrication, Foundation Retrofitting).

### Page 2: Vendor Risk & Quality Heatmap
* **Visual 1**: Matrix Visual displaying Vendor Name, Total PO Count, Total Committed Value, and Overrun Risk Flag conditionally formatted (Red for High Risk).
* **Visual 2**: Scatter Plot comparing Ultrasonic Pulse Velocity ($m/s$) vs Compressive Strength ($MPa$) with a constant reference line at $40.0 \text{ MPa}$.

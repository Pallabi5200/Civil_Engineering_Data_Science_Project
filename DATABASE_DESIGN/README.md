# Database Architecture & Python Data Pipeline

This directory contains the relational database architecture, schema DDL, automated database setup scripts, analytical SQL queries, and Python data preparation scripts for the Construction Intelligence Platform.

---

## SQL KPI Analytical Queries (`06_KPI_Queries.sql`)

The queries in `06_KPI_Queries.sql` analyze relational transactions across Work Orders, Invoices, Quality Logs, and BOQ items to derive operational and financial insights.

### 1. Project Billing & Financial Progress
* **Objective**: Calculates total contract value, cumulative billed amount, and billing completion percentage for wind turbine foundation retrofitting work.
* **Techniques**: `INNER JOIN` across `Projects`, `Work_Orders`, and `Tax_Invoices`, `SUM()` aggregations, and derived arithmetic percentages.

```sql
SELECT p.project_name, wo.work_order_number, wo.total_contract_value,
       SUM(ti.net_payable_amount) AS total_billed_amount,
       (SUM(ti.net_payable_amount)/wo.total_contract_value)*100 AS billing_percentage
FROM Projects p
JOIN Work_Orders wo ON wo.project_id = p.project_id
JOIN Tax_Invoices ti ON wo.work_order_id = ti.work_order_id
WHERE p.project_name = 'WTG Foundation Retrofitting - GAL33'
GROUP BY p.project_name, wo.work_order_number, wo.total_contract_value;
```

---

### 2. Concrete Strength Quality Compliance Check
* **Objective**: Categorizes site quality inspection logs into `PASS`, `PENDING_7DAY`, or `FAIL` based on compressive strength thresholds ($\ge 40.00$ MPa at 28 days).
* **Techniques**: Conditional evaluation using `CASE WHEN ... THEN ... ELSE ... END` and string pattern matching (`LIKE '%7-Day%'`).

```sql
SELECT inspection_date, activity_type, cube_test_result_mpa,
       CASE 
           WHEN cube_test_result_mpa >= 40.00 THEN 'PASS'
           WHEN activity_type LIKE '%7-Day%' THEN 'PENDING_7DAY'
           ELSE 'FAIL'
       END AS quality_check
FROM Field_Quality_Logs
WHERE project_id = 'PRJ-GAL33';
```

---

### 3. High-Value BOQ Items Ranking (Pareto Analysis)
* **Objective**: Ranks work items under a specific Work Order by estimated cost to identify major cost drivers.
* **Techniques**: `ORDER BY ... DESC` sorting on calculated monetary values.

```sql
SELECT item_code, description_of_work, unit_of_measurement, estimated_quantity, unit_rate, estimated_total_cost
FROM BOQ_Items
WHERE work_order_id = 'WO-MSUM-01'
ORDER BY estimated_total_cost DESC;
```

---

### 4. Cumulative Cashflow & Running Total Billing
* **Objective**: Computes a chronological running total of invoice payouts per project to track cash inflow trajectories.
* **Techniques**: SQL Window Function `SUM() OVER (PARTITION BY ... ORDER BY ...)` to calculate running totals without collapsing individual transaction rows.

```sql
SELECT p.project_name, ti.invoice_number, ti.invoice_date, ti.net_payable_amount,
       SUM(ti.net_payable_amount) OVER (
           PARTITION BY p.project_name
           ORDER BY ti.invoice_date
       ) AS cumulative_billing
FROM Projects p
JOIN Work_Orders wo ON p.project_id = wo.project_id
JOIN Tax_Invoices ti ON wo.work_order_id = ti.work_order_id
WHERE p.project_name = 'WTG Foundation Retrofitting - GAL33';
```

---

### 5. Field Quality Pass Rate Percentage
* **Objective**: Calculates the percentage of concrete cube tests meeting structural specifications across sites.
* **Techniques**: Conditional aggregation using `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` divided by total count.

```sql
SELECT project_id, COUNT(*) AS total_test,
       SUM(CASE WHEN cube_test_result_mpa >= 40.00 THEN 1 ELSE 0 END) AS passed_tests,
       (SUM(CASE WHEN cube_test_result_mpa >= 40.00 THEN 1 ELSE 0 END)*100.0/COUNT(*)) AS pass_percentage
FROM Field_Quality_Logs
GROUP BY project_id;
```

---

### 6. Budget Overrun Risk Analysis (CTE)
* **Objective**: Compares total vendor purchase order commitments against client contract values to identify budget overrun risks.
* **Techniques**: Common Table Expressions (CTEs) and multi-table joins.

```sql
WITH VendorCommitments AS (
    SELECT 
        project_id,
        SUM(total_po_value) AS total_po_commitment
    FROM Purchase_Orders
    GROUP BY project_id
)
SELECT 
    p.project_id,
    p.project_name,
    wo.work_order_number,
    wo.total_contract_value,
    vc.total_po_commitment,
    (vc.total_po_commitment * 100.0 / wo.total_contract_value) AS cost_commitment_ratio
FROM Projects p
JOIN Work_Orders wo ON p.project_id = wo.project_id
JOIN VendorCommitments vc ON p.project_id = vc.project_id;
```

---

## Python Database EDA & Data Cleaning (`01_Database_EDA.py`)

The `01_Database_EDA.py` script handles data extraction, feature engineering, missing value imputation, and multi-table merging using Pandas.

### Key Implementation Steps

1. **Feature Engineering**:
   * Parses string descriptions in `activity_type` to extract clean numeric curing durations (`curing_days`: 7, 28).
   * Creates a binary compliance indicator (`is_compliant`) based on characteristic compressive strength thresholds ($\ge 30\text{ MPa}$).

2. **Group-Based Median Imputation Strategy**:
   * Imputes missing ultrasonic pulse velocity values (`ndt_ultrasonic_velocity`) using group medians partitioned by `curing_days`.
   * **Rationale**: Ultrasonic velocity changes as concrete cures over time. Group median imputation preserves curing age distributions without distorting subgroup variance or introducing outlier bias.
   * **Multi-Stage Fallback**: Implements a 3-stage chain (`group median` -> `global median` -> `domain constant`) to guarantee pipeline execution stability.

3. **Multi-Table Relational Merges**:
   * Joins `df_quality`, `df_work_orders`, and `df_boq` using `pd.merge()` on `project_id` and `work_order_id` to link physical field test results with commercial cost line items.

---

---

## Automated Enterprise Data Ingestion Engine (`ingest_all_data.py` & `02_Excel_Ingestion.py`)

To transform raw operational records into an enterprise-grade analytics platform, we built two automated Python ETL ingestion scripts that extract, clean, schema-validate, and load heterogeneous data across all **PMPL** and **RENEW** project streams into `construction_project.db`.

---

### 1. Standalone Multi-Spreadsheet BOQ Engine (`02_Excel_Ingestion.py`)
* **Objective**: Automates header offset cleaning, forward-filling parent codes, and schema normalization across raw Bill of Quantities (BOQ) Excel files (`.xlsx` and `.xls`).
* **ETL Pipeline Rationale**:
  1. **Header Offset Alignment (`header=6` / `header=4`)**: Skips non-tabular project title blocks to isolate true line item tables.
  2. **Parent Code Forward-Fill (`.ffill()`)**: Propagates parent SAC codes down across sub-items to preserve hierarchical billing rules.
  3. **Data Hygiene & Typing**: Strips leading/trailing column whitespace and casts quantities, unit rates, and totals to float vectors.
* **Empirical Execution Insights**:
  * Extracted and mapped **96 total BOQ line items** across 4 major commercial projects:
    * `WO-PMPL-GAL33`: 29 items (PMPL Wind Turbine Retrofitting)
    * `WO-RENEW-SHED`: 29 items (Otha Phase 3 Hazardous Storage Shed)
    * `WO-SHED-PATAN`: 23 items (Patan Hazardous Storage Shed)
    * `WO-SHED-JAGLUR`: 15 items (Jaglur Industrial Shed)

---

### 2. Master Database Ingestion Orchestrator (`ingest_all_data.py`)
* **Objective**: Re-initializes the relational schema via `04_Schema_DDL.sql` and executes transactional batch loading across all 12 relational database tables.
* **Enterprise Ingestion Results**:
  * **Projects (8 Records)**: Ingested wind turbine foundation retrofitting sites (GAL33, GAL06, GAL07), WTG pedestal grouting (Molagavali & Patan/Kagwad), and industrial storage sheds (Otha, Jaglur, Patan).
  * **Commercial Transactions**: Ingested 7 Work Orders, 3 Purchase Orders, 1 Proforma Invoice, and 3 Tax Invoices.
  * **BOQ Line Items (96 Records)**: Populated full bill-of-quantity item structures linked directly to work orders.
  * **Field Quality & Inspections (7 Quality Logs & 18 Damage Reports)**: Loaded concrete compressive test logs (7-day, 28-day), NDT ultrasonic pulse velocities, and 18 turbine foundation damage inspection logs (`GML-25`, `GML-52`, Patan/Kagwad `KG01`, `RP33`, `RP41`...).

---

## Directory Layout & Execution Commands

```text
DATABASE_DESIGN/
├── 01_Database_EDA.py          # Python data extraction, imputation, and merge pipeline
├── 02_Excel_Ingestion.py       # Standalone multi-spreadsheet BOQ ingestion engine
├── 04_Schema_DDL.sql           # Table creation DDL statements and foreign key constraints
├── 05_insert_data.sql          # Database seed data DML
├── 06_KPI_Queries.sql          # Analytical SQL queries (CTEs, Window functions, aggregations)
├── ingest_all_data.py          # Master enterprise ETL database ingestion script
├── construction_project.db     # Populated relational SQLite database
└── README.md                   # Technical documentation
```

### Execution Commands

```bash
# 1. Execute Master ETL Ingestion (Populates all 12 database tables from PMPL & RENEW)
python DATABASE_DESIGN/ingest_all_data.py

# 2. Run Standalone BOQ Extraction & Cleaning Module
python DATABASE_DESIGN/02_Excel_Ingestion.py

# 3. Execute SQL Analytical KPI Queries
python -c "import sqlite3; conn=sqlite3.connect('DATABASE_DESIGN/construction_project.db'); print(conn.cursor().execute(open('DATABASE_DESIGN/06_KPI_Queries.sql').read()).fetchall())"
```

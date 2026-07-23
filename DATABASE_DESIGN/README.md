# Database Design & SQL KPI Analytics Module

This directory contains the relational database architecture, schema DDL, automated setup scripts, and business KPI analytical queries for the **Construction Intelligence Platform (CIP)**.

---

## 📌 Executive Summary of SQL KPI Queries (`06_KPI_Queries.sql`)

The queries in `06_KPI_Queries.sql` translate raw relational database transactions (Work Orders, Tax Invoices, Quality Logs, and BOQs) into high-value business intelligence insights for Civil Engineering Project Controllers and Site Engineers.

---

### 1. Project Billing & Financial Progress KPI
* **Query Purpose**: Calculates the total contract value, cumulative net billed amount, and current **billing percentage** for a specific civil engineering project (`WTG Foundation Retrofitting - GAL33`).
* **Civil Engineering Context**: Project managers use this metric to track progress payments against milestone completion limits and ensure invoicing is aligned with total work orders.
* **Key SQL Techniques**: `INNER JOIN` across 3 tables (`Projects`, `Work_Orders`, `Tax_Invoices`), `SUM()` aggregation, and derived arithmetic percentage calculations.

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
* **Query Purpose**: Categorizes site quality inspection logs into `PASS`, `PENDING_7DAY`, or `FAIL` based on concrete cube test compressive strength results (in MPa).
* **Civil Engineering Context**: Structural concrete (e.g., M40 grade for WTG turbine foundations) requires strict compliance ($\ge 40.00$ MPa at 28 days). 7-day tests are monitored as intermediate indicators before 28-day curing completes.
* **Key SQL Techniques**: Conditional logic using `CASE WHEN ... THEN ... ELSE ... END` and string pattern matching (`LIKE '%7-Day%'`).

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

### 3. High-Value Bill of Quantities (BOQ) Items Ranking
* **Query Purpose**: Lists all scheduled work items under a specific Work Order (`WO-MSUM-01`), sorted by `estimated_total_cost` in descending order.
* **Civil Engineering Context**: Identifies the top cost-driver line items (e.g., micro-piling, high-grade rebar steel, specialized grout) for Pareto Analysis ($80/20$ rule in procurement cost management).
* **Key SQL Techniques**: `ORDER BY ... DESC` sorting on calculated monetary values.

```sql
SELECT item_code, description_of_work, unit_of_measurement, estimated_quantity, unit_rate, estimated_total_cost
FROM BOQ_Items
WHERE work_order_id = 'WO-MSUM-01'
ORDER BY estimated_total_cost DESC;
```

---

### 4. Cumulative Cashflow & Running Total Billing (Window Function)
* **Query Purpose**: Computes a chronological running sum (`cumulative_billing`) of tax invoice payouts per project as time progresses.
* **Civil Engineering Context**: Provides cash inflow trajectory tracking over the project lifecycle, essential for working capital management and financial forecasting.
* **Key SQL Techniques**: SQL Window Function `SUM() OVER (PARTITION BY ... ORDER BY ...)` to calculate running totals without collapsing individual transaction rows.

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

### 5. Field Quality Compliance & Pass Rate KPI
* **Query Purpose**: Computes the concrete cube test pass rate percentage for each project site.
* **Civil Engineering Context**: Quality Control managers audit site compliance by calculating the percentage of poured concrete batches meeting structural strength specifications ($\ge 40.00$ MPa).
* **Key SQL Techniques**: Conditional Aggregation using `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`, `COUNT(*)`, and floating-point arithmetic (`* 100.0`).

```sql
SELECT project_id, COUNT(*) AS total_test,
       SUM(CASE WHEN cube_test_result_mpa >= 40.00 THEN 1 ELSE 0 END) AS passed_tests,
       (SUM(CASE WHEN cube_test_result_mpa >= 40.00 THEN 1 ELSE 0 END)*100.0/COUNT(*)) AS pass_percentage
FROM Field_Quality_Logs
GROUP BY project_id;
```

---

### 6. Cost Overrun Risk Analysis (CTE)
* **Query Purpose**: Calculates committed vendor expenditure vs client contract value to assess project budget overrun risk.
* **Civil Engineering Context**: Ensures vendor Purchase Orders stay within approved Work Order budget limits.
* **Key SQL Techniques**: Common Table Expressions (`WITH VendorCommitments AS (...)`), `SUM()` aggregation, and multi-table joins.

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

## 🐍 Python Database EDA & Data Cleaning Pipeline (`01_Database_EDA.py`)

The `01_Database_EDA.py` script bridges SQLite database queries with Python Pandas data cleaning, feature engineering, and statistical analysis.

### 1. Feature Engineering: Curing Age Extraction
* **Purpose**: Parses text descriptions in `activity_type` (e.g., `'7-Day Cube Test'`, `'28-Day Cube Test'`) to create a clean, numeric feature `curing_days` ($7, 28, 0$).
* **Data Science Context**: Converts unformatted categorical text into continuous numerical values needed for statistical grouping and ML modeling.

### 2. Group-Based Median Imputation Strategy (`ndt_ultrasonic_velocity`)
* **Problem**: Field sensor logs for Non-Destructive Testing (NDT) Ultrasonic Pulse Velocity contain missing entries.
* **Imputation Strategy**: Imputes missing values using the **group median** calculated per `curing_days` category.
* **Why Group Median over Global Mean (Interview Callout)**:
  1. **Domain Physics**: Ultrasonic pulse velocity increases significantly as concrete cures (7-day vs 28-day). A global mean would underestimate 28-day velocities and overestimate 7-day velocities.
  2. **Robustness to Sensor Outliers**: Field NDT readings are subject to sensor contact errors or surface voids. Median is robust to extreme outliers (50% breakdown point), whereas mean is heavily skewed by anomalies.
  3. **Data Leakage Prevention**: Group-wise transformation keeps imputation localized within homogeneous curing stages.

### 3. Concrete Strength Statistical Summaries
* **Purpose**: Aggregates compressive strength (`cube_test_result_mpa`) across `curing_days` to output `mean`, `std`, `min`, and `max`.

---

## 🛠️ How to Store & Organize This in Your Main Project

To keep your project structured, maintain clean version control, and follow your **12-Week Construction Intelligence Platform Schedule**:

### 📁 Directory Layout
```text
Civil_Engineering_Data_Science_Project/
│
├── DATABASE_DESIGN/               <-- 👈 Current Module (Week 2 & Week 5 SQL / Python EDA)
│   ├── 01_Database_EDA.py        <-- Python script for extraction, data cleaning & EDA
│   ├── 01_Master_Entity_List.xlsx
│   ├── 02_Master_Data_dict.csv
│   ├── 03_ER_Diagram_1.pdf
│   ├── 04_Schema_DDL.sql         <-- Table Creation (DDL)
│   ├── 05_insert_data.sql        <-- Seed Data (DML)
│   ├── 06_KPI_Queries.sql        <-- SQL Analytical Queries & Window Functions
│   ├── README.md                 <-- 📄 Technical Documentation (This File)
│   ├── setup_db.py               <-- Python script to build construction_project.db
│   └── construction_project.db   <-- SQLite Local Database
│
├── SQL/                           <-- Dedicated directory for exported SQL reports / notebooks
├── PYTHON/                        <-- Week 6: Python & EDA notebooks
├── README.md                      <-- Main Project Root README
```

---

## 🚀 How to Execute the Database & Queries

1. **Rebuild local SQLite Database**:
   ```bash
   python setup_db.py
   ```
2. **Execute Python Database EDA & Data Cleaning Pipeline**:
   ```bash
   python 01_Database_EDA.py
   ```
3. **Execute SQL KPI Queries via Python SQLite Client**:
   ```bash
   python -c "import sqlite3; conn=sqlite3.connect('construction_project.db'); print(conn.cursor().execute(open('06_KPI_Queries.sql').read()).fetchall())"
   ```
4. **Version Control Git Commit**:
   ```bash
   git add DATABASE_DESIGN/
   git commit -m "docs(database): update README with Python EDA, feature engineering, and imputation strategy"
   git push origin main
   ```


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

## Directory Layout & Execution

```text
DATABASE_DESIGN/
├── 01_Database_EDA.py        # Python data extraction, imputation, and merge pipeline
├── 01_Master_Entity_List.xlsx# Entity definitions and relationships
├── 02_Master_Data_dict.csv   # Field definitions and data types
├── 03_ER_Diagram_1.pdf       # Relational database schema diagram
├── 04_Schema_DDL.sql         # Table creation DDL statements
├── 05_insert_data.sql        # Database seed data DML
├── 06_KPI_Queries.sql        # Analytical SQL queries
├── README.md                 # Technical documentation
└── setup_db.py               # Python setup script to build construction_project.db
```

### Execution Commands

```bash
# 1. Rebuild SQLite database
python setup_db.py

# 2. Run Data Preparation & Imputation Pipeline
python 01_Database_EDA.py

# 3. Execute SQL KPI Queries
python -c "import sqlite3; conn=sqlite3.connect('construction_project.db'); print(conn.cursor().execute(open('06_KPI_Queries.sql').read()).fetchall())"
```

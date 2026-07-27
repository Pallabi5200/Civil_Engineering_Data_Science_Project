# SQL Analytics & Business KPI Engine (`SQL/`)

This directory contains production-ready SQL scripts that extract operational, financial, and quality compliance metrics from normalized relational tables in the Construction Intelligence Database (`construction_project.db`).

Each script addresses a core infrastructure business problem—such as monitoring project cashflow, auditing vendor cost commitments, and verifying structural quality standards—using modern ANSI SQL patterns (Window Functions, Common Table Expressions, and Conditional Aggregations).

---

## Analytical Query Modules

### 1. Cumulative Cashflow & Billing Trajectory (`01_cashflow_trajectory.sql`)

#### Business Context
In civil engineering projects, contractors bill clients in progressive milestones (e.g., foundation excavation, rebar casting, final grouting). Tracking single invoice amounts isn't enough—project managers need to monitor the **chronological cumulative cash inflow** per project to manage working capital and prevent cash flow bottlenecks.

#### SQL Technical Implementation
* **Joins**: Connects `Projects`, `Work_Orders`, and `Tax_Invoices` along primary/foreign key relationships (`project_id` and `work_order_id`).
* **Window Aggregation**: Computes a cumulative running sum using `SUM(ti.net_payable_amount) OVER (PARTITION BY p.project_name ORDER BY ti.invoice_date)`.
* **Partitioning & Ordering**: `PARTITION BY p.project_name` guarantees that running totals reset independently for each project. `ORDER BY ti.invoice_date` forces the window frame to compute an ascending chronological running sum.

```sql
SELECT 
    p.project_name, 
    ti.invoice_number, 
    ti.invoice_date, 
    ti.net_payable_amount,
    SUM(ti.net_payable_amount) OVER (
        PARTITION BY p.project_name 
        ORDER BY ti.invoice_date
    ) AS cumulative_billed_amount
FROM Projects p
JOIN Work_Orders wo ON p.project_id = wo.project_id
JOIN Tax_Invoices ti ON ti.work_order_id = wo.work_order_id;
```

#### Query Execution Results
When executed against `construction_project.db`, the query returns:

| Project Name | Invoice Number | Invoice Date | Net Payable Amount | Cumulative Billed Amount |
| :--- | :--- | :--- | :--- | :--- |
| Renew WTG Grouting Repair - Molagavali | `TI-PMPL-GROUT-01` | 2026-03-28 | ₹5,16,250.00 | **₹5,16,250.00** |
| WTG Foundation Retrofitting - GAL33 | `TI-PMPL-GAL33-01` | 2026-02-15 | ₹4,55,049.30 | **₹4,55,049.30** |
| WTG Foundation Retrofitting - GAL33 | `TI-PMPL-GAL33-03` | 2026-03-20 | ₹9,10,098.60 | **₹13,65,147.90** |

#### Key Engineering & Financial Insights
1. **Milestone Acceleration**: For *WTG Foundation Retrofitting - GAL33*, billing grew from **₹4.55L** in Feb 2026 to a cumulative **₹13.65L** by late March 2026, reflecting a 200% increase in verified site deliverables between Milestone 1 and Milestone 2.
2. **Partition Reset Verification**: The running total for *Renew WTG Grouting Repair* cleanly initialized at **₹5.16L**, confirming zero data bleed between independent commercial contracts.

---

### 2. Vendor Cost Commitment Ratio & Overrun Risk (`02_vendor_risk_cte.sql`)

#### Business Context
When executing EPC (Engineering, Procurement, and Construction) contracts, project managers issue Purchase Orders (POs) to sub-contractors for material procurement and specialized labor. If total PO commitments approach or exceed the client Work Order value, the project faces severe margin erosion or budget overruns.

#### SQL Technical Implementation
* **Common Table Expression (CTE)**: Uses `WITH VendorCommitments AS (...)` to pre-aggregate PO expenses by `project_id`. This eliminates **table fan-out**—a common SQL bug where joining multi-row transaction tables directly duplicates parent contract values.
* **Derived Percentage Calculation**: Computes `(vc.total_po_commitment * 100.0 / wo.total_contract_value)` to derive the cost commitment ratio.
* **Conditional Categorization (`CASE`)**: Classifies projects into risk categories (`HIGH` > 80%, `MODERATE` > 50%, else `LOW`).

```sql
WITH VendorCommitments AS (
    SELECT 
        project_id,
        SUM(total_po_value) AS total_po_commitment
    FROM Purchase_Orders
    GROUP BY project_id
)
SELECT 
    p.project_name,
    wo.total_contract_value,
    vc.total_po_commitment,
    (vc.total_po_commitment * 100.0 / wo.total_contract_value) AS cost_commitment_ratio,
    CASE 
        WHEN (vc.total_po_commitment * 100.0 / wo.total_contract_value) > 80.0 THEN 'HIGH'
        WHEN (vc.total_po_commitment * 100.0 / wo.total_contract_value) > 50.0 THEN 'MODERATE'
        ELSE 'LOW'
    END AS risk_level
FROM Projects p
JOIN Work_Orders wo ON p.project_id = wo.project_id
JOIN VendorCommitments vc ON p.project_id = vc.project_id;
```

#### Query Execution Results
When executed against `construction_project.db`, the query returns:

| Project Name | Total Contract Value | Total PO Commitment | Cost Commitment Ratio (%) | Risk Level |
| :--- | :--- | :--- | :--- | :--- |
| WTG Foundation Retrofitting - GAL33 | ₹12,85,450.00 | ₹12,85,450.00 | 100.0% | **HIGH** |
| Renew Hazardous Waste Storage Shed 5x6m - Otha Ph 3 | ₹4,25,000.00 | ₹4,25,000.00 | 100.0% | **HIGH** |
| Renew Hazardous Storage Shed - Patan | ₹4,10,000.00 | ₹4,10,000.00 | 100.0% | **HIGH** |

#### Key Engineering & Financial Insights
1. **100% Commitment Flag**: All 3 active subprojects currently show a **100% PO commitment ratio**, indicating that sub-contractor purchase orders have been fully committed up to the client contract ceiling.
2. **Operational Risk Assessment**: Because commitments have reached 100%, any unbudgeted site variation orders or material price escalations will directly cause budget overruns unless a formal client variation order (VO) is approved.

---

### 3. Concrete Quality Compliance & Pass Rate Analytics (`03_quality_pass_rate.sql`)

#### Business Context
On civil infrastructure sites (such as wind turbine foundation retrofitting and grouting operations), structural integrity is verified using compressive strength cube tests. For **M-40 grade structural concrete**, samples must reach a design strength of **$\ge 40.0 \text{ MPa}$**. Quality Assurance (QA/QC) leaders require automated site-level compliance reporting to track pass rates, identify defective batches early, and ensure compliance with structural engineering standards (IS 456 / BS 8110).

#### SQL Technical Implementation
* **Single-Pass Conditional Aggregation**: Utilizes `SUM(CASE WHEN ql.cube_test_result_mpa >= 40.0 THEN 1 ELSE 0 END)` and `SUM(CASE WHEN ql.cube_test_result_mpa < 40.0 THEN 1 ELSE 0 END)` to evaluate pass/fail criteria in a single table scan, avoiding redundant subqueries or multiple `JOIN` operations.
* **Derived Pass Rate KPI**: Computes the percentage pass rate using `ROUND(SUM(...) * 100.0 / COUNT(*), 2)`.
* **Relational Grouping**: Connects `Projects` (`p`) to `Field_Quality_Logs` (`ql`) via `project_id`, aggregating records by `p.project_name`.

```sql
SELECT 
    p.project_name, 
    COUNT(*) AS total_tests,
    SUM(CASE WHEN ql.cube_test_result_mpa >= 40.0 THEN 1 ELSE 0 END) AS passed_tests,
    SUM(CASE WHEN ql.cube_test_result_mpa < 40.0 THEN 1 ELSE 0 END) AS failed_tests,
    ROUND(SUM(CASE WHEN ql.cube_test_result_mpa >= 40.0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pass_rate_pct,
    ROUND(AVG(ql.cube_test_result_mpa), 2) AS avg_strength_mpa
FROM Projects p 
JOIN Field_Quality_Logs AS ql ON p.project_id = ql.project_id
GROUP BY p.project_name;
```

#### Query Execution Results
When executed against `construction_project.db`, the query returns:

| Project Name | Total Tests | Passed Tests | Failed Tests | Pass Rate (%) | Avg Strength (MPa) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Renew WTG Grouting Repair - Molagavali | 1 | 1 | 0 | **100.0%** | 58.40 |
| WTG Foundation Retrofitting - GAL06 | 2 | 1 | 1 | **50.0%** | 36.80 |
| WTG Foundation Retrofitting - GAL07 | 2 | 1 | 1 | **50.0%** | 38.65 |
| WTG Foundation Retrofitting - GAL33 | 2 | 1 | 1 | **50.0%** | 38.35 |

#### Key Engineering & Quality Control Insights
1. **High-Performance Grouting**: The *Renew WTG Grouting Repair* project shows a **100% pass rate** with an exceptional average compressive strength of **58.40 MPa**, well exceeding the 40.0 MPa target due to high-strength epoxy grout specification (Fosroc Nitomortar).
2. **Curing Timeline Variance Analysis**: The retrofitting sites (GAL06, GAL07, GAL33) show a **50.0% pass rate**. Domain analysis reveals this is driven by test scheduling: each site records one **7-day test** ($\approx 30.5 - 32.1 \text{ MPa}$) and one **28-day test** ($\approx 43.1 - 45.2 \text{ MPa}$). Evaluated statically against the final 28-day standard of $40.0 \text{ MPa}$, 7-day curing logs naturally fall below threshold, highlighting an opportunity for future query enhancement to partition compliance thresholds by curing duration (`activity_type`).

---

## 🚀 How to Run Queries

You can execute any SQL script directly from the project root using the provided CLI helper runner:

```bash
# Run Challenge 1: Cumulative Cashflow Trajectory
python SQL/run_sql.py SQL/01_cashflow_trajectory.sql

# Run Challenge 2: Vendor Risk CTE
python SQL/run_sql.py SQL/02_vendor_risk_cte.sql

# Run Challenge 3: Quality Compliance Pass Rates
python SQL/run_sql.py SQL/03_quality_pass_rate.sql
```

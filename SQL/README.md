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

### 3. Concrete Quality Compliance Pass Rates (`03_quality_pass_rate.sql`)
*(In Progress — Conditional aggregations of 7-day vs 28-day concrete cube test results)*

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

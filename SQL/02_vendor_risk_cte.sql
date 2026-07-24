-- 02_vendor_risk_cte.sql
-- Objective: Calculate vendor purchase order commitment ratio against client contract value
-- SQL Technique: Common Table Expressions (CTE), Foreign Key Joins, and Conditional CASE Statements

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
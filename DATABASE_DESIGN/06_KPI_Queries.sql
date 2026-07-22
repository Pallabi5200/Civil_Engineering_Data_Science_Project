SELECT p.project_name, wo.work_order_number, wo.total_contract_value,
SUM(ti.net_payable_amount) AS total_billed_amount,
(SUM(ti.net_payable_amount)/wo.total_contract_value)*100 AS billing_percentage
FROM Projects p
JOIN Work_Orders wo
ON wo.project_id = p.project_id
JOIN Tax_Invoices ti
ON  wo.work_order_id = ti.work_order_id
WHERE p.project_name = 'WTG Foundation Retrofitting - GAL33'
GROUP BY p.project_name, wo.work_order_number, wo.total_contract_value;


SELECT inspection_date, activity_type, cube_test_result_mpa,
CASE 
    WHEN cube_test_result_mpa >= 40.00 THEN 'PASS'
    WHEN activity_type LIKE '%7-Day%' THEN 'PENDING_7DAY'
    ELSE 'FAIL'
END AS quality_check
FROM Field_Quality_Logs
WHERE project_id='PRJ-GAL33';


SELECT item_code, description_of_work, unit_of_measurement, estimated_quantity, unit_rate, estimated_total_cost
FROM BOQ_Items
WHERE work_order_id = 'WO-MSUM-01'
ORDER BY estimated_total_cost DESC;


SELECT p.project_name, ti.invoice_number, ti.invoice_date, ti.net_payable_amount,
SUM(ti.net_payable_amount) OVER (
    PARTITION BY p.project_name
    ORDER BY ti.invoice_date
) AS cumulative_billing
FROM Projects p
JOIN Work_Orders wo ON p.project_id = wo.project_id
JOIN Tax_Invoices ti ON wo.work_order_id = ti.work_order_id
WHERE p.project_name = 'WTG Foundation Retrofitting - GAL33';



SELECT project_id, COUNT(*) AS total_test,
SUM(CASE WHEN cube_test_result_mpa >= 40.00 THEN 1 ELSE 0 END) AS passed_tests,
(SUM(CASE WHEN cube_test_result_mpa >= 40.00 THEN 1 ELSE 0 END)*100.0/COUNT(*)) AS pass_percentage
FROM Field_Quality_Logs
GROUP BY project_id;

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

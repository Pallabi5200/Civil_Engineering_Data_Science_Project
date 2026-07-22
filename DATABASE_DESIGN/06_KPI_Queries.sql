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

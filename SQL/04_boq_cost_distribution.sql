SELECT p.project_name, boq.description_of_work, boq.unit_rate, boq.estimated_quantity,
boq.estimated_total_cost,
(ROUND(boq.estimated_total_cost * 100.0 / wo.total_contract_value,2)) AS boq_cost_share_pct
FROM Projects p
JOIN Work_Orders wo
ON wo.project_id = p.project_id
JOIN BOQ_Items boq
ON boq.work_order_id = wo.work_order_id
WHERE boq.estimated_total_cost >= 50000.0
ORDER BY boq.estimated_total_cost DESC;
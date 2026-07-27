-- 05_top_items_per_project.sql
WITH RankedItems AS (
    SELECT p.project_name, boq.description_of_work, boq.estimated_total_cost,
    DENSE_RANK() OVER (PARTITION BY p.project_name ORDER BY boq.estimated_total_cost DESC) AS item_rank
    FROM Projects p JOIN Work_Orders wo ON p.project_id = wo.project_id
    JOIN BOQ_Items boq ON wo.work_order_id = boq.work_order_id
)
SELECT * 
FROM RankedItems
WHERE item_rank <= 2;

SELECT p.project_name, ti.invoice_number, ti.invoice_date, ti.net_payable_amount,
SUM(ti.net_payable_amount) OVER (PARTITION BY p.project_name ORDER BY ti.invoice_date)
AS cumulative_billed_amount
FROM Projects p
JOIN Work_Orders wo
ON p.project_id = wo.project_id
JOIN Tax_Invoices ti
ON ti.work_order_id = wo.work_order_id;
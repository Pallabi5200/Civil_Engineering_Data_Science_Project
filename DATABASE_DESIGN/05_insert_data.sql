-- 05_insert_data.sql

-- Level 0: Parent Tables
INSERT INTO Clients (client_id, client_name, billing_address, gstin, pan_number) VALUES
('CL-MSUM', 'Maharaja Shree Umaid Mills Ltd', 'MSUM Mill Gate, Jodhpur Road, Pali, Rajasthan 306401', '08AABCM1849B1ZS', 'AABCM1849B');

INSERT INTO Vendors (vendor_id, vendor_name, vendor_code, gstin, vendor_type) VALUES
('VEN-DYW', 'Dywidag Bridgecon India Private Limited', 'DYW-DELHI-01', '09AAFCD3018D1Z2', 'Material Supplier'),
('VEN-DIS', 'Disan Infra Pvt Ltd', 'DIS-MAAN-01', '27ABCDE1234F1Z1', 'Concrete Supplier'),
('VEN-FOS', 'Fosroc Chemicals (India) Pvt Ltd', 'FOS-ANK-01', '24AAAAA0000A1Z0', 'Chemical Supplier');

-- Level 1: Projects
INSERT INTO Projects (project_id, client_id, project_name, site_location, state, structure_type, start_date, delivery_deadline) VALUES
('PRJ-GAL33', 'CL-MSUM', 'WTG Foundation Retrofitting - GAL33', 'Village Altur, Kotoli, Karungale, Taluka Shahuwadi, Kolhapur', 'Maharashtra', 'Wind Turbine Foundation', '2025-09-11', '2025-12-31');

-- Level 2: Work Orders & Purchase Orders
INSERT INTO Work_Orders (work_order_id, work_order_number, project_id, issue_date, total_contract_value, payment_terms_description) VALUES
('WO-MSUM-01', 'MSUM/PWEPL/25-26/WO/01', 'PRJ-GAL33', '2025-09-11', 4855608.00, '40% advance against PO & Proforma Invoice, 25% post chipping/drilling/grouting, 20% post steel & concreting, 10% post completion, 5% retention');

INSERT INTO Purchase_Orders (po_id, po_number, project_id, vendor_id, issue_date, total_po_value, delivery_deadline_date) VALUES
('PO-DYW-01', 'PIPL/DSI/4/25-26', 'PRJ-GAL33', 'VEN-DYW', '2025-10-08', 507402.00, '2025-10-29');

-- Level 3: Invoices & Quality Logs
INSERT INTO Proforma_Invoices (proforma_invoice_id, pfi_number, po_id, issue_date, requested_advance_amount, gst_amount, gross_total_value) VALUES
('PFI-GAL33-01', 'PIPL/PRO/GAL33/MH/1', 'PO-DYW-01', '2025-09-22', 1942243.20, 349603.78, 2291846.98);

INSERT INTO Tax_Invoices (invoice_id, invoice_number, invoice_date, work_order_id, milestone_percentage_billed, taxable_value, cgst_amount, sgst_amount, igst_amount, net_payable_amount) VALUES
('INV-GAL33-01', 'PIPL/GAL33/MH/1', '2026-02-15', 'WO-MSUM-01', 40.00, 1942243.00, 0.00, 0.00, 349604.00, 2291847.00);

INSERT INTO Field_Quality_Logs (quality_log_id, project_id, activity_type, inspection_date, cube_test_result_mpa, ndt_ultrasonic_velocity, status) VALUES
('QL-GAL33-01', 'PRJ-GAL33', '7-Day Cube Strength Test (M-40)', '2026-02-21', 31.96, NULL, 'Approved'),
('QL-GAL33-02', 'PRJ-GAL33', '28-Day Cube Strength Test (M-40)', '2026-03-14', 44.74, NULL, 'Approved');

-- Level 3: BOQ Line Items (Linked to WO-MSUM-01)
INSERT INTO BOQ_Items (boq_item_id, work_order_id, item_code, description_of_work, unit_of_measurement, estimated_quantity, unit_rate, estimated_total_cost, sac_code) VALUES
('BOQ-GAL33-010', 'WO-MSUM-01', 'POS-10', 'Excavation for foundation strengthening', 'CUM', 321.000, 450.00, 144450.00, '995428'),
('BOQ-GAL33-020', 'WO-MSUM-01', 'POS-20', 'UPV test to find depth of crack & consultant visit', 'LS', 1.000, 25000.00, 25000.00, '995428'),
('BOQ-GAL33-030', 'WO-MSUM-01', 'POS-30', 'Surface chipping of concrete raft/pedestal', 'SQM', 149.000, 350.00, 52150.00, '995428'),
('BOQ-GAL33-040', 'WO-MSUM-01', 'POS-40', 'Pedestal demolition work', 'CUM', 3.000, 4200.00, 12600.00, '995428'),
('BOQ-GAL33-060', 'WO-MSUM-01', 'POS-60', 'Pressure grouting holes in raft', 'NOS', 1564.000, 120.00, 187680.00, '995428'),
('BOQ-GAL33-120', 'WO-MSUM-01', 'POS-120', 'Pressure grouting through nozzles using Conbextra EP 10 Epoxy grout', 'KGS', 115.000, 650.00, 74750.00, '995428'),
('BOQ-GAL33-180', 'WO-MSUM-01', 'POS-180', 'Steel Work as per BBS (16mm & 20mm dia)', 'MT', 9.545, 85000.00, 811325.00, '995428'),
('BOQ-GAL33-210', 'WO-MSUM-01', 'POS-210', 'Concreting in pedestal region (C30/M37 outside)', 'CUM', 98.500, 6800.00, 669800.00, '995428');

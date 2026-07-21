import sqlite3
import os

# Define the database path
db_path = "construction_project.db"

# Remove the old database file if you want a clean slate every time you run it
if os.path.exists(db_path):
    os.remove(db_path)

# Connect to SQLite (this will create the file automatically)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Enable foreign key support in SQLite (crucial for relational integrity)
cursor.execute("PRAGMA foreign_keys = ON;")

print("--- Step 1: Creating All 12 Tables from Schema ---")

# 1. Execute your complete 12-table DDL script
cursor.executescript("""
CREATE TABLE Clients (
    client_id VARCHAR(50) PRIMARY KEY,
    client_name VARCHAR(255) NOT NULL,
    billing_address TEXT NOT NULL,
    gstin CHAR(15) NOT NULL,
    pan_number CHAR(10) NOT NULL
);

CREATE TABLE Vendors (
    vendor_id VARCHAR(50) PRIMARY KEY,
    vendor_name VARCHAR(255) NOT NULL,
    vendor_code VARCHAR(50) NOT NULL,
    gstin CHAR(15) NOT NULL,
    vendor_type VARCHAR(100) NOT NULL
);

CREATE TABLE Materials (
    material_id VARCHAR(50) PRIMARY KEY,
    material_name VARCHAR(255) NOT NULL,
    manufacturer_name VARCHAR(255) NOT NULL,
    technical_property_summary TEXT,
    standard_coverage_rate VARCHAR(100)
);

CREATE TABLE Projects (
    project_id VARCHAR(50) PRIMARY KEY,
    client_id VARCHAR(50) NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    site_location VARCHAR(255) NOT NULL,
    state VARCHAR(100) NOT NULL,
    structure_type VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    delivery_deadline DATE NOT NULL,
    FOREIGN KEY (client_id) REFERENCES Clients(client_id)
);

CREATE TABLE Work_Orders(
    work_order_id VARCHAR(50) PRIMARY KEY,
    work_order_number VARCHAR(100) NOT NULL,
    project_id VARCHAR(50) NOT NULL,
    issue_date DATE NOT NULL,
    total_contract_value DECIMAL(15,2) NOT NULL,
    payment_terms_description TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id) 
);

CREATE TABLE Purchase_Orders(
    po_id VARCHAR(50) PRIMARY KEY,
    po_number VARCHAR(100) NOT NULL,
    project_id VARCHAR(50) NOT NULL,
    vendor_id VARCHAR(50) NOT NULL,
    issue_date DATE NOT NULL,
    total_contract_value DECIMAL(15,2) NOT NULL,
    delivery_deadline_date DATE NOT NULL,
    FOREIGN KEY (vendor_id) REFERENCES Vendors(vendor_id),
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);

CREATE TABLE Proforma_Invoices(
    proforma_invoice_id VARCHAR(50) PRIMARY KEY,
    pfi_number VARCHAR(100) NOT NULL,
    po_id VARCHAR(50) NOT NULL,
    issue_date DATE NOT NULL,
    requested_advance_amount DECIMAL(15,2) NOT NULL,
    gst_amount DECIMAL(15,2) NOT NULL,
    gross_total_value DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (po_id) REFERENCES Purchase_Orders(po_id)
);

CREATE TABLE Tax_Invoices(
    invoice_id VARCHAR(50) PRIMARY KEY,
    invoice_number VARCHAR(100) NOT NULL,
    invoice_date DATE NOT NULL,
    work_order_id VARCHAR(50) NOT NULL,
    total_invoice_value DECIMAL(15,2) NOT NULL,
    milestone_percentage_billed DECIMAL(5,2) NOT NULL,
    taxable_value DECIMAL(15,2) NOT NULL,
    cgst_amount DECIMAL(15,2) NOT NULL,
    sgst_amount DECIMAL(15,2) NOT NULL,
    igst_amount DECIMAL(15,2) NOT NULL,
    net_payable_amount DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (work_order_id) REFERENCES Work_Orders(work_order_id)
);

CREATE TABLE BOQ_Items (
    boq_item_id VARCHAR(50) PRIMARY KEY,
    work_order_id VARCHAR(50) NOT NULL,
    item_code VARCHAR(50) NOT NULL,
    description_of_work TEXT NOT NULL,
    unit_of_measurement VARCHAR(20) NOT NULL,
    estimated_quantity DECIMAL(12,3) NOT NULL,
    unit_rate DECIMAL(12,2) NOT NULL,
    estimated_total_cost DECIMAL(15,2) NOT NULL,
    sac_code CHAR(6) NOT NULL,
    FOREIGN KEY (work_order_id) REFERENCES Work_Orders(work_order_id)
);

CREATE TABLE WCC_Records (
    wcc_id VARCHAR(50) PRIMARY KEY,
    wcc_number VARCHAR(100) NOT NULL,
    work_order_id VARCHAR(50) NOT NULL,
    work_start_date DATE NOT NULL,
    work_completion_date DATE NOT NULL,
    quantity_completed_verified DECIMAL(12,3) NOT NULL,
    is_additional_work_included BOOLEAN NOT NULL,
    FOREIGN KEY (work_order_id) REFERENCES Work_Orders(work_order_id)
);

CREATE TABLE Field_Quality_Logs (
    quality_log_id VARCHAR(50) PRIMARY KEY,
    project_id VARCHAR(50) NOT NULL,
    activity_type VARCHAR(100) NOT NULL,
    inspection_date DATE NOT NULL,
    cube_test_result_mpa DECIMAL(5,2),
    ndt_ultrasonic_velocity INT,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);

CREATE TABLE Damage_Reports (
    damage_report_id VARCHAR(50) PRIMARY KEY,
    project_id VARCHAR(50) NOT NULL,
    turbine_number VARCHAR(50) NOT NULL,
    turbine_model VARCHAR(100) NOT NULL,
    nature_of_damage VARCHAR(255) NOT NULL,
    damaged_length_approx DECIMAL(10,2) NOT NULL,
    severity_rating INT NOT NULL,
    repair_recommendation TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);
""")

print("All 12 tables created successfully!\n")

print("--- Step 2: Inserting Dummy Data Across All 12 Tables ---")

# 1. Level 0: Independent Parents
cursor.execute("""
INSERT INTO Clients (client_id, client_name, billing_address, gstin, pan_number) VALUES
('CL-001', 'Apex Infrastructure Ltd', '12 Business Bay, Mumbai, MH', '27AAAAA0000A1Z5', 'AAAAA0000A'),
('CL-002', 'Metro Urban Builders', '45 Ring Road, Pune, MH', '27BBBBB1111B1Z6', 'BBBBB1111B');
""")

cursor.execute("""
INSERT INTO Vendors (vendor_id, vendor_name, vendor_code, gstin, vendor_type) VALUES
('VEN-001', 'SteelCorp India', 'SC-IND-01', '27CCCCC2222C1Z7', 'Material Supplier'),
('VEN-002', 'Apex Ready Mix Concrete', 'ARM-PUNE-02', '27DDDDD3333D1Z8', 'Subcontractor');
""")

cursor.execute("""
INSERT INTO Materials (material_id, material_name, manufacturer_name, technical_property_summary, standard_coverage_rate) VALUES
('MAT-001', 'OPC 53 Grade Cement', 'UltraTech', 'High early strength grey cement', '1.2 bags/sqm'),
('MAT-002', 'Fe 500D TMT Rebar', 'Tata Tiscon', 'High ductility reinforcement steel', '7850 kg/cum');
""")

# 2. Level 1: Projects (Depends on Clients)
cursor.execute("""
INSERT INTO Projects (project_id, client_id, project_name, site_location, state, structure_type, start_date, delivery_deadline) VALUES
('PRJ-101', 'CL-001', 'Amanora Commercial Tower', 'Amanora Park Town, Pune', 'Maharashtra', 'Commercial High-Rise', '2026-01-15', '2027-12-31'),
('PRJ-102', 'CL-002', 'Metro Residential Complex', 'Hadapsar, Pune', 'Maharashtra', 'Residential Apartments', '2026-03-01', '2028-06-30');
""")

# 3. Level 2: Work_Orders & Purchase_Orders (Depends on Projects & Vendors)
cursor.execute("""
INSERT INTO Work_Orders (work_order_id, work_order_number, project_id, issue_date, total_contract_value, payment_terms_description) VALUES
('WO-501', 'WO/2026/001', 'PRJ-101', '2026-01-20', 15000000.00, 'Net 30 days upon milestone completion'),
('WO-502', 'WO/2026/002', 'PRJ-102', '2026-03-05', 8500000.00, '50% advance, 50% upon structural capping');
""")

cursor.execute("""
INSERT INTO Purchase_Orders (po_id, po_number, project_id, vendor_id, issue_date, total_contract_value, delivery_deadline_date) VALUES
('PO-901', 'PO/SC/2026/01', 'PRJ-101', 'VEN-001', '2026-01-25', 4500000.00, '2026-04-30'),
('PO-902', 'PO/ARM/2026/02', 'PRJ-102', 'VEN-002', '2026-03-10', 2200000.00, '2026-05-15');
""")

# 4. Level 3: Dependent Records (Invoices, BOQ, WCC, Quality Logs, Damage Reports)
cursor.execute("""
INSERT INTO Proforma_Invoices (proforma_invoice_id, pfi_number, po_id, issue_date, requested_advance_amount, gst_amount, gross_total_value) VALUES
('PFI-001', 'PFI/2026/001', 'PO-901', '2026-01-26', 1000000.00, 180000.00, 1180000.00);
""")

cursor.execute("""
INSERT INTO Tax_Invoices (invoice_id, invoice_number, invoice_date, work_order_id, total_invoice_value, milestone_percentage_billed, taxable_value, cgst_amount, sgst_amount, igst_amount, net_payable_amount) VALUES
('INV-001', 'INV/2026/001', '2026-02-15', 'WO-501', 4425000.00, 25.00, 3750000.00, 337500.00, 337500.00, 0.00, 4425000.00);
""")

cursor.execute("""
INSERT INTO BOQ_Items (boq_item_id, work_order_id, item_code, description_of_work, unit_of_measurement, estimated_quantity, unit_rate, estimated_total_cost, sac_code) VALUES
('BOQ-001', 'WO-501', 'ITEM-01', 'RCC Foundation Puring', 'CUM', 1250.500, 4500.00, 5627250.00, '995411');
""")

cursor.execute("""
INSERT INTO WCC_Records (wcc_id, wcc_number, work_order_id, work_start_date, work_completion_date, quantity_completed_verified, is_additional_work_included) VALUES
('WCC-001', 'WCC/2026/01', 'WO-501', '2026-01-22', '2026-02-10', 1250.500, 0);
""")

cursor.execute("""
INSERT INTO Field_Quality_Logs (quality_log_id, project_id, activity_type, inspection_date, cube_test_result_mpa, ndt_ultrasonic_velocity, status) VALUES
('QL-001', 'PRJ-101', 'Foundation Cube Test', '2026-02-05', 54.50, 4800, 'Approved');
""")

cursor.execute("""
INSERT INTO Damage_Reports (damage_report_id, project_id, turbine_number, turbine_model, nature_of_damage, damaged_length_approx, severity_rating, repair_recommendation) VALUES
('DR-001', 'PRJ-101', 'TURB-04', 'V120-2.2MW', 'Surface hairline cracking on tower base', 1.50, 2, 'Apply epoxy resin injection');
""")

conn.commit()
print("All dummy records across all 12 tables inserted successfully!\n")

print("--- Step 3: Verifying Data via Multi-Table JOIN Query ---")
cursor.execute("""
SELECT p.project_name, c.client_name, w.work_order_number, b.description_of_work, f.status 
FROM Projects p
JOIN Clients c ON p.client_id = c.client_id
JOIN Work_Orders w ON p.project_id = w.project_id
JOIN BOQ_Items b ON w.work_order_id = b.work_order_id
JOIN Field_Quality_Logs f ON p.project_id = f.project_id;
""")

results = cursor.fetchall()
for row in results:
    print(f"Project: {row[0]} | Client: {row[1]} | WO Number: {row[2]} | BOQ Task: {row[3]} | Quality Status: {row[4]}")

conn.close()
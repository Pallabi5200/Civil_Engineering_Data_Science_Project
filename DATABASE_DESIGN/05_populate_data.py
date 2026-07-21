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

print("--- Step 1: Creating Tables from Schema ---")

# 1. Execute your exact DDL script
cursor.executescript("""
CREATE TABLE Clients (
    client_id VARCHAR(50) PRIMARY KEY,
    client_name VARCHAR(255) NOT NULL,
    billing_address TEXT NOT NULL,
    gstin CHAR(15) NOT NULL,
    pan_number CHAR(10) NOT NULL
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

CREATE TABLE Vendors(
    vendor_id VARCHAR(50) PRIMARY KEY,
    vendor_name VARCHAR(255) NOT NULL,
    vendor_code VARCHAR(50) NOT NULL,
    gstin CHAR(15) NOT NULL,
    vendor_type VARCHAR(100) NOT NULL
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
""")

print("Tables created successfully!\n")

print("--- Step 2: Inserting Dummy Data (Top-Down Order) ---")

# 1. Insert Parents: Clients
cursor.execute("""
INSERT INTO Clients (client_id, client_name, billing_address, gstin, pan_number) VALUES
('CL-001', 'Apex Infrastructure Ltd', '12 Business Bay, Mumbai, MH', '27AAAAA0000A1Z5', 'AAAAA0000A'),
('CL-002', 'Metro Urban Builders', '45 Ring Road, Pune, MH', '27BBBBB1111B1Z6', 'BBBBB1111B');
""")

# 2. Insert Parents: Vendors
cursor.execute("""
INSERT INTO Vendors (vendor_id, vendor_name, vendor_code, gstin, vendor_type) VALUES
('VEN-001', 'SteelCorp India', 'SC-IND-01', '27CCCCC2222C1Z7', 'Material Supplier'),
('VEN-002', 'Apex Ready Mix Concrete', 'ARM-PUNE-02', '27DDDDD3333D1Z8', 'Subcontractor');
""")

# 3. Insert Children: Projects (depends on Clients)
cursor.execute("""
INSERT INTO Projects (project_id, client_id, project_name, site_location, state, structure_type, start_date, delivery_deadline) VALUES
('PRJ-101', 'CL-001', 'Amanora Commercial Tower', 'Amanora Park Town, Pune', 'Maharashtra', 'Commercial High-Rise', '2026-01-15', '2027-12-31'),
('PRJ-102', 'CL-002', 'Metro Residential Complex', 'Hadapsar, Pune', 'Maharashtra', 'Residential Apartments', '2026-03-01', '2028-06-30');
""")

# 4. Insert Grandchildren: Work_Orders (depends on Projects)
cursor.execute("""
INSERT INTO Work_Orders (work_order_id, work_order_number, project_id, issue_date, total_contract_value, payment_terms_description) VALUES
('WO-501', 'WO/2026/001', 'PRJ-101', '2026-01-20', 15000000.00, 'Net 30 days upon milestone completion'),
('WO-502', 'WO/2026/002', 'PRJ-102', '2026-03-05', 8500000.00, '50% advance, 50% upon structural capping');
""")

# 5. Insert Grandchildren: Purchase_Orders (depends on Projects and Vendors)
cursor.execute("""
INSERT INTO Purchase_Orders (po_id, po_number, project_id, vendor_id, issue_date, total_contract_value, delivery_deadline_date) VALUES
('PO-901', 'PO/SC/2026/01', 'PRJ-101', 'VEN-001', '2026-01-25', 4500000.00, '2026-04-30'),
('PO-902', 'PO/ARM/2026/02', 'PRJ-102', 'VEN-002', '2026-03-10', 2200000.00, '2026-05-15');
""")

# Commit the transaction and close connection
conn.commit()
print("All dummy records inserted successfully!\n")

print("--- Step 3: Verifying Data via Query ---")
cursor.execute("""
SELECT p.project_name, c.client_name, w.work_order_number, w.total_contract_value 
FROM Projects p
JOIN Clients c ON p.client_id = c.client_id
JOIN Work_Orders w ON p.project_id = w.project_id;
""")

results = cursor.fetchall()
for row in results:
    print(f"Project: {row[0]} | Client: {row[1]} | WO Number: {row[2]} | Value: {row[3]}")

conn.close()
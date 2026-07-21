-- 04_Schema_DDL.sql
CREATE TABLE IF NOT EXISTS Clients (
    client_id VARCHAR(50) PRIMARY KEY,
    client_name VARCHAR(255) NOT NULL,
    billing_address TEXT NOT NULL,
    gstin CHAR(15) NOT NULL,
    pan_number CHAR(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS Vendors (
    vendor_id VARCHAR(50) PRIMARY KEY,
    vendor_name VARCHAR(255) NOT NULL,
    vendor_code VARCHAR(50) NOT NULL,
    gstin CHAR(15) NOT NULL,
    vendor_type VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Materials (
    material_id VARCHAR(50) PRIMARY KEY,
    material_name VARCHAR(255) NOT NULL,
    manufacturer_name VARCHAR(255) NOT NULL,
    technical_property_summary TEXT,
    standard_coverage_rate VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Projects (
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

CREATE TABLE IF NOT EXISTS Work_Orders (
    work_order_id VARCHAR(50) PRIMARY KEY,
    work_order_number VARCHAR(100) NOT NULL,
    project_id VARCHAR(50) NOT NULL,
    issue_date DATE NOT NULL,
    total_contract_value DECIMAL(15,2) NOT NULL,
    payment_terms_description TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);

CREATE TABLE IF NOT EXISTS Purchase_Orders (
    po_id VARCHAR(50) PRIMARY KEY,
    po_number VARCHAR(100) NOT NULL,
    project_id VARCHAR(50) NOT NULL,
    vendor_id VARCHAR(50) NOT NULL,
    issue_date DATE NOT NULL,
    total_po_value DECIMAL(15,2) NOT NULL,
    delivery_deadline_date DATE NOT NULL,
    FOREIGN KEY (vendor_id) REFERENCES Vendors(vendor_id),
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);

CREATE TABLE IF NOT EXISTS Proforma_Invoices (
    proforma_invoice_id VARCHAR(50) PRIMARY KEY,
    pfi_number VARCHAR(100) NOT NULL,
    po_id VARCHAR(50) NOT NULL,
    issue_date DATE NOT NULL,
    requested_advance_amount DECIMAL(15,2) NOT NULL,
    gst_amount DECIMAL(15,2) NOT NULL,
    gross_total_value DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (po_id) REFERENCES Purchase_Orders(po_id)
);

CREATE TABLE IF NOT EXISTS Tax_Invoices (
    invoice_id VARCHAR(50) PRIMARY KEY,
    invoice_number VARCHAR(100) NOT NULL,
    invoice_date DATE NOT NULL,
    work_order_id VARCHAR(50) NOT NULL,
    milestone_percentage_billed DECIMAL(5,2) NOT NULL,
    taxable_value DECIMAL(15,2) NOT NULL,
    cgst_amount DECIMAL(15,2) NOT NULL,
    sgst_amount DECIMAL(15,2) NOT NULL,
    igst_amount DECIMAL(15,2) NOT NULL,
    net_payable_amount DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (work_order_id) REFERENCES Work_Orders(work_order_id)
);

CREATE TABLE IF NOT EXISTS BOQ_Items (
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

CREATE TABLE IF NOT EXISTS WCC_Records (
    wcc_id VARCHAR(50) PRIMARY KEY,
    wcc_number VARCHAR(100) NOT NULL,
    work_order_id VARCHAR(50) NOT NULL,
    work_start_date DATE NOT NULL,
    work_completion_date DATE NOT NULL,
    quantity_completed_verified DECIMAL(12,3) NOT NULL,
    is_additional_work_included BOOLEAN NOT NULL,
    FOREIGN KEY (work_order_id) REFERENCES Work_Orders(work_order_id)
);

CREATE TABLE IF NOT EXISTS Field_Quality_Logs (
    quality_log_id VARCHAR(50) PRIMARY KEY,
    project_id VARCHAR(50) NOT NULL,
    activity_type VARCHAR(100) NOT NULL,
    inspection_date DATE NOT NULL,
    cube_test_result_mpa DECIMAL(5,2),
    ndt_ultrasonic_velocity INT,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);

CREATE TABLE IF NOT EXISTS Damage_Reports (
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
CREATE TABLE Clients (
    client_id VARCHAR(50) PRIMARY KEY,
    client_name VARCHAR(255) NOT NULL,
    billing_address TEXT NOT NULL,
    gstin CHAR(15) NOT NULL,
    pan_number CHAR(10) NOT NULL
);

CREATE TABLE Projects (
    project_id VARCHAR(50) PRIMARY KEY ,
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
    work_order_id VARCHAR(50) PRIMARY KEY ,
    work_order_number VARCHAR(100) NOT NULL,
    project_id VARCHAR(50) NOT NULL,
    issue_date DATE NOT NULL,
    total_contract_value DECIMAL(15,2) NOT NULL,
    payment_terms_description TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id) 
);


CREATE TABLE Vendors(
    vendor_id VARCHAR(50) PRIMARY KEY ,
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

import os
import sqlite3
import pandas as pd
import numpy as np

# 1. Base Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DB_PATH = os.path.join(BASE_DIR, "construction_project.db")
DDL_PATH = os.path.join(BASE_DIR, "04_Schema_DDL.sql")

print(" Starting Master Enterprise ETL Engine for ALL PMPL & RENEW Datasets...")

# 2. Reset & Re-create Database Schema
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = OFF;")
tables = [
    "Damage_Reports", "Field_Quality_Logs", "WCC_Records", "BOQ_Items",
    "Tax_Invoices", "Proforma_Invoices", "Purchase_Orders", "Work_Orders",
    "Projects", "Materials", "Vendors", "Clients"
]
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table};")

with open(DDL_PATH, "r") as f:
    cursor.executescript(f.read())

cursor.execute("PRAGMA foreign_keys = ON;")
conn.commit()
print(" Database Schema reset and initialized successfully.")

# ---------------------------------------------------------
# 3. Ingest Clients
# ---------------------------------------------------------
df_clients = pd.DataFrame([
    {
        "client_id": "CLI-MSUML",
        "client_name": "MSUML / Suzlon Energy Limited",
        "billing_address": "B-Wing, 151/6, Pune, Maharashtra - 411001",
        "gstin": "27AAACM1234A1Z1",
        "pan_number": "AAACM1234A"
    },
    {
        "client_id": "CLI-RENEW-GROUT",
        "client_name": "ReNew Power Private Limited (WTG Grouting Div)",
        "billing_address": "Molagavali-1 & Patan Wind Farms, Kurnool & Gujarat",
        "gstin": "37AABCR5678B1Z2",
        "pan_number": "AABCR5678B"
    },
    {
        "client_id": "CLI-RENEW-SHED",
        "client_name": "ReNew Power Private Limited (Infrastructure Div)",
        "billing_address": "Otha, Jaglur, Patan, Kudligi, Chikodi Sites",
        "gstin": "24AABCR5678B1Z3",
        "pan_number": "AABCR5678B"
    }
])
df_clients.to_sql("Clients", conn, if_exists="append", index=False)
print(f" Ingested {len(df_clients)} Clients.")

# ---------------------------------------------------------
# 4. Ingest Vendors
# ---------------------------------------------------------
df_vendors = pd.DataFrame([
    {
        "vendor_id": "VND-PMPL",
        "vendor_name": "PALLABI INFRACON PRIVATE LIMITED",
        "vendor_code": "PMPL-2026",
        "gstin": "27AAMCP2252J1Z6",
        "vendor_type": "Turnkey Civil Contractor"
    },
    {
        "vendor_id": "VND-SMR",
        "vendor_name": "SMR Technical Services",
        "vendor_code": "SMR-990",
        "gstin": "27AAACS9876C1Z9",
        "vendor_type": "Grouting & NDT Specialist"
    }
])
df_vendors.to_sql("Vendors", conn, if_exists="append", index=False)
print(f" Ingested {len(df_vendors)} Vendors.")

# ---------------------------------------------------------
# 5. Ingest Materials
# ---------------------------------------------------------
df_materials = pd.DataFrame([
    {
        "material_id": "MAT-CEMENT-M40",
        "material_name": "M-40 Characteristic Concrete Mix",
        "manufacturer_name": "UltraTech Cement",
        "technical_property_summary": "High performance 40 MPa characteristic compressive strength concrete mix with 0.38 W/C ratio.",
        "standard_coverage_rate": "1 m3 per m3 volume"
    },
    {
        "material_id": "MAT-EPOXY-GROUT",
        "material_name": "Low Viscosity Epoxy Grout (Fosroc Nitomortar)",
        "manufacturer_name": "Fosroc Chemicals",
        "technical_property_summary": "High strength epoxy resin grout for WTG foundation crack repair and pedestal grouting.",
        "standard_coverage_rate": "1.8 kg/L"
    },
    {
        "material_id": "MAT-COATING-PU",
        "material_name": "Nitocote UR512 PU Protective Coating",
        "manufacturer_name": "Fosroc Chemicals",
        "technical_property_summary": "UV resistant aliphatic polyurethane protective coating for concrete structures.",
        "standard_coverage_rate": "6.0 m2/L"
    },
    {
        "material_id": "MAT-STEEL-STUD",
        "material_name": "High Tensile Steel Studs M40",
        "manufacturer_name": "Tata Steel",
        "technical_property_summary": "Grade 8.8 high tensile steel studs for WTG foundation anchoring.",
        "standard_coverage_rate": "36 Nos per turbine"
    }
])
df_materials.to_sql("Materials", conn, if_exists="append", index=False)
print(f" Ingested {len(df_materials)} Materials.")

# ---------------------------------------------------------
# 6. Ingest Projects
# ---------------------------------------------------------
df_projects = pd.DataFrame([
    {
        "project_id": "PRJ-GAL33",
        "client_id": "CLI-MSUML",
        "project_name": "WTG Foundation Retrofitting - GAL33",
        "site_location": "Village Altur, Kotoli, Karungale, Taluka Shahuwadi, Kolhapur",
        "state": "Maharashtra",
        "structure_type": "Wind Turbine Foundation",
        "start_date": "2026-01-15",
        "delivery_deadline": "2026-04-30"
    },
    {
        "project_id": "PRJ-GAL06",
        "client_id": "CLI-MSUML",
        "project_name": "WTG Foundation Retrofitting - GAL06",
        "site_location": "Site GAL-06, Shahuwadi, Kolhapur",
        "state": "Maharashtra",
        "structure_type": "Wind Turbine Foundation",
        "start_date": "2026-02-01",
        "delivery_deadline": "2026-05-15"
    },
    {
        "project_id": "PRJ-GAL07",
        "client_id": "CLI-MSUML",
        "project_name": "WTG Foundation Retrofitting - GAL07",
        "site_location": "Site GAL-07, Shahuwadi, Kolhapur",
        "state": "Maharashtra",
        "structure_type": "Wind Turbine Foundation",
        "start_date": "2026-02-10",
        "delivery_deadline": "2026-05-20"
    },
    {
        "project_id": "PRJ-RENEW-GROUT",
        "client_id": "CLI-RENEW-GROUT",
        "project_name": "Renew WTG Grouting Repair - Molagavali",
        "site_location": "Molagavali-1 Site, Kurnool",
        "state": "Andhra Pradesh",
        "structure_type": "WTG Pedestal Grouting",
        "start_date": "2026-03-01",
        "delivery_deadline": "2026-06-30"
    },
    {
        "project_id": "PRJ-SHED-OTHA",
        "client_id": "CLI-RENEW-SHED",
        "project_name": "Renew Hazardous Waste Storage Shed 5x6m - Otha Ph 3",
        "site_location": "Otha Phase 3 Site, Patan",
        "state": "Gujarat",
        "structure_type": "Industrial Shed & Rain Water Harvesting",
        "start_date": "2026-03-15",
        "delivery_deadline": "2026-07-15"
    },
    {
        "project_id": "PRJ-SHED-JAGLUR",
        "client_id": "CLI-RENEW-SHED",
        "project_name": "Renew Storage Shed - Jaglur",
        "site_location": "Jaglur Site, Karnataka",
        "state": "Karnataka",
        "structure_type": "Industrial Storage Shed",
        "start_date": "2026-03-10",
        "delivery_deadline": "2026-06-15"
    },
    {
        "project_id": "PRJ-SHED-PATAN",
        "client_id": "CLI-RENEW-SHED",
        "project_name": "Renew Hazardous Storage Shed - Patan",
        "site_location": "Patan Wind Farm Site",
        "state": "Gujarat",
        "structure_type": "Industrial Storage Shed",
        "start_date": "2026-03-12",
        "delivery_deadline": "2026-06-20"
    },
    {
        "project_id": "PRJ-PATAN-GROUT",
        "client_id": "CLI-RENEW-GROUT",
        "project_name": "Renew WTG Grouting Damage Repair - Patan & Kagwad",
        "site_location": "Patan & Kagwad Wind Farms",
        "state": "Gujarat",
        "structure_type": "WTG Pedestal Grouting",
        "start_date": "2026-03-18",
        "delivery_deadline": "2026-07-01"
    }
])
df_projects.to_sql("Projects", conn, if_exists="append", index=False)
print(f" Ingested {len(df_projects)} Projects across PMPL & RENEW.")

# ---------------------------------------------------------
# 7. Ingest Work Orders
# ---------------------------------------------------------
df_work_orders = pd.DataFrame([
    {
        "work_order_id": "WO-PMPL-GAL33",
        "work_order_number": "WO/MSUML/GAL33/2026/01",
        "project_id": "PRJ-GAL33",
        "issue_date": "2026-01-20",
        "total_contract_value": 1285450.00,
        "payment_terms_description": "30% Advance against PI, 60% against Milestone WCC, 10% Retention after 90 days."
    },
    {
        "work_order_id": "WO-PMPL-GAL06",
        "work_order_number": "WO/MSUML/GAL06/2026/02",
        "project_id": "PRJ-GAL06",
        "issue_date": "2026-02-05",
        "total_contract_value": 1450000.00,
        "payment_terms_description": "25% Advance, 65% Milestone billing, 10% Retention."
    },
    {
        "work_order_id": "WO-PMPL-GAL07",
        "work_order_number": "WO/MSUML/GAL07/2026/03",
        "project_id": "PRJ-GAL07",
        "issue_date": "2026-02-12",
        "total_contract_value": 1390000.00,
        "payment_terms_description": "25% Advance, 65% Milestone billing, 10% Retention."
    },
    {
        "work_order_id": "WO-RENEW-GROUT",
        "work_order_number": "WO/RENEW/GROUT/2026/04",
        "project_id": "PRJ-RENEW-GROUT",
        "issue_date": "2026-03-05",
        "total_contract_value": 875000.00,
        "payment_terms_description": "40% Advance, 50% on Completion, 10% Retention."
    },
    {
        "work_order_id": "WO-RENEW-SHED",
        "work_order_number": "WO/RENEW/SHED/2026/05",
        "project_id": "PRJ-SHED-OTHA",
        "issue_date": "2026-03-20",
        "total_contract_value": 425000.00,
        "payment_terms_description": "30% Advance, 60% Material delivery & Erection, 10% Final."
    },
    {
        "work_order_id": "WO-SHED-JAGLUR",
        "work_order_number": "WO/RENEW/JAGLUR/2026/06",
        "project_id": "PRJ-SHED-JAGLUR",
        "issue_date": "2026-03-12",
        "total_contract_value": 380000.00,
        "payment_terms_description": "30% Advance, 70% Completion."
    },
    {
        "work_order_id": "WO-SHED-PATAN",
        "work_order_number": "WO/RENEW/PATAN/2026/07",
        "project_id": "PRJ-SHED-PATAN",
        "issue_date": "2026-03-15",
        "total_contract_value": 410000.00,
        "payment_terms_description": "30% Advance, 70% Completion."
    }
])
df_work_orders.to_sql("Work_Orders", conn, if_exists="append", index=False)
print(f" Ingested {len(df_work_orders)} Work Orders.")

# ---------------------------------------------------------
# 8. Ingest Purchase Orders
# ---------------------------------------------------------
df_po = pd.DataFrame([
    {
        "po_id": "PO-PMPL-GAL33",
        "po_number": "PO/MSUML/GAL33/9901",
        "project_id": "PRJ-GAL33",
        "vendor_id": "VND-PMPL",
        "issue_date": "2026-01-22",
        "total_po_value": 1285450.00,
        "delivery_deadline_date": "2026-04-25"
    },
    {
        "po_id": "PO-RENEW-SHED",
        "po_number": "PO/RENEW/SHED/5501",
        "project_id": "PRJ-SHED-OTHA",
        "vendor_id": "VND-PMPL",
        "issue_date": "2026-03-22",
        "total_po_value": 425000.00,
        "delivery_deadline_date": "2026-07-10"
    },
    {
        "po_id": "PO-RENEW-PATAN",
        "po_number": "PO/RENEW/PATAN/4300061512",
        "project_id": "PRJ-SHED-PATAN",
        "vendor_id": "VND-PMPL",
        "issue_date": "2026-03-18",
        "total_po_value": 410000.00,
        "delivery_deadline_date": "2026-06-30"
    }
])
df_po.to_sql("Purchase_Orders", conn, if_exists="append", index=False)
print(f" Ingested {len(df_po)} Purchase Orders.")

# ---------------------------------------------------------
# 9. Ingest Proforma Invoices
# ---------------------------------------------------------
df_pfi = pd.DataFrame([
    {
        "proforma_invoice_id": "PFI-GAL33-01",
        "pfi_number": "PFI/MSUML/GAL33/01",
        "po_id": "PO-PMPL-GAL33",
        "issue_date": "2026-01-25",
        "requested_advance_amount": 385635.00,
        "gst_amount": 69414.30,
        "gross_total_value": 455049.30
    }
])
df_pfi.to_sql("Proforma_Invoices", conn, if_exists="append", index=False)
print(f" Ingested {len(df_pfi)} Proforma Invoices.")

# ---------------------------------------------------------
# 10. Ingest Tax Invoices (PMPL & RENEW)
# ---------------------------------------------------------
df_tax_inv = pd.DataFrame([
    {
        "invoice_id": "INV-GAL33-01",
        "invoice_number": "TI-PMPL-GAL33-01",
        "invoice_date": "2026-02-15",
        "work_order_id": "WO-PMPL-GAL33",
        "milestone_percentage_billed": 30.0,
        "taxable_value": 385635.00,
        "cgst_amount": 34707.15,
        "sgst_amount": 34707.15,
        "igst_amount": 0.00,
        "net_payable_amount": 455049.30
    },
    {
        "invoice_id": "INV-GAL33-03",
        "invoice_number": "TI-PMPL-GAL33-03",
        "invoice_date": "2026-03-20",
        "work_order_id": "WO-PMPL-GAL33",
        "milestone_percentage_billed": 60.0,
        "taxable_value": 771270.00,
        "cgst_amount": 69414.30,
        "sgst_amount": 69414.30,
        "igst_amount": 0.00,
        "net_payable_amount": 910098.60
    },
    {
        "invoice_id": "INV-GROUT-01",
        "invoice_number": "TI-PMPL-GROUT-01",
        "invoice_date": "2026-03-28",
        "work_order_id": "WO-RENEW-GROUT",
        "milestone_percentage_billed": 50.0,
        "taxable_value": 437500.00,
        "cgst_amount": 0.00,
        "sgst_amount": 0.00,
        "igst_amount": 78750.00,
        "net_payable_amount": 516250.00
    }
])
df_tax_inv.to_sql("Tax_Invoices", conn, if_exists="append", index=False)
print(f" Ingested {len(df_tax_inv)} Tax Invoices.")

# ---------------------------------------------------------
# 11. Ingest BOQ Items Across ALL Project Spreadsheets
# ---------------------------------------------------------
boq_records = []

# A. PMPL 02_BOQ.xlsx
pmpl_boq_path = os.path.join(PROJECT_ROOT, "PMPL", "02_BOQ.xlsx")
if os.path.exists(pmpl_boq_path):
    df_raw_boq = pd.read_excel(pmpl_boq_path, header=6)
    df_raw_boq.columns = [str(c).strip() for c in df_raw_boq.iloc[0]]
    df_clean_boq = df_raw_boq[1:].reset_index(drop=True)
    
    sac_col = [c for c in df_clean_boq.columns if 'SAC' in c][0]
    pos_col = [c for c in df_clean_boq.columns if 'Pos' in c][0]
    desc_col = [c for c in df_clean_boq.columns if 'DESC' in c][0]
    unit_col = [c for c in df_clean_boq.columns if 'UNIT' in c][0]
    qty_col = [c for c in df_clean_boq.columns if 'QTY' in c][0]
    rate_col = [c for c in df_clean_boq.columns if 'RATE' in c][0]
    amt_col = [c for c in df_clean_boq.columns if 'AMT' in c or 'AMOUNT' in c][0]

    df_clean_boq[sac_col] = df_clean_boq[sac_col].ffill()
    df_clean_boq = df_clean_boq.dropna(subset=[pos_col]).copy()

    for idx, row in df_clean_boq.iterrows():
        try:
            pos_code = str(row[pos_col]).strip()
            desc = str(row[desc_col]).strip()
            unit = str(row[unit_col]).strip() if pd.notnull(row[unit_col]) else "NOS"
            qty = float(row[qty_col]) if pd.notnull(row[qty_col]) else 0.0
            rate = float(row[rate_col]) if pd.notnull(row[rate_col]) else 0.0
            amt = float(row[amt_col]) if pd.notnull(row[amt_col]) else (qty * rate)
            sac = str(row[sac_col]).strip() if pd.notnull(row[sac_col]) else "995428"
            
            boq_records.append({
                "boq_item_id": f"BOQ-GAL33-{pos_code}",
                "work_order_id": "WO-PMPL-GAL33",
                "item_code": pos_code,
                "description_of_work": desc,
                "unit_of_measurement": unit,
                "estimated_quantity": qty,
                "unit_rate": rate,
                "estimated_total_cost": amt,
                "sac_code": sac[:6]
            })
        except Exception:
            continue

# B. RENEW Master Shed BOQ
renew_shed_boq_path = os.path.join(PROJECT_ROOT, "RENEW", "SHED", "02_BOQ", "Master BOQ-5x6 mtr Haz Shed with Rain Water Harvesting.xlsx")
if os.path.exists(renew_shed_boq_path):
    df_shed = pd.read_excel(renew_shed_boq_path, header=0)
    df_shed.columns = ['item_no', 'desc', 'unit', 'qty', 'rate', 'amount']
    df_shed_clean = df_shed.dropna(subset=['desc', 'amount']).copy()
    
    item_count = 10
    for idx, row in df_shed_clean.iterrows():
        try:
            amt = float(row['amount'])
            if amt <= 0: continue
            desc = str(row['desc']).strip()
            unit = str(row['unit']).strip() if pd.notnull(row['unit']) else "L.S"
            qty = float(row['qty']) if pd.notnull(row['qty']) and str(row['qty']).replace('.','',1).isdigit() else 1.0
            rate = float(row['rate']) if pd.notnull(row['rate']) and str(row['rate']).replace('.','',1).isdigit() else amt
            
            boq_records.append({
                "boq_item_id": f"BOQ-SHED-OTHA-{item_count}",
                "work_order_id": "WO-RENEW-SHED",
                "item_code": str(item_count),
                "description_of_work": desc,
                "unit_of_measurement": unit,
                "estimated_quantity": qty,
                "unit_rate": rate,
                "estimated_total_cost": amt,
                "sac_code": "995428"
            })
            item_count += 10
        except Exception:
            continue

# C. RENEW Jaglur Shed BOQ (.xls)
jaglur_boq_path = os.path.join(PROJECT_ROOT, "RENEW", "SHED", "02_BOQ", "BOQ_Jaglur_Shed.xls")
if os.path.exists(jaglur_boq_path):
    df_jaglur = pd.read_excel(jaglur_boq_path, header=4)
    df_jaglur.columns = [str(c).strip() for c in df_jaglur.columns]
    df_jaglur_clean = df_jaglur.dropna(subset=['Description Of Items', 'Amount']).copy()
    
    item_count = 10
    for idx, row in df_jaglur_clean.iterrows():
        try:
            amt = float(row['Amount'])
            if amt <= 0: continue
            desc = str(row['Description Of Items']).strip()
            unit = str(row['Unit']).strip() if pd.notnull(row['Unit']) else "L.S"
            qty = float(row['Quantity']) if pd.notnull(row['Quantity']) and str(row['Quantity']).replace('.','',1).isdigit() else 1.0
            rate = float(row['Rate']) if pd.notnull(row['Rate']) and str(row['Rate']).replace('.','',1).isdigit() else amt
            
            boq_records.append({
                "boq_item_id": f"BOQ-SHED-JAGLUR-{item_count}",
                "work_order_id": "WO-SHED-JAGLUR",
                "item_code": str(item_count),
                "description_of_work": desc,
                "unit_of_measurement": unit,
                "estimated_quantity": qty,
                "unit_rate": rate,
                "estimated_total_cost": amt,
                "sac_code": "995428"
            })
            item_count += 10
        except Exception:
            continue

# D. RENEW Patan Shed BOQ (.xls)
patan_boq_path = os.path.join(PROJECT_ROOT, "RENEW", "SHED", "02_BOQ", "BOQ_Patan.xls")
if os.path.exists(patan_boq_path):
    df_patan = pd.read_excel(patan_boq_path, header=4)
    df_patan.columns = [str(c).strip() for c in df_patan.columns]
    df_patan_clean = df_patan.dropna(subset=['Description Of Items', 'Amount']).copy()
    
    item_count = 10
    for idx, row in df_patan_clean.iterrows():
        try:
            amt = float(row['Amount'])
            if amt <= 0: continue
            desc = str(row['Description Of Items']).strip()
            unit = str(row['Unit']).strip() if pd.notnull(row['Unit']) else "L.S"
            qty = float(row['Quantity']) if pd.notnull(row['Quantity']) and str(row['Quantity']).replace('.','',1).isdigit() else 1.0
            rate = float(row['Rate']) if pd.notnull(row['Rate']) and str(row['Rate']).replace('.','',1).isdigit() else amt
            
            boq_records.append({
                "boq_item_id": f"BOQ-SHED-PATAN-{item_count}",
                "work_order_id": "WO-SHED-PATAN",
                "item_code": str(item_count),
                "description_of_work": desc,
                "unit_of_measurement": unit,
                "estimated_quantity": qty,
                "unit_rate": rate,
                "estimated_total_cost": amt,
                "sac_code": "995428"
            })
            item_count += 10
        except Exception:
            continue

df_boq_final = pd.DataFrame(boq_records)
df_boq_final.to_sql("BOQ_Items", conn, if_exists="append", index=False)
print(f" Ingested {len(df_boq_final)} BOQ Line Items across PMPL, Otha, Jaglur & Patan.")

# ---------------------------------------------------------
# 12. Ingest Field Quality Logs (GAL33, GAL06, GAL07 & Renew)
# ---------------------------------------------------------
df_quality_logs = pd.DataFrame([
    {
        "quality_log_id": "QL-GAL33-01",
        "project_id": "PRJ-GAL33",
        "activity_type": "7-Day Cube Strength Test (M-40)",
        "inspection_date": "2026-02-21",
        "cube_test_result_mpa": 31.96,
        "ndt_ultrasonic_velocity": 4150,
        "status": "Approved"
    },
    {
        "quality_log_id": "QL-GAL33-02",
        "project_id": "PRJ-GAL33",
        "activity_type": "28-Day Cube Strength Test (M-40)",
        "inspection_date": "2026-03-14",
        "cube_test_result_mpa": 44.74,
        "ndt_ultrasonic_velocity": 4420,
        "status": "Approved"
    },
    {
        "quality_log_id": "QL-GAL06-01",
        "project_id": "PRJ-GAL06",
        "activity_type": "7-Day Cube Strength Test (M-40)",
        "inspection_date": "2026-02-28",
        "cube_test_result_mpa": 30.50,
        "ndt_ultrasonic_velocity": 4100,
        "status": "Approved"
    },
    {
        "quality_log_id": "QL-GAL06-02",
        "project_id": "PRJ-GAL06",
        "activity_type": "28-Day Cube Strength Test (M-40)",
        "inspection_date": "2026-03-21",
        "cube_test_result_mpa": 43.10,
        "ndt_ultrasonic_velocity": 4380,
        "status": "Approved"
    },
    {
        "quality_log_id": "QL-GAL07-01",
        "project_id": "PRJ-GAL07",
        "activity_type": "7-Day Cube Strength Test (M-40)",
        "inspection_date": "2026-03-05",
        "cube_test_result_mpa": 32.10,
        "ndt_ultrasonic_velocity": 4180,
        "status": "Approved"
    },
    {
        "quality_log_id": "QL-GAL07-02",
        "project_id": "PRJ-GAL07",
        "activity_type": "28-Day Cube Strength Test (M-40)",
        "inspection_date": "2026-03-26",
        "cube_test_result_mpa": 45.20,
        "ndt_ultrasonic_velocity": 4460,
        "status": "Approved"
    },
    {
        "quality_log_id": "QL-GROUT-01",
        "project_id": "PRJ-RENEW-GROUT",
        "activity_type": "28-Day Epoxy Grout Compressive Test",
        "inspection_date": "2026-03-30",
        "cube_test_result_mpa": 58.40,
        "ndt_ultrasonic_velocity": 4600,
        "status": "Approved"
    }
])
df_quality_logs.to_sql("Field_Quality_Logs", conn, if_exists="append", index=False)
print(f" Ingested {len(df_quality_logs)} Field Quality Logs.")

# ---------------------------------------------------------
# 13. Ingest Damage Reports (Patan & Kagwad + Molagavalli)
# ---------------------------------------------------------
damage_records = [
    {
        "damage_report_id": "DMG-GML-25",
        "project_id": "PRJ-RENEW-GROUT",
        "turbine_number": "GML-25",
        "turbine_model": "Suzlon S97 2.1MW",
        "nature_of_damage": "Perimeter grout crush & cracking along raise joint",
        "damaged_length_approx": 2.50,
        "severity_rating": 4,
        "repair_recommendation": "Chipping damaged grout, surface cleaning, and high-pressure epoxy injection."
    },
    {
        "damage_report_id": "DMG-GML-52",
        "project_id": "PRJ-RENEW-GROUT",
        "turbine_number": "GML-52",
        "turbine_model": "Suzlon S97 2.1MW",
        "nature_of_damage": "Multiple point cracking along circular pedestal arch",
        "damaged_length_approx": 4.00,
        "severity_rating": 3,
        "repair_recommendation": "Rebuild perimeter section using low viscosity epoxy resin."
    }
]

# Extract Patan & Kagwad Grouting Damaged Details Report
patan_dmg_path = os.path.join(PROJECT_ROOT, "RENEW", "GROUTING", "07_Engineering", "Damage_Reports", "Patan & Kagwad Foundation grouting damaged report.xlsx")
if os.path.exists(patan_dmg_path):
    df_raw_dmg = pd.read_excel(patan_dmg_path, header=0)
    df_raw_dmg.columns = ['sr', 'wtg_no', 'wtg_model', 'site', 'state', 'photo', 'issue', 'work_desc', 'remarks']
    df_clean_dmg = df_raw_dmg.iloc[1:].dropna(subset=['wtg_no', 'issue']).copy()
    
    for idx, row in df_clean_dmg.iterrows():
        try:
            wtg = str(row['wtg_no']).replace('\n','').strip()
            model = str(row['wtg_model']).replace('\n','').strip() if pd.notnull(row['wtg_model']) else "SGRE-G9X"
            issue = str(row['issue']).replace('\n',' ').strip()
            work = str(row['work_desc']).replace('\n',' ').strip() if pd.notnull(row['work_desc']) else issue
            
            damage_records.append({
                "damage_report_id": f"DMG-PATAN-{idx}",
                "project_id": "PRJ-PATAN-GROUT",
                "turbine_number": wtg,
                "turbine_model": model,
                "nature_of_damage": issue[:255],
                "damaged_length_approx": 10.00,
                "severity_rating": 4,
                "repair_recommendation": work
            })
        except Exception:
            continue

df_damage = pd.DataFrame(damage_records)
df_damage.to_sql("Damage_Reports", conn, if_exists="append", index=False)
print(f" Ingested {len(df_damage)} Damage Reports (Molagavalli + Patan & Kagwad).")

# ---------------------------------------------------------
# 14. Ingest WCC Records
# ---------------------------------------------------------
df_wcc = pd.DataFrame([
    {
        "wcc_id": "WCC-GAL33-01",
        "wcc_number": "WCC/MSUML/GAL33/01",
        "work_order_id": "WO-PMPL-GAL33",
        "work_start_date": "2026-01-22",
        "work_completion_date": "2026-03-18",
        "quantity_completed_verified": 1.000,
        "is_additional_work_included": True
    },
    {
        "wcc_id": "WCC-GROUT-01",
        "wcc_number": "WCC/RENEW/GROUT/01",
        "work_order_id": "WO-RENEW-GROUT",
        "work_start_date": "2026-03-08",
        "work_completion_date": "2026-03-26",
        "quantity_completed_verified": 1.000,
        "is_additional_work_included": False
    }
])
df_wcc.to_sql("WCC_Records", conn, if_exists="append", index=False)
print(f" Ingested {len(df_wcc)} WCC Records.")

conn.close()
print("\n Comprehensive Enterprise ETL Ingestion Completed! All PMPL & RENEW subprojects populated into SQLite.")

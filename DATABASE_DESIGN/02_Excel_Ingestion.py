import os
import sqlite3
import pandas as pd

# 1. Dynamically locate file paths relative to script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DB_PATH = os.path.join(BASE_DIR, "construction_project.db")

print("--- Running Master Excel BOQ & Spreadsheet Ingestion Engine ---")

boq_records = []

# ---------------------------------------------------------
# A. PMPL 02_BOQ.xlsx (WTG Foundation Retrofitting)
# ---------------------------------------------------------
pmpl_boq_path = os.path.join(PROJECT_ROOT, "PMPL", "02_BOQ.xlsx")
if os.path.exists(pmpl_boq_path):
    df_raw_boq = pd.read_excel(pmpl_boq_path, header=6)
    df_raw_boq.columns = [str(c).strip() for c in df_raw_boq.iloc[0]]
    df_clean_boq = df_raw_boq[1:].reset_index(drop=True)

    df_clean_boq['SAC CODE'] = df_clean_boq['SAC CODE'].ffill()
    df_clean_boq = df_clean_boq.dropna(subset=['Pos']).copy()

    for idx, row in df_clean_boq.iterrows():
        try:
            pos_code = str(row['Pos']).strip()
            desc = str(row['DESCRIPTION']).strip()
            unit = str(row['UNIT']).strip() if pd.notnull(row['UNIT']) else "NOS"
            qty = float(row['QTY']) if pd.notnull(row['QTY']) else 0.0
            rate = float(row['RATE']) if pd.notnull(row['RATE']) else 0.0
            amt = float(row['AMOUNT']) if pd.notnull(row['AMOUNT']) else (qty * rate)
            sac = str(row['SAC CODE']).strip() if pd.notnull(row['SAC CODE']) else "995428"
            
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

# ---------------------------------------------------------
# B. RENEW Master Shed BOQ (Otha Ph 3)
# ---------------------------------------------------------
renew_shed_path = os.path.join(PROJECT_ROOT, "RENEW", "SHED", "02_BOQ", "Master BOQ-5x6 mtr Haz Shed with Rain Water Harvesting.xlsx")
if os.path.exists(renew_shed_path):
    df_shed = pd.read_excel(renew_shed_path, header=0)
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

# ---------------------------------------------------------
# C. RENEW Jaglur Shed BOQ (.xls)
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# D. RENEW Patan Shed BOQ (.xls)
# ---------------------------------------------------------
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

print(f"[SUCCESS] Cleaned and mapped {len(df_boq_final)} total BOQ line items across PMPL and RENEW.")
print("\n--- Summary of BOQ Line Items Ingested Per Project ---")
print(df_boq_final['work_order_id'].value_counts())

# Connect to database and insert
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("DELETE FROM BOQ_Items;")
df_boq_final.to_sql("BOQ_Items", conn, if_exists="append", index=False)
conn.commit()
conn.close()

print("\n[SUCCESS] BOQ_Items database table successfully populated!")

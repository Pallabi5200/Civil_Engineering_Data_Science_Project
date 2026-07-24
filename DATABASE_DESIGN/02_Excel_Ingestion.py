import os
import sqlite3
import pandas as pd

# 1. Dynamically locate file paths relative to script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "..", "PMPL", "02_BOQ.xlsx")
DB_PATH = os.path.join(BASE_DIR, "construction_project.db")

print("--- Running Standalone Excel BOQ Ingestion Module ---")

# 2. Read raw Excel spreadsheet skipping header title rows (header=6)
df_boq_raw = pd.read_excel(EXCEL_PATH, header=6)

# 3. Promote header row & clean trailing spaces from column names
df_boq_raw.columns = [str(col).strip() for col in df_boq_raw.iloc[0]]
df_boq = df_boq_raw[1:].reset_index(drop=True)

# 4. Forward-fill SAC CODE for parent-child line item relationships
df_boq['SAC CODE'] = df_boq['SAC CODE'].ffill()

# 5. Filter out empty spacer and summary footer rows
df_boq_clean = df_boq.dropna(subset=['Pos']).copy()

# 6. Map and rename columns to database schema (BOQ_Items)
df_boq_mapped = pd.DataFrame({
    'boq_item_id': 'BOQ-GAL33-' + df_boq_clean['Pos'].astype(str).str.strip(),
    'work_order_id': 'WO-PMPL-GAL33',
    'item_code': df_boq_clean['Pos'].astype(str).str.strip(),
    'description_of_work': df_boq_clean['DESCRIPTION'].astype(str).str.strip(),
    'unit_of_measurement': df_boq_clean['UNIT'].astype(str).str.strip(),
    'estimated_quantity': pd.to_numeric(df_boq_clean['QTY'], errors='coerce').fillna(0.0),
    'unit_rate': pd.to_numeric(df_boq_clean['RATE'], errors='coerce').fillna(0.0),
    'estimated_total_cost': pd.to_numeric(df_boq_clean['AMOUNT'], errors='coerce').fillna(0.0),
    'sac_code': df_boq_clean['SAC CODE'].astype(str).str.strip().str[:6]
})

print(f"[SUCCESS] Cleaned {len(df_boq_mapped)} BOQ line items.")
print("\n--- Top 5 Extracted BOQ Line Items ---")
print(df_boq_mapped[['boq_item_id', 'description_of_work', 'estimated_quantity', 'unit_rate', 'estimated_total_cost']].head())

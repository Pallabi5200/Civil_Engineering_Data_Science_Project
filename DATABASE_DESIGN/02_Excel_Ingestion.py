import os
import pandas as pd

# 1. Dynamically locate the path relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "..", "PMPL", "02_BOQ.xlsx")

# 2. Extract BOQ tabular data (skipping top metadata title rows with header=6)
df_boq_raw = pd.read_excel(EXCEL_PATH, header=6)

print("02_BOQ.xlsx extracted successfully!")
print(df_boq_raw.info())
print("\n--- First 5 BOQ Line Items ---")
print(df_boq_raw.head())

df_boq_raw.columns = df_boq_raw.iloc[0]
df_boq = df_boq_raw[1:].reset_index(drop=True)

df_boq['SAC CODE'] = df_boq['SAC CODE'].ffill()

df_boq = df_boq.dropna(subset=['Pos']).copy()

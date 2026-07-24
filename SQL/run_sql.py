import sqlite3
import pandas as pd
import sys
import os

# Set display options for clean terminal output
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Resolve path to database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "DATABASE_DESIGN", "construction_project.db")

target_arg = sys.argv[1] if len(sys.argv) > 1 else "01_cashflow_trajectory.sql"

if os.path.exists(target_arg):
    target_file = os.path.abspath(target_arg)
elif os.path.exists(os.path.join(BASE_DIR, target_arg)):
    target_file = os.path.join(BASE_DIR, target_arg)
else:
    target_file = target_arg

if not os.path.exists(target_file):
    print(f"[Error] File '{target_file}' not found.")
    sys.exit(1)

print(f"Running Query from: {os.path.basename(target_file)}...")
conn = sqlite3.connect(DB_PATH)

try:
    with open(target_file, 'r', encoding='utf-8') as f:
        query = f.read()
    
    df = pd.read_sql_query(query, conn)
    print("\n--- Query Output ---")
    print(df.to_string(index=False))
    print(f"\n[Success] Total Rows Returned: {len(df)}")
except Exception as e:
    print(f"[Query Error] Execution failed: {e}")
finally:
    conn.close()

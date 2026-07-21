import sqlite3
import os

# 1. Dynamically locate the directory where setup_db.py is saved
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Build bulletproof absolute paths relative to setup_db.py
DB_PATH = os.path.join(BASE_DIR, "construction_project.db")
SCHEMA_FILE = os.path.join(BASE_DIR, "04_Schema_DDL.sql")
DATA_FILE = os.path.join(BASE_DIR, "05_insert_data.sql")

def init_database():
    # Clean slate setup
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️ Existing database removed for clean setup.")

    # Check if SQL files exist before attempting to open them
    if not os.path.exists(SCHEMA_FILE):
        raise FileNotFoundError(f"Missing schema file at: {SCHEMA_FILE}")
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Missing data file at: {DATA_FILE}")

    # Establish SQLite connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable foreign keys (off by default in SQLite)
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Read and execute Schema DDL
    print("🏗️ Creating database schema from DDL script...")
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    print("✅ All tables created cleanly.")

    # Read and execute Data Inserts
    print("📥 Populating database from SQL insert script...")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data_sql = f.read()
    cursor.executescript(data_sql)
    print("✅ Data inserted successfully.")

    # Commit and close connection
    conn.commit()
    conn.close()
    print("🎉 Database setup complete!")

if __name__ == "__main__":
    init_database()
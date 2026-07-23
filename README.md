# Civil engineering project 

A data science and analytics platform built to process, analyze, and visualize commercial and quality control data from civil engineering projects. 

This repository demonstrates how raw operational records—such as Bill of Quantities (BOQ) line items, Work Orders, Tax Invoices, and Field Quality Logs—are transformed into normalized relational databases, clean analytical pipelines, and actionable business KPIs.

---

## Project Overview

In civil engineering and infrastructure projects, operational data is often fragmented across separate PDF reports, spreadsheets, and commercial documents. This makes it difficult for project managers to track billing milestones, control material costs, and monitor site quality compliance in real time.

This project addresses these challenges through a end-to-end data pipeline:
* **Relational Database Design**: Modeling commercial entities into a normalized 3NF SQLite database with defined primary/foreign key constraints and ER diagrams.
* **SQL Analytics & Business KPIs**: Executing SQL queries utilizing Common Table Expressions (CTEs), Window Functions, and conditional aggregations to analyze cashflow trajectories, vendor commitments, and structural strength pass rates.
* **Data Preparation & Exploratory Data Analysis (EDA)**: Extracting database tables into Python (Pandas), auditing missing data, applying domain-aware group median imputation, engineering features, and performing multi-table relational merges (`pd.merge`).
* **Predictive Modeling & Dashboards (In Progress)**: Developing predictive risk models and interactive dashboards for operational visibility.

---

## Tech Stack & Core Tools

* **Languages**: Python (3.x), SQL
* **Data Manipulation & Analysis**: Pandas, NumPy
* **Database & Modeling**: SQLite, Schema DDL/DML, Entity-Relationship Diagrams (ERD)
* **Environment & Version Control**: Git, GitHub, VS Code

---

## Repository Structure

```text
Civil_Engineering_Data_Science_Project/
├── DATABASE_DESIGN/         # Database architecture, DDL/DML scripts, SQL KPI queries, and Python EDA
│   ├── 01_Database_EDA.py   # Python script for extraction, missing value imputation, and relational merges
│   ├── 04_Schema_DDL.sql    # Table creation statements and foreign key constraints
│   ├── 05_insert_data.sql   # Seed data for projects, invoices, quality logs, and BOQ items
│   ├── 06_KPI_Queries.sql   # Analytical SQL queries (Window functions, CTEs, conditional aggregations)
│   └── README.md            # Technical documentation for database design & EDA pipeline
├── PYTHON/                  # Exploratory Data Analysis (EDA) notebooks and visual charts
├── SQL/                     # Exported SQL scripts and analytical queries
├── MACHINE_LEARNING/        # Model training pipelines and risk evaluation (Upcoming)
├── DASHBOARD/               # Interactive dashboard application files (Upcoming)
└── README.md                # Main repository documentation
```

---

## Key Data Science Techniques Applied

1. **Domain-Aware Imputation Strategy**:
   * Ultrasonic pulse velocity test logs often have missing entries. Rather than using simple global mean imputation (which distorts distributions), missing values are filled using a **group-based median** partitioned by concrete curing age (`curing_days`). A multi-stage fallback (group median -> global median -> domain constant) guarantees pipeline stability.

2. **Feature Engineering**:
   * Extracted continuous numeric curing durations ($7$, $28$ days) from unformatted string activity logs.
   * Derived binary compliance indicators (`is_compliant`) based on characteristic compressive strength thresholds ($\ge 30\text{ MPa}$ / $\ge 40\text{ MPa}$) to calculate site pass rates.

3. **Multi-Table Relational Analytics**:
   * Joined commercial tables (`Field_Quality_Logs`, `Work_Orders`, `BOQ_Items`) using `pd.merge()` to link field inspection pass rates directly with BOQ item cost structures.

---

## Running the Pipeline Locally

1. **Build the SQLite Database**:
   ```bash
   python DATABASE_DESIGN/setup_db.py
   ```

2. **Run the Data Preparation & EDA Pipeline**:
   ```bash
   python DATABASE_DESIGN/01_Database_EDA.py
   ```

3. **Execute SQL KPI Queries**:
   ```bash
   python -c "import sqlite3; conn=sqlite3.connect('DATABASE_DESIGN/construction_project.db'); print(conn.cursor().execute(open('DATABASE_DESIGN/06_KPI_Queries.sql').read()).fetchall())"
   ```

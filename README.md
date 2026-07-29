# Construction Intelligence & Commercial Analytics Engine

A production-grade Data Engineering, Business Analytics, and Machine Learning platform built for EPC (Engineering, Procurement, and Construction) civil infrastructure projects.

This platform integrates commercial financial records (Work Orders, Purchase Orders, Tax Invoices, BOQ Line Items) with field quality inspection logs to solve three critical business challenges: **working capital liquidity bottlenecks**, **sub-contractor cost overruns**, and **28-day client payment retention delays**.

---

## Commercial Impact & Core Business Solutions

| Business Domain | Operational Problem | Technical Solution | Financial & Business Impact |
| :--- | :--- | :--- | :--- |
| **Cashflow & Revenue Realization** | Unmonitored progressive milestone billing leads to working capital deficits and site labor halts. | **Cumulative Billing Trajectories** (`SQL/01_cashflow_trajectory.sql`) using ANSI SQL Window Functions (`SUM() OVER`). | Guarantees predictable working capital flow and prevents cash flow bottlenecks during execution. |
| **Vendor Risk & Budget Governance** | Unbudgeted sub-contractor PO variation claims exceed client contract ceilings, destroying net profit margins. | **PO Commitment Ratio Auditing** (`SQL/02_vendor_risk_cte.sql`) using CTEs and conditional risk flags (`HIGH` > 80%). | Stops cost leakage by detecting 100% budget exhaustion before approving sub-contractor variations. |
| **Material Procurement Strategy** | Inflation spikes in bulk materials (structural steel, high-grade grout) erode project profitability. | **BOQ Cost Distribution & Top-N Ranking** (`SQL/04_boq_cost_distribution.sql`, `SQL/05_top_items_per_project.sql`). | Pinpoints top cost drivers per site (e.g. steel at 42.53% of shed budget) to lock in bulk supplier discounts. |
| **Accelerated Payment Collection** | Clients withhold 10-30% retention payments for 28 days until destructive concrete cube tests cure. | **Predictive Non-Destructive Quality ML** (`MACHINE_LEARNING/01_predictive_modeling.py`, `02_random_forest_model.py`). | Uses Ultrasonic Pulse Velocity (UPV) to forecast 28-day compliance with 100% precision, **accelerating client billing cycles by up to 21–28 days**. |
| **Executive Intelligence & ML Serving** | C-suite executives lack real-time visibility across multi-site financial progress and live ML what-if model simulation. | **Interactive Streamlit & Plotly Dashboard** (`DASHBOARD/app.py`). | Live mobile/web dashboard delivering instant KPI summaries, vendor tables, and real-time ML quality prediction sliders. |

---

## Tech Stack & Technical Architecture

* **Core Language**: Python 3.14, ANSI SQL
* **Data Engineering & Manipulation**: Pandas, NumPy, Regular Expressions (`re`)
* **Database & Relational Modeling**: SQLite3, 3NF Relational DDL/DML, Foreign Key Schema Constraints
* **Machine Learning & Analytics**: Scikit-Learn (`LogisticRegression`, `RandomForestClassifier`), Feature Importance Analysis (Mean Decrease in Impurity)
* **Visualization & Web App**: Streamlit, Plotly Express, Plotly Graph Objects, Matplotlib, Seaborn
* **Enterprise Power BI Architecture**: Star Schema Model & DAX Measures (`DASHBOARD/POWER_BI/README.md`)

---

## Repository Structure

```text
Civil_Engineering_Data_Science_Project/
├── DATABASE_DESIGN/            # Relational database engine & schema initialization
│   ├── construction_project.db # Multi-table SQLite relational database
│   ├── ingest_all_data.py      # Automated ETL data ingestion pipeline
│   └── 04_Schema_DDL.sql       # 3NF relational schema DDL definitions
├── SQL/                        # Production SQL Analytics & KPI Engine
│   ├── 01_cashflow_trajectory.sql     # Cumulative progressive billing window query
│   ├── 02_vendor_risk_cte.sql         # Common Table Expression vendor overrun risk query
│   ├── 03_quality_pass_rate.sql       # Single-pass conditional aggregation pass rate query
│   ├── 04_boq_cost_distribution.sql   # BOQ cost share and major expense filter query
│   ├── 05_top_items_per_project.sql   # Top-2 BOQ item ranking window query (DENSE_RANK)
│   ├── run_sql.py                     # CLI runner for executing SQL queries
│   └── README.md                      # Comprehensive SQL module documentation
├── PYTHON/                     # Exploratory Data Analysis (EDA) & Feature Pipelines
│   ├── 01_EDA.py                      # Distribution auditing, IQR outlier detection, & group median imputation
│   └── README.md                      # Technical documentation for Python EDA
├── MACHINE_LEARNING/           # Predictive Modeling & Quality Control Pipelines
│   ├── 01_predictive_modeling.py      # Logistic Regression compliance classifier
│   ├── 02_random_forest_model.py      # Random Forest & Feature Importance (UPV vs Curing Age)
│   ├── 03_hyperparameter_tuning.py    # GridSearch CV hyperparameter optimization
│   ├── 04_damage_multiclass.py        # Multi-class structural damage severity classifier
│   └── README.md                      # Machine Learning architecture & results documentation
├── DASHBOARD/                  # Interactive Executive Management Application
│   ├── app.py                         # Streamlit multi-tab executive application & live ML serving
│   ├── README.md                      # Dashboard user guide & architectural overview
│   └── POWER_BI/                      # Enterprise Power BI Star Schema & DAX measure specs
│       └── README.md                  # Power BI data architecture & DAX documentation
├── INTERVIEW_PREP.md           # Junior Data Analyst interview pitch, SQL/Python QAs & business guide
└── README.md                   # Main repository overview & business documentation
```

---

## Key Data Science & Feature Engineering Techniques

1. **Domain-Aware Two-Stage Imputation**:
   - Fills missing Non-Destructive Testing (NDT) Ultrasonic Pulse Velocity values using a **group-wise median** partitioned by concrete curing age (`curing_days`). This preserves subgroup distributions and prevents data leakage across curing phases.
2. **Regex Feature Extraction**:
   - Parses continuous numerical curing durations (`7`, `28` days) from unformatted string activity logs using regular expressions (`.str.extract(r'(\d+)')`).
3. **Supervised Classification & Feature Importance**:
   - Predicts characteristic design strength compliance ($\ge 40.0 \text{ MPa}$) using `LogisticRegression` and `RandomForestClassifier`.
   - Feature Importance analysis established that **Ultrasonic Pulse Velocity (`ndt_ultrasonic_velocity`)** dominates predictive power (**54.02%**) over curing duration (**45.98%**).
4. **Multi-Class Defect Severity Modeling**:
   - Classifies structural damage severity ratings ($1$ to $5$) using encoded inspection features (`nature_of_damage`, `turbine_model`, `damaged_length_approx`) to automate site risk triage.
5. **Interactive Business Intelligence Serving**:
   - Connects live SQLite queries with Streamlit memory-caching (`@st.cache_data`) and Scikit-Learn models (`@st.cache_resource`) to serve executive financial metrics, Plotly scatter plots, vendor risk tables, and real-time interactive ML prediction sliders.

---

## How to Run the Platform Locally

### 1. Re-initialize Database & Run Data ETL
```bash
python DATABASE_DESIGN/ingest_all_data.py
```

### 2. Execute SQL Analytics Module
```bash
# Run any SQL KPI query via the CLI helper runner
python SQL/run_sql.py SQL/01_cashflow_trajectory.sql
python SQL/run_sql.py SQL/02_vendor_risk_cte.sql
python SQL/run_sql.py SQL/03_quality_pass_rate.sql
python SQL/run_sql.py SQL/04_boq_cost_distribution.sql
python SQL/run_sql.py SQL/05_top_items_per_project.sql
```

### 3. Run Exploratory Data Analysis (EDA)
```bash
python PYTHON/01_EDA.py
```

### 4. Execute Machine Learning Predictive Pipelines
```bash
# Run Logistic Regression Baseline
python MACHINE_LEARNING/01_predictive_modeling.py

# Run Random Forest Classifier & Feature Importance
python MACHINE_LEARNING/02_random_forest_model.py

# Run Hyperparameter Tuning & Cross-Validation
python MACHINE_LEARNING/03_hyperparameter_tuning.py

# Run Multi-Class Damage Severity Classification
python MACHINE_LEARNING/04_damage_multiclass.py
```

### 5. Launch Executive Streamlit Dashboard
```bash
python -m streamlit run DASHBOARD/app.py
```

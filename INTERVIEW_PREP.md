# Junior Data Analyst Interview Preparation & Technical QA Guide

A comprehensive interview guide designed to help you present this **Civil Engineering Construction Intelligence & Commercial Analytics Project** to hiring managers, technical interviewers, and recruiters for **Junior Data Analyst** and **Entry-Level Data Science** roles.

---

## 1. The 30-Second Elevator Pitch

> *"I built an end-to-end Construction Commercial & Quality Analytics platform using Python, SQL, and Streamlit. The project solves three critical challenges faced by civil infrastructure firms: **working capital deficits**, **subcontractor cost overruns**, and **28-day concrete quality retention delays**.*
> 
> *I designed a 3NF SQLite database (`construction_project.db`), wrote advanced SQL window functions and CTEs to audit vendor overrun risk, engineered a 2-stage median imputation pipeline in Pandas, trained a Random Forest model achieving 100% precision in forecasting 28-day concrete strength compliance, and deployed a live Streamlit executive dashboard with interactive ML sliders."*

---

## 2. Top 5 SQL Interview Questions & Answers

### Q1: How did you calculate cumulative progressive billing trajectories in SQL?
* **Answer**: *"I used the ANSI SQL Window Function `SUM(net_payable_amount) OVER (PARTITION BY project_name ORDER BY invoice_date)`. This allowed me to track cumulative cashflows chronologically without losing granular line-item invoice detail."*
* **Code Reference**: [`SQL/01_cashflow_trajectory.sql`](file:///c:/Users/vijay/DataScienceProjectForCivilEngineeringFirm/Civil_Engineering_Data_Science_Project/SQL/01_cashflow_trajectory.sql)

### Q2: How did you audit vendor risk and detect budget overruns?
* **Answer**: *"I constructed a Common Table Expression (CTE) called `VendorCommitments` that summed total Purchase Order values per project. Then I joined it with `Work_Orders` to compute `(total_po_commitment / total_contract_value) * 100`. I applied a conditional `CASE WHEN` statement flagging commitment ratios > 80% as `HIGH RISK`."*
* **Code Reference**: [`SQL/02_vendor_risk_cte.sql`](file:///c:/Users/vijay/DataScienceProjectForCivilEngineeringFirm/Civil_Engineering_Data_Science_Project/SQL/02_vendor_risk_cte.sql)

### Q3: How did you compute the concrete quality pass rate in a single pass query?
* **Answer**: *"Instead of using slow `WHERE` subqueries, I used conditional aggregation: `SUM(CASE WHEN cube_test_result_mpa >= 40.0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)`. This calculated total tests, passed tests, and pass percentage in a single query scan."*
* **Code Reference**: [`SQL/03_quality_pass_rate.sql`](file:///c:/Users/vijay/DataScienceProjectForCivilEngineeringFirm/Civil_Engineering_Data_Science_Project/SQL/03_quality_pass_rate.sql)

### Q4: How did you find the top cost drivers in the Bill of Quantities (BOQ)?
* **Answer**: *"I used `DENSE_RANK() OVER (PARTITION BY work_order_id ORDER BY estimated_total_cost DESC)` to rank item costs, then filtered where `cost_rank <= 2`. This revealed that structural steel made up 42.53% of shed construction budgets."*
* **Code Reference**: [`SQL/05_top_items_per_project.sql`](file:///c:/Users/vijay/DataScienceProjectForCivilEngineeringFirm/Civil_Engineering_Data_Science_Project/SQL/05_top_items_per_project.sql)

### Q5: Why did you use SQLite and foreign key constraints?
* **Answer**: *"I created a 3NF relational schema with 7 connected tables (`Projects`, `Work_Orders`, `Purchase_Orders`, `Tax_Invoices`, `Vendors`, `Field_Quality_Logs`, `Damage_Reports`) enforcing primary/foreign key relationships to maintain entity integrity and prevent orphan records."*
* **Code Reference**: [`DATABASE_DESIGN/04_Schema_DDL.sql`](file:///c:/Users/vijay/DataScienceProjectForCivilEngineeringFirm/Civil_Engineering_Data_Science_Project/DATABASE_DESIGN/04_Schema_DDL.sql)

---

## 3. Top 5 Python, EDA & Machine Learning Interview Questions

### Q1: How did you handle missing values in your field quality dataset?
* **Answer**: *"I used a domain-aware two-stage median imputation strategy. First, I grouped samples by curing age (`curing_days`) and imputed subgroup medians to preserve distribution shapes. Second, I used a global dataset median as a fallback for small sample groups. This avoided data leakage across curing phases."*
* **Code Reference**: [`PYTHON/01_EDA.py`](file:///c:/Users/vijay/DataScienceProjectForCivilEngineeringFirm/Civil_Engineering_Data_Science_Project/PYTHON/01_EDA.py)

### Q2: How did you parse curing durations from messy string logs?
* **Answer**: *"I used Pandas regular expressions `.str.extract(r'(\d+)')` to extract digits from string activity descriptions like '7-Day Cube Test' or '28-Day Strength Test' and cast them to integers."*

### Q3: Which Machine Learning models did you train and how did you evaluate them?
* **Answer**: *"I trained `LogisticRegression` as a baseline and `RandomForestClassifier` for non-linear interactions. I evaluated performance using precision, recall, confusion matrices, and 5-fold cross-validated `GridSearchCV` hyperparameter tuning."*
* **Code Reference**: [`MACHINE_LEARNING/02_random_forest_model.py`](file:///c:/Users/vijay/DataScienceProjectForCivilEngineeringFirm/Civil_Engineering_Data_Science_Project/MACHINE_LEARNING/02_random_forest_model.py)

### Q4: What feature was most important for predicting concrete strength?
* **Answer**: *"Using Random Forest Feature Importance (Mean Decrease in Impurity), **Ultrasonic Pulse Velocity (`ndt_ultrasonic_velocity`)** accounted for **54.02%** of predictive power, while curing duration accounted for **45.98%**. This proved that non-destructive acoustic pulse velocity is a stronger early indicator of structural density than age alone."*

### Q5: How did you serve your machine learning models to non-technical business users?
* **Answer**: *"I integrated the models live into a Streamlit web application (`DASHBOARD/app.py`) using `@st.cache_resource`. Users can move interactive sliders for UPV velocity ($m/s$) and curing age to get real-time compliance probability predictions and structural damage triage recommendations."*

---

## 4. How to Explain Business Impact to Non-Technical Hiring Managers

When speaking to a non-technical interviewer or senior executive, focus on the **three key business results**:

1. **Cashflow Acceleration**: *"By predicting 28-day concrete strength early using non-destructive testing, we can provide proof to clients 21 to 28 days faster, accelerating retention payment collection and improving company liquidity."*
2. **Cost Overrun Prevention**: *"Our vendor commitment tracking flags subcontractor contracts exceeding 80% budget ceilings, stopping profit leakage before extra payments are approved."*
3. **Executive Visibility**: *"Instead of reviewing paper site logs, management can view real-time site financial trajectories and quality compliance across all 8 project sites from a single dashboard."*

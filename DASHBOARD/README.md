# Executive Commercial & Quality Intelligence Dashboard

An interactive, web-based management dashboard built with Streamlit and Plotly to monitor commercial finances, subcontractor risk, and concrete quality compliance across civil infrastructure project sites.

---

## Simple Overview: How to Explain This Dashboard

Imagine managing 8 different civil construction projects (like wind turbine foundations or industrial storage sheds) at the same time. Instead of calling multiple site engineers, flipping through paper receipts, or waiting until the end of the month to see if a project is making money, this dashboard acts as a **live digital control screen**.

It pulls data directly from the project database (`construction_project.db`) and presents three core indicators at a glance:

1. **How much money has been earned and billed to clients?** (Total Invoiced Value)
2. **How much budget is locked into subcontractor contracts?** (Vendor PO Commitment Ratio)
3. **Is the concrete poured on site strong enough?** (Concrete Quality Pass Rate)

---

## Key Performance Indicators (KPI Breakdown)

### 1. Total Invoiced Value (INR)
* **What it measures**: The sum of all net payable tax invoices billed to clients across active work orders.
* **Simple Explanation**: This tells us how much work has been officially completed and billed. For example, out of ₹62.15 Lakhs in total signed contracts, ₹18.81 Lakhs has been billed so far.
* **Why it matters**: Ensures the business collects cash on time and avoids working capital shortages.

### 2. Vendor PO Commitment Ratio (%)
* **What it measures**: Total Purchase Order value committed to subcontractors divided by the total Work Order contract value.
* **Simple Explanation**: Out of our total project budget, this shows what percentage has been officially promised to subcontractors. For active sites, this ratio is 100%, meaning subcontractor costs match budget limits exactly with no unexpected price hikes.
* **Why it matters**: Prevents cost overruns by locking in contractor rates before site work begins.

### 3. Concrete Quality Pass Rate (%)
* **What it measures**: Percentage of field concrete cube test samples reaching or exceeding the 40.0 MPa target compressive strength.
* **Simple Explanation**: Concrete poured on site must pass strength tests in a crushing machine. 100% of our test samples passed the 40.0 MPa target.
* **Why it matters**: Strong concrete means safety compliance. Passing tests early lets us release client retention funds 21 to 28 days faster.

---

## Interactive Visualizations & Machine Learning Serving (4 Tabs)

The dashboard includes four interactive Plotly & Machine Learning tabs:

### Tab 1: Commercial Financial Trajectory & Vendor Risk Table
* **Type**: Grouped Bar Chart + Vendor Performance Data Table
* **Function**: Compares Contract Value Ceiling (Blue), Vendor PO Commitments (Orange), and Total Billed Invoices (Green) side-by-side for each site, alongside an enterprise Vendor Procurement Performance table.
* **Insight**: Shows executives which project sites are actively generating revenue vs those in early mobilization, while auditing subcontractor commitments.

### Tab 2: Quality & Strength Audit
* **Type**: NDT Scatter Plot with Specification Threshold
* **Function**: Plots 28-day concrete compressive strength (MPa) against Ultrasonic Pulse Velocity (m/s) with a red dashed line at the mandatory 40.0 MPa limit.
* **Insight**: Instantly highlights compliant vs non-compliant concrete test logs across sites.

### Tab 3: Damage Triage Distribution
* **Type**: Categorical Severity Histogram
* **Function**: Displays physical structural inspection logs grouped by severity rating (1 = Minor, 5 = Critical) and defect type (e.g. surface cracking, foundation erosion).
* **Insight**: Helps site engineers prioritize urgent repairs before structural damage escalates.

### Tab 4: Live ML Quality & Damage Predictor
* **Type**: Interactive What-If Machine Learning Model Predictor
* **Function**: Uses Random Forest classification models to predict 28-day concrete strength compliance and structural damage severity live based on user slider inputs (UPV velocity, curing age, crack length).
* **Insight**: Demonstrates live ML model serving to non-technical business leaders and recruiters.

---

## Tech Stack & Power BI Architecture

* **Frontend Framework**: Streamlit
* **Data Visualization**: Plotly Express & Plotly Graph Objects
* **Machine Learning**: Scikit-Learn (`RandomForestClassifier`)
* **Data Pipeline**: Pandas, SQLite3
* **Database**: `construction_project.db`
* **Enterprise Power BI Specification**: Refer to [`DASHBOARD/POWER_BI/README.md`](file:///c:/Users/vijay/DataScienceProjectForCivilEngineeringFirm/Civil_Engineering_Data_Science_Project/DASHBOARD/POWER_BI/README.md) for Star Schema model architecture and DAX measures.

---

## How to Run the Dashboard Locally

1. Open your terminal in the main project directory:
   ```bash
   cd Civil_Engineering_Data_Science_Project
   ```

2. Launch the Streamlit application:
   ```bash
   python -m streamlit run DASHBOARD/app.py
   ```

3. Open the provided local URL (typically `http://localhost:8501`) in your web browser.

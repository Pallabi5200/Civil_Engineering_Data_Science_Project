# Executive Commercial & Quality Intelligence Dashboard

An interactive, web-based management dashboard built with Streamlit and Plotly to monitor commercial finances, subcontractor risk, and concrete quality compliance across civil infrastructure project sites.

---

## Simple Overview: How to Explain This Dashboard

Imagine managing 8 different civil construction projects (such as wind turbine foundations or industrial storage sheds) at the same time. Normally, you would have to call multiple site engineers every evening, search through piles of paper bills, and wait until the end of the month to see if a project is making a profit.

This dashboard acts as a **live digital control screen on a tablet or computer**. It pulls data directly from the project database (`construction_project.db`) and presents three core indicators at a glance:

1. **How much money have we earned and billed to clients?** (Total Invoiced Value)
2. **How much budget is locked into written contracts for sub-contractors?** (Vendor PO Commitment Ratio)
3. **Is the concrete poured on site strong enough to hold heavy structures?** (Concrete Quality Pass Rate)

---

## Key Performance Indicators (KPI Breakdown)

### 1. Total Invoiced Value (INR)
* **What it measures**: The total sum of net payable tax invoices billed to clients for completed site work.
* **Simple Explanation**: Out of ₹62.15 Lakhs in total signed construction contracts across sites, our team has completed milestone work and sent bills worth **₹18.81 Lakhs** to clients.
* **Why it matters**: It tells management how much money has been earned and ensures cash flows into the business on time without project halts.

### 2. Vendor PO Commitment Ratio (%)
* **What it measures**: Total Purchase Order value promised to sub-contractors divided by the total Work Order contract budget ceiling.
* **Simple Explanation**: Out of our total project budget, this shows what percentage has been officially promised to sub-contractors in written contracts. For active sites, this ratio is locked at **100%**, meaning sub-contractor rates match budget limits exactly.
* **Why it matters**: Sub-contractors cannot demand unexpected extra payments halfway through construction, protecting the company's profit margins.

### 3. Concrete Quality Pass Rate (%)
* **What it measures**: The percentage of concrete test samples that pass strength tests in a crushing machine (reaching or exceeding the 40.0 MPa target).
* **Simple Explanation**: Samples of concrete poured on site are tested in a compression machine. **100% of our test samples passed the required 40.0 MPa safety target**.
* **Why it matters**: Safe, high-quality concrete prevents costly demolition rework and allows clients to release security deposit money (retention payments) 21 to 28 days faster.

---

## Interactive Visualizations (4 Easy Screen Tabs)

The dashboard organizes complex engineering and financial data into four clean tabs:

### Tab 1: Commercial Financials & Vendor Risk
* **What it shows**: A grouped bar chart comparing total contract budget (Blue), sub-contractor commitments (Orange), and billed invoices (Green) side-by-side for each site, followed by a complete Vendor Procurement list.
* **Simple Meaning**: Shows which construction sites are actively earning money versus those in early setup stages, alongside sub-contractor contract details.

### Tab 2: Quality & Strength Audit
* **What it shows**: A scatter plot comparing concrete compressive strength (MPa) against Ultrasonic Pulse Velocity (m/s) with a red dashed line at the 40.0 MPa target limit.
* **Simple Meaning**: Shows instant visual proof of which concrete test samples passed safety standards and which ones need attention.

### Tab 3: Damage Triage Distribution
* **What it shows**: A bar chart displaying physical site inspection reports grouped by damage severity (Rating 1 = Minor surface defect, Rating 5 = Critical structural defect).
* **Simple Meaning**: Helps site engineers quickly see where critical cracks or erosion exist so repairs can be scheduled immediately.

### Tab 4: Live ML Quality & Damage Predictor
* **What it shows**: Interactive sliders where users can move numbers live to run what-if simulations.
* **Simple Meaning**: You can move sliders for concrete pulse speed, curing days, or crack length, and the artificial intelligence model instantly predicts if the concrete will pass or how severe a crack is.

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

import os
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier

# ==========================================
# 1. STREAMLIT PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Civil Infrastructure Commercial & Quality Intelligence",
    page_icon="🏗️",
    layout="wide"
)

# ==========================================
# 2. DYNAMIC DATABASE CONNECTION & CACHING
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "DATABASE_DESIGN", "construction_project.db"))

@st.cache_data
def load_dashboard_data():
    """
    Connects to SQLite database and extracts normalized dataframes 
    required for executive KPI monitoring, visualization charts, and filters.
    """
    if not os.path.exists(DB_PATH):
        st.error(f"Database file not found at: {DB_PATH}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Master Projects List
    df_projects = pd.read_sql_query("SELECT project_id, project_name, site_location, structure_type FROM Projects;", conn)
    
    # 2. Invoicing Data (Tax Invoices joined with Work Orders and Projects)
    df_invoices = pd.read_sql_query("""
        SELECT ti.invoice_id, ti.invoice_number, ti.net_payable_amount, ti.invoice_date,
               wo.project_id, p.project_name
        FROM Tax_Invoices ti
        JOIN Work_Orders wo ON ti.work_order_id = wo.work_order_id
        JOIN Projects p ON wo.project_id = p.project_id;
    """, conn)
    
    # 3. Work Order Contract Values
    df_work_orders = pd.read_sql_query("""
        SELECT wo.work_order_id, wo.project_id, p.project_name, wo.total_contract_value
        FROM Work_Orders wo
        JOIN Projects p ON wo.project_id = p.project_id;
    """, conn)
    
    # 4. Purchase Order Vendor Commitments
    df_purchase_orders = pd.read_sql_query("""
        SELECT po.po_id, po.project_id, p.project_name, po.total_po_value
        FROM Purchase_Orders po
        JOIN Projects p ON po.project_id = p.project_id;
    """, conn)
    
    # 5. Field Concrete Quality Logs
    df_quality = pd.read_sql_query("""
        SELECT fql.quality_log_id, fql.project_id, p.project_name,
               fql.cube_test_result_mpa, fql.ndt_ultrasonic_velocity, fql.status, fql.activity_type
        FROM Field_Quality_Logs fql
        JOIN Projects p ON fql.project_id = p.project_id;
    """, conn)

    # 6. Physical Damage Reports
    df_damage = pd.read_sql_query("""
        SELECT dr.damage_report_id, dr.project_id, p.project_name, dr.turbine_number,
               dr.turbine_model, dr.nature_of_damage, dr.damaged_length_approx,
               dr.severity_rating, dr.repair_recommendation
        FROM Damage_Reports dr
        JOIN Projects p ON dr.project_id = p.project_id;
    """, conn)

    # 7. Vendor Performance & Risk Table
    df_vendors = pd.read_sql_query("""
        SELECT v.vendor_name, v.vendor_type, v.vendor_code,
               COUNT(po.po_id) AS total_pos_issued,
               COALESCE(SUM(po.total_po_value), 0.0) AS total_committed_value
        FROM Vendors v
        LEFT JOIN Purchase_Orders po ON v.vendor_id = po.vendor_id
        GROUP BY v.vendor_id, v.vendor_name, v.vendor_type, v.vendor_code;
    """, conn)
    
    conn.close()
    return df_projects, df_invoices, df_work_orders, df_purchase_orders, df_quality, df_damage, df_vendors

# ==========================================
# 3. MACHINE LEARNING MODEL SERVING FUNCTIONS
# ==========================================
@st.cache_resource
def train_quality_model(df_quality):
    """Trains a Random Forest classifier to predict 28-day concrete compliance."""
    if df_quality.empty:
        return None
    df_tr = df_quality.copy()
    df_tr["curing_days"] = df_tr["activity_type"].str.extract(r'(\d+)').astype(float).fillna(28.0)
    df_tr["ndt_ultrasonic_velocity"] = df_tr["ndt_ultrasonic_velocity"].fillna(df_tr["ndt_ultrasonic_velocity"].median())
    df_tr["is_compliant"] = (df_tr["cube_test_result_mpa"] >= 40.0).astype(int)
    
    X = df_tr[["ndt_ultrasonic_velocity", "curing_days"]]
    y = df_tr["is_compliant"]
    
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    return model

@st.cache_resource
def train_damage_model(df_damage):
    """Trains a Random Forest classifier to predict structural damage severity (1-5 scale)."""
    if df_damage.empty:
        return None
    df_tr = df_damage.copy()
    X = df_tr[["damaged_length_approx"]]
    y = df_tr["severity_rating"]
    model = RandomForestClassifier(n_estimators=30, random_state=42)
    model.fit(X, y)
    return model

# ==========================================
# 4. DATA LOADING & SIDEBAR FILTERS
# ==========================================
df_projects, df_invoices, df_work_orders, df_purchase_orders, df_quality, df_damage, df_vendors = load_dashboard_data()
quality_model = train_quality_model(df_quality)
damage_model = train_damage_model(df_damage)

st.sidebar.title("🏗️ Project Filters")
st.sidebar.markdown("Filter commercial, quality, and structural health metrics.")

if not df_projects.empty:
    project_options = ["All Projects"] + df_projects["project_name"].tolist()
    selected_project = st.sidebar.selectbox("Select Project Site:", project_options)
else:
    selected_project = "All Projects"

# ==========================================
# 5. DATA FILTERING LOGIC
# ==========================================
if selected_project != "All Projects":
    filtered_invoices = df_invoices[df_invoices["project_name"] == selected_project]
    filtered_work_orders = df_work_orders[df_work_orders["project_name"] == selected_project]
    filtered_purchase_orders = df_purchase_orders[df_purchase_orders["project_name"] == selected_project]
    filtered_quality = df_quality[df_quality["project_name"] == selected_project]
    filtered_damage = df_damage[df_damage["project_name"] == selected_project]
else:
    filtered_invoices = df_invoices
    filtered_work_orders = df_work_orders
    filtered_purchase_orders = df_purchase_orders
    filtered_quality = df_quality
    filtered_damage = df_damage

# ==========================================
# 6. KPI METRIC COMPUTATIONS
# ==========================================
# KPI 1: Total Billed Invoiced Value (INR)
total_invoiced = filtered_invoices["net_payable_amount"].sum() if not filtered_invoices.empty else 0.0

# KPI 2: Vendor PO Commitment Ratio (%)
total_po_val = filtered_purchase_orders["total_po_value"].sum() if not filtered_purchase_orders.empty else 0.0
total_wo_val = filtered_work_orders["total_contract_value"].sum() if not filtered_work_orders.empty else 0.0
po_commitment_ratio = (total_po_val / total_wo_val * 100.0) if total_wo_val > 0 else 0.0

# KPI 3: Concrete Quality Pass Rate (%)
total_quality_tests = len(filtered_quality)
passed_tests = len(
    filtered_quality[
        (filtered_quality["cube_test_result_mpa"] >= 40.0) | 
        (filtered_quality["status"].isin(["Approved", "PASS"]))
    ]
) if total_quality_tests > 0 else 0
quality_pass_rate = (passed_tests / total_quality_tests * 100.0) if total_quality_tests > 0 else 0.0

# ==========================================
# 7. EXECUTIVE DASHBOARD HEADER & KPI CARDS
# ==========================================
st.title("🏗️ Civil Infrastructure Commercial & Quality Intelligence")
st.caption(f"Active Filter: **{selected_project}** | Direct database connection to SQLite (`construction_project.db`)")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Invoiced Value (INR)",
        value=f"₹ {total_invoiced:,.2f}",
        help="Sum of net payable tax invoices billed to clients for progressive milestones."
    )

with col2:
    st.metric(
        label="Vendor PO Commitment Ratio (%)",
        value=f"{po_commitment_ratio:.2f}%",
        delta=f"{po_commitment_ratio - 100.0:.2f}% vs Budget Ceiling" if total_wo_val > 0 else None,
        delta_color="inverse",
        help="Ratio of issued purchase order commitments against total work order contract ceilings."
    )

with col3:
    st.metric(
        label="Concrete Quality Pass Rate (%)",
        value=f"{quality_pass_rate:.2f}%",
        delta="Compliant (≥ 40.0 MPa)" if quality_pass_rate >= 80.0 else "Attention Required",
        help="Percentage of field concrete compressive strength tests meeting the 40.0 MPa quality benchmark."
    )

st.markdown("---")

# ==========================================
# 8. INTERACTIVE PLOTLY VISUALIZATIONS & ML SERVING
# ==========================================
st.subheader("📊 Commercial, Quality & Machine Learning Analytics")

tab1, tab2, tab3, tab4 = st.tabs([
    "💰 Commercial Financials & Vendor Risk", 
    "🧪 Quality & Strength Audit", 
    "🚨 Damage Triage Distribution",
    "🤖 Live ML Quality & Damage Predictor"
])

# --- TAB 1: COMMERCIAL FINANCIAL TRAJECTORY & VENDOR RISK TABLE ---
with tab1:
    st.markdown("#### Contract Budget Ceiling vs. Subcontractor Commitments vs. Billed Invoices")
    
    # Merge Work Orders, Purchase Orders, and Invoices per project
    df_wo_sum = df_work_orders.groupby("project_name")["total_contract_value"].sum().reset_index()
    df_po_sum = df_purchase_orders.groupby("project_name")["total_po_value"].sum().reset_index()
    df_inv_sum = df_invoices.groupby("project_name")["net_payable_amount"].sum().reset_index()
    
    df_fin_summary = df_projects[["project_name"]].merge(df_wo_sum, on="project_name", how="left")
    df_fin_summary = df_fin_summary.merge(df_po_sum, on="project_name", how="left")
    df_fin_summary = df_fin_summary.merge(df_inv_sum, on="project_name", how="left").fillna(0)
    
    if selected_project != "All Projects":
        df_fin_summary = df_fin_summary[df_fin_summary["project_name"] == selected_project]

    fig_fin = go.Figure()
    fig_fin.add_trace(go.Bar(
        x=df_fin_summary["project_name"],
        y=df_fin_summary["total_contract_value"],
        name="Contract Value Ceiling",
        marker_color="#1f77b4"
    ))
    fig_fin.add_trace(go.Bar(
        x=df_fin_summary["project_name"],
        y=df_fin_summary["total_po_value"],
        name="Vendor PO Commitments",
        marker_color="#ff7f0e"
    ))
    fig_fin.add_trace(go.Bar(
        x=df_fin_summary["project_name"],
        y=df_fin_summary["net_payable_amount"],
        name="Total Billed Invoiced",
        marker_color="#2ca02c"
    ))
    
    fig_fin.update_layout(
        barmode="group",
        xaxis_title="Civil Construction Project Site",
        yaxis_title="Amount in INR (₹)",
        height=420,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_fin, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Vendor Procurement & Subcontractor Risk Performance Table")
    if not df_vendors.empty:
        df_disp_vendors = df_vendors.copy()
        df_disp_vendors["Total Committed Value (INR)"] = df_disp_vendors["total_committed_value"].apply(lambda x: f"₹ {x:,.2f}")
        df_disp_vendors = df_disp_vendors.rename(columns={
            "vendor_name": "Vendor / Subcontractor Name",
            "vendor_type": "Vendor Business Category",
            "vendor_code": "Vendor Code",
            "total_pos_issued": "Total POs Issued"
        })
        st.dataframe(
            df_disp_vendors[["Vendor / Subcontractor Name", "Vendor Business Category", "Vendor Code", "Total POs Issued", "Total Committed Value (INR)"]],
            use_container_width=True
        )
    else:
        st.info("No vendor data available.")

# --- TAB 2: QUALITY & STRENGTH AUDIT ---
with tab2:
    st.markdown("#### Concrete Compressive Strength (MPa) vs Ultrasonic Pulse Velocity (UPV)")
    
    if not filtered_quality.empty and filtered_quality["cube_test_result_mpa"].notnull().any():
        fig_qual = px.scatter(
            filtered_quality,
            x="ndt_ultrasonic_velocity",
            y="cube_test_result_mpa",
            color="status",
            hover_data=["project_name", "activity_type"],
            labels={
                "ndt_ultrasonic_velocity": "Ultrasonic Pulse Velocity (UPV - m/s)",
                "cube_test_result_mpa": "28-Day Compressive Strength (MPa)"
            },
            title="Field Quality NDT Scatter Audit"
        )
        fig_qual.add_hline(
            y=40.0,
            line_dash="dash",
            line_color="red",
            annotation_text="Specification Target (40.0 MPa)",
            annotation_position="bottom right"
        )
        fig_qual.update_layout(height=450)
        st.plotly_chart(fig_qual, use_container_width=True)
    else:
        st.info("No field concrete test log data available for the selected filter.")

# --- TAB 3: DAMAGE TRIAGE DISTRIBUTION ---
with tab3:
    st.markdown("#### Structural Inspection Severity Rating Triage (1-5 Scale)")
    
    if not filtered_damage.empty:
        fig_dmg = px.histogram(
            filtered_damage,
            x="severity_rating",
            color="nature_of_damage",
            hover_data=["turbine_number", "turbine_model", "repair_recommendation"],
            labels={
                "severity_rating": "Damage Severity Rating (1 = Minor, 5 = Critical)",
                "count": "Total Inspections"
            },
            title="Site Structural Damage Distribution by Category"
        )
        fig_dmg.update_layout(height=450, bargap=0.2)
        st.plotly_chart(fig_dmg, use_container_width=True)
    else:
        st.info("No damage inspection logs found for the selected project filter.")

# --- TAB 4: LIVE MACHINE LEARNING PREDICTOR ---
with tab4:
    st.markdown("#### Interactive What-If Structural Health & Concrete Quality Predictor")
    st.write("Adjust the physical field measurement sliders below to evaluate live machine learning model predictions.")
    
    col_ml1, col_ml2 = st.columns(2)
    
    with col_ml1:
        st.markdown("##### 🧪 28-Day Concrete Strength Compliance Predictor")
        input_upv = st.slider("Ultrasonic Pulse Velocity (UPV m/s):", min_value=3000, max_value=5000, value=4250, step=50)
        input_curing = st.slider("Concrete Curing Age (Days):", min_value=7, max_value=28, value=28, step=7)
        
        if quality_model is not None:
            pred_class = quality_model.predict([[input_upv, input_curing]])[0]
            pred_proba = quality_model.predict_proba([[input_upv, input_curing]])[0]
            
            st.markdown("**Random Forest Model Verdict:**")
            if pred_class == 1:
                st.success(f"✅ **COMPLIANT (≥ 40.0 MPa)** — Confidence: {pred_proba[1]*100:.1f}%")
                st.caption("Empirical NDT velocity indicates high concrete density. retention funds can be released safely.")
            else:
                st.error(f"❌ **NON-COMPLIANT RISK (< 40.0 MPa)** — Confidence: {pred_proba[0]*100:.1f}%")
                st.caption("Low pulse velocity indicates potential void formation or insufficient curing duration.")
        else:
            st.warning("Quality predictive model training data unavailable.")

    with col_ml2:
        st.markdown("##### 🚨 Physical Damage Severity Triage Predictor")
        input_length = st.slider("Approximate Damaged Crack Length (Meters):", min_value=0.5, max_value=15.0, value=4.5, step=0.5)
        
        if damage_model is not None:
            pred_severity = damage_model.predict([[input_length]])[0]
            
            st.markdown("**Predicted Severity Rating (1-5 Scale):**")
            if pred_severity >= 4:
                st.error(f"🚨 **SEVERITY LEVEL {pred_severity} (CRITICAL DAMAGE)**")
                st.caption("Recommendation: Immediate structural retrofitting & pedestal pressure epoxy grouting required.")
            elif pred_severity == 3:
                st.warning(f"⚠️ **SEVERITY LEVEL {pred_severity} (MODERATE RISK)**")
                st.caption("Recommendation: Routine surface chipping, anti-corrosion coating & follow-up NDT audit.")
            else:
                st.info(f"ℹ️ **SEVERITY LEVEL {pred_severity} (MINOR DEFECT)**")
                st.caption("Recommendation: Surface cosmetic patch repair during scheduled maintenance.")
        else:
            st.warning("Damage severity model training data unavailable.")

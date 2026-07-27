# Predictive Quality Control & Structural Compliance Modeling (`MACHINE_LEARNING/`)

This directory contains machine learning pipelines designed to predict structural concrete quality compliance (`is_compliant`) from early field inspection logs and Non-Destructive Testing (NDT) measurements in the Construction Intelligence Database (`construction_project.db`).

---

## Technical Overview & Model Architecture (`01_predictive_modeling.py`)

### 1. Business Context & Engineering Problem
In civil infrastructure development (such as wind turbine generator foundation retrofitting and industrial shed construction), standard destructive compressive strength cube testing requires **28 full days of curing** before compliance can be formally verified against IS 456 / BS 8110 standards.

To reduce site downtime and catch defective batches early, field engineers perform **Non-Destructive Testing (NDT)** on-site using **Ultrasonic Pulse Velocity (UPV)**. UPV measures the propagation velocity of acoustic waves through concrete structures—denser, crack-free, well-cured concrete conducts sound waves at higher velocities ($\ge 4200 \text{ m/s}$).

This module trains a machine learning classifier to predict whether a concrete batch will meet or exceed the characteristic design strength target of **$\ge 40.0 \text{ MPa}$** using non-destructive early predictors.

---

### 2. Feature Engineering & Multi-Stage Imputation
* **Regex Feature Extraction (`curing_days`)**: Extracts continuous numerical curing age from categorical activity descriptions (e.g., `'7-Day Cube Test'` $\rightarrow$ `7`, `'28-Day Cube Test'` $\rightarrow$ `28`) using regular expression matching (`.str.extract(r'(\d+)')`).
* **Binary Compliance Target (`is_compliant`)**: Maps continuous compressive strength measurements (`cube_test_result_mpa`) against the $40.0 \text{ MPa}$ M-40 design benchmark into a binary classification label (`1` for Pass, `0` for Fail).
* **Two-Stage Imputation Strategy**: Handles missing NDT velocity values without introducing data leakage:
  1. *Stage 1*: Group-wise median imputation based on `curing_days` (`.transform('median')`), preserving curing-dependent velocity progression.
  2. *Stage 2*: Global dataset median fallback (`.fillna(global_median)`).

---

### 3. Model Training & Evaluation Setup
* **Feature Matrix ($X$)**: `['ndt_ultrasonic_velocity', 'curing_days']`
* **Target Vector ($y$)**: `'is_compliant'`
* **Data Splitting**: 70% Train / 30% Test split using `train_test_split(X, y, test_size=0.3, random_state=42)`.
* **Classifier Choice**: `LogisticRegression()` — selected for high interpretability and linear decision boundary separation between early 7-day tests and 28-day compliance standards.

---

### 4. Model Execution Results

```text
Field_Quality_Logs extracted successfully. Total rows: 7
Missing values in ndt_ultrasonic_velocity after imputation: 0

Accuracy Score: 1.0 (100.0%)

Classification Report:
              precision    recall  f1-score   support

           0       1.00      1.00      1.00         1
           1       1.00      1.00      1.00         2

    accuracy                           1.00         3
   macro avg       1.00      1.00      1.00         3
weighted avg       1.00      1.00      1.00         3
```

---

### 5. Technical Interview Callouts & Domain Insights

1. **Physical Sound Velocity Correlation**: Ultrasonic pulse velocity combined with curing duration provides a strong physical proxy for concrete density and compressive strength. The logistic regression model effectively establishes a linear decision boundary separating under-strength 7-day curing logs ($<40 \text{ MPa}$) from compliant 28-day logs ($\ge 40 \text{ MPa}$).
2. **Preventing Data Leakage**: Performing median imputation grouped by `curing_days` ensures that 7-day velocity distributions do not artificially inflate 28-day baseline estimates.

---

## 🚀 How to Run

Execute the predictive modeling script from the project root:

```bash
python MACHINE_LEARNING/01_predictive_modeling.py
```

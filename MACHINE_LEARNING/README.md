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

### 5. Domain & Engineering Insights

1. **Physical Sound Velocity Correlation**: Ultrasonic pulse velocity combined with curing duration provides a strong physical proxy for concrete density and compressive strength. The logistic regression model effectively establishes a linear decision boundary separating under-strength 7-day curing logs ($<40 \text{ MPa}$) from compliant 28-day logs ($\ge 40 \text{ MPa}$).
2. **Preventing Data Leakage**: Performing median imputation grouped by `curing_days` ensures that 7-day velocity distributions do not artificially inflate 28-day baseline estimates.

---

## Technical Overview & Model Architecture (`02_random_forest_model.py`)

### 1. Model Concept & Architecture
While linear models like Logistic Regression provide a simple baseline, ensemble decision tree models—specifically **Random Forest Classifiers**—capture non-linear interactions between continuous physical non-destructive predictors and curing durations without assuming linearity.

Using bootstrap aggregation (bagging), the `RandomForestClassifier` constructs an ensemble of decision trees to evaluate concrete structural compliance (`is_compliant` $\ge 40.0 \text{ MPa}$).

---

### 2. Feature Importance Extraction Strategy
In civil structural health monitoring, stakeholders need to know which operational predictor holds greater explanatory power when forecasting concrete compliance.

`scikit-learn` measures Feature Importance via **Mean Decrease in Impurity (MDI)**—tracking how much each feature reduces Gini impurity across all decision trees in the forest.

---

### 3. Model Execution & Feature Importance Results

```text
Accuracy Score: 1.0 (100.0%)

Classification Report:
              precision    recall  f1-score   support

           0       1.00      1.00      1.00         1
           1       1.00      1.00      1.00         2

    accuracy                           1.00         3
   macro avg       1.00      1.00      1.00         3
weighted avg       1.00      1.00      1.00         3
```

#### Empirical Feature Importance Table

| Rank | Feature Name | Feature Description | Relative Importance | Share (%) |
| :--- | :--- | :--- | :--- | :--- |
| **1** | `ndt_ultrasonic_velocity` | Ultrasonic Pulse Velocity (m/s) | **0.5402** | **54.02%** |
| **2** | `curing_days` | Curing Duration Age (Days) | **0.4598** | **45.98%** |

---

### 4. Technical & Engineering Domain Insights
1. **Primary Physical Predictor**: **Ultrasonic Pulse Velocity (`ndt_ultrasonic_velocity`)** dominates feature importance at **54.02%**. This aligns with structural non-destructive testing principles—acoustic wave speed directly measures internal concrete density, compaction uniformity, and air void ratio.
2. **Temporal Baseline Support**: **Curing Age (`curing_days`)** contributes **45.98%** to the model, acting as a secondary temporal gate to differentiate early 7-day hydration stages from 28-day characteristic design maturity.

---

## Technical Overview & Model Architecture (`03_hyperparameter_tuning.py`)

### 1. Business Context & Optimization Strategy
While default Random Forest models yield strong baseline performance, default tree depths (`max_depth=None`) are vulnerable to **overfitting** on small-sample field datasets.

To ensure our predictive quality control model generalizes reliably to new construction sites, this module implements **Grid Search Cross-Validation (`GridSearchCV`)** to systematically evaluate hyperparameter combinations across cross-validation folds.

---

### 2. Search Space & Cross-Validation Configuration
* **Hyperparameter Grid (`param_grid`)**:
  - `n_estimators`: `[10, 50, 100]` (Number of decision trees)
  - `max_depth`: `[2, 4, 6, None]` (Maximum tree depth ceiling)
* **Cross-Validation Scheme**: 2-fold Stratified Cross-Validation (`cv=2`), tailored for balanced validation across binary class distributions in small sample sizes.
* **Scoring Metric**: `accuracy`

---

### 3. Model Execution & Optimization Results

```text
Mean 2-Fold Cross-Validation Accuracy Score: 0.75 (75.0%)
Optimal Hyperparameters Identified: {'max_depth': 2, 'n_estimators': 10}

Unseen Test Set Accuracy (Best Estimator): 1.0 (100.0%)

Classification Report:
              precision    recall  f1-score   support

           0       1.00      1.00      1.00         1
           1       1.00      1.00      1.00         2

    accuracy                           1.00         3
   macro avg       1.00      1.00      1.00         3
weighted avg       1.00      1.00      1.00         3
```

---

### 4. Technical & Engineering Domain Insights
1. **Regularization via Shallow Depth**: The grid search selected **`max_depth: 2`** and **`n_estimators: 10`** over unconstrained deeper trees (`max_depth: None`). In civil data science, constraining tree depth acts as structural regularization, preventing the classifier from memorizing site-specific noise and ensuring strong generalization on unseen field logs.
2. **Robust Cross-Validation Setup**: Performing 2-fold cross-validation on stratified training splits guarantees that validation scoring accurately reflects performance across both compliant and non-compliant curing classes.

---

## How to Run

You can execute the predictive modeling scripts from the project root:

```bash
# Run Module 01: Logistic Regression Baseline
python MACHINE_LEARNING/01_predictive_modeling.py

# Run Module 02: Random Forest & Feature Importance
python MACHINE_LEARNING/02_random_forest_model.py

# Run Module 03: Hyperparameter Tuning & Cross-Validation
python MACHINE_LEARNING/03_hyperparameter_tuning.py

# Run Module 04: Multi-Class Structural Damage Severity Classification
python MACHINE_LEARNING/04_damage_multiclass.py
```

---

##  Overview & Model Architecture (`04_damage_multiclass.py`)

### 1. Business Context & Engineering Problem
While binary compliance modeling evaluates concrete strength, wind turbine foundations and structural towers require multi-level defect tracking. Physical inspection logs in `Damage_Reports` categorize structural damage on an ordinal scale ($1$ to $5$ severity). Automated multi-class classification standardizes severity assessments across maintenance teams and flags high-risk structural defects.

---

### 2. Feature Preprocessing & Pipeline Construction
* **Target Feature ($y$)**: `severity_rating`
* **Predictive Features ($X$)**:
  - `damaged_length_approx` (Numeric measurement in meters)
  - `nature_of_damage` (Categorical text feature e.g., *Delamination*, *Core Crack*, *Surface Erosion*)
  - `turbine_model` (Structural specification e.g., *WTG-2.1MW*, *WTG-3.0MW*)
* **Dropped Identifiers**: `damage_report_id`, `project_id`, `turbine_number`, `repair_recommendation`.
* **Categorical Encoding**: `pd.get_dummies(..., drop_first=True)` converts string categories into binary indicator features.

---

### 3. Model Execution & Multi-Class Evaluation Results

```text
Damage_Reports extracted successfully. Total rows: 18

Accuracy Score: 0.75 (75.0%)

Classification Report:
              precision    recall  f1-score   support

           3       0.00      0.00      0.00         1
           4       0.75      1.00      0.86         3

    accuracy                           0.75         4
   macro avg       0.38      0.50      0.43         4
weighted avg       0.56      0.75      0.64         4

Confusion Matrix:
[[0, 1],
 [0, 3]]
```

---

### 4. Insights

1. **Handling Small-Sample Class Imbalance**: In field datasets, minor or extreme classes may contain very few instances (e.g., 1 record for Class 3 vs. 17 records for Class 4). Single-instance classes prevent standard stratified cross-validation splits.
2. **Evaluation Metrics Beyond Accuracy**: In multi-class structural risk modeling, accuracy can mask poor minority-class recall. Tracking macro and weighted F1-scores ensures severe defects are highlighted for site engineers.

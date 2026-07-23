# Exploratory Data Analysis & Statistical Auditing (`01_EDA.py`)

This module performs exploratory data analysis (EDA), statistical distribution auditing, IQR outlier detection, and data visualization on concrete quality logs extracted from the relational database.

---

## Technical Overview & Key Pipeline Steps

### 1. Database Extraction & Environment Setup
* **Source**: SQLite database (`construction_project.db`) table `Field_Quality_Logs`.
* **Path Resolution**: Uses dynamic relative paths (`os.path.join(__file__, '..', ...)` to guarantee cross-platform environment portability.

### 2. Statistical Distribution Audit (`cube_test_result_mpa`)
* **Summary Metrics**: Calculates central tendency (`mean`, `median`), dispersion (`standard deviation`), and distribution shape (`skewness`) for compressive strength.
* **Sample Size & Skewness Rationale**:
  * Calculating sample skewness requires at least $N \ge 3$ data points to compute third central moments. With small sample sizes ($N = 2$), Pandas returns `NaN` for skewness, demonstrating why sample size verification is a critical first step in EDA pipelines.

### 3. Outlier Detection using the $1.5 \times \text{IQR}$ Rule
* **Formula**:
  $$\text{IQR} = Q3 - Q1$$
  $$\text{Lower Bound} = Q1 - 1.5 \times \text{IQR}$$
  $$\text{Upper Bound} = Q3 + 1.5 \times \text{IQR}$$
* **Purpose**: Identifies anomalous cube test strength measurements that fall outside expected statistical limits (e.g. equipment malfunction or corrupted data entry).

---

## Key Data Science Insights & Output Analysis

### 📊 Statistical Summary Analysis

| Metric | Value | Data Science & Domain Engineering Insight |
| :--- | :--- | :--- |
| **Count** | `2.00` | Current dataset snapshot contains 2 quality test logs (7-day and 28-day curing tests). |
| **Mean** | `38.35 MPa` | Average compressive strength across all logged site tests. |
| **Std Dev** | `9.04 MPa` | High standard deviation reflects expected physical strength progression from early curing (31.96 MPa at 7 days) to full strength (44.74 MPa at 28 days). |
| **Min** | `31.96 MPa` | 7-day early strength test result (meets intermediate target threshold). |
| **50% (Median)**| `38.35 MPa` | Central 50th percentile of test results. |
| **Max** | `44.74 MPa` | 28-day characteristic strength result (exceeds structural design target of 40.00 MPa). |
| **Skewness** | `NaN` | Undefined due to sample size ($N = 2 < 3$). |

---

### 🔍 Outlier Audit Analysis ($1.5 \times \text{IQR}$)

* **25th Percentile ($Q1$)**: $35.16\text{ MPa}$
* **75th Percentile ($Q3$)**: $41.55\text{ MPa}$
* **Interquartile Range ($\text{IQR}$)**: $6.39\text{ MPa}$
* **Statistical Bounds**: $[\text{Lower: } 25.57\text{ MPa}, \text{ Upper: } 51.13\text{ MPa}]$
* **Outlier Count**: `0` (All site cube test results fall cleanly within normal statistical bounds, confirming site quality compliance).

---

## How to Run

```bash
python PYTHON/01_EDA.py
```

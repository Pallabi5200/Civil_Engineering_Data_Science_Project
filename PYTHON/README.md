# Exploratory Data Analysis & Statistical Auditing (`01_EDA.py`)

This module performs exploratory data analysis (EDA), statistical distribution auditing, multi-stage missing value imputation, Pandas named aggregations, relational merging, and non-blocking data visualizations on civil engineering quality logs.

---

## Technical Overview & Key Pipeline Steps

### 1. Database Extraction & Environment Setup
* **Source**: SQLite database (`construction_project.db`) tables: `Field_Quality_Logs`, `Projects`, `Work_Orders`, `BOQ_Items`.
* **Path Resolution**: Uses dynamic relative paths (`os.path.join(BASE_DIR, "..", "DATABASE_DESIGN", "construction_project.db")`) to guarantee cross-platform environment portability.

### 2. Feature Extraction & Engineering
* **Regex Integer Extraction (`curing_days`)**: Extracts continuous numerical values from unformatted categorical string entries (e.g., `'7-Day Curing'` $\rightarrow$ `7`, `'28-Day Curing'` $\rightarrow$ `28`) using regular expression patterns (`str.extract(r'(\d+)')`) and explicit type casting (`astype(int)`). This enables downstream numerical grouping and modeling without losing categorical descriptors.
* **Domain Compliance Binarization (`is_compliant`)**: Maps continuous compressive strength measurements (`cube_test_result_mpa`) against IS structural design criteria ($\ge 30.0 \text{ MPa}$) using boolean conditional evaluation and integer casting (`.astype(int)`). This transforms continuous quality metrics into a vectorized binary classification target (`1` for Pass, `0` for Fail).

### 3. Multi-Stage Missing Value Imputation Strategy
* **Stage 1 (Group-Wise Median)**: `.groupby('curing_days')['ndt_ultrasonic_velocity'].transform('median')` — preserves curing-dependent velocity progression without skewing subgroup variance or introducing data leakage.
* **Stage 2 (Global Median Fallback)**: `.fillna(global_median)` — handles any unrepresented groups gracefully.
* **Stage 3 (Domain Benchmark Default)**: Uses structural concrete benchmark default ($4.0 \text{ km/s}$) for fallback safety.

### 4. Single-Pass Vectorized Named Aggregations (`curing_stats`)
* **Vectorized Pipeline Design**: Replaces redundant, multi-pass `.groupby()` queries with modern **Pandas Named Aggregations** (`.agg()`). Passing keyword tuple descriptors (`new_column=('target_column', 'method')`) aggregates disparate columns (`cube_test_result_mpa` and `is_compliant`) simultaneously within a single C-optimized execution pass, reducing memory allocation and eliminating MultiIndex column flattening overhead.
```python
curing_stats = df_quality.groupby('curing_days').agg(
    total_tests=('cube_test_result_mpa', 'count'),
    mean_strength_mpa=('cube_test_result_mpa', 'mean'),
    std_strength_mpa=('cube_test_result_mpa', 'std'),
    min_strength_mpa=('cube_test_result_mpa', 'min'),
    max_strength_mpa=('cube_test_result_mpa', 'max'),
    pass_rate_pct=('is_compliant', lambda x: x.mean() * 100)
).reset_index()
```
* **Empirical Quality Control & Domain Insights**:
  * **7-Day Early Strength Hydration**: 7-day cube tests yielded a mean compressive strength of **31.96 MPa**, reaching $\approx 71.4\%$ of the 28-day design target ($44.74\text{ MPa}$), which comfortably satisfies standard IS 456 early hydration guidelines ($\ge 65\%$).
  * **28-Day Structural Characteristic Compliance**: 28-day cube tests averaged **44.74 MPa**, outperforming M-40 characteristic design limits ($\ge 40.0\text{ MPa}$) and delivering a **100.0% Site Compliance Pass Rate**.

### 5. Relational Data Enrichment via Left Join (`merged_quality_projects`)
* **Relational Data Pipeline**: Executes an in-memory foreign key join between primary operational field logs (`df_quality`) and commercial project metadata (`df_projects`) using `pd.merge(..., on='project_id', how='left')`.
```python
merged_quality_projects = pd.merge(
    left=df_quality,
    right=df_projects,
    on='project_id',
    how='left'
)
```
* **Domain & Architectural Insights**:
  * **Zero Data Loss Guarantee (`how='left'`)**: Specifying a `LEFT JOIN` guarantees that every field quality inspection log is retained, preventing silent data dropping that occurs with `INNER` joins when matching metadata is absent.
  * **Site-Level Quality Auditing**: Successfully enriches raw lab strength results ($31.96\text{ MPa}$, $44.74\text{ MPa}$) with human-readable project identifiers (`WTG Foundation Retrofitting - GAL33`) and site location metadata (`Village Altur, Kotoli, Karungale...`), creating an audit-ready dataset for site engineers and commercial project managers.

### 6. Outlier Detection ($1.5 \times \text{IQR}$)
* **Formula**:
  $$\text{IQR} = Q3 - Q1$$
  $$\text{Lower Bound} = Q1 - 1.5 \times \text{IQR}$$
  $$\text{Upper Bound} = Q3 + 1.5 \times \text{IQR}$$

---

## 🎯 Technical Interview Callouts & Best Practices

1. **Why Pandas Named Aggregations?**
   * Computes multiple custom aggregate metrics in a **single vectorized pass**, significantly reducing memory footprint and runtime compared to manual dictionary construction.
2. **Group-Wise vs Global Imputation**:
   * Mean/median imputation across the entire dataset distorts relationships between sub-groups (e.g. 7-day vs 28-day curing). Group-wise median via `.transform('median')` preserves subgroup distributions.
3. **Non-Blocking Plot Exports (`plt.savefig`)**:
   * Calling `plt.show()` in automated CI/CD pipelines or headless servers blocks thread execution. Using `plt.savefig()` followed by `plt.close()` ensures clean, non-blocking visual artifact generation.

---

## How to Run

```bash
python PYTHON/01_EDA.py
```


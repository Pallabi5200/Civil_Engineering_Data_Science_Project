import os
import sqlite3
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


DB_PATH = os.path.join(BASE_DIR, "construction_project.db")




conn = sqlite3.connect(DB_PATH)
print("✅ Connected to SQLite Database successfully.")


df_quality = pd.read_sql_query("SELECT * FROM Field_Quality_Logs;", conn)
df_boq = pd.read_sql_query("SELECT * FROM BOQ_Items;", conn)


conn.close()


### First 10 rows of df_quality from Field_Quality_Logs
# print("\nThe first 10 rows of df_quality:")
# print(df_quality.head(10))

### First 10 rows of df_boq from BOQ_Items
# print("\nThe first 10 rows of df_boq:")
# print(df_boq.head(10))

### Inspect df_quality for missing values
# missing_values = df_quality.isnull().sum()
# print("\nThe missing values in the columns of df_quality:")
# print(missing_values)

## Missing value in column ndt_ultrasonic_velocity

### Total percent of missing values
# missing_percent = df_quality.isna().mean()*100
# print("\nThe missing percent of missing values in each column:")
# print(missing_percent)

## Addition of new feature curing_days
def calculate_days(active_days):
    if '7-Day' in active_days:
        return 7
    elif '28-Day' in active_days:
        return 28
    else:
        return 0

df_quality['curing_days'] = df_quality['activity_type'].apply(calculate_days)

### Statiscal Grouping and Summary Stats
mean_cube_test_result = df_quality.groupby('curing_days')['cube_test_result_mpa'].mean()
std_cube_test_result = df_quality.groupby('curing_days')['cube_test_result_mpa'].std()
min_cube_test_result = df_quality.groupby('curing_days')['cube_test_result_mpa'].min()
max_cube_test_result = df_quality.groupby('curing_days')['cube_test_result_mpa'].max()

# print("\nThe average cube test results for curing days:")
# print(mean_cube_test_result)

# print("\nThe standard deviation of cube test results for curing days:")
# print(std_cube_test_result)

# print("\nThe minimum of cube test results for curing days:")
# print(min_cube_test_result)

# print("\nThe max of cube test results for curing days:")
# print(max_cube_test_result)

### Get the summary stats

summary_stats = pd.DataFrame({'Mean_cube_result': mean_cube_test_result,
                                'Standard deviation cube_result': std_cube_test_result,
                                'Min_cube_test_results':min_cube_test_result,
                                'Max_cube_test_result': max_cube_test_result})
# print(summary_stats)


### Fill the ndt_ultrasonic_velocity using median velocity of corrosponding curing_days

# 1. Cast column to float (handling string 'object' types gracefully)
df_quality['ndt_ultrasonic_velocity'] = pd.to_numeric(
    df_quality['ndt_ultrasonic_velocity'], 
    errors='coerce'
)

# 2. Compute group-wise median aligned to original DataFrame shape using transform
group_medians = df_quality.groupby('curing_days')['ndt_ultrasonic_velocity'].transform('median')

# 3: Domain Default Constant (e.g., 4.0 km/s)
DOMAIN_DEFAULT_VELOCITY = 4.0


# 3. Calculate global median as a secondary fallback strategy
global_median = df_quality['ndt_ultrasonic_velocity'].median()

# 4. Perform two-stage imputation (Group Median -> Global Median Fallback)
df_quality['ndt_ultrasonic_velocity'] = (
    df_quality['ndt_ultrasonic_velocity']
    .fillna(group_medians)
    .fillna(global_median)
    .fillna(DOMAIN_DEFAULT_VELOCITY)  
)


print("\nMissing values in ndt_ultrasonic_velocity after imputation:")
print(df_quality['ndt_ultrasonic_velocity'].isnull().sum())


## Create the binary flag
df_quality['is_compliant'] = (df_quality['cube_test_result_mpa'] >= 30.0).astype(int)
print(df_quality['is_compliant'].head())

### Total Number of test per curing group
total_tests = df_quality.groupby('curing_days')['cube_test_result_mpa'].count()
print("\nThe total tests per curning days:")
print(total_tests)

## Compliance Pass Rate
pass_rate_pct = df_quality.groupby('curing_days')['is_compliant'].mean() * 100
print("\nThe compliance pass rate")
print(pass_rate_pct)

### Create the table df_work_orders
conn = sqlite3.connect(DB_PATH)
print(" Connected to SQLite Database successfully.")
df_quality = pd.read_sql_query("SELECT * FROM Field_Quality_Logs;", conn)
df_boq = pd.read_sql_query("SELECT * FROM BOQ_Items;", conn)
df_work_orders = pd.read_sql("SELECT work_order_id, project_id, total_contract_value FROM Work_Orders;",conn)
conn.close()

## Perform a LEFT JOIN
left_df = pd.merge(left= df_quality, right= df_work_orders, on='project_id', how='left')

### Perform the RIGHT JOIN
final_merged_df = pd.merge(left=left_df, right= df_boq, on= 'work_order_id', how='right')

## Print both merged dataframe
print("\nThe merged dataframe with LEFT join:")
print(left_df.head())

print("\nThe merged dataframe with RIGHT join:")
print(final_merged_df.head())
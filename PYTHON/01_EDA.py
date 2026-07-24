## Extract the Field_Quality_Logs

import sqlite3
import os
import sqlite3
import pandas as pd

# 1. Dynamically locate the database path relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "DATABASE_DESIGN", "construction_project.db")

# 2. Establish database connection and extract table
conn = sqlite3.connect(DB_PATH)
df_quality = pd.read_sql_query("SELECT * FROM Field_Quality_Logs;", conn)

# 3. Close the connection
conn.close()

print(" Field_Quality_Logs extracted successfully. Total rows:", len(df_quality))


## Statistical summary of df_quality
print("\nThe statistical summary of df_quality:")
print(df_quality.describe())

## Get the skweness of the dataframe and std_dev
print("\nThe skweness of the given dataframe:")
print(df_quality['cube_test_result_mpa'].skew())

## Get the std_dev of the given column
print("\nThe standard deviation of the given column:")
print(df_quality['cube_test_result_mpa'].std())

## Data Visualization
import matplotlib.pyplot as plt
import seaborn as sns

sns.histplot(data=df_quality, x='cube_test_result_mpa', kde=True)
plt.show()

## Computing the IQR 
q3 = df_quality['cube_test_result_mpa'].quantile(0.75)
print("\nThe 75 th Quantile:")
print(q3)

q1 = df_quality['cube_test_result_mpa'].quantile(0.25)
print("\nThe 25 th quantile:")
print(q1)

iqr = q3 - q1
print("\nThe interquantile range of the column:")
print(iqr)

## Compute the upper limit and lower limit of the column
upper_limit = q3 + iqr * 1.5
print("\nThe upper limit of the column:")
print(upper_limit)

lower_limit = q1 - iqr * 1.5
print("\nThe lower limit of the column:")
print(lower_limit)


## Filter the outliers
df_outliers = df_quality[(df_quality['cube_test_result_mpa'] < lower_limit) | (df_quality['cube_test_result_mpa'] > upper_limit)]
print("\nThe number of outliers in the dataframe:")
print(df_outliers.shape[0])

sns.boxplot(data=df_quality, x='activity_type', y='cube_test_result_mpa')
plt.show()


#### Feature Extraction and Engineering #####

## Extract Numeric Curing Age
df_quality['curing_days'] = df_quality['activity_type'].str.extract(r'(\d+)').astype(int)



## Create the binary flag
df_quality['is_compliant'] = (df_quality['cube_test_result_mpa'] >= 30.0).astype(int)
print("\nThe is_cpmpliant column:")
print(df_quality['is_compliant'].head())

## Calculating the group wise median
group_medians = df_quality.groupby('curing_days')['ndt_ultrasonic_velocity'].transform('median')

# 3. Calculate global median as a secondary fallback strategy
global_median = df_quality['ndt_ultrasonic_velocity'].median()

# 3: Domain Default Constant (e.g., 4.0 km/s)
DOMAIN_DEFAULT_VELOCITY = 4.0

# 4. Perform two-stage imputation (Group Median -> Global Median Fallback)
df_quality['ndt_ultrasonic_velocity'] = (
    df_quality['ndt_ultrasonic_velocity']
    .fillna(group_medians)
    .fillna(global_median)
    .fillna(DOMAIN_DEFAULT_VELOCITY)  
)


print("\nMissing values in ndt_ultrasonic_velocity after imputation:")
print(df_quality['ndt_ultrasonic_velocity'].isnull().sum())

### Vectorized Single Pass
curing_stats = df_quality.groupby('curing_days').agg(
    total_tests=('cube_test_result_mpa', 'count'),
    mean_strength_mpa=('cube_test_result_mpa', 'mean'),
    std_strength_mpa=('cube_test_result_mpa', 'std'),
    min_strength_mpa=('cube_test_result_mpa', 'min'),
    max_strength_mpa=('cube_test_result_mpa', 'max'),
    pass_rate_pct=('is_compliant', lambda x: x.mean() * 100)
).reset_index()

print("\n--- Curing Stats Summary ---")
print(curing_stats)

## Connecting the Field_Quality_Logs with the Projects Metadata

## Re-open the connection
conn= sqlite3.connect(DB_PATH)

## Query and extract the project metadata
df_projects = pd.read_sql('SELECT * FROM Projects;', conn)

## Close connection
conn.close()

print("\nProjects Metadata has been successfully extracted:")
print(df_projects.head())

## Perform the Relational Join with the df_quality and df_projects on project_id
merged_quality_projects = pd.merge(left= df_quality, right= df_projects,on='project_id',how='left')

## Print the top 10 rows
print("\nThe new merged dataframe:")
print(merged_quality_projects[['project_name', 'site_location', 'cube_test_result_mpa', 'is_compliant']].head())
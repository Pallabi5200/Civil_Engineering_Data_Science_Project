## Extract the Field_Quality_Logs

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

sns.histplot(df_quality,kde=True)
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
# 03_hyperparameter_tuning.py
# Machine Learning Hyperparameter Tuning & Cross-Validation
import sqlite3
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

## Extract the Field_Quality_Logs

# 1. Dynamically locate the database path relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "DATABASE_DESIGN", "construction_project.db")

# 2. Establish database connection and extract table
conn = sqlite3.connect(DB_PATH)
df_quality = pd.read_sql_query("SELECT * FROM Field_Quality_Logs;", conn)

# 3. Close the connection
conn.close()

print(" Field_Quality_Logs extracted successfully. Total rows:", len(df_quality))


#### Feature Extraction and Engineering #####

## Extract Numeric Curing Age
df_quality['curing_days'] = df_quality['activity_type'].str.extract(r'(\d+)').astype(int)



## Create the binary flag
df_quality['is_compliant'] = (df_quality['cube_test_result_mpa'] >= 40.0).astype(int)
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

### Define the feature (X) and the target variable (y)
## The feature X
X = df_quality[['ndt_ultrasonic_velocity', 'curing_days']]


## The target variable y
y = df_quality['is_compliant']


## Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)


## Create the param dict
param_grid = {
    'n_estimators': [10, 50, 100],
    'max_depth': [2, 4, 6, None]
}

## Intialize the GridSearchCV
grid_search = GridSearchCV(
    estimator=RandomForestClassifier(random_state=42), 
    param_grid=param_grid, 
    cv=2, 
    scoring='accuracy'
)


## Evalute and print the best parameters
grid_search.fit(X_train, y_train)

best_score = grid_search.best_score_
print("\nThe best score:")
print(best_score)

## Estimate the best param on unseen test data X_test
y_pred = grid_search.best_estimator_.predict(X_test)
print("\nThe best estimator:")
print(y_pred)

## Evalute the accuracy_score and classification_report
acc_3 = accuracy_score(y_test,y_pred)
print(f"\nThe accuracy score : {acc_3}")

report_3 = classification_report(y_test,y_pred)
print(f"\nThe classification report : {report_3}")

print("\nThe best hyperparameters:", grid_search.best_params_)

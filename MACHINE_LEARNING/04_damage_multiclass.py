## 04_damage_multiclass.py
# Multi-Class Machine Learning pipelinr

from sklearn.ensemble import RandomForestClassifier
import sqlite3
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


###############################################################################

#### DATABASE EXTRACTION ####

#########################################################################################

## Extract the Damage_Reports

# 1. Dynamically locate the database path relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "DATABASE_DESIGN", "construction_project.db")

# 2. Establish database connection and extract table
conn = sqlite3.connect(DB_PATH)
df_damage = pd.read_sql_query("SELECT * FROM Damage_Reports;", conn)

# 3. Close the connection
conn.close()

print(" Damage_Reports extracted successfully. Total rows:", len(df_damage))

## Print the first 10 rows of df_damage
print("\nThe damage report dataframe:")
print(df_damage.head())


#################################################

## FEATURE ENGINEERING AND PREPROCESSING #####

####################################################



df_clean = df_damage.drop(columns= ['damage_report_id','project_id','turbine_number','repair_recommendation'])

## Feature X and categorical encoding and target variable y

X = df_clean[['damaged_length_approx','nature_of_damage','turbine_model']]

X = pd.get_dummies(X, columns=["nature_of_damage",'turbine_model'], drop_first=True, dtype=int)

y = df_clean['severity_rating']

####################################################################

#### TRAIN-TEST SPLIT ####

######################################################################


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

########################################################################

######## MULTI-CLASS MODEL TRAINING AND EVALUTION #########

#######################################################################

rf_model = RandomForestClassifier(n_estimators=50, random_state=42)

## Train the model

rf_model.fit(X_train,y_train)

### Predict the test set

y_pred = rf_model.predict(X_test)

### Model Evalution and accuracy

## Evalution matrix
acc_3 = accuracy_score(y_test,y_pred)
print(f"\nThe accuracy score : {acc_3}")

report_3 = classification_report(y_test,y_pred)
print(f"\nThe classification report : {report_3}")

conf_matrix = confusion_matrix(y_test,y_pred)
print("\nThe confusion matrix:")
print(conf_matrix)
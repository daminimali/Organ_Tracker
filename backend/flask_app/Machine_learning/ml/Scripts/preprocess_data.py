#preprocess_data.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib

# Load datasets
donors_df = pd.read_csv('D:/OrganTracker/machine-learning/data/donors.csv')
recipients_df = pd.read_csv('D:/OrganTracker/machine-learning/data/recipients.csv')

# Combine for unified encoding
combined_df = pd.concat([donors_df, recipients_df], ignore_index=True)

# Categorical columns to encode
categorical_columns = ['Blood_Type', 'Organ_Type', 'Geographic_Location', 'Health_Conditions']
label_encoders = {}

# Handle missing values before encoding
for col in categorical_columns:
    combined_df[col] = combined_df[col].fillna('Unknown')

# Apply LabelEncoder on categorical columns
for col in categorical_columns:
    le = LabelEncoder()
    le.fit(combined_df[col])
    label_encoders[col] = le
    donors_df[col] = le.transform(donors_df[col].fillna('Unknown'))
    recipients_df[col] = le.transform(recipients_df[col].fillna('Unknown'))

# Handle missing values in numeric columns
numeric_columns = ['Age', 'BMI']
for col in numeric_columns:
    if col in donors_df.columns:
        donors_df[col] = donors_df[col].fillna(donors_df[col].mean())
    if col in recipients_df.columns:
        recipients_df[col] = recipients_df[col].fillna(recipients_df[col].mean())

# Save preprocessed files
donors_df.to_csv('D:/OrganTracker/machine-learning/data/preprocessed_donors.csv', index=False)
recipients_df.to_csv('D:/OrganTracker/machine-learning/data/preprocessed_recipients.csv', index=False)

# Save LabelEncoders
joblib.dump(label_encoders, 'D:/OrganTracker/machine-learning/models/label_encoders.pkl')

print("Preprocessing completed and saved.")

#/Machine_learning/ml/Scripts/train_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder
import joblib

# Load preprocessed data
donors_df = pd.read_csv(r"C:\Users\Suyash Marathe\Organ Tracker\backend\flask_app\Machine_learning\ml\Data\preprocessed_donors.csv")
recipients_df = pd.read_csv(r"C:\Users\Suyash Marathe\Organ Tracker\backend\flask_app\Machine_learning\ml\Data\preprocessed_recipients.csv")

# Load label_encoders
label_encoders = joblib.load(r"C:\Users\Suyash Marathe\Organ Tracker\backend\flask_app\Machine_learning\ml\models\label_encoders.pkl")

# Merge datasets on Organ_Type with suffixes
merged_df = pd.merge(donors_df, recipients_df, on='Organ_Type', suffixes=('_donor', '_recipient'))

# Blood Type Compatibility Rules
blood_type_rules = {
    'O-': ['O-', 'A-', 'B-', 'AB-'],
    'O+': ['O+', 'A+', 'B+', 'AB+'],
    'A-': ['A-', 'A+', 'AB-', 'AB+'],
    'A+': ['A+', 'AB+'],
    'B-': ['B-', 'B+', 'AB-', 'AB+'],
    'B+': ['B+', 'AB+'],
    'AB-': ['AB-', 'AB+'],
    'AB+': ['AB+']
}

def calculate_compatibility(row):
    try:
        # Blood type check
        blood_type_donor = label_encoders['Blood_Type'].inverse_transform([row['Blood_Type_donor']])[0]
        blood_type_recipient = label_encoders['Blood_Type'].inverse_transform([row['Blood_Type_recipient']])[0]
        if blood_type_recipient not in blood_type_rules[blood_type_donor]:
            return 0
        
        # HLA matching (60% threshold)
        donor_hla = set(row['HLA_Typing'].split(','))
        recipient_hla = set(row['HLA_Typing_Requirement'].split(','))
        match_percentage = len(donor_hla.intersection(recipient_hla)) / len(recipient_hla) * 100
        if match_percentage < 60:
            return 0
        
        # BMI compatibility (±10% range)
        bmi_range = 0.1 * row['BMI_recipient']
        if not (row['BMI_recipient'] - bmi_range <= row['BMI_donor'] <= row['BMI_recipient'] + bmi_range):
            return 0
        
        # Infection status
        if row['Infection_Status_donor'] == 1:
            return 0
        
        # Geographic urgency rule
        if row['Geographic_Location_donor'] != row['Geographic_Location_recipient'] and row['Urgency_Level'] != 'High':
            return 0

        return 1
    except Exception as e:
        print(f"Error processing row: {e}")
        return 0

# Apply compatibility function
merged_df['Compatibility'] = merged_df.apply(calculate_compatibility, axis=1)

# --- Feature Engineering ---
# 1. HLA Binarization
mlb = MultiLabelBinarizer()
hla_donor_encoded = mlb.fit_transform(merged_df['HLA_Typing'].str.split(','))
hla_recipient_encoded = mlb.transform(merged_df['HLA_Typing_Requirement'].str.split(','))

hla_donor_df = pd.DataFrame(hla_donor_encoded, columns=[f'HLA_Donor_{allele}' for allele in mlb.classes_])
hla_recipient_df = pd.DataFrame(hla_recipient_encoded, columns=[f'HLA_Recipient_{allele}' for allele in mlb.classes_])

# 2. Prepare for OneHotEncoding (convert all to strings)
ohe_columns = [
    'Infection_Status_donor', 
    'Infection_Status_recipient',
    'Urgency_Level',
    'Health_Conditions_donor',  # Will be double-encoded
    'Health_Conditions_recipient'  # Will be double-encoded
]

# Convert to string type for OHE
for col in ohe_columns:
    merged_df[col] = merged_df[col].astype(str)

# Initialize and fit OHE
ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
ohe_encoded = ohe.fit_transform(merged_df[ohe_columns])
ohe_df = pd.DataFrame(ohe_encoded, columns=ohe.get_feature_names_out(ohe_columns))

# 3. Other Features (directly use preprocessed values)
other_features = [
    'Age_donor', 'Age_recipient', 
    'BMI_donor', 'BMI_recipient',
    'Blood_Type_donor', 'Blood_Type_recipient',
    'Geographic_Location_donor', 'Geographic_Location_recipient'
]

# Combine all features
X = pd.concat([
    merged_df[other_features],
    hla_donor_df,
    hla_recipient_df,
    ohe_df
], axis=1)

y = merged_df['Compatibility']

# --- Model Training ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

# --- Evaluation ---
y_pred = rf_classifier.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred):.2f}')
print(classification_report(y_test, y_pred))

# --- Save Artifacts ---
artifacts_dir = r"C:\Users\Suyash Marathe\Organ Tracker\backend\flask_app\Machine_learning\ml\Models"
joblib.dump(rf_classifier, f"{artifacts_dir}/random_forest_model.pkl")
joblib.dump(ohe, f"{artifacts_dir}/onehot_encoder.pkl")
joblib.dump(mlb, f"{artifacts_dir}/multilabel_binarizer.pkl")
#joblib.dump(label_encoders, f"{artifacts_dir}/label_encoders.pkl")  # Updated encoders
joblib.dump(list(X.columns), f"{artifacts_dir}/feature_names.pkl")

print("Model and artifacts saved successfully.")
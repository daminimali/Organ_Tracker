# generate_matches.py
import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer

def generate_matches():
    # Load preprocessed data
    donors_df = pd.read_csv(r"C:\Users\Suyash Marathe\Organ Tracker\backend\flask_app\Machine_learning\ml\Data\preprocessed_donors.csv")
    recipients_df = pd.read_csv(r"C:\Users\Suyash Marathe\Organ Tracker\backend\flask_app\Machine_learning\ml\Data\preprocessed_recipients.csv")

    # Load Models
    rf_model = joblib.load(r"C:\Users\Suyash Marathe\Organ Tracker\backend\flask_app\Machine_learning\ml\Models\random_forest_model.pkl")
    onehot_encoder = joblib.load(r"C:\Users\Suyash Marathe\Organ Tracker\backend\flask_app\Machine_learning\ml\Models\onehot_encoder.pkl")
    mlb = joblib.load(r"C:\Users\Suyash Marathe\Organ Tracker\backend\flask_app\Machine_learning\ml\Models\multilabel_binarizer.pkl")
    label_encoders = joblib.load(r"C:\Users\Suyash Marathe\Organ Tracker\backend\flask_app\Machine_learning\ml\Models\label_encoders.pkl")

    # Merge Donors and Recipients on Organ_Type
    merged_df = pd.merge(donors_df, recipients_df, on='Organ_Type', suffixes=('_donor', '_recipient'))

    # Convert categorical columns to string and fill missing
    categorical_columns = ['Infection_Status_donor', 'Infection_Status_recipient', 'Urgency_Level', 'Health_Conditions_donor', 'Health_Conditions_recipient']
    for col in categorical_columns:
        merged_df[col] = merged_df[col].astype(str).fillna('Unknown')

    # Transform Categorical Features using OneHotEncoder
    encoded_features = onehot_encoder.transform(merged_df[categorical_columns])
    encoded_df = pd.DataFrame(encoded_features, columns=onehot_encoder.get_feature_names_out(categorical_columns))

    # Transform HLA Typing using MultiLabelBinarizer
    hla_donor_encoded = mlb.transform(merged_df['HLA_Typing_donor'].apply(lambda x: x.split(',')))
    hla_recipient_encoded = mlb.transform(merged_df['HLA_Typing_recipient'].apply(lambda x: x.split(',')))

    hla_donor_df = pd.DataFrame(hla_donor_encoded, columns=[f'HLA_Donor_{x}' for x in mlb.classes_])
    hla_recipient_df = pd.DataFrame(hla_recipient_encoded, columns=[f'HLA_Recipient_{x}' for x in mlb.classes_])

    # Concatenate all features
    final_df = pd.concat([merged_df, encoded_df, hla_donor_df, hla_recipient_df], axis=1)

    # Feature Selection - Ensure the right columns are selected
    features = ['Age_donor', 'Age_recipient', 'Blood_Type_donor', 'Blood_Type_recipient', 'BMI_donor', 'BMI_recipient', 
                'Geographic_Location_donor', 'Geographic_Location_recipient']
    features += list(hla_donor_df.columns) + list(hla_recipient_df.columns) + list(encoded_df.columns)

    X = final_df[features]

    # Predict Compatibility
    final_df['Compatibility_Score'] = rf_model.predict(X)

    # Return only compatible matches
    matches = final_df[['Donor_ID', 'Recipient_ID', 'Compatibility_Score']]
    return matches[matches['Compatibility_Score'] == 1]

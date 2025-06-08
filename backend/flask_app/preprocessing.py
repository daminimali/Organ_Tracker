#preprocessing.py
import pandas as pd
import numpy as np
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'Machine_Learning', 'ml', 'Models')

# Load label_encoders
label_encoders = joblib.load(os.path.join(MODELS_DIR, 'label_encoders.pkl'))

def preprocess_input_label_only(df, role):
    df = df.copy()

    if role == 'donor':
        expected_cols = [
            'Donor_ID', 'Age', 'Blood_Type', 'Organ_Type', 'HLA_Typing', 'BMI',
            'Organ_Size', 'Infection_Status', 'Geographic_Location', 'Health_Conditions'
        ]
        final_columns = [
            'Donor_ID', 'Age_donor', 'Blood_Type_donor', 'Organ_Type_donor', 'HLA_Typing_donor',
            'BMI_donor', 'Organ_Size_donor', 'Infection_Status_donor', 'Geographic_Location_donor',
            'Health_Conditions_donor'
        ]
    elif role == 'recipient':
        expected_cols = [
            'Recipient_ID', 'Age', 'Blood_Type', 'Organ_Type', 'HLA_Typing_Requirement', 'BMI',
            'Infection_Status', 'Urgency_Level', 'Waiting_Time', 'Geographic_Location', 'Health_Conditions'
        ]
        final_columns = [
            'Recipient_ID', 'Age_recipient', 'Blood_Type_recipient', 'Organ_Type_recipient',
            'HLA_Typing_Requirement_recipient', 'BMI_recipient', 'Infection_Status_recipient',
            'Urgency_Level_recipient', 'Waiting_Time_recipient', 'Geographic_Location_recipient',
            'Health_Conditions_recipient'
        ]
    else:
        raise ValueError(f"Unsupported role: {role}")

    # Copy expected columns into suffixed columns
    for col in expected_cols:
        if col in df.columns and col not in ['Donor_ID', 'Recipient_ID']:
            df[f'{col}_{role}'] = df[col]

    # Apply label encoding where applicable
    label_encoded_cols = ['Blood_Type', 'Organ_Type', 'Geographic_Location', 'Health_Conditions']
    for col in label_encoded_cols:
        col_name = f'{col}_{role}'
        if col_name in df.columns:
            encoder = label_encoders.get(col)
            if encoder:
                df[col_name] = df[col_name].apply(lambda x: x if str(x) in encoder.classes_ else 'unknown')
                if 'unknown' not in encoder.classes_:
                    encoder.classes_ = np.append(encoder.classes_, 'unknown')
                df[col_name] = encoder.transform(df[col_name])

    # Fill any missing columns in the final list
    for col in final_columns:
        if col not in df.columns:
            df[col] = np.nan

    final_features = df[final_columns].copy()

    # After label encoding and before returning
    infection_col = f'Infection_Status_{role}'
    if infection_col in final_features.columns:
        final_features[infection_col] = final_features[infection_col].replace("None", "").fillna("")

    # Debug output
    #print(f"[DEBUG] {infection_col} after replacing None with empty string:")
    #print(final_features[infection_col].values)

    return final_features
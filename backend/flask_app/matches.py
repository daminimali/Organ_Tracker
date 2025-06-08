#matches.py
import pandas as pd
import joblib
import numpy as np
import os
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'Machine_Learning', 'ml', 'Models')

# Load models and encoders
rf_model = joblib.load(os.path.join(MODELS_DIR, 'random_forest_model.pkl'))
onehot_encoder = joblib.load(os.path.join(MODELS_DIR, 'onehot_encoder.pkl'))
mlb = joblib.load(os.path.join(MODELS_DIR, 'multilabel_binarizer.pkl'))

# Load feature names to ensure correct column order
feature_names = joblib.load(os.path.join(MODELS_DIR, 'feature_names.pkl'))


def generate_runtime_matches(preprocessed_donors_df, preprocessed_recipients_df, raw_donors_df, raw_recipients_df):
    donors_raw = raw_donors_df.copy()
    recipients_raw = raw_recipients_df.copy()

    # Ensure Organ_Type column is present
    if 'Organ_Type' not in donors_raw.columns or 'Organ_Type' not in recipients_raw.columns:
        raise ValueError("Organ_Type must exist in both donor and recipient raw data.")

    # Ensure ID columns exist
    if 'Donor_ID' not in donors_raw.columns:
        donors_raw['Donor_ID'] = ['Unknown'] * len(donors_raw)
    if 'Recipient_ID' not in recipients_raw.columns:
        recipients_raw['Recipient_ID'] = ['Unknown'] * len(recipients_raw)

    # Merge donors and recipients on Organ_Type
    merged_raw = donors_raw.merge(recipients_raw, on='Organ_Type', suffixes=('_donor', '_recipient'))

    if merged_raw.empty:
        print("[DEBUG] Merged raw DataFrame is empty after joining on Organ_Type.")
        return pd.DataFrame(columns=['Donor_ID', 'Recipient_ID', 'Compatibility_Score'])

    # Fill required raw columns
    required_cols = [
        'Infection_Status_donor', 'Infection_Status_recipient',
        'Urgency_Level', 'Health_Conditions_donor', 'Health_Conditions_recipient',
        'HLA_Typing', 'HLA_Typing_Requirement'
    ]
    for col in required_cols:
        if col not in merged_raw.columns:
            merged_raw[col] = 'Unknown'

    # Convert categorical features to string
    categorical_features = [
        'Infection_Status_donor',
        'Infection_Status_recipient',
        'Urgency_Level',
        'Health_Conditions_donor',
        'Health_Conditions_recipient'
    ]

    for col in categorical_features:
        merged_raw[col] = merged_raw[col].fillna('nan').astype(str).replace('None', 'nan').str.strip().str.lower()

        # Apply casing fixes to match training encoders
        if col.startswith('Infection_Status'):
            merged_raw[col] = merged_raw[col].replace({
            'hiv-negative': 'HIV-negative',
            'hepatitis-negative': 'Hepatitis-negative',
            'nan': 'nan'
        })
        elif col == 'Urgency_Level':
            merged_raw[col] = merged_raw[col].replace({
            'high': 'High',
            'medium': 'Medium',
            'low': 'Low',
            'nan': 'nan'
        })
        elif col.startswith('Health_Conditions'):
            merged_raw[col] = merged_raw[col].str.strip()


    #print("==== FINAL NORMALIZED CATEGORIES ====")
    #for col in categorical_features:
         #print(f"{col}: {merged_raw[col].unique()}")
    #print("=====================================")

    # OneHot encode
    onehot_encoded = onehot_encoder.transform(merged_raw[categorical_features])
    onehot_df = pd.DataFrame(onehot_encoded, columns=onehot_encoder.get_feature_names_out(categorical_features))

    # HLA encoding
    hla_donor_encoded = mlb.transform(
        merged_raw['HLA_Typing'].fillna('').apply(lambda x: [i.strip() for i in str(x).split(',') if i.strip()])
    )
    hla_recipient_encoded = mlb.transform(
        merged_raw['HLA_Typing_Requirement'].fillna('').apply(lambda x: [i.strip() for i in str(x).split(',') if i.strip()])
    )
    hla_donor_df = pd.DataFrame(hla_donor_encoded, columns=[f'HLA_Donor_{x}' for x in mlb.classes_])
    hla_recipient_df = pd.DataFrame(hla_recipient_encoded, columns=[f'HLA_Recipient_{x}' for x in mlb.classes_])

    # Cross join donor-recipient features
    donors_encoded = preprocessed_donors_df.copy()
    recipients_encoded = preprocessed_recipients_df.copy()
    donors_encoded['key'] = 1
    recipients_encoded['key'] = 1
    cross_join_df = pd.merge(donors_encoded, recipients_encoded, on='key').drop('key', axis=1)

    # Row alignment check
    expected_rows = cross_join_df.shape[0]
    if not all(df.shape[0] == expected_rows for df in [onehot_df, hla_donor_df, hla_recipient_df]):
        print("[ERROR] Feature DataFrames do not align in row count.")
        print(f"cross_join_df: {cross_join_df.shape}, onehot_df: {onehot_df.shape}, hla_donor_df: {hla_donor_df.shape}, hla_recipient_df: {hla_recipient_df.shape}")
        return pd.DataFrame(columns=['Donor_ID', 'Recipient_ID', 'Compatibility_Score'])

    # Combine features
    final_df = pd.concat([
        cross_join_df.reset_index(drop=True),
        onehot_df.reset_index(drop=True),
        hla_donor_df.reset_index(drop=True),
        hla_recipient_df.reset_index(drop=True)
    ], axis=1)

    # Feature alignment check
    missing_features = [feat for feat in feature_names if feat not in final_df.columns]
    if missing_features:
        print(f"[ERROR] Missing expected features for prediction: {missing_features}")
        return pd.DataFrame(columns=['Donor_ID', 'Recipient_ID', 'Compatibility_Score'])

    final_df = final_df[feature_names]

    # Predict
    if final_df.empty:
        print("[DEBUG] Final feature DataFrame is empty after preprocessing.")
        return pd.DataFrame(columns=['Donor_ID', 'Recipient_ID', 'Compatibility_Score'])
    
     #🔍 Debug: Show all feature names and their corresponding values (top 5 rows)
    #print("[DEBUG] === Final Feature Matrix Sent to Random Forest ===")
    #for idx, row in final_df.head(5).iterrows():
    #        print(f"[Row {idx}]")
    #for col, val in row.items():
    #        print(f"  {col}: {val}")
    #        print("--------------------------------------------------")

    # Predict
    preds = rf_model.predict(final_df)

    # 🔍 Debug prints to inspect model output
    print("[DEBUG] Model raw predictions:", preds)
    print("[DEBUG] Compatibility_Score value counts:\n", pd.Series(preds).value_counts())


    # Assign predictions to DataFrame
    final_df['Compatibility_Score'] = preds

    matches_df = pd.DataFrame({
        'Donor_ID': merged_raw['Donor_ID'],
        'Recipient_ID': merged_raw['Recipient_ID'],
        'Compatibility_Score': final_df['Compatibility_Score']
    })

    compatible = matches_df[matches_df['Compatibility_Score'] == 1].reset_index(drop=True)
    if compatible.empty:
        print("[DEBUG] No compatible matches found for given input.")

    return compatible
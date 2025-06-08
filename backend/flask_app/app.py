#app.py
from flask import Flask, request, jsonify ,current_app
from flask_cors import CORS
#from flask_sqlalchemy import SQLAlchemy
from models import Donor, Recipient, db
import subprocess
import tempfile
import joblib
import os
import json
import mysql.connector
import traceback
import pandas as pd
#import sys

from dotenv import load_dotenv
from preprocessing import preprocess_input_label_only
from matches import generate_runtime_matches

load_dotenv()

column_mapping = {
    'Age_D': 'Age_donor',
    'Age_R': 'Age_recipient',
    'BMI_D': 'BMI_donor',
    'BMI_R': 'BMI_recipient',
    'Blood_Type_D': 'Blood_Type_donor',
    'Blood_Type_R': 'Blood_Type_recipient',
    'Organ_Type_D': 'Organ_Type_donor',
    'Organ_Type_R': 'Organ_Type_recipient',
    'Geographic_Location_D': 'Geographic_Location_donor',
    'Geographic_Location_R': 'Geographic_Location_recipient',
    'Health_Conditions_D': 'Health_Conditions_donor',
    'Health_Conditions_R': 'Health_Conditions_recipient',
    'Infection_Status_D': 'Infection_Status_donor',
    'Infection_Status_R': 'Infection_Status_recipient',
    'Organ_Size_D': 'Organ_Size_donor',
    'Urgency_Level_R': 'Urgency_Level_recipient',
    'Waiting_Time_R': 'Waiting_Time_recipient',
    'HLA_Typing_D': 'HLA_Typing_donor',
    'HLA_Typing_R': 'HLA_Typing_Requirement_recipient'
}

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Load ML model and helpers
model = joblib.load(os.path.join("Machine_learning", "ml", "Models", "random_forest_model.pkl"))
mlb = joblib.load(os.path.join("Machine_learning", "ml", "Models", "multilabel_binarizer.pkl"))
feature_names = joblib.load(os.path.join("Machine_learning", "ml", "Models", "feature_names.pkl"))

features = joblib.load('Machine_learning/ml/Models/feature_names.pkl')

def add_json_to_ipfs(data):
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json') as f:
        json.dump(data, f)
        temp_path = f.name
    try:
        result = subprocess.run(["ipfs", "add", "-Q", temp_path], capture_output=True, text=True, check=True)
        cid = result.stdout.strip()
    finally:
        os.remove(temp_path)
    return cid

def get_json_from_ipfs(cid):
    result = subprocess.run(["ipfs", "cat", cid], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

@app.route('/match', methods=['POST'])
def match_specific_user():
    data = request.get_json()
    auth0_id = data.get('auth0Id')
    role = data.get('role')

    if not auth0_id or not role:
        return jsonify({"error": "auth0Id and role are required"}), 400

    try:
        # Load model
        models_dir = os.path.join(current_app.root_path, 'Machine_Learning', 'ml', 'Models')
        model = joblib.load(os.path.join(models_dir, 'random_forest_model.pkl'))

        matches = []

        if role == 'donor':
            donor = Donor.query.filter_by(Auth0_ID=auth0_id).first()
            if not donor:
                return jsonify({"error": "Donor not found"}), 404

            recipients = Recipient.query.all()

            for recipient in recipients:
                donor_raw = pd.DataFrame([{
                    'Donor_ID': donor.Donor_ID,
                    'Age': donor.Age,
                    'Blood_Type': donor.Blood_Type,
                    'Organ_Type': donor.Organ_Type,
                    'HLA_Typing': donor.HLA_Typing,
                    'BMI': donor.BMI,
                    'Organ_Size': donor.Organ_Size,
                    'Infection_Status': donor.Infection_Status,
                    'Geographic_Location': donor.Geographic_Location,
                    'Health_Conditions': donor.Health_Conditions
                }])

                recipient_raw = pd.DataFrame([{
                    'Recipient_ID': recipient.Recipient_ID,
                    'Age': recipient.Age,
                    'Blood_Type': recipient.Blood_Type,
                    'Organ_Type': recipient.Organ_Type,
                    'HLA_Typing_Requirement': recipient.HLA_Typing_Requirement,
                    'BMI': recipient.BMI,
                    'Infection_Status': recipient.Infection_Status,
                    'Urgency_Level': recipient.Urgency_Level,
                    'Waiting_Time': recipient.Waiting_Time,
                    'Geographic_Location': recipient.Geographic_Location,
                    'Health_Conditions': recipient.Health_Conditions   
                }])

                donor_processed = preprocess_input_label_only(donor_raw, 'donor')
                recipient_processed = preprocess_input_label_only(recipient_raw, 'recipient')

                result = generate_runtime_matches(donor_processed, recipient_processed, donor_raw, recipient_raw)

                if not result.empty and result['Compatibility_Score'].values[0] == 1:
                    print("[DEBUG] Match found:", result.iloc[0].to_dict())
                    return jsonify({
                        "message": "Match Found!",
                        "match": result.iloc[0].to_dict()
                    }), 200

            print("[DEBUG] No matches returned from generate_runtime_matches.")
            return jsonify({"message": "We know the importance of time, but no matches were found. Please try again later."}), 200

        elif role == 'receiver':
            recipient = Recipient.query.filter_by(Auth0_ID=auth0_id).first()
            if not recipient:
                return jsonify({"error": "Receiver not found"}), 404

            donors = Donor.query.all()

            for donor in donors:
                donor_raw = pd.DataFrame([{
                    'Donor_ID': donor.Donor_ID,
                    'Age': donor.Age,
                    'Blood_Type': donor.Blood_Type,
                    'Organ_Type': donor.Organ_Type,
                    'HLA_Typing': donor.HLA_Typing,
                    'BMI': donor.BMI,
                    'Organ_Size': donor.Organ_Size,
                    'Infection_Status': donor.Infection_Status,
                    'Geographic_Location': donor.Geographic_Location,
                    'Health_Conditions': donor.Health_Conditions
                }])

                recipient_raw = pd.DataFrame([{
                    'Recipient_ID': recipient.Recipient_ID,
                    'Age': recipient.Age,
                    'Blood_Type': recipient.Blood_Type,
                    'Organ_Type': recipient.Organ_Type,
                    'HLA_Typing_Requirement': recipient.HLA_Typing_Requirement,
                    'BMI': recipient.BMI,
                    'Infection_Status': recipient.Infection_Status,
                    'Urgency_Level': recipient.Urgency_Level,
                    'Waiting_Time': recipient.Waiting_Time,
                    'Geographic_Location': recipient.Geographic_Location,
                    'Health_Conditions': recipient.Health_Conditions   
                }])

                donor_processed = preprocess_input_label_only(donor_raw, 'donor')
                recipient_processed = preprocess_input_label_only(recipient_raw, 'recipient')

                result = generate_runtime_matches(donor_processed, recipient_processed, donor_raw, recipient_raw)

                if not result.empty and result['Compatibility_Score'].values[0] == 1:
                    print("[DEBUG] Match found:", result.iloc[0].to_dict())
                    return jsonify({
                        "message": "Match Found!",
                        "match": result.iloc[0].to_dict()
                    }), 200

            print("[DEBUG] No matches returned from generate_runtime_matches.")
            return jsonify({"message": "We know the importance of time, but no matches were found. Please try again later."}), 200

        
        if matches:
            ipfs_data = [{"Donor_ID": m["Donor_ID"], "Recipient_ID": m["Recipient_ID"], "Compatibility_Score": 1} for m in matches]
            cid = add_json_to_ipfs(ipfs_data)
        else:
            cid = None

        return jsonify({
            "status": "success",
            "matches_found": len(matches),
            "matches": matches,
            "cid": cid
        })

    except Exception as e:
        current_app.logger.error(f"Error in /match: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "Internal server error"
        }), 500
    
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

@app.route("/get_user_details/<auth0_id>", methods=["GET"])
def get_user_details(auth0_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT donor_id FROM donors WHERE auth0_id = %s", (auth0_id,))
        donor_result = cursor.fetchone()
        if donor_result:
            return jsonify({"role": "donor", "user_id": donor_result[0]})

        cursor.execute("SELECT receiver_id FROM receivers WHERE auth0_id = %s", (auth0_id,))
        receiver_result = cursor.fetchone()
        if receiver_result:
            return jsonify({"role": "receiver", "user_id": receiver_result[0]})

        return jsonify({"error": "User not found"}), 404
    except mysql.connector.Error as err:
        print("MySQL error:", err)
        return jsonify({"error": "Database error"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def prepare_combined_data(donor, recipient):
    return {
        "Age_D": donor.Age,
        "Blood_Type_D": donor.Blood_Type,
        "Organ_Type_D": donor.Organ_Type,
        "HLA_Typing_D": donor.HLA_Typing,
        "BMI_D": donor.BMI,
        "Organ_Size_D": donor.Organ_Size,
        "Infection_Status_D": donor.Infection_Status,
        "Geographic_Location_D": donor.Geographic_Location,
        "Health_Conditions_D": donor.Health_Conditions,
        "Age_R": recipient.Age,
        "Blood_Type_R": recipient.Blood_Type,
        "Organ_Type_R": recipient.Organ_Type,
        "HLA_Typing_R": recipient.HLA_Typing_Requirement,
        "BMI_R": recipient.BMI,
        "Infection_Status_R": recipient.Infection_Status,
        "Urgency_Level_R": recipient.Urgency_Level,
        "Waiting_Time_R": recipient.Waiting_Time,
        "Geographic_Location_R": recipient.Geographic_Location,
        "Health_Conditions_R": recipient.Health_Conditions
    }

@app.route('/ipfs/<cid>', methods=['GET'])
def get_from_ipfs(cid):
    try:
        data = get_json_from_ipfs(cid)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch from IPFS: {str(e)}"}), 500

@app.route('/get_user/<role>/<id>', methods=['GET'])
def get_user_data(role, id):
    try:
        if role == 'donor':
            user = Donor.query.filter_by(Donor_ID=id).first()
            if user:
                return jsonify({
                    "id": user.Donor_ID,
                    "organ_type": user.Organ_Type,
                    "blood_group": user.Blood_Type,
                    "location": user.Geographic_Location,
                    "hla_typing": user.HLA_Typing,
                    "bmi": user.BMI,
                    "organ_size": user.Organ_Size,
                    "infection_status": user.Infection_Status,
                    "health_condition": user.Health_Conditions,
                    "urgency": None,
                    "waiting_time": None,
                    "age": user.Age,
                    "phone_number": user.phone_number
                })
        elif role == 'receiver':
            user = Recipient.query.filter_by(Recipient_ID=id).first()
            if user:
                return jsonify({
                    "id": user.Recipient_ID,
                    "organ_type": user.Organ_Type,
                    "blood_group": user.Blood_Type,
                    "location": user.Geographic_Location,
                    "hla_typing": user.HLA_Typing_Requirement,
                    "bmi": user.BMI,
                    "organ_size": None,
                    "infection_status": user.Infection_Status,
                    "health_condition": user.Health_Conditions,
                    "urgency": user.Urgency_Level,
                    "waiting_time": user.Waiting_Time,
                    "age": user.Age,
                    "phone_number": user.phone_number
                })
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
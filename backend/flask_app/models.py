#models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Donor(db.Model):
    __tablename__ = 'donors'

    Donor_ID = db.Column(db.Integer, primary_key=True)
    Auth0_ID = db.Column('Auth0_ID', db.String(100), unique=True, nullable=False)  
    Age = db.Column(db.Integer)
    Blood_Type = db.Column(db.String(5))
    Organ_Type = db.Column(db.String(50))
    HLA_Typing = db.Column(db.String(200))
    BMI = db.Column(db.Float)
    Organ_Size = db.Column(db.Float)
    Infection_Status = db.Column(db.String(20))
    Geographic_Location = db.Column(db.String(100))
    Health_Conditions = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    
class Recipient(db.Model):
    __tablename__ = 'receivers'

    Recipient_ID = db.Column(db.Integer, primary_key=True)
    Auth0_ID = db.Column('Auth0_ID', db.String(100), unique=True, nullable=False)  
    Age = db.Column(db.Integer)
    Blood_Type = db.Column(db.String(5))
    Organ_Type = db.Column(db.String(50))
    HLA_Typing_Requirement = db.Column(db.String(200))
    BMI = db.Column(db.Float)
    Infection_Status = db.Column(db.String(20))
    Urgency_Level = db.Column(db.String(50))
    Waiting_Time = db.Column(db.Integer)
    Geographic_Location = db.Column(db.String(100))
    Health_Conditions = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PatientIntake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    arrival_mode = db.Column(db.String(50), nullable=False)  # private car, ambulance, etc.
    car_location = db.Column(db.String(200))  # GPS coords or text
    eta_minutes = db.Column(db.Integer)  # estimated minutes until arrival
    
    # Pregnancy-specific fields
    is_pregnant = db.Column(db.Boolean, default=True)  # All patients are pregnant women
    pregnancy_week = db.Column(db.Integer)  # Current pregnancy week (1-40)
    trimester = db.Column(db.String(20))  # First, Second, Third
    due_date = db.Column(db.Date)  # Expected due date
    pregnancy_complications = db.Column(db.Text)  # Any pregnancy complications
    previous_pregnancies = db.Column(db.Integer, default=0)  # Number of previous pregnancies
    blood_type = db.Column(db.String(10))  # Blood type for pregnancy care
    last_menstrual_period = db.Column(db.Date)  # LMP date
    
    # AI Classification fields
    severity_level = db.Column(db.String(20))  # Critical, Urgent, Light
    ticket_number = db.Column(db.String(10), unique=True)  # R123, Y456, G789
    color_code = db.Column(db.String(1))  # R, Y, G
    ai_analysis = db.Column(db.Text)  # JSON string of AI analysis
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

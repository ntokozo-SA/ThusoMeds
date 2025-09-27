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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

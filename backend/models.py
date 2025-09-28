from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class PatientIntake(db.Model):
    __tablename__ = 'patient_intake'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    arrival_mode = db.Column(db.String(50), nullable=False)
    car_location = db.Column(db.String(200))
    eta_minutes = db.Column(db.Integer)
    
    # Pregnancy-specific fields
    is_pregnant = db.Column(db.Boolean, default=False)
    pregnancy_week = db.Column(db.Integer)
    trimester = db.Column(db.String(20))
    due_date = db.Column(db.Date)
    pregnancy_complications = db.Column(db.Text)
    previous_pregnancies = db.Column(db.Integer, default=0)
    blood_type = db.Column(db.String(10))
    last_menstrual_period = db.Column(db.Date)
    next_of_kin = db.Column(db.Text)  # JSON string to store next of kin data
    
    # AI Classification fields
    severity_level = db.Column(db.String(20), default="Light")
    ticket_number = db.Column(db.String(20))
    color_code = db.Column(db.String(5), default="G")
    ai_analysis = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'contact': self.contact,
            'symptoms': self.symptoms,
            'arrival_mode': self.arrival_mode,
            'car_location': self.car_location,
            'eta_minutes': self.eta_minutes,
            'is_pregnant': self.is_pregnant,
            'pregnancy_week': self.pregnancy_week,
            'trimester': self.trimester,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'pregnancy_complications': self.pregnancy_complications,
            'previous_pregnancies': self.previous_pregnancies,
            'blood_type': self.blood_type,
            'last_menstrual_period': self.last_menstrual_period.isoformat() if self.last_menstrual_period else None,
            'next_of_kin': self.next_of_kin,
            'severity_level': self.severity_level,
            'ticket_number': self.ticket_number,
            'color_code': self.color_code,
            'ai_analysis': self.ai_analysis,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class MoodEntry(db.Model):
    __tablename__ = 'mood_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_intake.id'), nullable=True)  # Optional patient reference
    date = db.Column(db.Date, default=date.today)  # Changed from date_recorded to date
    mood = db.Column(db.String(50), nullable=False)  # e.g., "excellent", "good", "okay", "anxious", "sad", "overwhelmed"
    notes = db.Column(db.Text)
    symptoms = db.Column(db.Text)  # JSON string of symptoms
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    patient = db.relationship('PatientIntake', backref=db.backref('mood_entries', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'date': self.date.isoformat() if self.date else None,
            'mood': self.mood,
            'notes': self.notes,
            'symptoms': self.symptoms,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import json

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


class MoodEntry(db.Model):
    """Model for storing daily mood tracking data for pregnant women"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Patient reference (optional - can track mood without patient record)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_intake.id'), nullable=True)
    
    # Mood tracking data
    date = db.Column(db.Date, nullable=False, default=date.today)
    mood = db.Column(db.String(20), nullable=False)  # excellent, good, okay, anxious, sad, overwhelmed
    notes = db.Column(db.Text, nullable=True)  # Optional notes from the user
    symptoms = db.Column(db.Text, nullable=True)  # JSON string of selected symptoms
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to patient (optional)
    patient = db.relationship('PatientIntake', backref=db.backref('mood_entries', lazy=True))
    
    def __repr__(self):
        return f'<MoodEntry {self.date}: {self.mood}>'
    
    def to_dict(self):
        """Convert mood entry to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'date': self.date.isoformat() if self.date else None,
            'mood': self.mood,
            'notes': self.notes,
            'symptoms': json.loads(self.symptoms) if self.symptoms else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create mood entry from dictionary"""
        mood_entry = cls()
        mood_entry.patient_id = data.get('patient_id')
        mood_entry.date = datetime.strptime(data['date'], '%Y-%m-%d').date() if data.get('date') else date.today()
        mood_entry.mood = data['mood']
        mood_entry.notes = data.get('notes', '')
        mood_entry.symptoms = json.dumps(data.get('symptoms', []))
        return mood_entry

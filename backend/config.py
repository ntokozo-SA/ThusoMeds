import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "hospital.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Hospital coordinates (example - replace with actual hospital location)
    HOSPITAL_LAT = -26.2041  # Johannesburg coordinates as example
    HOSPITAL_LNG = 28.0473
    
    # ETA estimation settings
    AVERAGE_DRIVING_SPEED_KMH = 50  # Average driving speed in km/h for ETA estimation
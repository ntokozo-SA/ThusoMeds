from flask import Flask, request, jsonify
from config import Config
from models import db
from routes.intake import intake_bp
from routes.dashboard import dashboard_bp
from flask_cors import CORS
import re

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=['http://127.0.0.1:5500', 'http://localhost:5500', 'http://127.0.0.1:3000', 'http://localhost:3000', 'http://127.0.0.1:8080', 'http://localhost:8080', 'file://'])

# Security headers
@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# Input validation helper
def validate_input(data, field, min_length=1, max_length=255, pattern=None):
    if field not in data:
        return False, f"{field} is required"
    
    value = str(data[field]).strip()
    
    if len(value) < min_length:
        return False, f"{field} must be at least {min_length} characters"
    
    if len(value) > max_length:
        return False, f"{field} must be less than {max_length} characters"
    
    if pattern and not re.match(pattern, value):
        return False, f"{field} format is invalid"
    
    return True, value

db.init_app(app)
app.register_blueprint(intake_bp)
app.register_blueprint(dashboard_bp)

@app.route("/")
def home():
    return "MamaCare Pregnancy Care Backend is running!"

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

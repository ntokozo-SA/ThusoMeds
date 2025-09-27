from flask import Flask
from config import Config
from models import db
from routes.intake import intake_bp
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)
app.register_blueprint(intake_bp)

@app.route("/")
def home():
    return "Hospital Intake Backend is running!"

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

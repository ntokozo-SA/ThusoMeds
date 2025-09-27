from flask import Blueprint, request, jsonify
from models import db, PatientIntake

intake_bp = Blueprint("intake", __name__)

# Create new intake
@intake_bp.route("/intake", methods=["POST"])
def create_intake():
    data = request.get_json()
    required_fields = ["name", "age", "contact", "symptoms", "arrival_mode"]

    # Check for missing fields
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    new_patient = PatientIntake(
        name=data["name"],
        age=data["age"],
        contact=data["contact"],
        symptoms=data["symptoms"],
        arrival_mode=data["arrival_mode"],
        car_location=data.get("car_location"),
        eta_minutes=data.get("eta_minutes")
    )

    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"message": "Patient intake created", "id": new_patient.id}), 201

# Get all intakes
@intake_bp.route("/intake", methods=["GET"])
def get_intakes():
    patients = PatientIntake.query.all()
    result = []
    for p in patients:
        result.append({
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "contact": p.contact,
            "symptoms": p.symptoms,
            "arrival_mode": p.arrival_mode,
            "car_location": p.car_location,
            "eta_minutes": p.eta_minutes,
            "created_at": p.created_at
        })
    return jsonify(result)

# Get one intake by ID
@intake_bp.route("/intake/<int:id>", methods=["GET"])
def get_intake(id):
    p = PatientIntake.query.get_or_404(id)
    return jsonify({
        "id": p.id,
        "name": p.name,
        "age": p.age,
        "contact": p.contact,
        "symptoms": p.symptoms,
        "arrival_mode": p.arrival_mode,
        "car_location": p.car_location,
        "eta_minutes": p.eta_minutes,
        "created_at": p.created_at
    })

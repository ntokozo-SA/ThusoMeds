from flask import Blueprint, request, jsonify
from models import db, PatientIntake
from services.eta_service import ETAService

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

    # Calculate ETA if car_location is provided
    eta_minutes = None
    car_location = data.get("car_location")
    
    if car_location:
        try:
            eta_service = ETAService()
            eta_minutes = eta_service.get_eta_from_location(car_location)
        except ValueError as e:
            return jsonify({"error": f"Invalid car location: {str(e)}"}), 400
        except Exception as e:
            return jsonify({"error": f"Failed to calculate ETA: {str(e)}"}), 500

    # Convert car_location to string for storage if it's a dict
    car_location_str = None
    if car_location:
        if isinstance(car_location, dict):
            # Store as JSON string for flexibility
            import json
            car_location_str = json.dumps(car_location)
        else:
            car_location_str = str(car_location)

    new_patient = PatientIntake(
        name=data["name"],
        age=data["age"],
        contact=data["contact"],
        symptoms=data["symptoms"],
        arrival_mode=data["arrival_mode"],
        car_location=car_location_str,
        eta_minutes=eta_minutes
    )

    db.session.add(new_patient)
    db.session.commit()
    
    response_data = {
        "message": "Patient intake created",
        "id": new_patient.id
    }
    
    if eta_minutes is not None:
        response_data["eta_minutes"] = eta_minutes
    
    return jsonify(response_data), 201

# Get all intakes
@intake_bp.route("/intake", methods=["GET"])
def get_intakes():
    patients = PatientIntake.query.all()
    result = []
    for p in patients:
        # Parse car_location JSON if it exists
        car_location = p.car_location
        if car_location:
            try:
                import json
                car_location = json.loads(car_location)
            except (json.JSONDecodeError, TypeError):
                # Keep as string if not valid JSON
                pass
        
        result.append({
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "contact": p.contact,
            "symptoms": p.symptoms,
            "arrival_mode": p.arrival_mode,
            "car_location": car_location,
            "eta_minutes": p.eta_minutes,
            "created_at": p.created_at
        })
    return jsonify(result)

# Get one intake by ID
@intake_bp.route("/intake/<int:id>", methods=["GET"])
def get_intake(id):
    p = PatientIntake.query.get_or_404(id)
    
    # Parse car_location JSON if it exists
    car_location = p.car_location
    if car_location:
        try:
            import json
            car_location = json.loads(car_location)
        except (json.JSONDecodeError, TypeError):
            # Keep as string if not valid JSON
            pass
    
    return jsonify({
        "id": p.id,
        "name": p.name,
        "age": p.age,
        "contact": p.contact,
        "symptoms": p.symptoms,
        "arrival_mode": p.arrival_mode,
        "car_location": car_location,
        "eta_minutes": p.eta_minutes,
        "created_at": p.created_at
    })

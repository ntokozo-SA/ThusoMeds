from flask import Blueprint, request, jsonify
from models import db, PatientIntake
from services.eta_service import ETAService
from services.emergency_classifier import EmergencyClassifier
import json

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

    # AI Emergency Classification
    try:
        classifier = EmergencyClassifier()
        
        # Extract risk conditions from the data
        risk_conditions = []
        if data.get("chronic") == "Yes":
            risk_conditions.append("Chronic medication")
        if data.get("conditions") == "Yes":
            risk_conditions.append("Medical conditions")
        if data.get("contactSick") == "Yes":
            risk_conditions.append("Contact with sick person")
        
        # Classify emergency level
        severity_level, ticket_number, color_code = classifier.classify_emergency(
            symptoms=data["symptoms"],
            age=data["age"],
            risk_conditions=risk_conditions
        )
        
        # Get detailed analysis
        ai_analysis = classifier.analyze_symptoms(data["symptoms"])
        severity_explanation = classifier.get_severity_explanation(severity_level, data["symptoms"])
        
    except Exception as e:
        return jsonify({"error": f"AI classification failed: {str(e)}"}), 500

    # Convert car_location to string for storage if it's a dict
    car_location_str = None
    if car_location:
        if isinstance(car_location, dict):
            # Store as JSON string for flexibility
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
        eta_minutes=eta_minutes,
        severity_level=severity_level,
        ticket_number=ticket_number,
        color_code=color_code,
        ai_analysis=json.dumps(ai_analysis)
    )

    db.session.add(new_patient)
    db.session.commit()
    
    response_data = {
        "message": "Patient intake created",
        "id": new_patient.id,
        "ticket_number": ticket_number,
        "severity_level": severity_level,
        "color_code": color_code,
        "severity_explanation": severity_explanation,
        "ai_analysis": ai_analysis
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
        
        # Parse AI analysis JSON if it exists
        ai_analysis = None
        if p.ai_analysis:
            try:
                ai_analysis = json.loads(p.ai_analysis)
            except (json.JSONDecodeError, TypeError):
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
            "severity_level": p.severity_level,
            "ticket_number": p.ticket_number,
            "color_code": p.color_code,
            "ai_analysis": ai_analysis,
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
    
    # Parse AI analysis JSON if it exists
    ai_analysis = None
    if p.ai_analysis:
        try:
            ai_analysis = json.loads(p.ai_analysis)
        except (json.JSONDecodeError, TypeError):
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
        "severity_level": p.severity_level,
        "ticket_number": p.ticket_number,
        "color_code": p.color_code,
        "ai_analysis": ai_analysis,
        "created_at": p.created_at
    })

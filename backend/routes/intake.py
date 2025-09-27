from flask import Blueprint, request, jsonify
from models import db, PatientIntake, MoodEntry
from services.eta_service import ETAService
from services.emergency_classifier import EmergencyClassifier
from datetime import datetime, date, timedelta
import json
import re

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
        if data.get("multiple_pregnancy") == "Yes":
            risk_conditions.append("Multiple pregnancy")
        if data.get("previous_complications") == "Yes":
            risk_conditions.append("Previous pregnancy complications")
        
        # Get pregnancy-specific data
        pregnancy_week = data.get("pregnancy_week")
        trimester = data.get("trimester")
        
        # Classify emergency level with pregnancy data
        severity_level, ticket_number, color_code = classifier.classify_emergency(
            symptoms=data["symptoms"],
            age=data["age"],
            risk_conditions=risk_conditions,
            pregnancy_week=pregnancy_week,
            trimester=trimester
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

    # Parse pregnancy dates
    due_date = None
    last_menstrual_period = None
    
    if data.get("due_date"):
        try:
            due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
        except (ValueError, TypeError):
            pass
    
    if data.get("last_menstrual_period"):
        try:
            last_menstrual_period = datetime.strptime(data["last_menstrual_period"], "%Y-%m-%d").date()
        except (ValueError, TypeError):
            pass

    new_patient = PatientIntake(
        name=data["name"],
        age=data["age"],
        contact=data["contact"],
        symptoms=data["symptoms"],
        arrival_mode=data["arrival_mode"],
        car_location=car_location_str,
        eta_minutes=eta_minutes,
        # Pregnancy-specific fields
        is_pregnant=True,  # All patients are pregnant women
        pregnancy_week=data.get("pregnancy_week"),
        trimester=data.get("trimester"),
        due_date=due_date,
        pregnancy_complications=data.get("pregnancy_complications"),
        previous_pregnancies=data.get("previous_pregnancies", 0),
        blood_type=data.get("blood_type"),
        last_menstrual_period=last_menstrual_period,
        # AI Classification fields
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
            # Pregnancy-specific fields
            "is_pregnant": p.is_pregnant,
            "pregnancy_week": p.pregnancy_week,
            "trimester": p.trimester,
            "due_date": p.due_date.isoformat() if p.due_date else None,
            "pregnancy_complications": p.pregnancy_complications,
            "previous_pregnancies": p.previous_pregnancies,
            "blood_type": p.blood_type,
            "last_menstrual_period": p.last_menstrual_period.isoformat() if p.last_menstrual_period else None,
            # AI Classification fields
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
        # Pregnancy-specific fields
        "is_pregnant": p.is_pregnant,
        "pregnancy_week": p.pregnancy_week,
        "trimester": p.trimester,
        "due_date": p.due_date.isoformat() if p.due_date else None,
        "pregnancy_complications": p.pregnancy_complications,
        "previous_pregnancies": p.previous_pregnancies,
        "blood_type": p.blood_type,
        "last_menstrual_period": p.last_menstrual_period.isoformat() if p.last_menstrual_period else None,
        # AI Classification fields
        "severity_level": p.severity_level,
        "ticket_number": p.ticket_number,
        "color_code": p.color_code,
        "ai_analysis": ai_analysis,
        "created_at": p.created_at
    })

# Pregnancy form submission endpoint
@intake_bp.route("/pregnancy-form", methods=["POST"])
def submit_pregnancy_form():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Input validation
    try:
        # Validate required fields
        if not data.get("fullname") or len(str(data["fullname"]).strip()) < 2:
            return jsonify({"error": "Full name is required and must be at least 2 characters"}), 400
        
        if not data.get("age") or not str(data["age"]).isdigit():
            return jsonify({"error": "Valid age is required"}), 400
        
        age = int(data["age"])
        if age < 12 or age > 55:
            return jsonify({"error": "Age must be between 12 and 55"}), 400
        
        if not data.get("month") or not str(data["month"]).isdigit():
            return jsonify({"error": "Valid pregnancy month is required"}), 400
        
        month = int(data["month"])
        if month < 1 or month > 9:
            return jsonify({"error": "Pregnancy month must be between 1 and 9"}), 400
        
        if not data.get("due-date"):
            return jsonify({"error": "Due date is required"}), 400
        
        # Validate email format if provided
        if data.get("email"):
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, data["email"]):
                return jsonify({"error": "Invalid email format"}), 400
        
        # Validate phone format if provided
        if data.get("phone"):
            phone_pattern = r'^[0-9+\-\s\(\)]{10,15}$'
            if not re.match(phone_pattern, data["phone"]):
                return jsonify({"error": "Invalid phone number format"}), 400
        
        # Validate blood type if provided
        if data.get("blood-type"):
            valid_blood_types = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
            if data["blood-type"] not in valid_blood_types:
                return jsonify({"error": "Invalid blood type"}), 400
        
        # Check consent
        if not data.get("consent"):
            return jsonify({"error": "You must confirm that the information is accurate"}), 400
            
    except (ValueError, TypeError) as e:
        return jsonify({"error": "Invalid data format"}), 400
    
    try:
        # Parse due date
        due_date = None
        if data.get("due-date"):
            due_date = datetime.strptime(data["due-date"], "%Y-%m-%d").date()
        
        # Calculate pregnancy week from month
        pregnancy_week = int(data["month"]) * 4  # Approximate weeks from months
        
        # Determine trimester
        month = int(data["month"])
        if month <= 3:
            trimester = "First"
        elif month <= 6:
            trimester = "Second"
        else:
            trimester = "Third"
        
        # Create new patient intake record
        new_patient = PatientIntake(
            name=data["fullname"],
            age=int(data["age"]),
            contact=data.get("phone", "") or data.get("email", ""),
            symptoms="Pregnancy care registration",  # Default symptom for form submissions
            arrival_mode="Not specified",  # Default since this is just registration
            is_pregnant=True,
            pregnancy_week=pregnancy_week,
            trimester=trimester,
            due_date=due_date,
            blood_type=data.get("blood-type"),
            pregnancy_complications=data.get("medical-history"),
            previous_pregnancies=data.get("previous_pregnancies", 0),
            # Set default values for AI classification (can be updated later)
            severity_level="Light",
            ticket_number="REG001",  # Registration ticket
            color_code="G",
            ai_analysis=json.dumps({"form_type": "pregnancy_registration", "status": "registered"})
        )
        
        db.session.add(new_patient)
        db.session.commit()
        
        response_data = {
            "message": "Pregnancy information submitted successfully",
            "patient_id": new_patient.id,
            "name": new_patient.name,
            "ticket_number": new_patient.ticket_number,
            "pregnancy_week": pregnancy_week,
            "trimester": trimester,
            "due_date": due_date.isoformat() if due_date else None
        }
        
        return jsonify(response_data), 201
        
    except ValueError as e:
        return jsonify({"error": f"Invalid date format: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to submit pregnancy form: {str(e)}"}), 500


# Mood Tracker Endpoints
@intake_bp.route("/mood-tracker", methods=["POST"])
def submit_mood_entry():
    """Submit a daily mood entry for tracking"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        # Validate required fields
        if not data.get("mood"):
            return jsonify({"error": "Mood is required"}), 400
        
        # Validate mood value
        valid_moods = ["excellent", "good", "okay", "anxious", "sad", "overwhelmed"]
        if data["mood"] not in valid_moods:
            return jsonify({"error": f"Invalid mood. Must be one of: {', '.join(valid_moods)}"}), 400
        
        # Parse date (default to today if not provided)
        mood_date = date.today()
        if data.get("date"):
            try:
                mood_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        
        # Check if mood entry already exists for this date
        existing_entry = MoodEntry.query.filter_by(date=mood_date).first()
        if existing_entry:
            # Update existing entry
            existing_entry.mood = data["mood"]
            existing_entry.notes = data.get("notes", "")
            existing_entry.symptoms = json.dumps(data.get("symptoms", []))
            existing_entry.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return jsonify({
                "message": "Mood entry updated successfully",
                "mood_entry": existing_entry.to_dict(),
                "updated": True
            }), 200
        else:
            # Create new mood entry
            new_mood_entry = MoodEntry(
                date=mood_date,
                mood=data["mood"],
                notes=data.get("notes", ""),
                symptoms=json.dumps(data.get("symptoms", [])),
                patient_id=data.get("patient_id")  # Optional patient reference
            )
            
            db.session.add(new_mood_entry)
            db.session.commit()
            
            return jsonify({
                "message": "Mood entry created successfully",
                "mood_entry": new_mood_entry.to_dict(),
                "created": True
            }), 201
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to save mood entry: {str(e)}"}), 500


@intake_bp.route("/mood-tracker", methods=["GET"])
def get_mood_entries():
    """Get mood entries for a specific date range"""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        patient_id = request.args.get('patient_id')
        limit = request.args.get('limit', 30, type=int)  # Default to 30 entries
        
        # Build query
        query = MoodEntry.query
        
        # Filter by patient if provided
        if patient_id:
            query = query.filter_by(patient_id=patient_id)
        
        # Filter by date range if provided
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
                query = query.filter(MoodEntry.date >= start_date_obj)
            except ValueError:
                return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400
        
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
                query = query.filter(MoodEntry.date <= end_date_obj)
            except ValueError:
                return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400
        
        # Order by date descending and limit results
        query = query.order_by(MoodEntry.date.desc()).limit(limit)
        
        # Execute query
        mood_entries = query.all()
        
        return jsonify({
            "mood_entries": [entry.to_dict() for entry in mood_entries],
            "count": len(mood_entries)
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve mood entries: {str(e)}"}), 500


@intake_bp.route("/mood-tracker/stats", methods=["GET"])
def get_mood_stats():
    """Get mood statistics for analysis"""
    try:
        patient_id = request.args.get('patient_id')
        days = request.args.get('days', 30, type=int)  # Default to 30 days
        
        # Calculate date range
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        # Build query
        query = MoodEntry.query.filter(
            MoodEntry.date >= start_date,
            MoodEntry.date <= end_date
        )
        
        if patient_id:
            query = query.filter_by(patient_id=patient_id)
        
        # Get all entries in date range
        mood_entries = query.all()
        
        # Calculate statistics
        mood_counts = {}
        total_entries = len(mood_entries)
        
        for entry in mood_entries:
            mood = entry.mood
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        # Calculate percentages
        mood_percentages = {}
        for mood, count in mood_counts.items():
            mood_percentages[mood] = round((count / total_entries) * 100, 1) if total_entries > 0 else 0
        
        # Find most common mood
        most_common_mood = max(mood_counts.items(), key=lambda x: x[1])[0] if mood_counts else None
        
        return jsonify({
            "date_range": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": days
            },
            "total_entries": total_entries,
            "mood_counts": mood_counts,
            "mood_percentages": mood_percentages,
            "most_common_mood": most_common_mood,
            "average_entries_per_day": round(total_entries / days, 2) if days > 0 else 0
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to calculate mood statistics: {str(e)}"}), 500
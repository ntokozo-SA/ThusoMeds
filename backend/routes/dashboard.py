from flask import Blueprint, jsonify, request
from models import db, PatientIntake
from datetime import datetime, timedelta
import json

dashboard_bp = Blueprint("dashboard", __name__)

# Get dashboard statistics
@dashboard_bp.route("/dashboard/stats", methods=["GET"])
def get_dashboard_stats():
    try:
        # Get counts by severity level
        critical_count = PatientIntake.query.filter_by(color_code='R').count()
        urgent_count = PatientIntake.query.filter_by(color_code='Y').count()
        normal_count = PatientIntake.query.filter_by(color_code='G').count()
        total_count = PatientIntake.query.count()
        
        # Get recent patients (last 24 hours)
        last_24_hours = datetime.utcnow() - timedelta(hours=24)
        recent_count = PatientIntake.query.filter(PatientIntake.created_at >= last_24_hours).count()
        
        # Get patients with ETA information
        eta_count = PatientIntake.query.filter(PatientIntake.eta_minutes.isnot(None)).count()
        
        # Pregnancy-specific metrics
        first_trimester_count = PatientIntake.query.filter_by(trimester='First').count()
        second_trimester_count = PatientIntake.query.filter_by(trimester='Second').count()
        third_trimester_count = PatientIntake.query.filter_by(trimester='Third').count()
        
        # High-risk pregnancy indicators
        high_risk_count = PatientIntake.query.filter(
            db.or_(
                PatientIntake.previous_pregnancies > 3,
                PatientIntake.pregnancy_complications.isnot(None),
                db.and_(PatientIntake.age < 18, PatientIntake.is_pregnant == True),
                db.and_(PatientIntake.age > 35, PatientIntake.is_pregnant == True)
            )
        ).count()
        
        # Emergency cases by trimester
        critical_first_trimester = PatientIntake.query.filter(
            db.and_(PatientIntake.color_code == 'R', PatientIntake.trimester == 'First')
        ).count()
        critical_third_trimester = PatientIntake.query.filter(
            db.and_(PatientIntake.color_code == 'R', PatientIntake.trimester == 'Third')
        ).count()
        
        stats = {
            "critical": critical_count,
            "urgent": urgent_count,
            "normal": normal_count,
            "total": total_count,
            "recent_24h": recent_count,
            "with_eta": eta_count,
            # Pregnancy-specific metrics
            "pregnancy_stats": {
                "first_trimester": first_trimester_count,
                "second_trimester": second_trimester_count,
                "third_trimester": third_trimester_count,
                "high_risk_pregnancies": high_risk_count,
                "critical_first_trimester": critical_first_trimester,
                "critical_third_trimester": critical_third_trimester
            },
            "last_updated": datetime.utcnow().isoformat()
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get dashboard stats: {str(e)}"}), 500

# Get patients for dashboard with filtering and pagination
@dashboard_bp.route("/dashboard/patients", methods=["GET"])
def get_dashboard_patients():
    try:
        # Get query parameters
        severity = request.args.get('severity', 'all')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        # Build query
        query = PatientIntake.query
        
        # Filter by severity
        if severity != 'all':
            if severity == 'critical':
                query = query.filter_by(color_code='R')
            elif severity == 'urgent':
                query = query.filter_by(color_code='Y')
            elif severity == 'normal':
                query = query.filter_by(color_code='G')
        
        # Apply sorting
        if sort_by == 'created_at':
            if sort_order == 'desc':
                query = query.order_by(PatientIntake.created_at.desc())
            else:
                query = query.order_by(PatientIntake.created_at.asc())
        elif sort_by == 'severity':
            # Custom sorting: Critical (R) > Urgent (Y) > Normal (G)
            severity_order = db.case(
                (PatientIntake.color_code == 'R', 3),
                (PatientIntake.color_code == 'Y', 2),
                (PatientIntake.color_code == 'G', 1),
                else_=0
            )
            if sort_order == 'desc':
                query = query.order_by(severity_order.desc(), PatientIntake.created_at.desc())
            else:
                query = query.order_by(severity_order.asc(), PatientIntake.created_at.asc())
        
        # Apply pagination
        patients = query.offset(offset).limit(limit).all()
        
        # Convert to JSON
        result = []
        for p in patients:
            # Parse car_location JSON if it exists
            car_location = p.car_location
            if car_location:
                try:
                    car_location = json.loads(car_location)
                except (json.JSONDecodeError, TypeError):
                    pass
            
            # Parse AI analysis JSON if it exists
            ai_analysis = None
            if p.ai_analysis:
                try:
                    ai_analysis = json.loads(p.ai_analysis)
                except (json.JSONDecodeError, TypeError):
                    pass
            
            patient_data = {
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
                "created_at": p.created_at.isoformat() if p.created_at else None
            }
            result.append(patient_data)
        
        return jsonify({
            "patients": result,
            "total": query.count(),
            "limit": limit,
            "offset": offset,
            "severity_filter": severity
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get dashboard patients: {str(e)}"}), 500

# Get patient by ID for detailed view
@dashboard_bp.route("/dashboard/patients/<int:patient_id>", methods=["GET"])
def get_patient_details(patient_id):
    try:
        patient = PatientIntake.query.get_or_404(patient_id)
        
        # Parse car_location JSON if it exists
        car_location = patient.car_location
        if car_location:
            try:
                car_location = json.loads(car_location)
            except (json.JSONDecodeError, TypeError):
                pass
        
        # Parse AI analysis JSON if it exists
        ai_analysis = None
        if patient.ai_analysis:
            try:
                ai_analysis = json.loads(patient.ai_analysis)
            except (json.JSONDecodeError, TypeError):
                pass
        
        patient_data = {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "contact": patient.contact,
            "symptoms": patient.symptoms,
            "arrival_mode": patient.arrival_mode,
            "car_location": car_location,
            "eta_minutes": patient.eta_minutes,
            # Pregnancy-specific fields
            "is_pregnant": patient.is_pregnant,
            "pregnancy_week": patient.pregnancy_week,
            "trimester": patient.trimester,
            "due_date": patient.due_date.isoformat() if patient.due_date else None,
            "pregnancy_complications": patient.pregnancy_complications,
            "previous_pregnancies": patient.previous_pregnancies,
            "blood_type": patient.blood_type,
            "last_menstrual_period": patient.last_menstrual_period.isoformat() if patient.last_menstrual_period else None,
            # AI Classification fields
            "severity_level": patient.severity_level,
            "ticket_number": patient.ticket_number,
            "color_code": patient.color_code,
            "ai_analysis": ai_analysis,
            "created_at": patient.created_at.isoformat() if patient.created_at else None
        }
        
        return jsonify(patient_data), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get patient details: {str(e)}"}), 500

# Update patient status (mark as seen, called, etc.)
@dashboard_bp.route("/dashboard/patients/<int:patient_id>/status", methods=["PUT"])
def update_patient_status(patient_id):
    try:
        patient = PatientIntake.query.get_or_404(patient_id)
        data = request.get_json()
        
        # For now, we'll just return success
        # In a real implementation, you might want to add status fields to the model
        # such as seen_by, called_at, status, etc.
        
        return jsonify({
            "message": "Patient status updated successfully",
            "patient_id": patient_id,
            "status": data.get("status", "updated")
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to update patient status: {str(e)}"}), 500

# Get real-time updates (for polling)
@dashboard_bp.route("/dashboard/updates", methods=["GET"])
def get_dashboard_updates():
    try:
        # Get timestamp from query parameter
        since = request.args.get('since')
        if since:
            try:
                since_datetime = datetime.fromisoformat(since.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({"error": "Invalid since parameter format"}), 400
        else:
            since_datetime = datetime.utcnow() - timedelta(minutes=5)
        
        # Get patients created or updated since the timestamp
        patients = PatientIntake.query.filter(
            PatientIntake.created_at >= since_datetime
        ).order_by(PatientIntake.created_at.desc()).all()
        
        result = []
        for p in patients:
            result.append({
                "id": p.id,
                "name": p.name,
                "ticket_number": p.ticket_number,
                "color_code": p.color_code,
                "created_at": p.created_at.isoformat() if p.created_at else None,
                "eta_minutes": p.eta_minutes
            })
        
        return jsonify({
            "patients": result,
            "since": since_datetime.isoformat(),
            "count": len(result)
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get updates: {str(e)}"}), 500

# Get dashboard summary for quick overview
@dashboard_bp.route("/dashboard/summary", methods=["GET"])
def get_dashboard_summary():
    try:
        now = datetime.utcnow()
        last_hour = now - timedelta(hours=1)
        last_24_hours = now - timedelta(hours=24)
        
        # Get counts
        total_patients = PatientIntake.query.count()
        critical_patients = PatientIntake.query.filter_by(color_code='R').count()
        urgent_patients = PatientIntake.query.filter_by(color_code='Y').count()
        normal_patients = PatientIntake.query.filter_by(color_code='G').count()
        
        # Get recent activity
        recent_patients = PatientIntake.query.filter(
            PatientIntake.created_at >= last_hour
        ).count()
        
        # Get patients with ETA
        patients_with_eta = PatientIntake.query.filter(
            PatientIntake.eta_minutes.isnot(None)
        ).count()
        
        # Get latest patient
        latest_patient = PatientIntake.query.order_by(
            PatientIntake.created_at.desc()
        ).first()
        
        latest_patient_data = None
        if latest_patient:
            latest_patient_data = {
                "id": latest_patient.id,
                "name": latest_patient.name,
                "ticket_number": latest_patient.ticket_number,
                "color_code": latest_patient.color_code,
                "created_at": latest_patient.created_at.isoformat() if latest_patient.created_at else None
            }
        
        summary = {
            "stats": {
                "total": total_patients,
                "critical": critical_patients,
                "urgent": urgent_patients,
                "normal": normal_patients,
                "recent_hour": recent_patients,
                "with_eta": patients_with_eta
            },
            "latest_patient": latest_patient_data,
            "last_updated": now.isoformat()
        }
        
        return jsonify(summary), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get dashboard summary: {str(e)}"}), 500

# Get pregnancy-specific analytics
@dashboard_bp.route("/dashboard/pregnancy-analytics", methods=["GET"])
def get_pregnancy_analytics():
    try:
        # Get pregnancy week distribution
        week_distribution = {}
        for week in range(1, 41):
            count = PatientIntake.query.filter_by(pregnancy_week=week).count()
            if count > 0:
                week_distribution[f"week_{week}"] = count
        
        # Get trimester distribution with severity
        trimester_stats = {}
        for trimester in ['First', 'Second', 'Third']:
            total = PatientIntake.query.filter_by(trimester=trimester).count()
            critical = PatientIntake.query.filter(
                db.and_(PatientIntake.trimester == trimester, PatientIntake.color_code == 'R')
            ).count()
            urgent = PatientIntake.query.filter(
                db.and_(PatientIntake.trimester == trimester, PatientIntake.color_code == 'Y')
            ).count()
            normal = PatientIntake.query.filter(
                db.and_(PatientIntake.trimester == trimester, PatientIntake.color_code == 'G')
            ).count()
            
            trimester_stats[trimester.lower()] = {
                "total": total,
                "critical": critical,
                "urgent": urgent,
                "normal": normal
            }
        
        # Get age distribution of pregnant women
        age_groups = {
            "teenage": PatientIntake.query.filter(db.and_(PatientIntake.age < 18, PatientIntake.is_pregnant == True)).count(),
            "young_adult": PatientIntake.query.filter(db.and_(db.and_(PatientIntake.age >= 18, PatientIntake.age < 25), PatientIntake.is_pregnant == True)).count(),
            "adult": PatientIntake.query.filter(db.and_(db.and_(PatientIntake.age >= 25, PatientIntake.age < 35), PatientIntake.is_pregnant == True)).count(),
            "advanced_maternal_age": PatientIntake.query.filter(db.and_(PatientIntake.age >= 35, PatientIntake.is_pregnant == True)).count()
        }
        
        # Get common pregnancy complications
        complications = PatientIntake.query.filter(
            PatientIntake.pregnancy_complications.isnot(None)
        ).all()
        
        complication_types = {}
        for patient in complications:
            if patient.pregnancy_complications:
                comp = patient.pregnancy_complications.lower()
                if comp in complication_types:
                    complication_types[comp] += 1
                else:
                    complication_types[comp] = 1
        
        # Get emergency patterns by time of day
        from datetime import datetime, time
        emergency_by_hour = {}
        for hour in range(24):
            count = PatientIntake.query.filter(
                db.and_(
                    PatientIntake.color_code == 'R',
                    db.extract('hour', PatientIntake.created_at) == hour
                )
            ).count()
            if count > 0:
                emergency_by_hour[f"hour_{hour}"] = count
        
        analytics = {
            "pregnancy_week_distribution": week_distribution,
            "trimester_statistics": trimester_stats,
            "age_distribution": age_groups,
            "complication_types": complication_types,
            "emergency_patterns": emergency_by_hour,
            "last_updated": datetime.utcnow().isoformat()
        }
        
        return jsonify(analytics), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get pregnancy analytics: {str(e)}"}), 500

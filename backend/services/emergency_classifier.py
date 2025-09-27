import re
import random
from typing import Dict, List, Tuple


class EmergencyClassifier:
    """
    AI-powered emergency classification system for hospital triage
    Classifies patients into Red (Critical), Yellow (Urgent), or Green (Light) categories
    """
    
    def __init__(self):
        # Critical symptoms that require immediate attention
        self.critical_keywords = [
            'chest pain', 'heart attack', 'stroke', 'unconscious', 'bleeding heavily',
            'difficulty breathing', 'severe injury', 'trauma', 'cardiac arrest',
            'severe allergic reaction', 'overdose', 'severe burn', 'head injury',
            'seizure', 'shock', 'severe pain', 'emergency', 'urgent', 'critical'
        ]
        
        # Urgent symptoms that need attention within hours
        self.urgent_keywords = [
            'fever', 'high temperature', 'severe headache', 'abdominal pain',
            'vomiting', 'diarrhea', 'dehydration', 'infection', 'wound',
            'fracture', 'sprain', 'moderate pain', 'allergic reaction',
            'respiratory issues', 'dizziness', 'nausea', 'fatigue'
        ]
        
        # Light symptoms for routine care
        self.light_keywords = [
            'cold', 'flu', 'cough', 'sore throat', 'runny nose', 'mild headache',
            'checkup', 'routine', 'follow-up', 'prescription refill', 'mild pain',
            'skin rash', 'minor injury', 'consultation', 'preventive care'
        ]
        
        # Risk factors that increase severity
        self.risk_factors = [
            'diabetes', 'high blood pressure', 'heart condition', 'asthma',
            'chronic illness', 'chronic medication', 'medical conditions',
            'pregnancy', 'elderly', 'child', 'immunocompromised', 'contact with sick person'
        ]
    
    def classify_emergency(self, symptoms: str, age: int, risk_conditions: List[str] = None) -> Tuple[str, str, str]:
        """
        Classify patient emergency level and generate ticket
        
        Args:
            symptoms: Patient symptoms description
            age: Patient age
            risk_conditions: List of risk factors/conditions
            
        Returns:
            Tuple of (severity, ticket_number, color_code)
        """
        if not risk_conditions:
            risk_conditions = []
        
        # Convert to lowercase for matching
        symptoms_lower = symptoms.lower()
        risk_lower = [condition.lower() for condition in risk_conditions]
        
        # Calculate severity score
        severity_score = self._calculate_severity_score(symptoms_lower, age, risk_lower)
        
        # Determine classification
        if severity_score >= 6:
            severity = "Critical"
            color_code = "R"
        elif severity_score >= 3:
            severity = "Urgent"
            color_code = "Y"
        else:
            severity = "Light"
            color_code = "G"
        
        # Generate ticket number
        ticket_number = self._generate_ticket_number(color_code)
        
        return severity, ticket_number, color_code
    
    def _calculate_severity_score(self, symptoms: str, age: int, risk_conditions: List[str]) -> int:
        """Calculate severity score based on symptoms, age, and risk factors"""
        score = 0
        
        # Check for critical symptoms
        critical_found = False
        for keyword in self.critical_keywords:
            if keyword in symptoms:
                score += 3
                critical_found = True
                break  # Only count the highest severity match
        
        # Check for urgent symptoms
        if not critical_found:  # Only if no critical symptoms found
            for keyword in self.urgent_keywords:
                if keyword in symptoms:
                    score += 2
                    break
        
        # Check for light symptoms (only if no higher severity)
        if score == 0:
            for keyword in self.light_keywords:
                if keyword in symptoms:
                    score += 1
                    break
        
        # Age-based adjustments
        if age < 5:  # Children
            score += 1
        elif age > 65:  # Elderly
            score += 1
        
        # Risk factor adjustments
        for risk in risk_conditions:
            risk_lower = risk.lower()
            if any(rf in risk_lower for rf in self.risk_factors):
                score += 1
                break  # Only add once for risk factors
        
        # Additional severity indicators
        if any(word in symptoms for word in ['severe', 'severe pain', 'can\'t breathe', 'can\'t walk']):
            score += 2
        
        if any(word in symptoms for word in ['sudden', 'acute', 'rapid onset']):
            score += 1
        
        return min(score, 10)  # Cap at 10
    
    def _generate_ticket_number(self, color_code: str) -> str:
        """Generate a unique ticket number with color prefix"""
        # Generate 3 random digits
        random_number = random.randint(100, 999)
        return f"{color_code}{random_number}"
    
    def get_severity_explanation(self, severity: str, symptoms: str) -> str:
        """Provide explanation for the classification"""
        explanations = {
            "Critical": "🔴 Critical - Requires immediate medical attention. Please proceed to emergency department immediately.",
            "Urgent": "🟡 Urgent - Needs medical attention within a few hours. Please wait in urgent care area.",
            "Light": "🟢 Light - Routine care needed. Please wait in general waiting area."
        }
        
        base_explanation = explanations.get(severity, "")
        
        # Add specific recommendations
        if severity == "Critical":
            base_explanation += " Do not delay seeking immediate care."
        elif severity == "Urgent":
            base_explanation += " Monitor symptoms and seek care if they worsen."
        else:
            base_explanation += " You can be seen during regular hours."
        
        return base_explanation
    
    def analyze_symptoms(self, symptoms: str) -> Dict[str, any]:
        """Detailed analysis of symptoms for better classification"""
        symptoms_lower = symptoms.lower()
        
        analysis = {
            "detected_keywords": [],
            "severity_indicators": [],
            "recommendations": []
        }
        
        # Find detected keywords
        all_keywords = self.critical_keywords + self.urgent_keywords + self.light_keywords
        for keyword in all_keywords:
            if keyword in symptoms_lower:
                analysis["detected_keywords"].append(keyword)
        
        # Check for severity indicators
        if any(word in symptoms_lower for word in ['severe', 'acute', 'sudden']):
            analysis["severity_indicators"].append("High severity indicators present")
        
        if any(word in symptoms_lower for word in ['mild', 'slight', 'minor']):
            analysis["severity_indicators"].append("Low severity indicators present")
        
        # Generate recommendations
        if any(keyword in symptoms_lower for keyword in self.critical_keywords):
            analysis["recommendations"].append("Immediate medical attention required")
        elif any(keyword in symptoms_lower for keyword in self.urgent_keywords):
            analysis["recommendations"].append("Urgent care recommended")
        else:
            analysis["recommendations"].append("Routine care appropriate")
        
        return analysis

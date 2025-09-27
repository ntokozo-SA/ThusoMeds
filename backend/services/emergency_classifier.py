import re
import random
from typing import Dict, List, Tuple


class EmergencyClassifier:
    """
    AI-powered emergency classification system for pregnancy care triage
    Classifies pregnant patients into Red (Critical), Yellow (Urgent), or Green (Light) categories
    """
    
    def __init__(self):
        # Critical pregnancy symptoms that require immediate attention
        self.critical_keywords = [
            'severe bleeding', 'heavy vaginal bleeding', 'placenta previa', 'placental abruption',
            'preterm labor', 'labor contractions', 'water breaking', 'ruptured membranes',
            'severe preeclampsia', 'eclampsia', 'seizure during pregnancy', 'unconscious',
            'severe abdominal pain', 'severe headache with vision changes', 'difficulty breathing',
            'chest pain', 'heart palpitations', 'severe dizziness', 'fainting',
            'high fever', 'severe dehydration', 'emergency', 'urgent', 'critical'
        ]
        
        # Urgent pregnancy symptoms that need attention within hours
        self.urgent_keywords = [
            'moderate bleeding', 'spotting', 'cramping', 'abdominal pain', 'back pain',
            'nausea and vomiting', 'severe morning sickness', 'dehydration',
            'fever', 'infection symptoms', 'urinary tract infection', 'yeast infection',
            'swelling', 'high blood pressure', 'headache', 'vision changes',
            'decreased fetal movement', 'baby not moving', 'contractions',
            'pelvic pressure', 'pressure in pelvis', 'leaking fluid'
        ]
        
        # Light pregnancy symptoms for routine care
        self.light_keywords = [
            'mild nausea', 'morning sickness', 'mild cramping', 'round ligament pain',
            'mild back pain', 'fatigue', 'mild swelling', 'mild headache',
            'heartburn', 'constipation', 'mild mood changes', 'checkup',
            'routine visit', 'follow-up', 'prenatal care', 'ultrasound appointment',
            'blood work', 'glucose test', 'mild discomfort', 'normal pregnancy symptoms'
        ]
        
        # Pregnancy-specific risk factors that increase severity
        self.risk_factors = [
            'gestational diabetes', 'preeclampsia', 'high blood pressure', 'pregnancy hypertension',
            'multiple pregnancy', 'twins', 'triplets', 'previous preterm birth',
            'previous miscarriage', 'previous pregnancy complications', 'advanced maternal age',
            'teenage pregnancy', 'first pregnancy', 'high risk pregnancy',
            'placenta issues', 'cervical incompetence', 'chronic conditions',
            'diabetes', 'heart condition', 'asthma', 'autoimmune disease'
        ]
    
    def classify_emergency(self, symptoms: str, age: int, risk_conditions: List[str] = None, pregnancy_week: int = None, trimester: str = None) -> Tuple[str, str, str]:
        """
        Classify pregnant patient emergency level and generate ticket
        
        Args:
            symptoms: Patient symptoms description
            age: Patient age
            risk_conditions: List of risk factors/conditions
            pregnancy_week: Current pregnancy week (1-40)
            trimester: Current trimester (First, Second, Third)
            
        Returns:
            Tuple of (severity, ticket_number, color_code)
        """
        if not risk_conditions:
            risk_conditions = []
        
        # Convert to lowercase for matching
        symptoms_lower = symptoms.lower()
        risk_lower = [condition.lower() for condition in risk_conditions]
        
        # Calculate severity score
        severity_score = self._calculate_severity_score(symptoms_lower, age, risk_lower, pregnancy_week, trimester)
        
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
    
    def _calculate_severity_score(self, symptoms: str, age: int, risk_conditions: List[str], pregnancy_week: int = None, trimester: str = None) -> int:
        """Calculate severity score based on pregnancy symptoms, age, and risk factors"""
        score = 0
        
        # Check for critical pregnancy symptoms
        critical_found = False
        for keyword in self.critical_keywords:
            if keyword in symptoms:
                score += 3
                critical_found = True
                break  # Only count the highest severity match
        
        # Check for urgent pregnancy symptoms
        if not critical_found:  # Only if no critical symptoms found
            for keyword in self.urgent_keywords:
                if keyword in symptoms:
                    score += 2
                    break
        
        # Check for light pregnancy symptoms (only if no higher severity)
        if score == 0:
            for keyword in self.light_keywords:
                if keyword in symptoms:
                    score += 1
                    break
        
        # Age-based adjustments for pregnant women
        if age < 18:  # Teenage pregnancy
            score += 1
        elif age > 35:  # Advanced maternal age
            score += 1
        
        # Pregnancy week adjustments
        if pregnancy_week:
            if pregnancy_week < 12:  # First trimester
                score += 1  # Higher risk in early pregnancy
            elif pregnancy_week > 36:  # Late pregnancy
                score += 1  # Higher risk in late pregnancy
        
        # Trimester-specific adjustments
        if trimester:
            if trimester.lower() == 'first':
                score += 1  # Higher monitoring needed in first trimester
            elif trimester.lower() == 'third':
                score += 1  # Higher monitoring needed in third trimester
        
        # Risk factor adjustments
        for risk in risk_conditions:
            risk_lower = risk.lower()
            if any(rf in risk_lower for rf in self.risk_factors):
                score += 1
                break  # Only add once for risk factors
        
        # Additional severity indicators for pregnancy
        if any(word in symptoms for word in ['severe', 'severe pain', 'can\'t breathe', 'can\'t walk']):
            score += 2
        
        if any(word in symptoms for word in ['sudden', 'acute', 'rapid onset']):
            score += 1
        
        # Pregnancy-specific severity indicators
        if any(word in symptoms for word in ['bleeding', 'blood', 'spotting']):
            score += 2  # Any bleeding during pregnancy is concerning
        
        if any(word in symptoms for word in ['contractions', 'labor', 'birth']):
            score += 2  # Labor-related symptoms are critical
        
        return min(score, 10)  # Cap at 10
    
    def _generate_ticket_number(self, color_code: str) -> str:
        """Generate a unique ticket number with color prefix"""
        # Generate 3 random digits
        random_number = random.randint(100, 999)
        return f"{color_code}{random_number}"
    
    def get_severity_explanation(self, severity: str, symptoms: str) -> str:
        """Provide pregnancy-specific explanation for the classification"""
        explanations = {
            "Critical": "🔴 Critical - Requires immediate obstetric emergency care. Please proceed to labor & delivery or emergency department immediately. This could affect you and your baby's safety.",
            "Urgent": "🟡 Urgent - Needs pregnancy care attention within a few hours. Please wait in the maternity urgent care area. Monitor your baby's movements.",
            "Light": "🟢 Light - Routine prenatal care needed. Please wait in the general maternity waiting area. This is normal for your pregnancy stage."
        }
        
        base_explanation = explanations.get(severity, "")
        
        # Add pregnancy-specific recommendations
        if severity == "Critical":
            base_explanation += " Do not delay - seek immediate care for you and your baby."
        elif severity == "Urgent":
            base_explanation += " Monitor your symptoms and your baby's movements. Seek care immediately if symptoms worsen."
        else:
            base_explanation += " You can be seen during regular prenatal care hours."
        
        return base_explanation
    
    def analyze_symptoms(self, symptoms: str) -> Dict[str, any]:
        """Detailed analysis of pregnancy symptoms for better classification"""
        symptoms_lower = symptoms.lower()
        
        analysis = {
            "detected_keywords": [],
            "severity_indicators": [],
            "recommendations": [],
            "pregnancy_concerns": []
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
        
        # Check for pregnancy-specific concerns
        if any(word in symptoms_lower for word in ['bleeding', 'blood', 'spotting']):
            analysis["pregnancy_concerns"].append("Vaginal bleeding detected - requires immediate evaluation")
        
        if any(word in symptoms_lower for word in ['contractions', 'labor', 'birth']):
            analysis["pregnancy_concerns"].append("Labor symptoms detected - immediate assessment needed")
        
        if any(word in symptoms_lower for word in ['water breaking', 'leaking fluid']):
            analysis["pregnancy_concerns"].append("Possible rupture of membranes - urgent evaluation required")
        
        if any(word in symptoms_lower for word in ['decreased movement', 'baby not moving']):
            analysis["pregnancy_concerns"].append("Decreased fetal movement - needs immediate assessment")
        
        # Generate recommendations
        if any(keyword in symptoms_lower for keyword in self.critical_keywords):
            analysis["recommendations"].append("Immediate obstetric emergency care required")
        elif any(keyword in symptoms_lower for keyword in self.urgent_keywords):
            analysis["recommendations"].append("Urgent pregnancy care recommended")
        else:
            analysis["recommendations"].append("Routine prenatal care appropriate")
        
        return analysis

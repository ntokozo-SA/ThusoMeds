#!/usr/bin/env python3
"""
Debug script to test the AI classifier
"""

from services.emergency_classifier import EmergencyClassifier

def test_classifier():
    classifier = EmergencyClassifier()
    
    test_cases = [
        ("Chest pain, difficulty breathing", 35, ["Chronic medication", "Medical conditions"]),
        ("High fever, severe headache", 28, ["Contact with sick person"]),
        ("Cold, runny nose, mild cough", 45, [])
    ]
    
    for symptoms, age, risk_conditions in test_cases:
        print(f"\n{'='*50}")
        print(f"Symptoms: {symptoms}")
        print(f"Age: {age}")
        print(f"Risk: {risk_conditions}")
        
        # Get detailed analysis
        analysis = classifier.analyze_symptoms(symptoms)
        print(f"Detected keywords: {analysis['detected_keywords']}")
        
        # Calculate severity score manually
        symptoms_lower = symptoms.lower()
        score = 0
        critical_found = False
        
        # Check critical keywords
        for keyword in classifier.critical_keywords:
            if keyword in symptoms_lower:
                print(f"Found critical keyword: {keyword}")
                score += 3
                critical_found = True
                break
        
        if not critical_found:
            for keyword in classifier.urgent_keywords:
                if keyword in symptoms_lower:
                    print(f"Found urgent keyword: {keyword}")
                    score += 2
                    break
        
        # Age adjustments
        if age < 5 or age > 65:
            score += 1
        
        # Risk adjustments
        risk_found = False
        for risk in risk_conditions:
            if any(rf in risk.lower() for rf in classifier.risk_factors):
                print(f"Found risk factor: {risk}")
                score += 1
                risk_found = True
                break
        
        if risk_conditions and not risk_found:
            print(f"No matching risk factors found for: {risk_conditions}")
            print(f"Available risk factors: {classifier.risk_factors}")
        
        print(f"Calculated score: {score}")
        
        # Get classification
        severity, ticket, color = classifier.classify_emergency(symptoms, age, risk_conditions)
        print(f"Classification: {severity} ({color})")
        print(f"Ticket: {ticket}")

if __name__ == "__main__":
    test_classifier()

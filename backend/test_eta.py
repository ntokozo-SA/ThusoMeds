#!/usr/bin/env python3
"""
Test script for the ETA feature using OpenStreetMap/Nominatim
No API key required - completely free!
"""

import requests
import json

# Test data examples
BASE_URL = "http://localhost:5000"

# Example 1: Critical case - Severe chest pain with multiple risk factors (should get R ticket)
test_data_critical = {
    "name": "John Doe",
    "age": 75,  # Elderly (risk factor)
    "contact": "+1234567890",
    "symptoms": "Severe chest pain, can't breathe, heart attack symptoms",
    "arrival_mode": "ambulance",
    "chronic": "Yes",
    "conditions": "Yes",
    "contactSick": "No",
    "car_location": {
        "lat": -26.2041,  # Johannesburg coordinates
        "lng": 28.0473
    }
}

# Example 2: Urgent case - Fever (should get Y ticket)
test_data_urgent = {
    "name": "Jane Smith",
    "age": 28,
    "contact": "+1234567891",
    "symptoms": "High fever, severe headache",
    "arrival_mode": "private car",
    "chronic": "No",
    "conditions": "No",
    "contactSick": "Yes",
    "car_location": {
        "address": "Sandton City, Johannesburg, South Africa"
    }
}

# Example 3: Light case - Cold symptoms (should get G ticket)
test_data_light = {
    "name": "Bob Wilson",
    "age": 45,
    "contact": "+1234567892",
    "symptoms": "Cold, runny nose, mild cough",
    "arrival_mode": "public transport",
    "chronic": "No",
    "conditions": "No",
    "contactSick": "No"
}

def test_intake_with_ai_classification():
    """Test the intake endpoint with AI classification and ETA calculation"""
    
    test_cases = [
        ("Critical Case (Chest Pain)", test_data_critical),
        ("Urgent Case (Fever)", test_data_urgent),
        ("Light Case (Cold)", test_data_light)
    ]
    
    for case_name, test_data in test_cases:
        print(f"\n{'='*60}")
        print(f"Testing {case_name}")
        print(f"{'='*60}")
        
        try:
            response = requests.post(f"{BASE_URL}/intake", json=test_data)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Success!")
                print(f"Patient ID: {result['id']}")
                print(f"Ticket Number: {result['ticket_number']}")
                print(f"Severity Level: {result['severity_level']}")
                print(f"Color Code: {result['color_code']}")
                print(f"AI Explanation: {result['severity_explanation']}")
                
                if result.get('eta_minutes'):
                    print(f"ETA: {result['eta_minutes']} minutes")
                
                print(f"AI Analysis: {json.dumps(result['ai_analysis'], indent=2)}")
            else:
                print(f"❌ Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: Could not connect to the server. Make sure the Flask app is running.")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*60}")
    print("AI Classification Test Complete!")
    print(f"{'='*60}")

if __name__ == "__main__":
    test_intake_with_ai_classification()

#!/usr/bin/env python3
"""
Test script for the ETA feature using OpenStreetMap/Nominatim
No API key required - completely free!
"""

import requests
import json

# Test data examples
BASE_URL = "http://localhost:5000"

# Example 1: Using GPS coordinates
test_data_coords = {
    "name": "John Doe",
    "age": 35,
    "contact": "+1234567890",
    "symptoms": "Chest pain",
    "arrival_mode": "private car",
    "car_location": {
        "lat": -26.2041,  # Johannesburg coordinates
        "lng": 28.0473
    }
}

# Example 2: Using text address
test_data_address = {
    "name": "Jane Smith",
    "age": 28,
    "contact": "+1234567891",
    "symptoms": "Shortness of breath",
    "arrival_mode": "private car",
    "car_location": {
        "address": "Sandton City, Johannesburg, South Africa"
    }
}

def test_intake_with_eta():
    """Test the intake endpoint with ETA calculation"""
    
    print("Testing ETA feature with GPS coordinates...")
    try:
        response = requests.post(f"{BASE_URL}/intake", json=test_data_coords)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the Flask app is running.")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    print("Testing ETA feature with text address...")
    try:
        response = requests.post(f"{BASE_URL}/intake", json=test_data_address)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the Flask app is running.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_intake_with_eta()

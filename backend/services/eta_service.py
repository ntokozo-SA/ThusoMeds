import requests
import json
import math
from flask import current_app
from typing import Dict, Optional, Tuple


class ETAService:
    """Service for calculating ETA using OpenStreetMap/Nominatim APIs"""
    
    def __init__(self):
        self.hospital_lat = current_app.config.get('HOSPITAL_LAT')
        self.hospital_lng = current_app.config.get('HOSPITAL_LNG')
        self.average_speed = current_app.config.get('AVERAGE_DRIVING_SPEED_KMH', 50)
        
        if not self.hospital_lat or not self.hospital_lng:
            raise ValueError("Hospital coordinates not configured")
    
    def geocode_address(self, address: str) -> Tuple[float, float]:
        """
        Convert text address to GPS coordinates using Nominatim (OpenStreetMap)
        
        Args:
            address: Text address to geocode
            
        Returns:
            Tuple of (latitude, longitude)
            
        Raises:
            ValueError: If address cannot be geocoded
            requests.RequestException: If API request fails
        """
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': address,
            'format': 'json',
            'limit': 1,
            'addressdetails': 1
        }
        headers = {
            'User-Agent': 'HospitalIntakeSystem/1.0'  # Required by Nominatim
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                raise ValueError("Address not found")
            
            location = data[0]
            return float(location['lat']), float(location['lon'])
            
        except requests.RequestException as e:
            raise requests.RequestException(f"Geocoding API request failed: {str(e)}")
        except (KeyError, ValueError, TypeError, IndexError) as e:
            raise ValueError(f"Invalid geocoding response: {str(e)}")
    
    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance between two points on Earth using the Haversine formula
        
        Args:
            lat1, lon1: First point coordinates in decimal degrees
            lat2, lon2: Second point coordinates in decimal degrees
            
        Returns:
            Distance in kilometers
        """
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of earth in kilometers
        r = 6371
        return c * r
    
    def calculate_eta(self, origin_lat: float, origin_lng: float) -> int:
        """
        Calculate ETA in minutes from origin to hospital using haversine distance
        
        Args:
            origin_lat: Origin latitude
            origin_lng: Origin longitude
            
        Returns:
            ETA in minutes (estimated)
            
        Raises:
            ValueError: If coordinates are invalid
        """
        # Calculate straight-line distance
        distance_km = self.haversine_distance(
            origin_lat, origin_lng, 
            self.hospital_lat, self.hospital_lng
        )
        
        # Estimate driving time (straight-line distance * factor for roads)
        # Urban driving typically requires 1.3-1.5x straight-line distance
        road_distance_km = distance_km * 1.4
        
        # Calculate time in hours, then convert to minutes
        time_hours = road_distance_km / self.average_speed
        eta_minutes = int(time_hours * 60)
        
        # Ensure reasonable range (1 minute to 8 hours)
        return max(1, min(eta_minutes, 480))
    
    def get_eta_from_location(self, car_location: Dict) -> int:
        """
        Calculate ETA from car location to hospital
        
        Args:
            car_location: Dict containing either:
                - 'lat' and 'lng' keys for GPS coordinates, or
                - 'address' key for text address
                
        Returns:
            ETA in minutes
            
        Raises:
            ValueError: If location is invalid or ETA cannot be calculated
            requests.RequestException: If API request fails
        """
        if not car_location:
            raise ValueError("Car location is required")
        
        # Check if GPS coordinates are provided
        if 'lat' in car_location and 'lng' in car_location:
            try:
                lat = float(car_location['lat'])
                lng = float(car_location['lng'])
                
                # Validate coordinate ranges
                if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                    raise ValueError("Invalid GPS coordinates")
                
                return self.calculate_eta(lat, lng)
                
            except (ValueError, TypeError):
                raise ValueError("Invalid GPS coordinates format")
        
        # Check if text address is provided
        elif 'address' in car_location:
            address = car_location['address'].strip()
            if not address:
                raise ValueError("Address cannot be empty")
            
            try:
                # Geocode the address first
                lat, lng = self.geocode_address(address)
                return self.calculate_eta(lat, lng)
            except (requests.RequestException, ValueError) as e:
                # If geocoding fails, provide a reasonable default estimate
                # This assumes the address is somewhere in the same city
                print(f"Geocoding failed for '{address}': {e}")
                print("Using default city-wide estimate of 30 minutes")
                return 30
        
        else:
            raise ValueError("Car location must contain either 'lat'/'lng' or 'address'")

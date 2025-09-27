# OpenStreetMap ETA Feature Setup Guide

This guide explains how to use the free OpenStreetMap/Nominatim ETA feature in the hospital intake system.

## Features

✅ **Completely Free** - No API keys required  
✅ **OpenStreetMap geocoding** - Convert addresses to coordinates  
✅ **Haversine distance calculation** - Calculate straight-line distances  
✅ **ETA estimation** - Estimate driving time using average speed  

## No Setup Required!

Unlike Google Maps, OpenStreetMap/Nominatim is completely free and requires no API keys or billing setup.

## Configuration

### 1. Update Hospital Coordinates

Edit `backend/config.py` and set your hospital's coordinates:

```python
# Hospital coordinates (replace with actual hospital location)
HOSPITAL_LAT = -26.2041  # Your hospital's latitude
HOSPITAL_LNG = 28.0473   # Your hospital's longitude

# ETA estimation settings
AVERAGE_DRIVING_SPEED_KMH = 50  # Average driving speed in km/h
```

### 2. Adjust ETA Settings (Optional)

You can customize the ETA calculation:

- `AVERAGE_DRIVING_SPEED_KMH`: Average driving speed (default: 50 km/h)
- Road distance factor: Currently set to 1.4x straight-line distance (adjustable in `eta_service.py`)

## API Usage

### POST /intake

The `/intake` endpoint accepts a `car_location` field that can be either:

#### Option 1: GPS Coordinates
```json
{
    "name": "John Doe",
    "age": 35,
    "contact": "+1234567890",
    "symptoms": "Chest pain",
    "arrival_mode": "private car",
    "car_location": {
        "lat": -26.2041,
        "lng": 28.0473
    }
}
```

#### Option 2: Text Address
```json
{
    "name": "Jane Smith",
    "age": 28,
    "contact": "+1234567891",
    "symptoms": "Shortness of breath",
    "arrival_mode": "private car",
    "car_location": {
        "address": "Sandton City, Johannesburg, South Africa"
    }
}
```

### Response

The endpoint will return the patient ID and estimated ETA:

```json
{
    "message": "Patient intake created",
    "id": 1,
    "eta_minutes": 15
}
```

## How It Works

1. **Geocoding**: If a text address is provided, Nominatim converts it to GPS coordinates
2. **Distance Calculation**: Haversine formula calculates straight-line distance
3. **Road Distance**: Multiplies by 1.4x to account for actual road routes
4. **ETA Calculation**: Divides by average driving speed to get estimated time

## Testing

Run the test script to verify the ETA feature:

```bash
python test_eta.py
```

Make sure your Flask app is running first:
```bash
python app.py
```

## Limitations

- **Estimated ETA**: Based on straight-line distance × factor, not actual road routes
- **No traffic data**: Doesn't account for traffic conditions
- **No turn-by-turn routing**: Uses simplified distance calculation

## Advantages

- **Free**: No costs or API limits
- **No registration**: No Google Cloud account needed
- **Open source**: Uses open data from OpenStreetMap
- **Reliable**: Nominatim has good global coverage

## Rate Limits

Nominatim has a usage policy:
- Maximum 1 request per second
- No commercial use without permission
- Include a proper User-Agent header (already configured)

For production use with high volume, consider running your own Nominatim instance.

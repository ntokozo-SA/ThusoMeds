# ETA Feature Setup Guide

This guide explains how to set up and use the ETA (Estimated Time of Arrival) feature in the hospital intake system.

## Prerequisites

1. **Google Maps API Key**: You need a Google Cloud Platform account with the following APIs enabled:
   - Geocoding API
   - Distance Matrix API

2. **Python Dependencies**: Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### 1. Set Environment Variables

Set your Google Maps API key as an environment variable:

**Windows (PowerShell):**
```powershell
$env:GOOGLE_MAPS_API_KEY="your_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set GOOGLE_MAPS_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export GOOGLE_MAPS_API_KEY="your_api_key_here"
```

### 2. Update Hospital Coordinates

Edit `config.py` and update the hospital coordinates:

```python
# Hospital coordinates (replace with actual hospital location)
HOSPITAL_LAT = 40.7128  # Your hospital's latitude
HOSPITAL_LNG = -74.0060  # Your hospital's longitude
```

## API Usage

### POST /intake

The `/intake` endpoint now accepts a `car_location` field that can be either:

#### Option 1: GPS Coordinates
```json
{
    "name": "John Doe",
    "age": 35,
    "contact": "+1234567890",
    "symptoms": "Chest pain",
    "arrival_mode": "private car",
    "car_location": {
        "lat": 40.7589,
        "lng": -73.9851
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
        "address": "Central Park, New York, NY"
    }
}
```

### Response

The endpoint will return the patient ID and calculated ETA:

```json
{
    "message": "Patient intake created",
    "id": 1,
    "eta_minutes": 15
}
```

## Error Handling

The API handles various error scenarios:

- **400 Bad Request**: Invalid car location format or unrecognized address
- **500 Internal Server Error**: Google Maps API failures or configuration issues

### Common Error Messages

- `"Invalid car location: Address not found"` - The provided address cannot be geocoded
- `"Invalid car location: Invalid GPS coordinates"` - Coordinates are out of valid range
- `"Failed to calculate ETA: API request failed"` - Google Maps API is unavailable

## Testing

Run the test script to verify the ETA feature:

```bash
python test_eta.py
```

Make sure your Flask app is running first:
```bash
python app.py
```

## Security Notes

- The Google Maps API key is kept secret on the backend
- Never expose the API key to the frontend
- Consider implementing API key rotation for production use
- Monitor API usage to avoid unexpected charges

## Cost Considerations

Google Maps APIs have usage limits and costs:
- Geocoding API: $5 per 1,000 requests
- Distance Matrix API: $5 per 1,000 requests

Consider implementing caching for frequently requested locations to reduce API calls.

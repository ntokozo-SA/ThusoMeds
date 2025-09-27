// Global variables
let userLocation = null;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeForm();
});

function initializeForm() {
    // Show/hide location section based on arrival mode
    const arrivalModeSelect = document.querySelector('select[name="arrival_mode"]');
    const locationSection = document.getElementById('locationSection');
    
    if (arrivalModeSelect && locationSection) {
        arrivalModeSelect.addEventListener('change', function() {
            if (this.value === 'private car') {
                locationSection.style.display = 'block';
            } else {
                locationSection.style.display = 'none';
            }
        });
    }

    // Handle location type toggle
    const locationTypeRadios = document.querySelectorAll('input[name="locationType"]');
    const gpsLocation = document.getElementById('gpsLocation');
    const addressLocation = document.getElementById('addressLocation');
    
    locationTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'gps') {
                gpsLocation.style.display = 'block';
                addressLocation.style.display = 'none';
            } else {
                gpsLocation.style.display = 'none';
                addressLocation.style.display = 'block';
            }
        });
    });

    // Get location button
    const getLocationBtn = document.getElementById('getLocationBtn');
    if (getLocationBtn) {
        getLocationBtn.addEventListener('click', getCurrentLocation);
    }

    // Form submission
    const form = document.getElementById('triageForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
}

function getCurrentLocation() {
    const statusElement = document.getElementById('locationStatus');
    
    if (!navigator.geolocation) {
        statusElement.textContent = '❌ Geolocation not supported by this browser.';
        return;
    }

    statusElement.textContent = '📍 Getting your location...';
    
    navigator.geolocation.getCurrentPosition(
        function(position) {
            userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            
            document.getElementById('carLat').value = userLocation.lat;
            document.getElementById('carLng').value = userLocation.lng;
            
            statusElement.textContent = `✅ Location found! (${userLocation.lat.toFixed(4)}, ${userLocation.lng.toFixed(4)})`;
        },
        function(error) {
            let errorMessage = '❌ Error getting location: ';
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    errorMessage += 'Permission denied.';
                    break;
                case error.POSITION_UNAVAILABLE:
                    errorMessage += 'Position unavailable.';
                    break;
                case error.TIMEOUT:
                    errorMessage += 'Request timeout.';
                    break;
                default:
                    errorMessage += 'Unknown error.';
                    break;
            }
            statusElement.textContent = errorMessage;
        }
    );
}

async function handleFormSubmit(e) {
    e.preventDefault();

    // Collect form data
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    // Handle checkbox values (symptoms)
    const symptomCheckboxes = document.querySelectorAll('input[name="symptoms"]:checked');
    const symptoms = Array.from(symptomCheckboxes).map(cb => cb.value);
    
    // Add other symptoms if provided
    if (data.otherSymptoms && data.otherSymptoms.trim()) {
        symptoms.push(data.otherSymptoms.trim());
    }
    
    // Prepare request data
    const requestData = {
        name: data.fullname,
        age: parseInt(data.age),
        contact: data.contact,
        symptoms: symptoms.join(', '),
        arrival_mode: data.arrival_mode
    };

    // Add car location if arriving by private car
    if (data.arrival_mode === 'private car') {
        if (data.locationType === 'gps' && data.car_lat && data.car_lng) {
            requestData.car_location = {
                lat: parseFloat(data.car_lat),
                lng: parseFloat(data.car_lng)
            };
        } else if (data.locationType === 'address' && data.car_address) {
            requestData.car_location = {
                address: data.car_address
            };
        }
    }

    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('resultSection').style.display = 'block';
    document.getElementById('resultCard').style.display = 'none';

    try {
        // Send to backend
        const response = await fetch('http://localhost:5000/intake', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });

        const result = await response.json();
        
        // Hide loading
        document.getElementById('loading').style.display = 'none';
        document.getElementById('resultCard').style.display = 'block';
        
        // Redirect to ticket display page with ticket data
        const ticketParams = new URLSearchParams({
            ticket: result.ticket_number,
            severity: result.color_code,
            color: result.color_code,
            explanation: result.severity_explanation || ''
        });
        
        // Add ETA data if available
        if (result.eta_minutes) {
            let etaDetails = 'Estimated driving time to hospital';
            if (data.locationType === 'gps') {
                etaDetails += ' (using GPS coordinates)';
            } else if (data.locationType === 'address') {
                etaDetails += ' (using address)';
            }
            
            ticketParams.append('eta', result.eta_minutes);
            ticketParams.append('etaDetails', etaDetails);
        }
        
        // Redirect to ticket display page
        window.location.href = `ticket-display.html?${ticketParams.toString()}`;

    } catch (err) {
        console.error('Error:', err);
        document.getElementById('loading').style.display = 'none';
        document.getElementById('resultCard').style.display = 'block';
        
        document.getElementById('ticketNumber').textContent = '❌ Error';
        document.getElementById('severityLevel').textContent = 'Failed to submit form. Please try again.';
    }
}

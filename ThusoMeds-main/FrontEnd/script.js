// Global variables
let userLocation = null;

// Enhanced Clinic Page Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize pain scale functionality
    const painLevelSlider = document.getElementById('painLevel');
    const painValueDisplay = document.getElementById('painValue');
    
    if (painLevelSlider && painValueDisplay) {
        painLevelSlider.addEventListener('input', function() {
            painValueDisplay.textContent = this.value;
            
            // Add visual feedback based on pain level
            const painLevel = parseInt(this.value);
            if (painLevel <= 3) {
                painValueDisplay.style.color = '#4CAF50';
            } else if (painLevel <= 7) {
                painValueDisplay.style.color = '#ffc107';
            } else {
                painValueDisplay.style.color = '#ff6b6b';
            }
        });
    }

    // Enhanced form submission with animations
    const triageForm = document.getElementById('triageForm');
    if (triageForm) {
        triageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleTriageSubmission();
        });
    }

    // Auto-detect location on page load
    detectLocation();
    
    // Initialize chat functionality
    initializeChat();
});

function handleTriageSubmission() {
    const submitBtn = document.querySelector('.submit-btn');
    const loadingOverlay = document.getElementById('loading');
    const resultSection = document.getElementById('resultSection');
    
    // Show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Processing...</span>';
    
    // Show loading overlay
    if (loadingOverlay) {
        loadingOverlay.style.display = 'block';
    }
    
    if (resultSection) {
        resultSection.style.display = 'block';
    }
    
    // Simulate processing time
    setTimeout(() => {
        processTriageResults();
    }, 3000);
}

function processTriageResults() {
    const loadingOverlay = document.getElementById('loading');
    const resultCard = document.getElementById('resultCard');
    const ticketNumber = document.getElementById('ticketNumber');
    const severityLevel = document.getElementById('severityLevel');
    const etaInfo = document.getElementById('etaInfo');
    
    // Hide loading overlay
    if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
    }
    
    // Show result card with animation
    if (resultCard) {
        resultCard.style.display = 'block';
        resultCard.style.animation = 'fadeInUp 0.8s ease-out';
    }
    
    // Generate ticket and severity
    const ticket = generateTicket();
    const severity = determineSeverity();
    
    if (ticketNumber) {
        ticketNumber.textContent = ticket;
    }
    
    if (severityLevel) {
        severityLevel.textContent = severity.text;
        severityLevel.className = `severity-badge ${severity.class}`;
    }
    
    // Show ETA information
    if (etaInfo) {
        etaInfo.style.display = 'block';
        showETA();
    }
    
    // Reset submit button
    const submitBtn = document.querySelector('.submit-btn');
    if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i><span>Submit Triage</span>';
    }
    
    // Show chat section after a delay
    setTimeout(() => {
        const chatSection = document.getElementById('chatSection');
        if (chatSection) {
            chatSection.style.display = 'block';
            chatSection.style.animation = 'fadeInUp 0.8s ease-out';
        }
    }, 1500);
}

function determineSeverity() {
    const symptomCheckboxes = document.querySelectorAll('input[name="symptoms"]:checked');
    const selectedSymptoms = Array.from(symptomCheckboxes).map(checkbox => checkbox.value);
    const painLevel = parseInt(document.getElementById('painLevel').value);
    
    // High priority symptoms
    const highPrioritySymptoms = ['chest-pain', 'shortness-breath', 'loss-consciousness', 'severe-headache', 'difficulty-speaking', 'allergic-reaction'];
    
    // Medium priority symptoms
    const mediumPrioritySymptoms = ['severe-back-pain', 'abdominal-pain', 'contractions', 'water-broke', 'bleeding', 'vision-problems'];
    
    // Check for high priority symptoms
    const hasHighPriority = selectedSymptoms.some(symptom => highPrioritySymptoms.includes(symptom));
    const hasMediumPriority = selectedSymptoms.some(symptom => mediumPrioritySymptoms.includes(symptom));
    
    // Determine severity
    if (hasHighPriority || painLevel >= 8) {
        return { text: 'HIGH', class: 'high' };
    } else if (hasMediumPriority || painLevel >= 5) {
        return { text: 'MEDIUM', class: 'medium' };
    } else {
        return { text: 'LOW', class: 'low' };
    }
}

function showETA() {
    const etaMinutes = document.getElementById('etaMinutes');
    const etaDetails = document.getElementById('etaDetails');
    
    if (etaMinutes && etaDetails) {
        // Simulate ETA calculation
        const baseTime = 15; // Base time in minutes
        const randomVariation = Math.floor(Math.random() * 10) + 1;
        const totalMinutes = baseTime + randomVariation;
        
        etaMinutes.textContent = `${totalMinutes} minutes`;
        etaDetails.textContent = `Based on current traffic and facility capacity`;
    }
}

function detectLocation() {
    const nearestHospital = document.getElementById('nearestHospital');
    const facilitySpinner = document.getElementById('facilitySpinner');
    
    if (nearestHospital && facilitySpinner) {
        nearestHospital.textContent = 'Detecting nearest hospital or clinic...';
        facilitySpinner.style.display = 'block';
        
        // Simulate location detection
        setTimeout(() => {
            const facilities = [
                'City General Hospital - 2.3 km away',
                'Metro Medical Center - 1.8 km away',
                'Central Clinic - 3.1 km away',
                'Emergency Care Facility - 4.2 km away'
            ];
            
            const randomFacility = facilities[Math.floor(Math.random() * facilities.length)];
            nearestHospital.textContent = randomFacility;
            facilitySpinner.style.display = 'none';
        }, 2000);
    }
}

function initializeChat() {
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    
    if (chatInput && sendBtn) {
        // Handle enter key press
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Auto-resize textarea
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    }
}

// Enhanced chat functionality
function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    
    if (chatInput && chatMessages && chatInput.value.trim()) {
        // Add user message
        addMessage(chatInput.value.trim(), 'user');
        
        // Clear input
        chatInput.value = '';
        
        // Simulate bot response
        setTimeout(() => {
            const response = generateBotResponse(chatInput.value);
            addMessage(response, 'bot');
        }, 1000);
    }
}

function sendQuickMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    
    if (chatMessages) {
        addMessage(message, 'user');
        
        setTimeout(() => {
            const response = generateQuickResponse(message);
            addMessage(response, 'bot');
        }, 1000);
    }
}

function addMessage(text, sender) {
    const chatMessages = document.getElementById('chatMessages');
    
    if (chatMessages) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = sender === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const headerDiv = document.createElement('div');
        headerDiv.className = 'message-header';
        headerDiv.innerHTML = `
            <strong>${sender === 'bot' ? 'Medical Assistant' : 'You'}</strong>
            <span class="timestamp">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
        `;
        
        const textDiv = document.createElement('p');
        textDiv.textContent = text;
        
        contentDiv.appendChild(headerDiv);
        contentDiv.appendChild(textDiv);
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function generateBotResponse(userMessage) {
    const responses = [
        "I understand your concern. Can you provide more details about the symptoms you're experiencing?",
        "That sounds concerning. How long have you been experiencing these symptoms?",
        "I'm here to help. Are you experiencing any other symptoms along with what you mentioned?",
        "Thank you for sharing that information. Are you able to move around comfortably?",
        "I understand this is stressful. Have you taken any medication for these symptoms?",
        "That's important information. Are you currently feeling dizzy or lightheaded?"
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
}

function generateQuickResponse(quickMessage) {
    const responses = {
        'Contractions': "I understand you're experiencing contractions. How far apart are they? Are they getting stronger or more frequent?",
        'Bleeding': "Any bleeding during pregnancy needs immediate attention. How much bleeding are you experiencing? Is it bright red or dark?",
        'Pain': "I'm concerned about your pain level. Can you describe the type of pain - is it sharp, dull, or cramping? Where exactly do you feel it?",
        'Water broke': "If your water has broken, this is important timing information. What color was the fluid? Clear, pink, or greenish?"
    };
    
    return responses[quickMessage] || "I understand your concern. Please provide more details about your symptoms.";
}

// Ticket generation function
function generateTicket() {
    // Letters: Q, W, E
    const letters = ['Q', 'W', 'E'];
    
    // Numbers: 1, 2, 3, 4, 5, 6, 7, 8, 9, 0
    const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0];
    
    // Select one random letter from QWE
    const randomLetter = letters[Math.floor(Math.random() * letters.length)];
    
    // Select three random numbers
    const randomNumbers = [];
    for (let i = 0; i < 3; i++) {
        randomNumbers.push(numbers[Math.floor(Math.random() * numbers.length)]);
    }
    
    // Combine letter and numbers
    const ticket = randomLetter + randomNumbers.join('');
    
    return ticket;
}

// Initialize when DOM is loaded

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

    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('resultSection').style.display = 'block';
    document.getElementById('resultCard').style.display = 'none';

    // Simulate processing time
    setTimeout(() => {
        // Generate ticket
        const ticket = generateTicket();
        
        // Hide loading
        document.getElementById('loading').style.display = 'none';
        document.getElementById('resultCard').style.display = 'block';
        
        // Display ticket
        document.getElementById('ticketNumber').textContent = `Ticket: ${ticket}`;
        document.getElementById('severityLevel').textContent = 'Your triage has been submitted successfully!';
        
        // Scroll to result section
        document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth' });
        
        // Show chat system after ticket is generated
        setTimeout(() => {
            document.getElementById('chatSection').style.display = 'block';
            document.getElementById('chatSection').scrollIntoView({ behavior: 'smooth' });
        }, 2000);
        
    }, 1500); // 1.5 second delay to simulate processing
}

// Chat System Functions
const pregnancyGuidance = {
    contractions: {
        keywords: ['contraction', 'contractions', 'labor', 'labour', 'pushing'],
        response: `<div class="emergency-alert">🚨 ACTIVE LABOR DETECTED</div>
        <div class="medical-tip">
        <strong>Immediate Actions:</strong><br>
        • Time contractions (from start to start)<br>
        • If contractions are <5 minutes apart, you're in active labor<br>
        • Stay calm and breathe deeply<br>
        • Get to hospital immediately if contractions are regular and close together<br>
        • Don't push until you're at the hospital unless baby is crowning
        </div>
        <strong>When to call emergency:</strong> If you feel the urge to push or see the baby's head.`
    },
    bleeding: {
        keywords: ['bleeding', 'blood', 'hemorrhage', 'spotting', 'discharge'],
        response: `<div class="emergency-alert">🚨 BLEEDING EMERGENCY</div>
        <div class="medical-tip">
        <strong>Immediate Actions:</strong><br>
        • Lie down on your left side<br>
        • Elevate your legs if possible<br>
        • Do NOT insert anything into vagina<br>
        • Monitor amount of bleeding<br>
        • Save any tissue/clots for medical examination
        </div>
        <strong>Emergency signs:</strong> Heavy bleeding (soaking a pad in <1 hour), bright red blood, or bleeding with severe pain.`
    },
    pain: {
        keywords: ['pain', 'severe pain', 'cramping', 'ache', 'hurt', 'uncomfortable'],
        response: `<div class="medical-tip">
        <strong>Pain Management:</strong><br>
        • Try different positions (on hands and knees, side lying)<br>
        • Apply heat pack to lower back<br>
        • Take slow, deep breaths<br>
        • Use relaxation techniques<br>
        • Avoid lying flat on your back
        </div>
        <strong>Emergency pain:</strong> If pain is severe, constant, or in upper abdomen, get medical help immediately.`
    },
    water: {
        keywords: ['water broke', 'water break', 'amniotic', 'fluid', 'leaking'],
        response: `<div class="emergency-alert">💧 WATER BROKE</div>
        <div class="medical-tip">
        <strong>Immediate Actions:</strong><br>
        • Note the time your water broke<br>
        • Check color and smell of fluid<br>
        • Put on a sanitary pad<br>
        • Do NOT have sex or insert anything<br>
        • Prepare to go to hospital within 24 hours
        </div>
        <strong>Emergency signs:</strong> Green/brown fluid (meconium), foul smell, or fever.`
    },
    general: {
        response: `I'm here to help with your pregnancy emergency. Please describe your symptoms or use the quick buttons above. Common concerns include:
        <br>• 💪 Contractions and labor signs
        <br>• 🩸 Bleeding or spotting  
        <br>• 😰 Severe pain or discomfort
        <br>• 💧 Water breaking
        <br><br>Remember: When in doubt, it's always better to seek medical attention immediately.`
    }
};

function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (message) {
        addUserMessage(message);
        input.value = '';
        
        // Simulate bot thinking
        setTimeout(() => {
            const response = getBotResponse(message);
            addBotMessage(response);
        }, 1000);
    }
}

function sendQuickMessage(symptom) {
    addUserMessage(symptom);
    
    setTimeout(() => {
        const response = getBotResponse(symptom);
        addBotMessage(response);
    }, 1000);
}

function getBotResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    // Check for specific symptoms
    for (const [key, guidance] of Object.entries(pregnancyGuidance)) {
        if (key === 'general') continue;
        
        if (guidance.keywords.some(keyword => lowerMessage.includes(keyword))) {
            return guidance.response;
        }
    }
    
    // Emergency keywords that need immediate attention
    const emergencyKeywords = ['emergency', 'urgent', 'help', 'can\'t breathe', 'fainting', 'unconscious'];
    if (emergencyKeywords.some(keyword => lowerMessage.includes(keyword))) {
        return `<div class="emergency-alert">🚨 EMERGENCY DETECTED</div>
        <div class="medical-tip">
        <strong>Call emergency services immediately!</strong><br>
        While waiting for help:<br>
        • Stay calm and breathe slowly<br>
        • Lie down if feeling faint<br>
        • Have someone stay with you<br>
        • Gather medical records if possible
        </div>`;
    }
    
    // Default response
    return pregnancyGuidance.general.response;
}

function addUserMessage(message) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `<div class="message-content">${message}</div>`;
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function addBotMessage(message) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.innerHTML = `<div class="message-content"><strong>Emergency Bot:</strong><br>${message}</div>`;
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function scrollToBottom() {
    const messagesContainer = document.getElementById('chatMessages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Initialize chat functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeForm();
    
    // Chat input event listeners
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
});

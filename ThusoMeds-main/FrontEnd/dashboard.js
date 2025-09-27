// Dashboard JavaScript
class Dashboard {
    constructor() {
        this.patients = [];
        this.currentFilter = 'all';
        this.autoRefreshInterval = null;
        this.isAutoRefreshEnabled = false;
        this.refreshInterval = 5000; // 5 seconds
        
        this.init();
    }

    init() {
        this.loadPatients();
        this.setupEventListeners();
        this.startAutoRefresh();
        this.updateLastUpdatedTime();
    }

    setupEventListeners() {
        // Add any additional event listeners here
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.stopAutoRefresh();
            } else {
                this.startAutoRefresh();
            }
        });
    }

    async loadPatients() {
        try {
            this.showLoading();
            
            // Use dashboard-specific endpoint for better performance
            const response = await fetch('http://localhost:5000/dashboard/patients', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.patients = data.patients || data;
            this.renderPatients();
            this.updateStats();
            this.updateLastUpdatedTime();

        } catch (error) {
            console.error('Error loading patients:', error);
            this.showError('Failed to load patient data. Please check your connection.');
        }
    }

    renderPatients() {
        const container = document.getElementById('patientsContainer');
        const template = document.getElementById('patientCardTemplate');
        
        if (this.patients.length === 0) {
            this.showEmptyState();
            return;
        }

        this.hideLoading();
        this.hideEmptyState();

        // Clear existing cards
        container.innerHTML = '';

        // Filter patients based on current filter
        const filteredPatients = this.getFilteredPatients();

        // Sort patients by priority and creation time
        const sortedPatients = this.sortPatients(filteredPatients);

        // Create patient cards
        sortedPatients.forEach(patient => {
            const card = this.createPatientCard(patient, template);
            container.appendChild(card);
        });
    }

    createPatientCard(patient, template) {
        const card = template.content.cloneNode(true);
        
        // Set data attributes
        card.querySelector('.patient-card').setAttribute('data-severity', patient.color_code?.toLowerCase() || 'normal');
        card.querySelector('.patient-card').setAttribute('data-id', patient.id);

        // Priority badge
        const priorityText = card.querySelector('.priority-text');
        const ticketNumber = card.querySelector('.ticket-number');
        
        if (patient.color_code === 'R') {
            priorityText.textContent = 'Critical';
        } else if (patient.color_code === 'Y') {
            priorityText.textContent = 'Urgent';
        } else {
            priorityText.textContent = 'Normal';
        }
        
        ticketNumber.textContent = patient.ticket_number || `#${patient.id}`;

        // ETA information
        const etaText = card.querySelector('.eta-text');
        if (patient.eta_minutes) {
            etaText.textContent = `${patient.eta_minutes} min`;
        } else {
            etaText.textContent = 'Unknown';
        }

        // Patient information
        card.querySelector('.patient-name').textContent = patient.name;
        card.querySelector('.patient-age').textContent = `${patient.age} years`;
        card.querySelector('.patient-contact').textContent = patient.contact;

        // Symptoms
        card.querySelector('.symptoms-text').textContent = patient.symptoms || 'No symptoms reported';

        // Arrival mode
        const modeIcon = card.querySelector('.arrival-mode i');
        const modeText = card.querySelector('.mode-text');
        
        switch(patient.arrival_mode) {
            case 'private car':
                modeIcon.className = 'fas fa-car';
                modeText.textContent = 'Private Car';
                break;
            case 'ambulance':
                modeIcon.className = 'fas fa-ambulance';
                modeText.textContent = 'Ambulance';
                break;
            case 'public transport':
                modeIcon.className = 'fas fa-bus';
                modeText.textContent = 'Public Transport';
                break;
            case 'walking':
                modeIcon.className = 'fas fa-walking';
                modeText.textContent = 'Walking';
                break;
            default:
                modeIcon.className = 'fas fa-question';
                modeText.textContent = patient.arrival_mode || 'Unknown';
        }

        // Submission time
        const timeText = card.querySelector('.time-text');
        if (patient.created_at) {
            const submissionTime = new Date(patient.created_at);
            timeText.textContent = this.formatTime(submissionTime);
        } else {
            timeText.textContent = 'Unknown';
        }

        return card;
    }

    sortPatients(patients) {
        return patients.sort((a, b) => {
            // First sort by priority (Critical > Urgent > Normal)
            const priorityOrder = { 'R': 3, 'Y': 2, 'G': 1 };
            const aPriority = priorityOrder[a.color_code] || 1;
            const bPriority = priorityOrder[b.color_code] || 1;
            
            if (aPriority !== bPriority) {
                return bPriority - aPriority;
            }
            
            // Then sort by creation time (newest first)
            const aTime = new Date(a.created_at);
            const bTime = new Date(b.created_at);
            return bTime - aTime;
        });
    }

    getFilteredPatients() {
        if (this.currentFilter === 'all') {
            return this.patients;
        }
        
        return this.patients.filter(patient => {
            const severity = patient.color_code?.toLowerCase() || 'normal';
            return severity === this.currentFilter;
        });
    }

    filterPatients(filter) {
        this.currentFilter = filter;
        
        // Update active tab
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-filter="${filter}"]`).classList.add('active');
        
        // Re-render patients
        this.renderPatients();
    }

    updateStats() {
        const stats = {
            critical: 0,
            urgent: 0,
            normal: 0,
            total: this.patients.length
        };

        this.patients.forEach(patient => {
            const severity = patient.color_code?.toLowerCase() || 'normal';
            if (severity === 'r') {
                stats.critical++;
            } else if (severity === 'y') {
                stats.urgent++;
            } else {
                stats.normal++;
            }
        });

        // Update stat cards
        document.getElementById('criticalCount').textContent = stats.critical;
        document.getElementById('urgentCount').textContent = stats.urgent;
        document.getElementById('normalCount').textContent = stats.normal;
        document.getElementById('totalCount').textContent = stats.total;
    }

    viewPatientDetails(button) {
        const card = button.closest('.patient-card');
        const patientId = parseInt(card.getAttribute('data-id'));
        const patient = this.patients.find(p => p.id === patientId);
        
        if (patient) {
            this.showPatientDetails(patient);
        }
    }

    showPatientDetails(patient) {
        const detailsPanel = document.getElementById('patientDetails');
        const detailsContent = document.getElementById('detailsContent');
        
        // Create detailed patient information
        detailsContent.innerHTML = `
            <div class="patient-detail-card">
                <div class="detail-header">
                    <h4>${patient.name}</h4>
                    <div class="priority-badge-large ${patient.color_code?.toLowerCase() || 'normal'}">
                        ${patient.color_code === 'R' ? 'Critical' : patient.color_code === 'Y' ? 'Urgent' : 'Normal'}
                    </div>
                </div>
                
                <div class="detail-section">
                    <h5><i class="fas fa-user"></i> Patient Information</h5>
                    <div class="detail-grid">
                        <div class="detail-item">
                            <label>Age:</label>
                            <span>${patient.age} years</span>
                        </div>
                        <div class="detail-item">
                            <label>Contact:</label>
                            <span>${patient.contact}</span>
                        </div>
                        <div class="detail-item">
                            <label>Ticket #:</label>
                            <span>${patient.ticket_number || `#${patient.id}`}</span>
                        </div>
                        <div class="detail-item">
                            <label>Arrival Mode:</label>
                            <span>${patient.arrival_mode || 'Unknown'}</span>
                        </div>
                    </div>
                </div>
                
                <div class="detail-section">
                    <h5><i class="fas fa-stethoscope"></i> Symptoms</h5>
                    <p>${patient.symptoms || 'No symptoms reported'}</p>
                </div>
                
                ${patient.eta_minutes ? `
                <div class="detail-section">
                    <h5><i class="fas fa-clock"></i> ETA Information</h5>
                    <div class="eta-detail">
                        <span class="eta-number">${patient.eta_minutes}</span>
                        <span class="eta-unit">minutes</span>
                    </div>
                </div>
                ` : ''}
                
                ${patient.ai_analysis ? `
                <div class="detail-section">
                    <h5><i class="fas fa-brain"></i> AI Analysis</h5>
                    <div class="ai-analysis">
                        ${JSON.stringify(patient.ai_analysis, null, 2)}
                    </div>
                </div>
                ` : ''}
                
                <div class="detail-section">
                    <h5><i class="fas fa-calendar"></i> Submission Details</h5>
                    <div class="detail-grid">
                        <div class="detail-item">
                            <label>Submitted:</label>
                            <span>${this.formatDateTime(new Date(patient.created_at))}</span>
                        </div>
                        <div class="detail-item">
                            <label>ID:</label>
                            <span>${patient.id}</span>
                        </div>
                    </div>
                </div>
                
                <div class="detail-actions">
                    <button class="btn btn-primary" onclick="dashboard.callPatient(${patient.id})">
                        <i class="fas fa-phone"></i> Call Patient
                    </button>
                    <button class="btn btn-secondary" onclick="dashboard.markAsSeen(${patient.id})">
                        <i class="fas fa-check"></i> Mark as Seen
                    </button>
                </div>
            </div>
        `;
        
        detailsPanel.style.display = 'block';
    }

    closePatientDetails() {
        document.getElementById('patientDetails').style.display = 'none';
    }

    callPatient(patientId) {
        const patient = this.patients.find(p => p.id === patientId);
        if (patient && patient.contact) {
            // Create a phone link
            const phoneLink = `tel:${patient.contact}`;
            window.open(phoneLink, '_self');
        } else {
            alert('No contact information available for this patient.');
        }
    }

    markAsSeen(patientId) {
        // This would typically send a request to the backend to mark patient as seen
        console.log(`Marking patient ${patientId} as seen`);
        // For now, just close the details panel
        this.closePatientDetails();
    }

    refreshQueue() {
        this.loadPatients();
    }

    toggleAutoRefresh() {
        if (this.isAutoRefreshEnabled) {
            this.stopAutoRefresh();
        } else {
            this.startAutoRefresh();
        }
    }

    startAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
        }
        
        this.autoRefreshInterval = setInterval(() => {
            this.loadPatients();
        }, this.refreshInterval);
        
        this.isAutoRefreshEnabled = true;
        this.updateAutoRefreshButton();
    }

    stopAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
            this.autoRefreshInterval = null;
        }
        
        this.isAutoRefreshEnabled = false;
        this.updateAutoRefreshButton();
    }

    updateAutoRefreshButton() {
        const icon = document.getElementById('autoRefreshIcon');
        const text = document.getElementById('autoRefreshText');
        
        if (this.isAutoRefreshEnabled) {
            icon.className = 'fas fa-pause';
            text.textContent = 'Pause Auto Refresh';
        } else {
            icon.className = 'fas fa-play';
            text.textContent = 'Auto Refresh';
        }
    }

    updateLastUpdatedTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        document.getElementById('lastUpdated').textContent = timeString;
    }

    formatTime(date) {
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMins / 60);
        
        if (diffMins < 1) {
            return 'Just now';
        } else if (diffMins < 60) {
            return `${diffMins}m ago`;
        } else if (diffHours < 24) {
            return `${diffHours}h ago`;
        } else {
            return date.toLocaleDateString();
        }
    }

    formatDateTime(date) {
        return date.toLocaleString();
    }

    showLoading() {
        document.getElementById('loadingState').style.display = 'flex';
        document.getElementById('emptyState').style.display = 'none';
    }

    hideLoading() {
        document.getElementById('loadingState').style.display = 'none';
    }

    showEmptyState() {
        document.getElementById('emptyState').style.display = 'flex';
        document.getElementById('loadingState').style.display = 'none';
    }

    hideEmptyState() {
        document.getElementById('emptyState').style.display = 'none';
    }

    showError(message) {
        const container = document.getElementById('patientsContainer');
        container.innerHTML = `
            <div class="error-state">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Error</h3>
                <p>${message}</p>
                <button class="btn btn-primary" onclick="dashboard.loadPatients()">
                    <i class="fas fa-redo"></i> Retry
                </button>
            </div>
        `;
    }
}

// Global functions for HTML onclick handlers
function refreshQueue() {
    dashboard.loadPatients();
}

function toggleAutoRefresh() {
    dashboard.toggleAutoRefresh();
}

function filterPatients(filter) {
    dashboard.filterPatients(filter);
}

function viewPatientDetails(button) {
    dashboard.viewPatientDetails(button);
}

function callPatient(patientId) {
    dashboard.callPatient(patientId);
}

function closePatientDetails() {
    dashboard.closePatientDetails();
}

// Initialize dashboard when DOM is loaded
let dashboard;
document.addEventListener('DOMContentLoaded', function() {
    dashboard = new Dashboard();
});

// Add CSS for detail panel
const detailStyles = `
<style>
.patient-detail-card {
    padding: 1rem 0;
}

.detail-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #ecf0f1;
}

.detail-header h4 {
    margin: 0;
    color: #2c3e50;
    font-size: 1.3rem;
    font-weight: 600;
}

.priority-badge-large {
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.priority-badge-large.r {
    background: #e74c3c;
    color: white;
}

.priority-badge-large.y {
    background: #f39c12;
    color: white;
}

.priority-badge-large.normal {
    background: #27ae60;
    color: white;
}

.detail-section {
    margin-bottom: 1.5rem;
}

.detail-section h5 {
    margin: 0 0 1rem 0;
    color: #2c3e50;
    font-size: 1rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.detail-section h5 i {
    color: #3498db;
}

.detail-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
}

.detail-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.detail-item label {
    font-size: 0.8rem;
    color: #7f8c8d;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.detail-item span {
    color: #2c3e50;
    font-weight: 500;
}

.eta-detail {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
}

.eta-number {
    font-size: 2rem;
    font-weight: 700;
    color: #3498db;
}

.eta-unit {
    color: #7f8c8d;
    font-size: 0.9rem;
}

.ai-analysis {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    font-family: 'Courier New', monospace;
    font-size: 0.8rem;
    color: #2c3e50;
    white-space: pre-wrap;
    max-height: 200px;
    overflow-y: auto;
}

.detail-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 2px solid #ecf0f1;
}

.error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    color: #e74c3c;
    text-align: center;
}

.error-state i {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.error-state h3 {
    margin: 0 0 0.5rem 0;
    color: #e74c3c;
}

.error-state p {
    margin: 0 0 1rem 0;
    color: #7f8c8d;
}
</style>
`;

// Inject styles
document.head.insertAdjacentHTML('beforeend', detailStyles);

# ThusoMed Clinic/Hospital Dashboard

## Overview
The ThusoMed Dashboard is a real-time patient queue management system designed for clinics and hospitals. It displays patient information submitted through the patient intake forms and provides a comprehensive view of the current patient queue with priority-based sorting.

## Features

### 🎯 Real-time Patient Queue
- **Live Updates**: Automatically refreshes every 5 seconds to show new patient submissions
- **Priority-based Sorting**: Patients are sorted by severity (Critical > Urgent > Normal)
- **Color-coded System**: 
  - 🔴 **Critical (Red)**: Emergency cases requiring immediate attention
  - 🟡 **Urgent (Yellow)**: Cases that need attention within hours
  - 🟢 **Normal (Green)**: Regular cases for standard consultation

### 📊 Dashboard Statistics
- **Live Counters**: Real-time counts for each priority level
- **Total Patients**: Overall patient count in the system
- **Recent Activity**: Track patients submitted in the last 24 hours

### 🔍 Patient Management
- **Detailed View**: Click on any patient to see comprehensive information
- **Contact Integration**: Direct call functionality for patient contact
- **ETA Information**: Shows estimated arrival times for patients traveling by car
- **Symptom Tracking**: Complete symptom information with AI analysis

### 🎛️ Dashboard Controls
- **Auto Refresh**: Toggle automatic updates on/off
- **Manual Refresh**: Force immediate data refresh
- **Filter System**: View patients by priority level
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## How to Access

### For Clinic/Hospital Staff:
1. Open the main ThusoMed application (`Coverpage.html`)
2. Click the "🏥 Clinic Dashboard" button in the header
3. The dashboard will open showing the current patient queue

### Direct Access:
- Navigate directly to `dashboard.html` in your browser

## Patient Flow

1. **Patient Submission**: Patients fill out the intake form on `clinic.html` or `hospital.html`
2. **AI Classification**: The system automatically classifies the patient's severity level
3. **Dashboard Update**: The patient appears on the dashboard in real-time
4. **Staff Action**: Clinic staff can view details, call patients, and manage the queue

## Technical Details

### Backend Endpoints:
- `GET /dashboard/patients` - Retrieve all patients with filtering
- `GET /dashboard/stats` - Get dashboard statistics
- `GET /dashboard/summary` - Quick overview of current status
- `GET /dashboard/updates` - Real-time updates since a timestamp

### Frontend Features:
- **Polling-based Updates**: Checks for new patients every 5 seconds
- **Responsive Grid Layout**: Adapts to different screen sizes
- **Progressive Enhancement**: Works without JavaScript for basic functionality
- **Accessibility**: Screen reader friendly with proper ARIA labels

## Color Coding System

| Color | Priority | Description | Typical Response Time |
|-------|----------|-------------|----------------------|
| 🔴 Red | Critical | Life-threatening emergencies | Immediate |
| 🟡 Yellow | Urgent | Serious but not life-threatening | Within 1-2 hours |
| 🟢 Green | Normal | Routine consultations | Standard appointment |

## Browser Compatibility
- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

## Mobile Support
The dashboard is fully responsive and optimized for:
- 📱 Mobile phones (320px+)
- 📱 Tablets (768px+)
- 💻 Desktop computers (1200px+)

## Troubleshooting

### Dashboard Not Loading:
1. Ensure the backend server is running on `http://localhost:5000`
2. Check browser console for JavaScript errors
3. Verify CORS settings are properly configured

### No Patients Showing:
1. Check if patients have submitted intake forms
2. Verify database connection
3. Check backend logs for errors

### Auto-refresh Not Working:
1. Ensure JavaScript is enabled in your browser
2. Check if the page is in the background (refresh pauses when tab is inactive)
3. Click "Auto Refresh" button to restart polling

## Security Notes
- The dashboard displays patient information - ensure proper access controls
- Consider implementing user authentication for production use
- Patient data should be handled according to healthcare privacy regulations

## Future Enhancements
- 🔐 User authentication and role-based access
- 📱 Mobile app version
- 🔔 Push notifications for new critical patients
- 📈 Analytics and reporting features
- 🎯 Integration with hospital management systems
- 📞 VoIP calling integration
- 📍 Real-time patient location tracking

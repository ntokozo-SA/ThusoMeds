# 🤱 MamaCare - Pregnancy Care Assistant

A comprehensive pregnancy care application designed specifically for expecting mothers, providing intelligent triage, emergency classification, and care coordination.

## 🌟 Features

### For Expecting Mothers
- **Smart Pregnancy Triage**: AI-powered classification of pregnancy-related symptoms
- **Emergency Detection**: Immediate identification of critical pregnancy complications
- **Facility Locator**: Find nearby maternity clinics and hospitals with labor wards
- **Personalized Care**: Pregnancy-specific risk assessment and recommendations
- **Easy Access**: Simple, intuitive interface designed for pregnant women

### For Healthcare Providers
- **Pregnancy-Focused Dashboard**: Monitor expecting mothers and their care needs
- **Risk Stratification**: Automated classification of pregnancy emergencies
- **Patient Tracking**: Complete pregnancy history and medical records
- **Real-time Alerts**: Immediate notifications for critical cases

## 🚨 Emergency Classification System

### Critical (Red) - Immediate Care Required
- Severe vaginal bleeding
- Labor contractions
- Water breaking
- Severe preeclampsia symptoms
- Severe abdominal pain
- Difficulty breathing
- Fainting or loss of consciousness

### Urgent (Yellow) - Care Within Hours
- Moderate bleeding or spotting
- Severe cramping
- Decreased baby movement
- Fever during pregnancy
- Severe swelling
- High blood pressure symptoms

### Light (Green) - Routine Care
- Mild nausea and morning sickness
- Mild cramping
- Normal pregnancy discomforts
- Routine checkups
- Prenatal appointments

## 🏥 Facility Types

### Maternity Clinics
- Routine prenatal care
- Ultrasounds and checkups
- Prenatal consultations
- Birthing classes
- Postnatal support

### Hospitals with Labor Wards
- Emergency obstetric care
- Labor and delivery services
- High-risk pregnancy management
- NICU facilities
- 24/7 emergency services

## 🛠️ Technical Features

### AI-Powered Classification
- **Pregnancy-Specific Keywords**: Specialized symptom recognition for pregnancy
- **Risk Factor Assessment**: Age, trimester, and medical history consideration
- **Severity Scoring**: Intelligent scoring system for pregnancy emergencies
- **Real-time Analysis**: Instant classification and recommendations

### Database Schema
- **Pregnancy Information**: Week, trimester, due date, complications
- **Medical History**: Previous pregnancies, blood type, risk factors
- **Symptom Tracking**: Detailed pregnancy-specific symptom recording
- **Care Coordination**: ETA calculation and facility matching

## 📱 User Interface

### Design Philosophy
- **Maternal Colors**: Soft pinks and warm tones for comfort
- **Intuitive Navigation**: Easy-to-use interface for pregnant women
- **Clear Categorization**: Color-coded symptoms by severity
- **Accessible Design**: Large buttons and clear text for all users

### Key Pages
- **Coverpage**: Facility selection and introduction
- **Clinic Form**: Comprehensive pregnancy intake form
- **Dashboard**: Healthcare provider monitoring interface
- **Results**: Clear triage results and next steps

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Flask
- SQLite3
- Modern web browser

### Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run database migration: `python migrate_pregnancy_fields.py`
4. Start the application: `python app.py`

### Usage
1. Open the application in your browser
2. Select your preferred facility type (Maternity Clinic or Hospital)
3. Allow location access for nearby facility detection
4. Choose your facility and complete the pregnancy intake form
5. Receive your triage classification and next steps

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to 'development' for debug mode
- `DATABASE_URL`: Database connection string
- `API_KEY`: External service API keys (if needed)

### Customization
- Update facility data in `Coverpage.html`
- Modify symptom classifications in `emergency_classifier.py`
- Customize styling in `style.css`

## 📊 Monitoring and Analytics

### Dashboard Features
- Patient intake statistics
- Emergency classification distribution
- Facility utilization metrics
- Response time tracking
- Risk factor analysis

### Reports
- Daily intake summaries
- Emergency case reports
- Facility performance metrics
- Patient outcome tracking

## 🛡️ Security and Privacy

### Data Protection
- Encrypted data transmission
- Secure database storage
- HIPAA-compliant data handling
- Patient privacy protection

### Access Control
- Role-based permissions
- Audit trail logging
- Secure authentication
- Data access monitoring

## 🤝 Contributing

We welcome contributions to improve MamaCare! Please see our contributing guidelines for:
- Code style and standards
- Testing requirements
- Documentation updates
- Feature requests

## 📞 Support

For technical support or questions:
- Email: support@mamacare.com
- Documentation: [Link to docs]
- Issue Tracker: [GitHub Issues]

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Healthcare professionals who provided domain expertise
- Expecting mothers who tested and provided feedback
- Open source community for foundational technologies

---

**MamaCare** - Caring for you and your baby, every step of the way. 🤱💕

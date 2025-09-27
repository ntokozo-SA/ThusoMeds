# AI Emergency Classification System

## Overview

The AI Emergency Classification System automatically analyzes patient symptoms and generates color-coded tickets for hospital triage:

- **🔴 Red (R)**: Critical - Immediate attention required
- **🟡 Yellow (Y)**: Urgent - Attention within hours  
- **🟢 Green (G)**: Light - Routine care

## How It Works

### 1. Symptom Analysis
The AI analyzes patient symptoms using keyword matching and severity scoring:

**Critical Keywords (Score +3)**:
- chest pain, heart attack, stroke, unconscious, bleeding heavily
- difficulty breathing, severe injury, trauma, cardiac arrest
- severe allergic reaction, overdose, severe burn, head injury
- seizure, shock, severe pain, emergency, urgent, critical

**Urgent Keywords (Score +2)**:
- fever, high temperature, severe headache, abdominal pain
- vomiting, diarrhea, dehydration, infection, wound
- fracture, sprain, moderate pain, allergic reaction
- respiratory issues, dizziness, nausea, fatigue

**Light Keywords (Score +1)**:
- cold, flu, cough, sore throat, runny nose, mild headache
- checkup, routine, follow-up, prescription refill, mild pain
- skin rash, minor injury, consultation, preventive care

### 2. Risk Factor Assessment
Additional points for:
- Age factors (children <5, elderly >65): +1 point
- Chronic conditions: +1 point
- Medical history: +1 point
- Severity indicators ("severe", "acute", "sudden"): +1-2 points

### 3. Classification Logic
- **Score ≥8**: Critical (R ticket)
- **Score ≥4**: Urgent (Y ticket)  
- **Score <4**: Light (G ticket)

## Ticket Generation

Tickets are generated with format: `[COLOR][3-DIGIT-NUMBER]`

Examples:
- `R123` - Critical patient #123
- `Y456` - Urgent patient #456
- `G789` - Light patient #789

## API Response

When a patient submits their intake, the API returns:

```json
{
  "message": "Patient intake created",
  "id": 1,
  "ticket_number": "R123",
  "severity_level": "Critical",
  "color_code": "R",
  "severity_explanation": "🔴 Critical - Requires immediate medical attention...",
  "ai_analysis": {
    "detected_keywords": ["chest pain", "difficulty breathing"],
    "severity_indicators": ["High severity indicators present"],
    "recommendations": ["Immediate medical attention required"]
  },
  "eta_minutes": 15
}
```

## Usage Examples

### Critical Case
```json
{
  "name": "John Doe",
  "age": 35,
  "symptoms": "Chest pain, difficulty breathing",
  "chronic": "Yes",
  "conditions": "Yes"
}
```
**Result**: R123 ticket (Critical)

### Urgent Case
```json
{
  "name": "Jane Smith", 
  "age": 28,
  "symptoms": "High fever, severe headache",
  "chronic": "No",
  "conditions": "No",
  "contactSick": "Yes"
}
```
**Result**: Y456 ticket (Urgent)

### Light Case
```json
{
  "name": "Bob Wilson",
  "age": 45,
  "symptoms": "Cold, runny nose, mild cough",
  "chronic": "No",
  "conditions": "No"
}
```
**Result**: G789 ticket (Light)

## Testing

Run the test script to verify AI classification:

```bash
python test_eta.py
```

This will test all three severity levels and show:
- Generated ticket numbers
- Severity classifications
- AI explanations
- Detailed analysis

## Customization

### Adding New Keywords
Edit `backend/services/emergency_classifier.py`:

```python
self.critical_keywords.append('your_new_keyword')
self.urgent_keywords.append('another_keyword')
self.light_keywords.append('mild_keyword')
```

### Adjusting Scoring
Modify the scoring logic in `_calculate_severity_score()`:

```python
# Change thresholds
if severity_score >= 10:  # Make critical harder to achieve
    severity = "Critical"
```

### Custom Ticket Format
Modify `_generate_ticket_number()`:

```python
def _generate_ticket_number(self, color_code: str) -> str:
    # Custom format: R001, Y002, G003
    return f"{color_code}{self._get_next_number():03d}"
```

## Frontend Integration

The frontend automatically displays:
- Color-coded ticket numbers
- Severity explanations
- AI recommendations
- Visual indicators (🔴🟡🟢)

## Database Schema

New fields added to `PatientIntake`:
- `severity_level`: Critical/Urgent/Light
- `ticket_number`: R123/Y456/G789 format
- `color_code`: R/Y/G
- `ai_analysis`: JSON analysis details

## Benefits

1. **Consistent Triage**: Standardized emergency classification
2. **Priority Management**: Clear visual priority system
3. **Staff Efficiency**: Automatic severity assessment
4. **Patient Flow**: Optimized waiting room management
5. **Data Analytics**: Track emergency patterns

## Future Enhancements

- Machine learning model training
- Integration with hospital systems
- Real-time severity monitoring
- Predictive analytics
- Mobile app integration

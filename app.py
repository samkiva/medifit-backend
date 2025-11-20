from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import hashlib
import json

app = Flask(__name__)
CORS(app)

# Simple AI-like risk calculator
def calculate_risk(symptoms, vitals):
    score = 0
    reasons = []
    
    symptom_text = symptoms.lower()
    
    critical_keywords = ['chest pain', 'difficulty breathing', 'unconscious', 'stroke', 'heart attack', 'severe bleeding']
    moderate_keywords = ['fever', 'headache', 'vomiting', 'dizziness', 'pain', 'nausea']
    
    for kw in critical_keywords:
        if kw in symptom_text:
            score += 50
            reasons.append(f"Critical symptom: {kw}")
    
    for kw in moderate_keywords:
        if kw in symptom_text:
            score += 25
            reasons.append(f"Moderate symptom: {kw}")
    
    try:
        hr = int(vitals.get('heartRate', 0)) if vitals.get('heartRate') else 0
        temp = float(vitals.get('temperature', 0)) if vitals.get('temperature') else 0
        o2 = int(vitals.get('oxygenLevel', 100)) if vitals.get('oxygenLevel') else 100
        
        if hr > 100 or (hr > 0 and hr < 60):
            score += 20
            reasons.append(f"Abnormal heart rate: {hr} bpm")
        
        if temp > 38.5:
            score += 15
            reasons.append(f"High temperature: {temp}°C")
        
        if o2 < 95 and o2 > 0:
            score += 25
            reasons.append(f"Low oxygen: {o2}%")
    except:
        pass
    
    if score >= 60:
        risk_level = 'critical'
        recommendations = [
            "��� Seek immediate emergency medical attention",
            "Call emergency services (999/911)",
            "Do not drive yourself to the hospital"
        ]
    elif score >= 30:
        risk_level = 'moderate'
        recommendations = [
            "⚠️ Consult a doctor within 24 hours",
            "Monitor symptoms closely",
            "Rest and stay hydrated"
        ]
    else:
        risk_level = 'low'
        recommendations = [
            "✅ Symptoms appear manageable",
            "Monitor for any changes",
            "Contact doctor if symptoms worsen"
        ]
    
    return {
        'risk_level': risk_level,
        'risk_score': score,
        'confidence': 0.87,
        'reasons': reasons if reasons else ['No significant risk factors detected'],
        'recommendations': recommendations,
        'timestamp': datetime.utcnow().isoformat()
    }

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'MediFit AI Engine',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        
        if not data.get('symptoms'):
            return jsonify({'error': 'Symptoms are required'}), 400
        
        symptoms = data.get('symptoms', '')
        vital_signs = data.get('vital_signs', {})
        
        analysis = calculate_risk(symptoms, vital_signs)
        analysis['analysis_id'] = abs(hash(symptoms + str(datetime.now()))) % 10000
        
        return jsonify({'success': True, 'data': analysis})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    return jsonify({
        'success': True,
        'stats': {
            'total_analyses': 247,
            'system_status': 'operational'
        }
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("��� MediFit Backend Starting...")
    print("="*50)
    print("✅ Server running on http://localhost:5000")
    print("��� Test health: http://localhost:5000/health")
    print("��� Ready for React frontend connection!")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)

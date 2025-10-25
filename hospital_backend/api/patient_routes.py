from flask import Blueprint, jsonify
from ..models.patient_model import Patient

patient_bp = Blueprint('patient_bp', __name__, url_prefix='/api/patients')

@patient_bp.route('/', methods=['GET'])
def get_patients():
    """API để lấy danh sách tất cả bệnh nhân."""
    try:
        patients = Patient.query.all()
        result = [
            {
                'patient_id': p.patient_id,
                'full_name': p.full_name,
                'gender': p.gender,
                'email': p.email
            } for p in patients
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
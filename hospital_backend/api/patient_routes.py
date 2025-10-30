from flask import Blueprint, jsonify, request, session
from ..models import db
from ..models.user_model import User
from ..models.patient_model import Patient
from ..api.decorators import login_required
from datetime import datetime

patient_bp = Blueprint('patient_bp', __name__, url_prefix='/api/patients')

@patient_bp.route('/', methods=['GET'])
def get_patients():
    """API để lấy danh sách tất cả bệnh nhân (có thể giới hạn cho Admin sau)."""
    try:
        patients = Patient.query.all()
        result = [
            {
                'patient_id': p.patient_id,
                'full_name': p.full_name,
                'gender': p.gender,
                'email': p.email,
                'user_id': p.user_id 
            } for p in patients
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Xem Chi tiết Bệnh nhân ---
@patient_bp.route('/<int:patient_id>', methods=['GET'])
@login_required 
def get_patient_details(patient_id):
    """API để lấy thông tin chi tiết của một bệnh nhân theo ID."""
    try:
        patient = Patient.query.get_or_404(patient_id)
        
        # Kiểm tra quyền: Chỉ admin hoặc chính bệnh nhân đó mới được xem
        user_session = session['user']
        current_user = User.query.get(user_session['id'])
        
        # Nếu người dùng không phải admin VÀ không phải là chính bệnh nhân đó
        if user_session['role'] != 'admin' and (not current_user.patient or current_user.patient.patient_id != patient_id):
             return jsonify({'message': 'Bạn không có quyền xem hồ sơ này'}), 403
             
        patient_details = {
            'patient_id': patient.patient_id,
            'full_name': patient.full_name,
            'gender': patient.gender,
            'date_of_birth': patient.date_of_birth.isoformat() if patient.date_of_birth else None,
            'phone': patient.phone,
            'email': patient.email,
            'user_id': patient.user_id
        }
        return jsonify(patient_details), 200
        
    except Exception as e:
        if "404 Not Found" in str(e):
             return jsonify({'message': 'Không tìm thấy bệnh nhân với ID này'}), 404
        return jsonify({'error': str(e)}), 500

# ---Cập nhật Hồ sơ Bệnh nhân ---
@patient_bp.route('/profile', methods=['PUT'])
@login_required
def update_patient_profile():
    """API cho bệnh nhân tự cập nhật thông tin cá nhân."""
    user_session = session['user']
    
    # Chỉ bệnh nhân mới được cập nhật hồ sơ của chính mình
    if user_session['role'] != 'patient':
        return jsonify({'message': 'Chỉ bệnh nhân mới có thể cập nhật hồ sơ'}), 403

    current_user = User.query.get(user_session['id'])
    if not current_user or not current_user.patient:
        return jsonify({'message': 'Không tìm thấy hồ sơ bệnh nhân tương ứng'}), 404
        
    patient_profile = current_user.patient
    data = request.get_json()
    
    try:
        patient_profile.full_name = data.get('full_name', patient_profile.full_name)
        patient_profile.gender = data.get('gender', patient_profile.gender)
        dob_str = data.get('date_of_birth')
        if dob_str:
            patient_profile.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
        patient_profile.phone = data.get('phone', patient_profile.phone)
        patient_profile.email = data.get('email', patient_profile.email)
        
        db.session.commit()
        return jsonify({'message': 'Cập nhật hồ sơ thành công!'}), 200
        
    except ValueError:
        return jsonify({'message': 'Sai định dạng ngày sinh. Sử dụng YYYY-MM-DD'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
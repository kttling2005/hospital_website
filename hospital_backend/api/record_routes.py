from flask import Blueprint, jsonify, request, session
from ..models import db
from ..models.user_model import User
from ..models.appointment_model import Appointment
from ..models.medical_record_model import MedicalRecord
from ..api.decorators import login_required, role_required

record_bp = Blueprint('record_bp', __name__, url_prefix='/api/records')

@record_bp.route('/', methods=['POST'])
@login_required
@role_required('doctor') # Chỉ bác sĩ mới được tạo kết quả
def create_medical_record():
    """API cho bác sĩ (đã đăng nhập) tạo kết quả khám cho một lịch hẹn."""
    user_session = session['user']
    data = request.get_json()
    
    # Kiểm tra dữ liệu đầu vào
    required_fields = ['appointment_id', 'diagnosis']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Thiếu appointment_id hoặc diagnosis'}), 400

    try:
        current_user = User.query.get(user_session['id'])
        if not current_user or not current_user.doctor:
            return jsonify({'message': 'Không tìm thấy hồ sơ bác sĩ'}), 404
        
        doctor_id = current_user.doctor.doctor_id
        
        # --- Kiểm tra tính hợp lệ ---
        appointment = Appointment.query.get(data['appointment_id'])
        if not appointment:
            return jsonify({'message': 'Không tìm thấy lịch hẹn'}), 404
            
        # Kiểm tra xem bác sĩ này có phải là người khám không
        if appointment.doctor_id != doctor_id:
            return jsonify({'message': 'Bạn không có quyền tạo kết quả cho lịch hẹn này'}), 403
            
        # Kiểm tra xem lịch hẹn này đã có kết quả chưa (vì là quan hệ 1-1)
        if appointment.medical_record:
            return jsonify({'message': 'Lịch hẹn này đã có kết quả khám rồi'}), 409
            
        # --- Tạo kết quả mới ---
        new_record = MedicalRecord(
            appointment_id=data['appointment_id'],
            doctor_id=doctor_id,
            patient_id=appointment.patient_id,
            diagnosis=data['diagnosis'],
            prescription=data.get('prescription'),
            notes=data.get('notes')
        )
        
        # Đánh dấu lịch hẹn là "Đã khám"
        appointment.status = 'Đã khám'
        
        db.session.add(new_record)
        # (Chúng ta không cần add(appointment) vì nó đã ở trong session)
        db.session.commit()
        
        return jsonify({'message': 'Tạo kết quả khám thành công!'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@record_bp.route('/', methods=['GET'])
@login_required # Cả bệnh nhân và bác sĩ đều có thể gọi
def get_my_records():
    """API cho bệnh nhân/bác sĩ xem danh sách kết quả khám của họ."""
    user_session = session['user']
    current_user = User.query.get(user_session['id'])
    
    query = MedicalRecord.query
    
    # Lọc theo vai trò
    if user_session['role'] == 'patient':
        if not current_user.patient: return jsonify([]), 200
        query = query.filter_by(patient_id=current_user.patient.patient_id)
        
    elif user_session['role'] == 'doctor':
        if not current_user.doctor: return jsonify([]), 200
        query = query.filter_by(doctor_id=current_user.doctor.doctor_id)
        
    # (Admin sẽ thấy tất cả)
    
    records = query.order_by(MedicalRecord.created_at.desc()).all()
    
    result_list = [
        {
            'record_id': r.id,
            'appointment_id': r.appointment_id,
            'doctor_id': r.doctor_id,
            'diagnosis': r.diagnosis, # Chỉ hiển thị tóm tắt
            'created_at': r.created_at.isoformat()
        } for r in records
    ]
    
    return jsonify(result_list), 200

@record_bp.route('/<int:record_id>', methods=['GET'])
@login_required
def get_record_details(record_id):
    """API lấy chi tiết một kết quả khám (của tôi)."""
    user_session = session['user']
    current_user = User.query.get(user_session['id'])
    
    record = MedicalRecord.query.get_or_404(record_id)
    
    # --- Kiểm tra quyền sở hữu ---
    is_admin = user_session['role'] == 'admin'
    is_patient_owner = False
    is_doctor_owner = False

    if user_session['role'] == 'patient' and current_user.patient:
        is_patient_owner = current_user.patient.patient_id == record.patient_id
        
    if user_session['role'] == 'doctor' and current_user.doctor:
        is_doctor_owner = current_user.doctor.doctor_id == record.doctor_id

    if not (is_admin or is_patient_owner or is_doctor_owner):
        return jsonify({'message': 'Bạn không có quyền xem kết quả này'}), 403
        
    # Trả về chi tiết đầy đủ
    return jsonify({
        'record_id': record.id,
        'appointment_id': record.appointment_id,
        'doctor_id': record.doctor_id,
        'patient_id': record.patient_id,
        'diagnosis': record.diagnosis,
        'prescription': record.prescription,
        'notes': record.notes,
        'created_at': record.created_at.isoformat()
    }), 200
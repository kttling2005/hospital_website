from flask import Blueprint, request, jsonify, session
from ..models import db
from ..models.user_model import User
from ..models.patient_model import Patient
from ..models.doctor_model import Doctor
from ..models.appointment_model import Appointment
from ..models.shift_model import Shift
from ..api.decorators import login_required
from datetime import datetime

appointment_bp = Blueprint('appointment_bp', __name__, url_prefix='/api/appointments')

# --- API TẠO LỊCH HẸN ---
@appointment_bp.route('/', methods=['POST'])
@login_required
def create_appointment():
    """API cho bệnh nhân (đã đăng nhập) đặt lịch hẹn trực tiếp với bác sĩ."""
    user_session = session['user']
    if user_session['role'] != 'patient':
        return jsonify({'message': 'Chỉ bệnh nhân mới có thể đặt lịch hẹn'}), 403

    data = request.get_json()
    if not data or not data.get('doctor_id') or not data.get('appointment_date'):
        return jsonify({'message': 'Thiếu doctor_id hoặc appointment_date'}), 400

    try:
        current_user = User.query.get(user_session['id'])
        if not current_user or not current_user.patient:
            return jsonify({'message': 'Không tìm thấy hồ sơ bệnh nhân'}), 404
        
        patient_id = current_user.patient.patient_id
        doctor_id = data['doctor_id']
        appointment_dt = datetime.fromisoformat(data['appointment_date'])

        shift = Shift.query.filter(
            Shift.doctor_id == doctor_id,
            Shift.shift_date == appointment_dt.date(),
            Shift.start_time <= appointment_dt.time(),
            Shift.end_time > appointment_dt.time()
        ).first()
        
        if not shift:
            return jsonify({'message': 'Bác sĩ không có ca làm việc vào thời điểm này'}), 409

        existing_appointment = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=appointment_dt
        ).first()
        
        if existing_appointment:
            return jsonify({'message': 'Khung giờ này đã có người đặt. Vui lòng chọn giờ khác'}), 409
        
        new_appointment = Appointment(
            doctor_id=doctor_id,
            patient_id=patient_id,  
            appointment_date=appointment_dt,
            reason=data.get('reason', ''),
            status='Đã đặt' 
        )
        db.session.add(new_appointment)
        db.session.commit()

        return jsonify({'message': 'Đặt lịch hẹn thành công!'}), 201

    except ValueError:
        return jsonify({'message': 'Định dạng ngày giờ không hợp lệ (VD: YYYY-MM-DDTHH:MM:SS)'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# --- API XEM LỊCH HẸN ---
@appointment_bp.route('/', methods=['GET'])
@login_required
def get_appointments():
    user_session = session['user']
    current_user = User.query.get(user_session['id'])
    
    if not current_user:
        return jsonify({'message': 'Đăng nhập không hợp lệ'}), 401
    
    query = db.session.query(Appointment).join(Doctor).join(Patient)

    if user_session['role'] == 'patient':
        if current_user.patient:
             query = query.filter(Appointment.patient_id == current_user.patient.patient_id)
        else:
            return jsonify([]), 200 
    elif user_session['role'] == 'doctor':
        if current_user.doctor:
            query = query.filter(Appointment.doctor_id == current_user.doctor.doctor_id)
        else:
            return jsonify([]), 200
    
    appointments = query.order_by(Appointment.appointment_date.asc()).all()
    
    appointments_list = [
        {
            'appointment_id': a.appointment_id,
            'doctor_id': a.doctor_id,
            'doctor_name': a.doctor.full_name, 
            'patient_id': a.patient_id,
            'patient_name': a.patient.full_name,
            'appointment_date': a.appointment_date.isoformat(),
            'status': a.status, 
            'reason': a.reason,
            'notes': a.notes
        } for a in appointments
    ]
    
    return jsonify(appointments_list), 200

# --- API HỦY LỊCH HẸN ---
@appointment_bp.route('/<int:appointment_id>/cancel', methods=['PUT'])
@login_required 
def cancel_appointment(appointment_id):
    user_session = session['user']
    current_user = User.query.get(user_session['id'])
    if not current_user: return jsonify({'message': 'Phiên đăng nhập không hợp lệ'}), 401
    
    appointment = Appointment.query.get_or_404(appointment_id)
    can_cancel = False
    if user_session['role'] == 'admin': can_cancel = True
    elif user_session['role'] == 'patient':
        if current_user.patient and current_user.patient.patient_id == appointment.patient_id: can_cancel = True
    elif user_session['role'] == 'doctor':
        if current_user.doctor and current_user.doctor.doctor_id == appointment.doctor_id: can_cancel = True
    if not can_cancel: return jsonify({'message': 'Bạn không có quyền hủy lịch hẹn này'}), 403
    
    if appointment.status == 'Hủy':
         return jsonify({'message': 'Lịch hẹn này đã được hủy trước đó'}), 400
    if appointment.status == 'Đã khám':
        return jsonify({'message': 'Không thể hủy lịch hẹn đã hoàn thành'}), 400

    try:
        appointment.status = 'Hủy' 
        db.session.commit()
        return jsonify({'message': f'Đã hủy lịch hẹn {appointment_id}'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
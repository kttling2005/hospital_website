from flask import Blueprint, request, jsonify, session
from ..models import db
from ..models.appointment_model import Appointment
from ..models.shift_model import Shift
from ..api.decorators import login_required
from datetime import datetime

appointment_bp = Blueprint('appointment_bp', __name__, url_prefix='/api/appointments')

@appointment_bp.route('/', methods=['POST'])
@login_required
def create_appointment():
    user_session = session['user']
    if user_session['role'] != 'patient':
        return jsonify({'message': 'Chỉ bệnh nhân mới có thể đặt lịch hẹn'}), 403

    data = request.get_json()
    if not data or not data.get('doctor_id') or not data.get('appointment_date'):
        return jsonify({'message': 'Thiếu thông tin bác sĩ hoặc ngày hẹn'}), 400

    try:
    
        patient_id_from_session = user_session['id']

        appointment_dt = datetime.fromisoformat(data['appointment_date'])

        # Logic kiểm tra ca trực
        shift = Shift.query.filter(
            Shift.doctor_id == data['doctor_id'],
            Shift.shift_date == appointment_dt.date(),
            Shift.start_time <= appointment_dt.time(),
            Shift.end_time > appointment_dt.time()
        ).first()
        if not shift:
            return jsonify({'message': 'Bác sĩ không có lịch làm việc vào thời điểm này'}), 409

        # Logic kiểm tra trùng lịch
        existing_appointment = Appointment.query.filter_by(
            doctor_id=data['doctor_id'],
            appointment_date=appointment_dt
        ).first()
        if existing_appointment:
            return jsonify({'message': 'Khung giờ này đã có người đặt. Vui lòng chọn giờ khác'}), 409

        # Sử dụng patient_id không chính xác từ session
        new_appointment = Appointment(
            doctor_id=data['doctor_id'],
            patient_id=patient_id_from_session,
            appointment_date=appointment_dt,
            reason=data.get('reason', '')
        )
        db.session.add(new_appointment)
        db.session.commit()

        return jsonify({'message': 'Đặt lịch hẹn thành công!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@appointment_bp.route('/', methods=['GET'])
@login_required
def get_appointments():
    user = session['user']
    query = Appointment.query
    
    if user['role'] == 'patient':
         query = query.filter_by(patient_id=user['id'])
    elif user['role'] == 'doctor':
        pass
    
    appointments = query.all()
    
    appointments_list = [
        {
            'appointment_id': a.appointment_id,
            'doctor_id': a.doctor_id,
            'patient_id': a.patient_id,
            'appointment_date': a.appointment_date.isoformat(),
            'status': a.status,
            'reason': a.reason
        } for a in appointments
    ]
    
    return jsonify(appointments_list), 200
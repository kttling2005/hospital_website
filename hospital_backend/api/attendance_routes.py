from flask import Blueprint, jsonify, session
from ..models import db
from ..models.user_model import User
from ..models.attendance_model import Attendance
from ..api.decorators import login_required, role_required
from datetime import datetime, date

attendance_bp = Blueprint('attendance_bp', __name__, url_prefix='/api/attendance')

@attendance_bp.route('/checkin', methods=['POST'])
@login_required
@role_required('doctor') # Chỉ bác sĩ mới được chấm công
def check_in():
    """API cho bác sĩ check-in đầu ngày."""
    try:
        user_session = session['user']
        current_user = User.query.get(user_session['id'])
        
        # Kiểm tra xem có hồ sơ bác sĩ không
        if not current_user or not current_user.doctor:
            return jsonify({'message': 'Không tìm thấy hồ sơ bác sĩ'}), 404
            
        doctor_id = current_user.doctor.doctor_id
        
        # Kiểm tra xem bác sĩ đã check-in hôm nay chưa
        today = date.today()
        existing_record = Attendance.query.filter_by(
            doctor_id=doctor_id,
            date=today
        ).first()
        
        if existing_record:
            return jsonify({'message': 'Bạn đã check-in hôm nay rồi'}), 409

        # Tạo bản ghi chấm công mới
        new_attendance_record = Attendance(
            doctor_id=doctor_id,
            check_in_time=datetime.utcnow(),
            date=today
        )
        
        db.session.add(new_attendance_record)
        db.session.commit()
        
        return jsonify({
            'message': 'Check-in thành công!',
            'check_in_time': new_attendance_record.check_in_time.isoformat()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@attendance_bp.route('/checkout', methods=['PUT'])
@login_required
@role_required('doctor')
def check_out():
    """API cho bác sĩ check-out cuối ngày."""
    try:
        user_session = session['user']
        current_user = User.query.get(user_session['id'])
        
        if not current_user or not current_user.doctor:
            return jsonify({'message': 'Không tìm thấy hồ sơ bác sĩ'}), 404
            
        doctor_id = current_user.doctor.doctor_id
        today = date.today()
        
        # Tìm bản ghi check-in của hôm nay
        record_to_checkout = Attendance.query.filter_by(
            doctor_id=doctor_id,
            date=today
        ).first()
        
        if not record_to_checkout:
            return jsonify({'message': 'Bạn chưa check-in hôm nay'}), 404
            
        if record_to_checkout.check_out_time:
            return jsonify({'message': 'Bạn đã check-out hôm nay rồi'}), 409
            
        # Cập nhật thời gian check-out
        record_to_checkout.check_out_time = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Check-out thành công!',
            'check_out_time': record_to_checkout.check_out_time.isoformat()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
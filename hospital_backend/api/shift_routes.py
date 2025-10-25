from flask import Blueprint, request, jsonify
from ..models import db
from ..models.shift_model import Shift
from ..api.decorators import role_required
from datetime import date, time

shift_bp = Blueprint('shift_bp', __name__, url_prefix='/api/shifts')

@shift_bp.route('/', methods=['POST'])
@role_required('admin') # <-- Chỉ Admin mới có quyền tạo ca trực
def create_shift():
    """API cho Admin tạo một ca làm việc mới cho bác sĩ."""
    data = request.get_json()
    
    # Kiểm tra dữ liệu đầu vào
    required_fields = ['doctor_id', 'shift_date', 'start_time', 'end_time']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Thiếu thông tin cần thiết'}), 400

    try:
        # Chuyển đổi chuỗi thành đối tượng date và time
        shift_date_obj = date.fromisoformat(data['shift_date']) # format: "YYYY-MM-DD"
        start_time_obj = time.fromisoformat(data['start_time']) # format: "HH:MM:SS"
        end_time_obj = time.fromisoformat(data['end_time'])
        
        new_shift = Shift(
            doctor_id=data['doctor_id'],
            shift_date=shift_date_obj,
            start_time=start_time_obj,
            end_time=end_time_obj,
            room=data.get('room') # .get() để không bị lỗi nếu thiếu 'room'
        )
        
        db.session.add(new_shift)
        db.session.commit()
        
        return jsonify({'message': 'Tạo ca trực thành công!'}), 201

    except ValueError:
        return jsonify({'message': 'Sai định dạng ngày hoặc giờ. Sử dụng YYYY-MM-DD và HH:MM:SS'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@shift_bp.route('/', methods=['GET'])
def get_shifts():
    """API để xem danh sách các ca trực, có thể lọc theo doctor_id."""
    doctor_id = request.args.get('doctor_id') 
    
    query = Shift.query
    if doctor_id:
        query = query.filter_by(doctor_id=doctor_id)
        
    shifts = query.all()
    
    shifts_list = [
        {
            'shift_id': s.shift_id,
            'doctor_id': s.doctor_id,
            'shift_date': s.shift_date.isoformat(),
            'start_time': s.start_time.isoformat(),
            'end_time': s.end_time.isoformat(),
            'room': s.room
        } for s in shifts
    ]
    
    return jsonify(shifts_list), 200

@shift_bp.route('/<int:shift_id>', methods=['DELETE'])
@role_required('admin') # <-- Chỉ Admin mới có quyền xóa ca trực
def delete_shift(shift_id):
    """API cho Admin xóa một ca trực."""
    shift = Shift.query.get_or_404(shift_id)
    
    db.session.delete(shift)
    db.session.commit()
    
    return jsonify({'message': 'Xóa ca trực thành công'}), 200
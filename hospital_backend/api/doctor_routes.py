from flask import Blueprint, jsonify
from ..models.doctor_model import Doctor

doctor_bp = Blueprint('doctor_bp', __name__, url_prefix='/api/doctors')

@doctor_bp.route('/', methods=['GET'])
def get_all_doctors():
    """
    API để lấy danh sách tất cả các bác sĩ.
    Bất kỳ ai cũng có thể gọi API này.
    """
    try:
        # Truy vấn tất cả bác sĩ từ database
        doctors = Doctor.query.all()

        # Chuyển đổi danh sách đối tượng Doctor thành danh sách dictionary
        doctors_list = [
            {
                'doctor_id': doc.doctor_id,
                'full_name': doc.full_name,
                'gender': doc.gender,
                'specialization': doc.specialization,
                'email': doc.email,
                'phone': doc.phone
            }
            for doc in doctors
        ]
        
        return jsonify(doctors_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@doctor_bp.route('/<int:doctor_id>', methods=['GET'])
def get_doctor_by_id(doctor_id):
    """
    API để lấy thông tin chi tiết của một bác sĩ theo ID.
    """
    try:
        # Tìm bác sĩ theo ID, nếu không thấy sẽ tự động báo lỗi 404 Not Found
        doctor = Doctor.query.get_or_404(doctor_id)

        doctor_details = {
            'doctor_id': doctor.doctor_id,
            'full_name': doctor.full_name,
            'gender': doctor.gender,
            'phone': doctor.phone,
            'email': doctor.email,
            'specialization': doctor.specialization
        }

        return jsonify(doctor_details), 200
    except Exception as e:
        if "404 Not Found" in str(e):
            return jsonify({'message': 'Không tìm thấy bác sĩ với ID này'}), 404
        return jsonify({'error': str(e)}), 500
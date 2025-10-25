from flask import Blueprint, request, jsonify
from .decorators import role_required
from ..models.user_model import User, UserRole
from ..models.doctor_model import Doctor
from ..models import db

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/api/admin')


@admin_bp.route('/create_doctor_account', methods=['POST'])
@role_required('admin')
def create_doctor_account():
    """API cho Admin tạo tài khoản đăng nhập cho một bác sĩ đã có hồ sơ."""
    data = request.get_json()
    required = ['username', 'password', 'doctor_id']
    if not all(field in data for field in required):
        return jsonify({'message': 'Thiếu username, password, hoặc doctor_id'}), 400

    doctor_profile = Doctor.query.get(data['doctor_id'])
    if not doctor_profile:
        return jsonify({'message': f"Không tìm thấy bác sĩ với ID {data['doctor_id']}"}), 404

    if doctor_profile.user_id:
        return jsonify({'message': 'Bác sĩ này đã có tài khoản rồi'}), 409

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Tên tài khoản đã tồn tại'}), 409

    new_doctor_user = User(username=data['username'], role=UserRole.DOCTOR)
    new_doctor_user.set_password(data['password'])

    doctor_profile.user = new_doctor_user

    db.session.add(new_doctor_user)
    db.session.commit()

    return jsonify({'message': f"Đã tạo tài khoản cho bác sĩ '{doctor_profile.full_name}' thành công!"}), 201


@admin_bp.route('/create_doctor', methods=['POST'])
@role_required('admin')
def create_doctor():
    """
    API cho Admin tạo một hồ sơ Bác sĩ VÀ tài khoản đăng nhập mới
    cùng một lúc.
    """
    data = request.get_json()

    # 1. Kiểm tra thông tin đầu vào
    required_fields = ['username', 'password', 'full_name', 'gender', 'specialization']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Thiếu thông tin: username, password, full_name, gender, hoặc specialization'}), 400

    # 2. Kiểm tra tài khoản đã tồn tại chưa
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Tên tài khoản đã tồn tại'}), 409

    try:
        # 3. Tạo tài khoản User mới
        new_user = User(
            username=data['username'],
            role=UserRole.DOCTOR
        )
        new_user.set_password(data['password'])

        # 4. Tạo hồ sơ Doctor mới và liên kết trực tiếp với User
        new_doctor_profile = Doctor(
            full_name=data['full_name'],
            gender=data['gender'],
            specialization=data.get('specialization'),
            email=data.get('email'),
            phone=data.get('phone'),
            user=new_user
        )

        db.session.add(new_user)
        db.session.add(new_doctor_profile)
        db.session.commit()

        return jsonify({
            'message': 'Tạo tài khoản và hồ sơ bác sĩ mới thành công!',
            'doctor_id': new_doctor_profile.doctor_id,
            'user_id': new_user.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
from flask import Blueprint, request, jsonify, session
from ..models import db
from ..models.user_model import User, UserRole
from ..models.patient_model import Patient
from ..models.doctor_model import Doctor

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register_patient():
    """API để đăng ký, tự động tạo cả User và Patient profile."""
    data = request.get_json()
    required_fields = ['username', 'password', 'full_name', 'gender']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Thiếu thông tin username, password, full_name hoặc gender'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Tên tài khoản đã tồn tại'}), 409

    try:
        # 1. Tạo tài khoản User mới
        new_user = User(username=data['username'], role=UserRole.PATIENT)
        new_user.set_password(data['password'])

        # 2. Tạo hồ sơ Patient mới và liên kết trực tiếp với User
        new_patient_profile = Patient(
            full_name=data['full_name'],
            gender=data['gender'],
            email=data.get('email'),
            phone=data.get('phone'),
            user=new_user  
        )

        db.session.add(new_user)
        db.session.add(new_patient_profile)
        db.session.commit()

        return jsonify({'message': 'Đăng ký tài khoản bệnh nhân thành công!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Thiếu tên đăng nhập hoặc mật khẩu'}), 400

    user = User.query.filter_by(username=data['username']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Sai tên đăng nhập hoặc mật khẩu'}), 401

    session['user'] = {
        'id': user.id,
        'username': user.username,
        'role': user.role.value
    }
    return jsonify({'message': 'Đăng nhập thành công!', 'user': session['user']}), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Đăng xuất thành công!'}), 200

@auth_bp.route('/me', methods=['GET'])
def me():
    """API trả về thông tin user đang đăng nhập dựa trên session."""
    user_session = session.get('user')
    if not user_session:
        return jsonify({'message': 'Chưa đăng nhập hoặc phiên đã hết hạn'}), 401

    # Lấy thông tin user từ database để có dữ liệu đầy đủ
    user = User.query.get(user_session['id'])
    if not user:
        return jsonify({'message': 'Người dùng không tồn tại'}), 404
    doctor_id = None  # khởi tạo trước
    patient_info = None
    # Nếu là bác sĩ → tìm doctor_id
    if user.role == UserRole.DOCTOR:
        doctor = Doctor.query.filter_by(user_id=user.id).first()
        if doctor:
            doctor_id = doctor.doctor_id
            full_name = doctor.full_name

    # Nếu user là bệnh nhân, có thể lấy thêm thông tin Patient
    if user.role == UserRole.PATIENT:
        patient = Patient.query.filter_by(user_id=user.id).first()
        if patient:
            patient_info = {
                'full_name': patient.full_name,
                'gender': patient.gender,
                'email': patient.email,
                'phone': patient.phone
            }
            full_name = patient.full_name

    return jsonify({
        'id': user.id,
        'username': user.username,
        'role': user.role.value,
        'patient_info': patient_info,
        'full_name': full_name,
        'doctor_id': doctor_id
    }), 200

from flask import Blueprint, request, jsonify, session
from ..models import db
from ..models.user_model import User, UserRole

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register_patient():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Thiếu tên đăng nhập hoặc mật khẩu'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Tên tài khoản đã tồn tại'}), 409

    new_user = User(username=data['username'], role=UserRole.PATIENT)
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    # Làm mới session để xóa cache object vừa add
    db.session.expire_all()

    return jsonify({'message': 'Đăng ký tài khoản thành công!'}), 201

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

from flask import Blueprint, request, jsonify, session
from ..models import db
from ..models.user_model import User, UserRole
from ..models.doctor_model import Doctor   # 👈 Thêm dòng này
from ..models.patient_model import Patient # 👈 Và dòng này

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Trả về thông tin người dùng hiện đang đăng nhập (dựa trên session)."""
    user = session.get('user')
    if not user:
        return jsonify({'message': 'Chưa đăng nhập'}), 401

    doctor_id = None
    patient_id = None

    # Nếu là bác sĩ → tìm doctor_id
    if user.get('role') == 'doctor':
        doctor = Doctor.query.filter_by(user_id=user['id']).first()
        if doctor:
            doctor_id = doctor.doctor_id

    # Nếu là bệnh nhân → tìm patient_id
    elif user.get('role') == 'patient':
        patient = Patient.query.filter_by(user_id=user['id']).first()
        if patient:
            patient_id = patient.patient_id

    return jsonify({
        'id': user.get('id'),
        'username': user.get('username'),
        'role': user.get('role'),
        'doctor_id': doctor_id,
        'patient_id': patient_id
    }), 200
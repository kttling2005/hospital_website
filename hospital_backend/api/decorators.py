from functools import wraps
from flask import session, jsonify

def login_required(f):
    """
    Decorator kiểm tra xem người dùng đã đăng nhập hay chưa.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'message': 'Yêu cầu đăng nhập để thực hiện hành động này'}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    """
    Decorator kiểm tra vai trò cụ thể của người dùng.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                return jsonify({'message': 'Yêu cầu đăng nhập để truy cập'}), 401

            user_role = session['user'].get('role')
            if not user_role or user_role != required_role:
                return jsonify({'message': 'Bạn không có quyền thực hiện hành động này'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
from ..app import create_app, db
from ..models.user_model import User, UserRole
from getpass import getpass  

app = create_app()

with app.app_context():
    # 1. Kiểm tra xem admin đã tồn tại chưa
    username = 'admin'
    if User.query.filter_by(username=username).first():
        print(f"Tài khoản '{username}' đã tồn tại.")
    else:
        # 2. Nếu chưa, yêu cầu người dùng nhập mật khẩu
        print(f"Tạo tài khoản quản trị viên: '{username}'")
        password = getpass("Nhập mật khẩu cho admin: ")
        
        # 3. Tạo người dùng mới
        admin_user = User(
            username=username,
            role=UserRole.ADMIN  # Gán vai trò là admin
        )
        admin_user.set_password(password)  # Mã hóa mật khẩu
        
        # 4. Lưu vào database
        db.session.add(admin_user)
        db.session.commit()
        
        print(f"✅ Đã tạo tài khoản '{username}' thành công!")
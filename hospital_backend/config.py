import os

class Config:
    """
    Lớp cấu hình trung tâm cho ứng dụng Flask.
    Chứa tất cả các biến cài đặt và thông số quan trọng.
    """

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-super-secret-key-that-no-one-can-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:555555@localhost/hospital_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
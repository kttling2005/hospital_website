from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import enum

class UserRole(str,enum.Enum):
    ADMIN = 'admin'
    DOCTOR = 'doctor'
    PATIENT = 'patient'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.PATIENT)
    patient = db.relationship('Patient', backref='user', uselist=False, cascade="all, delete-orphan")
    doctor = db.relationship('Doctor', backref='user', uselist=False, cascade="all, delete-orphan")
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
from . import db

class Doctor(db.Model):
    __tablename__ = 'doctors'
    doctor_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum('Nam', 'Nữ', 'Khác'), nullable=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100), unique=True)
    specialization = db.Column(db.String(100))
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    shifts = db.relationship('Shift', backref='doctor', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=True)
    user = db.relationship('User', back_populates='doctor_profile', uselist=False)
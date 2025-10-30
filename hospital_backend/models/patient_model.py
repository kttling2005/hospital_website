from . import db

class Patient(db.Model):
    __tablename__ = 'patients'
    patient_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum('Nam', 'Nữ', 'Khác'), nullable=False)
    date_of_birth = db.Column(db.Date)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100), unique=True)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False,unique=True)
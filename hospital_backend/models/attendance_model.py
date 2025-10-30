from . import db
from datetime import datetime

class Attendance(db.Model):
    __tablename__ = 'attendance_records'
    
    id = db.Column(db.Integer, primary_key=True)
    
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), nullable=False)
    check_in_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    check_out_time = db.Column(db.DateTime, nullable=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())

    def __repr__(self):
        return f'<Attendance {self.doctor_id} @ {self.check_in_time}>'
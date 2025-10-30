from . import db
from datetime import datetime

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    
    id = db.Column(db.Integer, primary_key=True)
    
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.appointment_id'), unique=True, nullable=False)
    
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    
    diagnosis = db.Column(db.Text, nullable=False) 
    prescription = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True) 
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    appointment = db.relationship('Appointment', backref=db.backref('medical_record', uselist=False))

    def __repr__(self):
        return f'<MedicalRecord for Appointment {self.appointment_id}>'
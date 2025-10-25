from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from .user_model import User
from .patient_model import Patient
from .doctor_model import Doctor
from .appointment_model import Appointment
from .shift_model import Shift
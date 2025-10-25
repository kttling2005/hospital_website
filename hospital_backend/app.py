from flask import Flask
from .config import Config
from .models import db
from flask_cors import CORS
from .api.auth_routes import auth_bp

from .api.auth_routes import auth_bp
from .api.admin_routes import admin_bp
from .api.patient_routes import patient_bp
from .api.doctor_routes import doctor_bp
from .api.shift_routes import shift_bp
from .api.appointment_routes import appointment_bp
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    # ✅ Bật CORS cho toàn bộ API
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)  
    app.register_blueprint(shift_bp)
    app.register_blueprint(appointment_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    for rule in app.url_map.iter_rules():
        print(rule)
    app.run(debug=True)
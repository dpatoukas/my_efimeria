from flask import Flask
from flask_jwt_extended import JWTManager
import logging
from flask_cors import CORS

# Import blueprints
from api.schedule_routes import schedule_blueprint
from api.auth_routes import auth_blueprint
from api.doctor_routes import doctor_blueprint  # Added doctor routes

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Application factory function
def create_app():
    """
    Creates and configures the Flask application.
    """
    app = Flask(__name__)

    # Configure application settings
    app.config['JWT_SECRET_KEY'] = 'supersecretkey'

    # Enable CORS
    CORS(app)

    # Initialize JWT for authentication
    JWTManager(app)

    # Register blueprints for routes
    app.register_blueprint(schedule_blueprint, url_prefix='/api/schedules')
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    app.register_blueprint(doctor_blueprint, url_prefix='/api/doctors')  # Added doctor blueprint

    logging.info("Flask application initialized successfully.")

    return app
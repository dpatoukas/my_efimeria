from flask import Flask
from flask_jwt_extended import JWTManager
import logging
from flask_cors import CORS
from flask import Flask, request
# Import blueprints
from api.schedule_routes import schedule_blueprint
from api.auth_routes import auth_blueprint
from api.doctor_routes import doctor_blueprint
from api.shift_routes import shift_blueprint  # Added shift routes

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    app.register_blueprint(doctor_blueprint, url_prefix='/api/doctors')
    app.register_blueprint(shift_blueprint, url_prefix='/api/shifts')  # Added shift blueprint

    logging.info("Flask application initialized successfully.")

        # Log all incoming requests
    @app.before_request
    def log_request_info():
        """
        Logs incoming request details.
        """
        try:
            logging.info(f"Request: {request.method} {request.url}")
            if request.is_json:  # Check if JSON data is present
                logging.info(f"Request Body: {request.json}")
        except Exception as e:
            logging.error(f"Error logging request info: {str(e)}")


    # Log responses
    @app.after_request
    def log_response_info(response):
        logging.info(f"Response: {response.status} {response.data[:200]}")
        return response

    return app

from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import logging
from flasgger import Swagger
from swagger_config import setup_swagger  # Import Swagger setup

# Import blueprints
from api.schedule_routes import schedule_blueprint
from api.auth_routes import auth_blueprint
from api.doctor_routes import doctor_blueprint
from api.shift_routes import shift_blueprint

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Application factory function
def create_app():
    """
    Creates and configures the Flask application.
    """
    # Initialize Flask App
    app = Flask(__name__)

    # Configure application settings
    app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Replace with environment variable in production!

    # Enable CORS
    CORS(app)

    # Initialize JWT for authentication
    JWTManager(app)

    # Setup Swagger
    swagger = setup_swagger(app)  # Initialize Swagger UI

    # Register blueprints for routes
    app.register_blueprint(schedule_blueprint, url_prefix='/api/schedules')
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    app.register_blueprint(doctor_blueprint, url_prefix='/api/doctors')
    app.register_blueprint(shift_blueprint, url_prefix='/api/shifts')

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
        """
        Logs outgoing responses, ensuring passthrough responses are handled.
        """
        try:
            # Skip logging for streamed or passthrough responses
            if response.direct_passthrough:
                logging.info(f"Response: {response.status} [Streamed/Passthrough Response]")
            else:
                # Log up to 200 characters of the response body
                logging.info(f"Response: {response.status} {response.get_data(as_text=True)[:200]}")
        except Exception as e:
            logging.error(f"Error logging response info: {str(e)}")
        return response

    return app

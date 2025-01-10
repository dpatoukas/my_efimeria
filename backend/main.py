from api import create_app
from config.logging_config import setup_logging

# Create Flask application instance
app = create_app()

# Run the Flask application
if __name__ == "__main__":
    setup_logging()
    app.run(debug=True)

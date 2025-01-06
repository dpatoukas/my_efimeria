from flasgger import Swagger

swagger_template = {
    "swagger": "2.0",  # Correct Swagger version
    "info": {
        "title": "Clinic Scheduling API",
        "description": "API documentation for managing doctor schedules and shifts.",
        "version": "1.0.0"
    },
    "basePath": "/",  # Base path for all endpoints
    "schemes": ["http"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter: Bearer <JWT_TOKEN>"
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}

def setup_swagger(app):
    """
    Initializes Swagger for the Flask app.
    """
    swagger = Swagger(app, template=swagger_template, config={
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',  # Ensure endpoint name is correct
                "route": '/apispec.json',  # Path to JSON spec file
                "rule_filter": lambda rule: True,  # Include all routes
                "model_filter": lambda tag: True   # Include all models
            }
        ],
        "static_url_path": "/flasgger_static",  # Serve static files properly
        "swagger_ui": True,
        "specs_route": "/api/docs"  # Path for Swagger UI
    })
    return swagger

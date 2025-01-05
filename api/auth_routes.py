from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import logging

# Create blueprint for authentication routes
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    """
    Login endpoint to authenticate user and generate JWT token.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Hardcoded authentication (Replace with secure validation later)
    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity='admin')
        logging.info("Admin logged in successfully.")
        return jsonify(access_token=access_token)

    logging.warning("Failed login attempt.")
    return jsonify({'msg': 'Invalid credentials'}), 401
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database.database_setup import Session as DBSession
from services.doctor_service import DoctorService
from flask_jwt_extended import jwt_required
from flasgger import swag_from

# Create a blueprint for doctor routes
doctor_blueprint = Blueprint('doctor', __name__)


@doctor_blueprint.route('/', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Doctors'],
    'summary': 'Get all doctors',
    'description': 'Retrieve a list of all doctors with their details.',
    'responses': {
        200: {
            'description': 'List of doctors',
            'examples': {
                'application/json': [
                    {'id': 1, 'name': 'Dr. Brown', 'days_off': '2025-01-01,2025-01-02'},
                    {'id': 2, 'name': 'Dr. Smith', 'days_off': '2025-01-03,2025-01-04'}
                ]
            }
        },
        400: {'description': 'Bad request'}
    }
})
def get_doctors():
    session: Session = DBSession()
    try:
        doctors = DoctorService.get_all_doctors(session)
        return jsonify([{'id': d.id, 'name': d.name, 'days_off': d.days_off} for d in doctors])
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()


@doctor_blueprint.route('/<int:doctor_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Doctors'],
    'summary': 'Get a specific doctor',
    'description': 'Retrieve details of a specific doctor by their ID.',
    'parameters': [
        {
            'name': 'doctor_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'Doctor ID'
        }
    ],
    'responses': {
        200: {
            'description': 'Doctor details',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'days_off': {'type': 'string'},
                    'shifts': {'type': 'array'}
                }
            }
        },
        404: {'description': 'Doctor not found'}
    }
})
def get_doctor(doctor_id):
    session: Session = DBSession()
    try:
        doctor = DoctorService.get_doctor_by_id(session, doctor_id)
        return jsonify({
            'id': doctor['doctor'].id,
            'name': doctor['doctor'].name,
            'days_off': doctor['doctor'].days_off,
            'shifts': [{'id': s.id, 'date': s.date, 'status': s.status} for s in doctor['shifts']]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 404
    finally:
        session.close()


@doctor_blueprint.route('/', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Doctors'],
    'summary': 'Create a new doctor',
    'description': 'Add a new doctor with their details.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'days_off': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Doctor created successfully'},
        400: {'description': 'Bad request'}
    }
})
def create_doctor():
    session: Session = DBSession()
    try:
        data = request.json
        doctor = DoctorService.create_doctor(session, data['name'], data['days_off'])
        return jsonify({'id': doctor.id, 'name': doctor.name, 'days_off': doctor.days_off}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()


@doctor_blueprint.route('/<int:doctor_id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Doctors'],
    'summary': 'Update a doctor',
    'description': 'Modify an existing doctor’s details.',
    'parameters': [
        {
            'name': 'doctor_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'Doctor ID'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'days_off': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Doctor updated successfully'},
        400: {'description': 'Bad request'}
    }
})
def update_doctor(doctor_id):
    session: Session = DBSession()
    try:
        data = request.json
        doctor = DoctorService.update_doctor(
            session,
            doctor_id,
            data.get('name'),
            data.get('days_off')
        )
        return jsonify({'id': doctor.id, 'name': doctor.name, 'days_off': doctor.days_off})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()


@doctor_blueprint.route('/<int:doctor_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['Doctors'],
    'summary': 'Delete a doctor',
    'description': 'Remove a doctor from the system.',
    'parameters': [
        {
            'name': 'doctor_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'Doctor ID'
        }
    ],
    'responses': {
        200: {'description': 'Doctor deleted successfully'},
        400: {'description': 'Bad request'}
    }
})
def delete_doctor(doctor_id):
    session: Session = DBSession()
    try:
        DoctorService.delete_doctor(session, doctor_id)
        return jsonify({'message': 'Doctor deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

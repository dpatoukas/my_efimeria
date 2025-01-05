from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database.database_setup import Session as DBSession
from services.doctor_service import DoctorService
from flask_jwt_extended import jwt_required

# Create a blueprint for doctor routes
doctor_blueprint = Blueprint('doctor', __name__)


@doctor_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_doctors():
    """
    Retrieve all doctors.

    Returns:
        JSON response with a list of doctors or an error message.
    """
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
def get_doctor(doctor_id):
    """
    Retrieve a specific doctor by ID.

    Args:
        doctor_id (int): Doctor ID.

    Returns:
        JSON response with doctor details or an error message.
    """
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
def create_doctor():
    """
    Add a new doctor.

    Request Body:
        - name (str): Name of the doctor.
        - days_off (str): Comma-separated days off.

    Returns:
        JSON response with the created doctor or an error message.
    """
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
def update_doctor(doctor_id):
    """
    Update an existing doctor's details.

    Args:
        doctor_id (int): Doctor ID.

    Request Body:
        - name (str, optional): Updated name of the doctor.
        - days_off (str, optional): Updated days off.

    Returns:
        JSON response with updated doctor details or an error message.
    """
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
def delete_doctor(doctor_id):
    """
    Delete a doctor by ID.

    Args:
        doctor_id (int): Doctor ID.

    Returns:
        JSON response indicating success or failure.
    """
    session: Session = DBSession()
    try:
        DoctorService.delete_doctor(session, doctor_id)
        return jsonify({'message': 'Doctor deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

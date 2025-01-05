from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import Session
from database.database_setup import Session as DBSession
from services.shift_service import ShiftService
import logging

# Create a blueprint for shift routes
shift_blueprint = Blueprint('shift', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)


@shift_blueprint.route('', methods=['GET'])
@jwt_required()
def get_shifts_by_schedule():
    """
    Retrieve shifts for a specific schedule.

    Query Parameters:
        schedule_id (int): ID of the schedule.

    Returns:
        JSON response with a list of shifts or an error message.
    """
    session: Session = DBSession()
    try:
        # Extract query parameter
        schedule_id = request.args.get('schedule_id')
        if not schedule_id:
            raise ValueError("Schedule ID is required.")

        # Retrieve shifts
        shifts = ShiftService.get_shifts_by_schedule(session, int(schedule_id))
        result = [{'id': s.id, 'doctor_id': s.doctor_id, 'date': s.date, 'status': s.status} for s in shifts]

        logging.info(f"Retrieved {len(result)} shifts for schedule ID {schedule_id}.")
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Error retrieving shifts: {str(e)}")
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()


@shift_blueprint.route('', methods=['POST'])
@jwt_required()
def create_shift():
    """
    Assign a new shift.

    Request Body:
        - schedule_id (int): ID of the schedule.
        - doctor_id (int): ID of the doctor.
        - date (str): Date of the shift.

    Returns:
        JSON response with the created shift or an error message.
    """
    session: Session = DBSession()
    try:
        data = request.json
        schedule_id = data.get('schedule_id')
        doctor_id = data.get('doctor_id')
        date = data.get('date')

        # Create shift
        shift = ShiftService.create_shift(session, schedule_id, doctor_id, date)
        logging.info(f"Shift created: {shift.id}")
        return jsonify({'id': shift.id, 'doctor_id': shift.doctor_id, 'date': shift.date, 'status': shift.status}), 201
    except Exception as e:
        logging.error(f"Error creating shift: {str(e)}")
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()


@shift_blueprint.route('/<int:shift_id>', methods=['PUT'])
@jwt_required()
def update_shift(shift_id):
    """
    Update an existing shift.

    URL Parameter:
        - shift_id (int): ID of the shift.

    Request Body:
        - doctor_id (int): Updated doctor ID.
        - date (str): Updated date.

    Returns:
        JSON response with the updated shift or an error message.
    """
    session: Session = DBSession()
    try:
        data = request.json
        doctor_id = data.get('doctor_id')
        date = data.get('date')

        # Update shift
        shift = ShiftService.update_shift(session, shift_id, doctor_id, date)
        logging.info(f"Shift updated: {shift.id}")
        return jsonify({'id': shift.id, 'doctor_id': shift.doctor_id, 'date': shift.date, 'status': shift.status}), 200
    except Exception as e:
        logging.error(f"Error updating shift: {str(e)}")
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()


@shift_blueprint.route('/<int:shift_id>', methods=['DELETE'])
@jwt_required()
def delete_shift(shift_id):
    """
    Remove a shift from a schedule.

    URL Parameter:
        - shift_id (int): ID of the shift to delete.

    Returns:
        JSON response indicating success or error.
    """
    session: Session = DBSession()
    try:
        # Delete shift
        ShiftService.delete_shift(session, shift_id)
        logging.info(f"Shift deleted: {shift_id}")
        return jsonify({'message': 'Shift deleted successfully'}), 200
    except Exception as e:
        logging.error(f"Error deleting shift: {str(e)}")
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

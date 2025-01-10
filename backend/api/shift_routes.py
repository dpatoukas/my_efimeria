from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import Session
from database.database_setup import Session as DBSession
from services.shift_service import ShiftService
from flasgger import swag_from
import logging

# Create a blueprint for shift routes
shift_blueprint = Blueprint('shift', __name__)

# Configure logging
logging.basicConfig(level=logging.WARNING)


@shift_blueprint.route('', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Shifts'],
    'summary': 'Get shifts by schedule',
    'description': 'Retrieve all shifts associated with a specific schedule.',
    'parameters': [
        {
            'name': 'schedule_id',
            'in': 'query',
            'required': True,
            'type': 'integer',
            'description': 'ID of the schedule to fetch shifts for.'
        }
    ],
    'responses': {
        200: {
            'description': 'List of shifts retrieved successfully',
            'examples': {
                'application/json': [
                    {'id': 1, 'doctor_id': 1, 'date': '2025-01-06', 'status': 'Assigned'},
                    {'id': 2, 'doctor_id': 2, 'date': '2025-01-07', 'status': 'Assigned'}
                ]
            }
        },
        400: {'description': 'Bad request'}
    }
})
def get_shifts_by_schedule():
    session: Session = DBSession()
    try:
        schedule_id = request.args.get('schedule_id')
        if not schedule_id:
            raise ValueError("Schedule ID is required.")

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
@swag_from({
    'tags': ['Shifts'],
    'summary': 'Create a new shift',
    'description': 'Assign a new shift to a doctor for a specific schedule and date.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'schedule_id': {'type': 'integer'},
                    'doctor_id': {'type': 'integer'},
                    'date': {'type': 'string'}
                },
                'required': ['schedule_id', 'doctor_id', 'date']
            }
        }
    ],
    'responses': {
        201: {'description': 'Shift created successfully'},
        400: {'description': 'Bad request'}
    }
})
def create_shift():
    session: Session = DBSession()
    try:
        data = request.json
        schedule_id = data.get('schedule_id')
        doctor_id = data.get('doctor_id')
        date = data.get('date')

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
@swag_from({
    'tags': ['Shifts'],
    'summary': 'Update an existing shift',
    'description': 'Update the details of a shift including doctor assignment or date.',
    'parameters': [
        {
            'name': 'shift_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the shift to update.'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'doctor_id': {'type': 'integer'},
                    'date': {'type': 'string'}
                },
                'required': ['doctor_id', 'date']
            }
        }
    ],
    'responses': {
        200: {'description': 'Shift updated successfully'},
        400: {'description': 'Bad request'}
    }
})
def update_shift(shift_id):
    session: Session = DBSession()
    try:
        data = request.json
        doctor_id = data.get('doctor_id')
        date = data.get('date')

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
@swag_from({
    'tags': ['Shifts'],
    'summary': 'Delete a shift',
    'description': 'Remove a shift from a schedule.',
    'parameters': [
        {
            'name': 'shift_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the shift to delete.'
        }
    ],
    'responses': {
        200: {'description': 'Shift deleted successfully'},
        400: {'description': 'Bad request'}
    }
})
def delete_shift(shift_id):
    session: Session = DBSession()
    try:
        ShiftService.delete_shift(session, shift_id)
        logging.info(f"Shift deleted: {shift_id}")
        return jsonify({'message': 'Shift deleted successfully'}), 200
    except Exception as e:
        logging.error(f"Error deleting shift: {str(e)}")
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

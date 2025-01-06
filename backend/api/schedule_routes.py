from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required
from database.database_setup import Session
from services.schedule_service import ScheduleService
from flasgger import swag_from
import logging

# Create blueprint for schedule routes
schedule_blueprint = Blueprint('schedule', __name__)

@schedule_blueprint.route('/generate', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Schedules'],
    'summary': 'Generate a schedule',
    'description': 'Generates a new schedule for a given month and year.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'month': {'type': 'string', 'example': 'January'},
                    'year': {'type': 'integer', 'example': 2025}
                },
                'required': ['month', 'year']
            }
        }
    ],
    'responses': {
        201: {'description': 'Schedule generated successfully'},
        500: {'description': 'Internal server error'}
    }
})
def generate_schedule():
    session = Session()
    try:
        data = request.json
        month = data.get('month')
        year = data.get('year')
        result = ScheduleService.generate_schedule(session, month, year)
        logging.info(f"Schedule generated for {month} {year}.")
        return jsonify(result), 201
    except Exception as e:
        logging.error(f"Error generating schedule: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@schedule_blueprint.route('/history', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Schedules'],
    'summary': 'Get schedule history',
    'description': 'Retrieve schedules based on optional filters like month and year.',
    'parameters': [
        {'name': 'month', 'in': 'query', 'type': 'string', 'required': False, 'description': 'Filter by month'},
        {'name': 'year', 'in': 'query', 'type': 'integer', 'required': False, 'description': 'Filter by year'}
    ],
    'responses': {
        200: {'description': 'List of schedules'},
        500: {'description': 'Internal server error'}
    }
})
def browse_schedules():
    session = Session()
    try:
        month = request.args.get('month')
        year = request.args.get('year')
        schedules = ScheduleService.get_schedules(session, month, year)
        logging.info("Retrieved schedule history.")
        return jsonify(schedules), 200
    except Exception as e:
        logging.error(f"Error retrieving schedule history: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@schedule_blueprint.route('/<int:id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Schedules'],
    'summary': 'Get schedule details',
    'description': 'Retrieve details of a specific schedule by ID.',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'Schedule ID'}
    ],
    'responses': {
        200: {'description': 'Schedule details'},
        500: {'description': 'Internal server error'}
    }
})
def get_schedule(id):
    session = Session()
    try:
        schedule = ScheduleService.get_schedule_by_id(session, id)
        logging.info(f"Retrieved schedule ID {id}.")
        return jsonify(schedule), 200
    except Exception as e:
        logging.error(f"Error retrieving schedule by ID: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@schedule_blueprint.route('/<int:id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Schedules'],
    'summary': 'Update schedule status',
    'description': 'Updates the status of a specific schedule.',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'Schedule ID'},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'Finalized'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Schedule updated successfully'},
        500: {'description': 'Internal server error'}
    }
})
def update_schedule(id):
    session = Session()
    try:
        data = request.json
        status = data.get('status')
        result = ScheduleService.update_schedule(session, id, status)
        logging.info(f"Updated schedule ID {id} to status '{status}'.")
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Error updating schedule: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@schedule_blueprint.route('/export/<int:id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Schedules'],
    'summary': 'Export schedule as CSV',
    'description': 'Exports a schedule by ID as a CSV file.',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'Schedule ID'}
    ],
    'responses': {
        200: {'description': 'CSV file exported successfully'},
        500: {'description': 'Internal server error'}
    }
})
def export_schedule(id):
    session = Session()
    try:
        response = ScheduleService.export_schedule_as_csv(session, id)
        logging.info(f"Exported schedule ID {id} as CSV.")
        return response
    except Exception as e:
        logging.error(f"Error exporting schedule: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

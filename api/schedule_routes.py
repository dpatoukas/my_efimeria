from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required
from database.database_setup import Session
from services.schedule_service import ScheduleService
import logging

# Create blueprint for schedule routes
schedule_blueprint = Blueprint('schedule', __name__)

@schedule_blueprint.route('/generate', methods=['POST'])
@jwt_required()
def generate_schedule():
    """
    Generates a schedule based on input month and year.

    Request Body:
        - month (str): Month for schedule generation.
        - year (int): Year for schedule generation.

    Returns:
        JSON response with success or error message.
    """
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
def browse_schedules():
    """
    Retrieves schedules based on optional filters like month and year.

    Query Parameters:
        - month (str, optional): Filter schedules by month.
        - year (int, optional): Filter schedules by year.

    Returns:
        JSON response with list of schedules or error message.
    """
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
def get_schedule(id):
    """
    Retrieves details of a specific schedule by ID.

    URL Parameter:
        - id (int): Schedule ID.

    Returns:
        JSON response with schedule details or error message.
    """
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
def update_schedule(id):
    """
    Updates the status of a specific schedule.

    URL Parameter:
        - id (int): Schedule ID.

    Request Body:
        - status (str): New status for the schedule.

    Returns:
        JSON response with success or error message.
    """
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

@schedule_blueprint.route('/<int:id>/finalize', methods=['POST'])
@jwt_required()
def finalize_schedule(id):
    """
    Finalizes a schedule by locking its status.

    URL Parameter:
        - id (int): Schedule ID.

    Returns:
        JSON response with success or error message.
    """
    session = Session()
    try:
        result = ScheduleService.update_schedule(session, id, 'Finalized')
        logging.info(f"Finalized schedule ID {id}.")
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Error finalizing schedule: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@schedule_blueprint.route('/export/<int:id>', methods=['GET'])
@jwt_required()
def export_schedule(id):
    """
    Exports a schedule as a CSV file.

    URL Parameter:
        - id (int): Schedule ID.

    Returns:
        CSV file as a response or error message.
    """
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

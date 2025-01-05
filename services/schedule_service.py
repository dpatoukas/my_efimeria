from repositories.repository import ScheduleRepository
from services.database_to_clinic_request_service import DatabaseToClinicRequestService
from services.doctor_scheduling_service import DoctorSchedulingProblem
from services.solution_service import SolutionService
import numpy as np
import logging
from database.models import Schedule  # Added import
from flask import Response
import csv
from io import StringIO

class ScheduleService:
    """
    Service layer for handling schedule-related logic.

    This class includes methods for generating schedules, retrieving schedules,
    editing schedule details, finalizing schedules, and exporting schedules in CSV format.
    """

    @staticmethod
    def generate_schedule(session, month, year):
        """
        Generates a schedule for a given month and year.

        Args:
            session: Database session for queries and transactions.
            month (str): Target month for the schedule.
            year (int): Target year for the schedule.

        Returns:
            dict: Success message indicating schedule generation.

        Raises:
            Exception: Logs and raises errors during processing.
        """
        try:
            # Step 1: Fetch clinic request data
            service = DatabaseToClinicRequestService(session)
            clinic_request = service.get_monthly_clinic_request(month, year)

            # Step 2: Prepare input data for scheduling
            doctorNames = clinic_request['doctorNames']
            doctorPreference = clinic_request['doctorPreference']
            weekendPositionArray = clinic_request['weekendPositions']
            doctorExperience = [1] * len(doctorNames)
            doctorshiftMax = clinic_request['maxShifts']
            doctorshiftMin = clinic_request['minShifts']

            # Step 3: Create scheduling problem instance
            problem = DoctorSchedulingProblem(
                hardConstraintPenalty=10000,
                listOfDoctors=doctorNames,
                listOfDoctorPreferce=doctorPreference,
                doctorshiftMax=doctorshiftMax,
                doctorshiftMin=doctorshiftMin,
                weekendPositionArray=weekendPositionArray,
                doctorExperience=doctorExperience
            )

            # Solve the problem using genetic algorithm
            solution_service = SolutionService(problem)
            best_solution = solution_service.run_genetic_algorithm()

            # Reshape output to match schedule format
            num_days = 30
            num_doctors = len(doctorNames)
            reshaped_solution = np.array(best_solution).reshape(num_days, num_doctors)

            # Step 4: Save schedule to the database
            schedule = ScheduleRepository.add_schedule(session, month, year)
            solution_service.save_solution_to_db(session, month, year, reshaped_solution)
            logging.info(f"Schedule generated and saved for {month} {year}.")
            return {"message": f"Schedule for {month} {year} generated successfully!"}
        except Exception as e:
            logging.error(f"Error in generating schedule: {str(e)}")
            raise

    @staticmethod
    def get_schedules(session, month=None, year=None):
        """
        Retrieves schedules based on optional filters like month and year.

        Args:
            session: Database session for queries.
            month (str, optional): Filter schedules by month.
            year (int, optional): Filter schedules by year.

        Returns:
            list: List of schedules matching the filters in JSON format.

        Raises:
            Exception: Logs and raises errors during processing.
        """
        try:
            query = session.query(Schedule)
            if month:
                query = query.filter(Schedule.month == month)
            if year:
                query = query.filter(Schedule.year == year)

            schedules = query.all()
            result = [
                {
                    "id": schedule.id,
                    "month": schedule.month,
                    "year": schedule.year,
                    "status": schedule.status
                }
                for schedule in schedules
            ]
            logging.info(f"Retrieved {len(result)} schedules.")
            return result
        except Exception as e:
            logging.error(f"Error retrieving schedules: {str(e)}")
            raise

    @staticmethod
    def get_schedule_by_id(session, schedule_id):
        """
        Retrieves details of a specific schedule by ID.

        Args:
            session: Database session for queries.
            schedule_id (int): ID of the schedule to retrieve.

        Returns:
            dict: Details of the schedule.

        Raises:
            Exception: Logs and raises errors during processing.
        """
        try:
            schedule = session.query(Schedule).filter(Schedule.id == schedule_id).first()
            if not schedule:
                raise ValueError(f"Schedule with ID {schedule_id} not found.")
            result = {
                "id": schedule.id,
                "month": schedule.month,
                "year": schedule.year,
                "status": schedule.status
            }
            logging.info(f"Retrieved schedule ID {schedule_id}.")
            return result
        except Exception as e:
            logging.error(f"Error retrieving schedule by ID: {str(e)}")
            raise

    @staticmethod
    def update_schedule(session, schedule_id, status):
        """
        Updates the status of a specific schedule.

        Args:
            session: Database session for queries.
            schedule_id (int): ID of the schedule to update.
            status (str): New status of the schedule.

        Returns:
            dict: Success message.

        Raises:
            Exception: Logs and raises errors during processing.
        """
        try:
            schedule = session.query(Schedule).filter(Schedule.id == schedule_id).first()
            if not schedule:
                raise ValueError(f"Schedule with ID {schedule_id} not found.")
            schedule.status = status
            session.commit()
            logging.info(f"Updated schedule ID {schedule_id} to status '{status}'.")
            return {"message": f"Schedule {schedule_id} updated successfully!"}
        except Exception as e:
            logging.error(f"Error updating schedule: {str(e)}")
            raise

    @staticmethod
    def export_schedule_as_csv(session, schedule_id):
        """
        Exports a specific schedule as a CSV file.

        Args:
            session: Database session for queries.
            schedule_id (int): ID of the schedule to export.

        Returns:
            Response: CSV file content as an HTTP response.

        Raises:
            Exception: Logs and raises errors during processing.
        """
        try:
            schedule = session.query(Schedule).filter(Schedule.id == schedule_id).first()
            if not schedule:
                raise ValueError(f"Schedule with ID {schedule_id} not found.")

            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(["ID", "Month", "Year", "Status"])
            writer.writerow([schedule.id, schedule.month, schedule.year, schedule.status])
            logging.info(f"Exported schedule ID {schedule_id} as CSV.")
            output.seek(0)
            return Response(output, mimetype="text/csv", headers={
                "Content-Disposition": f"attachment; filename=schedule_{schedule_id}.csv"
            })
        except Exception as e:
            logging.error(f"Error exporting schedule as CSV: {str(e)}")
            raise

from sqlalchemy.orm import Session
from repositories.repository import ShiftRepository
import logging

class ShiftService:
    """
    Service layer for handling shift-related business logic and delegating database
    operations to the repository.
    """

    @staticmethod
    def get_shifts_by_schedule(session: Session, schedule_id: int):
        """
        Retrieves all shifts for a specific schedule.

        Args:
            session (Session): Database session.
            schedule_id (int): ID of the schedule.

        Returns:
            list: List of shifts for the schedule.

        Raises:
            ValueError: If schedule ID is invalid.
        """
        logging.info(f"Fetching shifts for schedule ID {schedule_id}")
        return ShiftRepository.get_shifts_by_schedule(session, schedule_id)

    @staticmethod
    def create_shift(session: Session, schedule_id: int, doctor_id: int, date: str):
        """
        Assigns a new shift.

        Args:
            session (Session): Database session.
            schedule_id (int): Schedule ID.
            doctor_id (int): Doctor ID.
            date (str): Date of the shift.

        Returns:
            Shift: Newly created shift.

        Raises:
            ValueError: If validation fails or doctor is double-booked.
        """
        logging.info(f"Creating shift for schedule ID {schedule_id}, doctor ID {doctor_id}, date {date}")
        if not schedule_id or not doctor_id or not date:
            logging.error("Missing required fields for creating shift.")
            raise ValueError("Schedule ID, Doctor ID, and Date are required.")

        return ShiftRepository.assign_shift(session, schedule_id, doctor_id, date)

    @staticmethod
    def update_shift(session: Session, shift_id: int, doctor_id: int, date: str):
        """
        Updates an existing shift.

        Args:
            session (Session): Database session.
            shift_id (int): ID of the shift to update.
            doctor_id (int): Updated doctor ID.
            date (str): Updated date.

        Returns:
            Shift: Updated shift.

        Raises:
            ValueError: If shift does not exist or conflicts occur.
        """
        logging.info(f"Updating shift ID {shift_id} to doctor ID {doctor_id}, date {date}")
        if not shift_id or not doctor_id or not date:
            logging.error("Missing required fields for updating shift.")
            raise ValueError("Shift ID, Doctor ID, and Date are required.")

        # Delete and reassign the shift to handle date/doctor updates
        ShiftRepository.delete_shift(session, shift_id)
        return ShiftRepository.assign_shift(session, doctor_id, date)

    @staticmethod
    def delete_shift(session: Session, shift_id: int):
        """
        Removes a shift.

        Args:
            session (Session): Database session.
            shift_id (int): ID of the shift to delete.

        Returns:
            bool: True if deletion was successful.

        Raises:
            ValueError: If the shift does not exist.
        """
        logging.info(f"Deleting shift ID {shift_id}")
        return ShiftRepository.delete_shift(session, shift_id)

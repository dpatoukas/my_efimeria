from sqlalchemy.orm import Session
from repositories.dao import DoctorDAO, ScheduleDAO, ShiftDAO
from database.models import Doctor, Schedule, Shift
from repositories.dao import ScheduleDAO, ShiftDAO

# Doctor Repository - Business Rules
class DoctorRepository:
    """
    Repository for managing Doctor-related database operations and business rules.
    """

    @staticmethod
    def add_doctor(session: Session, name: str, days_off: str):
        """
        Adds a new doctor to the database.

        Args:
            session (Session): Database session.
            name (str): Name of the doctor.
            days_off (str): Comma-separated string of days off.

        Returns:
            Doctor: The newly created doctor.

        Raises:
            ValueError: If a doctor with the same name already exists.
        """
        # Business rule: Ensure no duplicate doctor names
        existing_doctor = session.query(Doctor).filter(Doctor.name == name).first()
        if existing_doctor:
            raise ValueError("Doctor with this name already exists.")
        return DoctorDAO.create_doctor(session, name, days_off)

    @staticmethod
    def get_all_doctors(session: Session):
        """
        Retrieves all doctors from the database.

        Args:
            session (Session): Database session.

        Returns:
            list: List of all doctors.
        """
        return session.query(Doctor).all()

    @staticmethod
    def get_doctor_with_shifts(session: Session, doctor_id: int):
        """
        Retrieves a doctor along with their assigned shifts.

        Args:
            session (Session): Database session.
            doctor_id (int): ID of the doctor.

        Returns:
            dict: Doctor details and assigned shifts.

        Raises:
            ValueError: If the doctor is not found.
        """
        # Fetch doctor details
        doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doctor:
            raise ValueError("Doctor not found.")

        # Fetch all shifts assigned to the doctor
        shifts = session.query(Shift).filter(Shift.doctor_id == doctor_id).all()
        return {"doctor": doctor, "shifts": shifts}

    @staticmethod
    def update_doctor(session: Session, doctor_id: int, name: str, days_off: str):
        """
        Updates a doctor's details.

        Args:
            session (Session): Database session.
            doctor_id (int): ID of the doctor.
            name (str): Updated name of the doctor.
            days_off (str): Updated days off.

        Returns:
            Doctor: The updated doctor object.

        Raises:
            ValueError: If the doctor is not found.
        """
        doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doctor:
            raise ValueError("Doctor not found.")

        # Update fields if provided
        if name:
            doctor.name = name
        if days_off:
            doctor.days_off = days_off

        session.commit()
        return doctor

    @staticmethod
    def delete_doctor(session: Session, doctor_id: int):
        """
        Deletes a doctor from the database.

        Args:
            session (Session): Database session.
            doctor_id (int): ID of the doctor.

        Returns:
            bool: True if deletion was successful.

        Raises:
            ValueError: If the doctor is not found.
        """
        doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doctor:
            raise ValueError("Doctor not found.")

        session.delete(doctor)
        session.commit()
        return True

# Schedule Repository - Business Rules
class ScheduleRepository:
    @staticmethod
    def add_schedule(session: Session, month: str, year: int):
        # Business rule: Only one schedule per month and year
        existing_schedule = session.query(Schedule).filter(
            Schedule.month == month, Schedule.year == year
        ).first()
        if existing_schedule:
            raise ValueError("Schedule for this month already exists.")
        return ScheduleDAO.create_schedule(session, month, year, "Draft")

    @staticmethod
    def finalize_schedule(session: Session, schedule_id: int):
        # Fetch the schedule
        schedule = session.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not schedule:
            raise ValueError("Schedule not found.")

        # Finalize the schedule
        schedule.status = "Finalized"
        session.commit()
        return schedule
    
    @staticmethod
    def delete_schedule(session: Session, schedule_id: int):
        """
        Deletes a schedule and associated shifts using DAO layer.

        Args:
            session (Session): Database session.
            schedule_id (int): ID of the schedule to delete.

        Returns:
            bool: True if deletion is successful, False if not found.

        Raises:
            Exception: If an error occurs during deletion.
        """
        try:
            # Check if the schedule exists
            schedule = ScheduleDAO.get_schedule_by_id(session, schedule_id)
            if not schedule:
                raise ValueError("Schedule not found.")

            # Delete associated shifts using ShiftDAO
            shifts = ShiftDAO.get_shifts_by_schedule(session, schedule_id)
            for shift in shifts:
                ShiftDAO.delete_shift(session, shift.id)  # Reuse ShiftDAO delete method

            # Delete the schedule using ScheduleDAO
            return ScheduleDAO.delete_schedule(session, schedule_id)

        except Exception as e:
            session.rollback()  # Ensure rollback on failure
            raise e
    
# Shift Repository - Business Rules
class ShiftRepository:
    @staticmethod
    def assign_shift(session: Session, schedule_id: int, doctor_id: int, date: str):
        # Business rule: Prevent double booking on the same day
        existing_shift = session.query(Shift).filter(
            Shift.doctor_id == doctor_id, Shift.date == date
        ).first()
        if existing_shift:
            raise ValueError("Doctor is already assigned a shift on this date.")
        return ShiftDAO.create_shift(session, schedule_id, doctor_id, date, "Assigned")
    
    @staticmethod
    def save_shifts(session: Session, schedule_id: int, shifts: list):
        """
        Saves multiple shifts in bulk to improve performance.

        Parameters:
        - session (Session): Database session for transactions.
        - schedule_id (int): ID of the schedule to associate shifts.
        - shifts (list): List of dictionaries with shift details (doctor_id, date).

        Raises:
        - ValueError: If a conflict arises during shift assignment.
        """
        for shift in shifts:
            # Check for conflicts before saving
            existing_shift = session.query(Shift).filter(
                Shift.doctor_id == shift['doctor_id'], Shift.date == shift['date']
            ).first()
            if existing_shift:
                raise ValueError(f"Conflict: Doctor {shift['doctor_id']} already assigned on {shift['date']}.")

            # Save each shift
            ShiftDAO.create_shift(
                session,
                schedule_id,
                shift['doctor_id'],
                shift['date'],
                "Assigned"
            )

        # Commit changes after all inserts
        session.commit()
        print("Shifts saved successfully!")
    
    @staticmethod
    def clear_shifts_for_schedule(session: Session, schedule_id: int):
        """
        Deletes all shifts associated with a given schedule.

        Parameters:
        - session (Session): Database session.
        - schedule_id (int): ID of the schedule to clear shifts for.
        """
        session.query(Shift).filter_by(schedule_id=schedule_id).delete()
        session.commit()
        print(f"All shifts cleared for schedule ID {schedule_id}")

    @staticmethod
    def get_shifts_by_schedule(session: Session, schedule_id: int):
        """
        Retrieves all shifts for a specific schedule.

        Args:
            session (Session): Database session.
            schedule_id (int): ID of the schedule.

        Returns:
            list: List of shifts.
        """
        return session.query(Shift).filter(Shift.schedule_id == schedule_id).all()

    @staticmethod
    def delete_shift(session: Session, shift_id: int):
        """
        Deletes a shift by ID.

        Args:
            session (Session): Database session.
            shift_id (int): ID of the shift to delete.

        Returns:
            bool: True if deletion was successful.

        Raises:
            ValueError: If the shift is not found.
        """
        # Find the shift
        shift = session.query(Shift).filter(Shift.id == shift_id).first()
        if not shift:
            raise ValueError("Shift not found.")

        # Delete the shift
        session.delete(shift)
        session.commit()
        return True
    
    @staticmethod
    def get_shift_by_id(session: Session, shift_id: int):
        """
        Retrieves a shift by its ID.

        Args:
            session (Session): Database session.
            shift_id (int): ID of the shift.

        Returns:
            Shift: The shift object if found, else None.
        """
        return session.query(Shift).filter(Shift.id == shift_id).first()


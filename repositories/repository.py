from sqlalchemy.orm import Session
from repositories.dao import DoctorDAO, ScheduleDAO, ShiftDAO
from database.models import Doctor, Schedule, Shift


# Doctor Repository - Business Rules
class DoctorRepository:
    @staticmethod
    def add_doctor(session: Session, name: str, days_off: str):
        # Business rule: Ensure no duplicate doctor names
        existing_doctor = session.query(Doctor).filter(Doctor.name == name).first()
        if existing_doctor:
            raise ValueError("Doctor with this name already exists.")
        return DoctorDAO.create_doctor(session, name, days_off)

    @staticmethod
    def get_doctor_with_shifts(session: Session, doctor_id: int):
        # Fetch doctor details
        doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doctor:
            raise ValueError("Doctor not found.")

        # Fetch all shifts assigned to the doctor
        shifts = session.query(Shift).filter(Shift.doctor_id == doctor_id).all()
        return {"doctor": doctor, "shifts": shifts}


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

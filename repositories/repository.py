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

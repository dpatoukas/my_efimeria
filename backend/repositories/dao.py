from sqlalchemy.orm import Session
from database.models import Doctor, Schedule, Shift


# DAO for Doctor Table
class DoctorDAO:
    @staticmethod
    def create_doctor(session: Session, name: str, days_off: str):
        doctor = Doctor(name=name, days_off=days_off)
        session.add(doctor)
        session.commit()
        return doctor

    @staticmethod
    def get_doctor_by_id(session: Session, doctor_id: int):
        return session.query(Doctor).filter(Doctor.id == doctor_id).first()

    @staticmethod
    def get_all_doctors(session: Session):
        return session.query(Doctor).all()

    @staticmethod
    def update_doctor_days_off(session: Session, doctor_id: int, days_off: str):
        doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
        if doctor:
            doctor.days_off = days_off
            session.commit()
        return doctor

    @staticmethod
    def delete_doctor(session: Session, doctor_id: int):
        doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
        if doctor:
            session.delete(doctor)
            session.commit()
        return doctor


# DAO for Schedule Table
class ScheduleDAO:
    @staticmethod
    def create_schedule(session: Session, month: str, year: int, status: str):
        schedule = Schedule(month=month, year=year, status=status)
        session.add(schedule)
        session.commit()
        return schedule

    @staticmethod
    def get_schedule_by_id(session: Session, schedule_id: int):
        return session.query(Schedule).filter(Schedule.id == schedule_id).first()


# DAO for Shift Table
class ShiftDAO:
    @staticmethod
    def create_shift(session: Session, schedule_id: int, doctor_id: int, date: str, status: str):
        shift = Shift(schedule_id=schedule_id, doctor_id=doctor_id, date=date, status=status)
        session.add(shift)
        session.commit()
        return shift

    @staticmethod
    def get_shifts_by_schedule(session: Session, schedule_id: int):
        return session.query(Shift).filter(Shift.schedule_id == schedule_id).all()

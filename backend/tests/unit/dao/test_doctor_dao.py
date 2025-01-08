import pytest
from sqlalchemy.exc import IntegrityError
from database.models import Doctor
from repositories.dao import DoctorDAO


def test_create_doctor(test_session):
    doctor = DoctorDAO.create_doctor(test_session, "Dr. John", "Monday,Tuesday")
    assert doctor.id is not None
    assert doctor.name == "Dr. John"
    assert doctor.days_off == "Monday,Tuesday"


def test_get_doctor_by_id(test_session):
    doctor = DoctorDAO.create_doctor(test_session, "Dr. Smith", "Wednesday")
    fetched_doctor = DoctorDAO.get_doctor_by_id(test_session, doctor.id)
    assert fetched_doctor is not None
    assert fetched_doctor.name == "Dr. Smith"


def test_update_doctor_days_off(test_session):
    doctor = DoctorDAO.create_doctor(test_session, "Dr. Anna", "Monday")
    updated_doctor = DoctorDAO.update_doctor_days_off(test_session, doctor.id, "Friday")
    assert updated_doctor.days_off == "Friday"


def test_delete_doctor(test_session):
    doctor = DoctorDAO.create_doctor(test_session, "Dr. Lee", "Thursday")
    deleted_doctor = DoctorDAO.delete_doctor(test_session, doctor.id)
    assert deleted_doctor is not None
    assert test_session.query(Doctor).filter(Doctor.id == doctor.id).first() is None

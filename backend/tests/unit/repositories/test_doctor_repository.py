import pytest
from repositories.repository import DoctorRepository
from repositories.dao import DoctorDAO


def test_add_doctor(test_session):
    doctor = DoctorRepository.add_doctor(test_session, "Dr. Mike", "Saturday")
    assert doctor.id is not None
    assert doctor.name == "Dr. Mike"


def test_duplicate_doctor_error(test_session):
    DoctorRepository.add_doctor(test_session, "Dr. Mike", "Saturday")
    with pytest.raises(ValueError):
        DoctorRepository.add_doctor(test_session, "Dr. Mike", "Sunday")


def test_get_all_doctors(test_session):
    DoctorRepository.add_doctor(test_session, "Dr. Jane", "Friday")
    doctors = DoctorRepository.get_all_doctors(test_session)
    assert len(doctors) == 1


def test_update_doctor(test_session):
    doctor = DoctorRepository.add_doctor(test_session, "Dr. Amy", "Tuesday")
    updated_doctor = DoctorRepository.update_doctor(test_session, doctor.id, "Dr. Amy Updated", "Wednesday")
    assert updated_doctor.name == "Dr. Amy Updated"
    assert updated_doctor.days_off == "Wednesday"


def test_delete_doctor(test_session):
    doctor = DoctorRepository.add_doctor(test_session, "Dr. Adam", "Monday")
    result = DoctorRepository.delete_doctor(test_session, doctor.id)
    assert result is True

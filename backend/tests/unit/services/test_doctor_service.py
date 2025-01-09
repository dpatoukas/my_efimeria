import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from services.doctor_service import DoctorService
from repositories.repository import DoctorRepository
from database.models import Doctor


@pytest.fixture
def session():
    """Fixture for a mocked database session."""
    return MagicMock(spec=Session)


def test_get_all_doctors(session):
    """Test retrieving all doctors."""
    # Mock repository response
    expected_doctors = [
        Doctor(id=1, name="Dr. Alice", days_off="2025-01-01,2025-01-02"),
        Doctor(id=2, name="Dr. Bob", days_off="2025-01-03"),
    ]
    DoctorRepository.get_all_doctors = MagicMock(return_value=expected_doctors)

    # Call the service
    doctors = DoctorService.get_all_doctors(session)

    # Verify
    DoctorRepository.get_all_doctors.assert_called_once_with(session)
    assert doctors == expected_doctors


def test_get_doctor_by_id(session):
    """Test retrieving a doctor by ID."""
    # Mock repository response
    expected_doctor = {
        "doctor": Doctor(id=1, name="Dr. Alice", days_off="2025-01-01,2025-01-02"),
        "shifts": []
    }
    DoctorRepository.get_doctor_with_shifts = MagicMock(return_value=expected_doctor)

    # Call the service
    doctor = DoctorService.get_doctor_by_id(session, 1)

    # Verify
    DoctorRepository.get_doctor_with_shifts.assert_called_once_with(session, 1)
    assert doctor == expected_doctor


def test_create_doctor(session):
    """Test creating a doctor."""
    # Mock repository response
    expected_doctor = Doctor(id=1, name="Dr. Alice", days_off="2025-01-01,2025-01-02")
    DoctorRepository.add_doctor = MagicMock(return_value=expected_doctor)

    # Call the service
    doctor = DoctorService.create_doctor(session, "Dr. Alice", "2025-01-01,2025-01-02")

    # Verify
    DoctorRepository.add_doctor.assert_called_once_with(session, "Dr. Alice", "2025-01-01,2025-01-02")
    assert doctor == expected_doctor


def test_create_doctor_validation_error(session):
    """Test creating a doctor with missing inputs."""
    with pytest.raises(ValueError, match="Name and days off are required."):
        DoctorService.create_doctor(session, None, None)


def test_update_doctor(session):
    """Test updating a doctor."""
    # Mock repository response
    updated_doctor = Doctor(id=1, name="Dr. Alice Updated", days_off="2025-01-04")
    DoctorRepository.update_doctor = MagicMock(return_value=updated_doctor)

    # Call the service
    doctor = DoctorService.update_doctor(session, 1, name="Dr. Alice Updated", days_off="2025-01-04")

    # Verify
    DoctorRepository.update_doctor.assert_called_once_with(session, 1, "Dr. Alice Updated", "2025-01-04")
    assert doctor == updated_doctor


def test_update_doctor_validation_error(session):
    """Test updating a doctor with no fields provided."""
    with pytest.raises(ValueError, match="At least one field.*is required to update."):
        DoctorService.update_doctor(session, 1)


def test_delete_doctor(session):
    """Test deleting a doctor."""
    # Mock repository response
    DoctorRepository.delete_doctor = MagicMock(return_value=True)

    # Call the service
    result = DoctorService.delete_doctor(session, 1)

    # Verify
    DoctorRepository.delete_doctor.assert_called_once_with(session, 1)
    assert result is True


def test_delete_nonexistent_doctor(session):
    """Test deleting a non-existent doctor."""
    DoctorRepository.delete_doctor = MagicMock(side_effect=ValueError("Doctor does not exist."))

    with pytest.raises(ValueError, match="Doctor does not exist."):
        DoctorService.delete_doctor(session, 999)

import pytest
from unittest.mock import MagicMock, patch
from services.shift_service import ShiftService
from database.models import Shift


@pytest.fixture
def session():
    """Fixture for a mocked database session."""
    return MagicMock()


def test_get_shifts_by_schedule(session):
    """Test retrieving all shifts for a specific schedule."""
    with patch("repositories.repository.ShiftRepository.get_shifts_by_schedule") as MockShiftRepo:
        # Mock repository response
        MockShiftRepo.return_value = [
            {"id": 1, "schedule_id": 1, "doctor_id": 1, "date": "2025-01-01"},
            {"id": 2, "schedule_id": 1, "doctor_id": 2, "date": "2025-01-02"}
        ]

        # Call the service method
        shifts = ShiftService.get_shifts_by_schedule(session, schedule_id=1)

        # Assertions
        MockShiftRepo.assert_called_once_with(session, 1)
        assert len(shifts) == 2
        assert shifts[0]["date"] == "2025-01-01"


def test_create_shift_success(session):
    """Test creating a shift successfully."""
    with patch("repositories.repository.ShiftRepository.assign_shift") as MockShiftRepo:
        # Mock repository response
        MockShiftRepo.return_value = {"id": 1, "schedule_id": 1, "doctor_id": 1, "date": "2025-01-01"}

        # Call the service method
        shift = ShiftService.create_shift(session, schedule_id=1, doctor_id=1, date="2025-01-01")

        # Assertions
        MockShiftRepo.assert_called_once_with(session, 1, 1, "2025-01-01")
        assert shift["date"] == "2025-01-01"


def test_create_shift_validation_error(session):
    """Test creating a shift with missing required fields."""
    with pytest.raises(ValueError, match="Schedule ID, Doctor ID, and Date are required."):
        ShiftService.create_shift(session, schedule_id=None, doctor_id=1, date="2025-01-01")


def test_update_shift_success(session):
    """Test updating a shift successfully."""
    with patch("repositories.repository.ShiftRepository.get_shift_by_id") as MockGetShift, \
         patch("repositories.repository.ShiftRepository.delete_shift") as MockDeleteShift, \
         patch("repositories.repository.ShiftRepository.assign_shift") as MockAssignShift:
        
        # Mock repository responses
        MockGetShift.return_value = {"id": 1, "schedule_id": 1, "doctor_id": 1, "date": "2025-01-01"}
        MockAssignShift.return_value = {"id": 1, "schedule_id": 1, "doctor_id": 2, "date": "2025-01-02"}

        # Call the service method
        updated_shift = ShiftService.update_shift(session, shift_id=1, doctor_id=2, date="2025-01-02")

        # Assertions
        MockGetShift.assert_called_once_with(session, 1)
        MockDeleteShift.assert_called_once_with(session, 1)
        MockAssignShift.assert_called_once_with(session, 1, 2, "2025-01-02")
        assert updated_shift["date"] == "2025-01-02"


def test_update_shift_not_found(session):
    """Test updating a shift that does not exist."""
    with patch("repositories.repository.ShiftRepository.get_shift_by_id") as MockGetShift:
        # Mock repository response
        MockGetShift.return_value = None

        # Call the service method
        with pytest.raises(ValueError, match="Shift not found."):
            ShiftService.update_shift(session, shift_id=1, doctor_id=2, date="2025-01-02")


def test_update_shift_success(session):
    """Test updating a shift successfully."""
    with patch("repositories.repository.ShiftRepository.get_shift_by_id") as MockGetShift, \
         patch("repositories.repository.ShiftRepository.delete_shift") as MockDeleteShift, \
         patch("repositories.repository.ShiftRepository.assign_shift") as MockAssignShift:

        # Mock the existing shift to emulate the Shift object structure
        existing_shift_mock = MagicMock()
        existing_shift_mock.schedule_id = 1

        # Mock repository responses
        MockGetShift.return_value = existing_shift_mock
        MockAssignShift.return_value = {"id": 1, "schedule_id": 1, "doctor_id": 2, "date": "2025-01-02"}

        # Call the service method
        updated_shift = ShiftService.update_shift(session, shift_id=1, doctor_id=2, date="2025-01-02")

        # Assertions
        MockGetShift.assert_called_once_with(session, 1)
        MockDeleteShift.assert_called_once_with(session, 1)
        MockAssignShift.assert_called_once_with(session, 1, 2, "2025-01-02")
        assert updated_shift["date"] == "2025-01-02"



def test_delete_shift_not_found(session):
    """Test deleting a shift that does not exist."""
    with patch("repositories.repository.ShiftRepository.delete_shift") as MockDeleteShift:
        # Mock repository response
        MockDeleteShift.return_value = False

        # Call the service method
        result = ShiftService.delete_shift(session, shift_id=999)

        # Assertions
        MockDeleteShift.assert_called_once_with(session, 999)
        assert result is False

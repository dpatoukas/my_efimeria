import pytest
from repositories.repository import ShiftRepository
from repositories.dao import ShiftDAO


def test_assign_shift(test_session):
    shift = ShiftRepository.assign_shift(test_session, 1, 1, "2025-01-08")
    assert shift.id is not None
    assert shift.date == "2025-01-08"


def test_double_booking_error(test_session):
    ShiftRepository.assign_shift(test_session, 1, 1, "2025-01-08")
    with pytest.raises(ValueError):
        ShiftRepository.assign_shift(test_session, 1, 1, "2025-01-08")


def test_save_shifts(test_session):
    shifts = [
        {"doctor_id": 1, "date": "2025-01-09"},
        {"doctor_id": 2, "date": "2025-01-10"}
    ]
    ShiftRepository.save_shifts(test_session, 1, shifts)
    saved_shifts = ShiftDAO.get_shifts_by_schedule(test_session, 1)
    assert len(saved_shifts) == 2


def test_clear_shifts(test_session):
    ShiftRepository.assign_shift(test_session, 1, 1, "2025-01-08")
    ShiftRepository.clear_shifts_for_schedule(test_session, 1)
    shifts = ShiftDAO.get_shifts_by_schedule(test_session, 1)
    assert len(shifts) == 0

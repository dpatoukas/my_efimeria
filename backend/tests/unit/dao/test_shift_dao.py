import pytest
from database.models import Shift
from repositories.dao import ShiftDAO


def test_create_shift(test_session):
    shift = ShiftDAO.create_shift(test_session, 1, 1, "2025-01-06", "Assigned")
    assert shift.id is not None
    assert shift.schedule_id == 1
    assert shift.doctor_id == 1
    assert shift.date == "2025-01-06"
    assert shift.status == "Assigned"


def test_get_shifts_by_schedule(test_session):
    ShiftDAO.create_shift(test_session, 1, 1, "2025-01-06", "Assigned")
    shifts = ShiftDAO.get_shifts_by_schedule(test_session, 1)
    assert len(shifts) == 1
    assert shifts[0].date == "2025-01-06"

import pytest
from repositories.repository import ScheduleRepository
from repositories.dao  import ScheduleDAO


def test_add_schedule(test_session):
    schedule = ScheduleRepository.add_schedule(test_session, "March", 2025)
    assert schedule.id is not None
    assert schedule.month == "March"


def test_duplicate_schedule_error(test_session):
    ScheduleRepository.add_schedule(test_session, "April", 2025)
    with pytest.raises(ValueError):
        ScheduleRepository.add_schedule(test_session, "April", 2025)


def test_finalize_schedule(test_session):
    schedule = ScheduleRepository.add_schedule(test_session, "May", 2025)
    finalized_schedule = ScheduleRepository.finalize_schedule(test_session, schedule.id)
    assert finalized_schedule.status == "Finalized"

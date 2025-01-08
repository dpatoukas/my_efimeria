import pytest
from database.models import Schedule
from repositories.dao import ScheduleDAO


def test_create_schedule(test_session):
    schedule = ScheduleDAO.create_schedule(test_session, "January", 2025, "Draft")
    assert schedule.id is not None
    assert schedule.month == "January"
    assert schedule.year == 2025
    assert schedule.status == "Draft"


def test_get_schedule_by_id(test_session):
    schedule = ScheduleDAO.create_schedule(test_session, "February", 2025, "Draft")
    fetched_schedule = ScheduleDAO.get_schedule_by_id(test_session, schedule.id)
    assert fetched_schedule is not None
    assert fetched_schedule.month == "February"
    assert fetched_schedule.year == 2025

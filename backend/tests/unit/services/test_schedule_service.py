import pytest
from unittest.mock import MagicMock, patch
from services.schedule_service import ScheduleService
from database.models import Schedule


@pytest.fixture
def session():
    """Fixture for a mocked database session."""
    return MagicMock()


def test_generate_schedule_success(session):
    """Test generating a schedule successfully."""
    with patch("services.schedule_service.DatabaseToClinicRequestService") as MockClinicService, \
         patch("services.schedule_service.DoctorSchedulingProblem") as MockSchedulingProblem, \
         patch("services.schedule_service.SolutionService") as MockSolutionService, \
         patch("services.schedule_service.ScheduleRepository") as MockScheduleRepo:

        # Mock the clinic request service
        mock_clinic_request_service = MockClinicService.return_value
        mock_clinic_request_service.get_monthly_clinic_request.return_value = {
            "doctorNames": ["Dr. Alice", "Dr. Bob"],
            "doctorPreference": [[1, 1, 0], [0, 1, 1]],
            "weekendPositions": [0, 0, 1],
            "maxShifts": [2, 2, 2],
            "minShifts": [1, 1, 1],
        }

        # Mock the solution service
        mock_solution_service = MockSolutionService.return_value
        mock_solution_service.run_genetic_algorithm.return_value = [1] * 62

        # Mock schedule repository
        MockScheduleRepo.add_schedule.return_value = Schedule(id=1, month="January", year=2025, status="Draft")

        # Call the service method
        response = ScheduleService.generate_schedule(session, "January", 2025)

        # Assertions
        mock_clinic_request_service.get_monthly_clinic_request.assert_called_once_with("January", 2025)
        mock_solution_service.run_genetic_algorithm.assert_called_once()
        MockScheduleRepo.add_schedule.assert_called_once_with(session, "January", 2025)
        assert response["message"] == "Schedule for January 2025 generated successfully!"


def test_get_schedules_success(session):
    """Test retrieving schedules successfully."""
    session.query.return_value.filter.return_value.filter.return_value.all.return_value = [
        Schedule(id=1, month="January", year=2025, status="Draft"),
        Schedule(id=2, month="February", year=2025, status="Finalized"),
    ]

    schedules = ScheduleService.get_schedules(session, month="January", year=2025)

    session.query.assert_called_once()
    assert len(schedules) == 2
    assert schedules[0]["month"] == "January"


def test_get_schedule_by_id_success(session):
    """Test retrieving a schedule by ID successfully."""
    session.query.return_value.filter.return_value.first.return_value = Schedule(
        id=1, month="January", year=2025, status="Draft"
    )

    schedule = ScheduleService.get_schedule_by_id(session, 1)

    session.query.assert_called_once()
    assert schedule["month"] == "January"
    assert schedule["status"] == "Draft"


def test_export_schedule_as_csv_success(session):
    """Test exporting a schedule as CSV successfully."""
    session.query.return_value.filter.return_value.first.return_value = Schedule(
        id=1, month="January", year=2025, status="Draft"
    )

    response = ScheduleService.export_schedule_as_csv(session, 1)

    session.query.assert_called_once()
    assert response.mimetype == "text/csv"
    assert "attachment" in response.headers["Content-Disposition"]

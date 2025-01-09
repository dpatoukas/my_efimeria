import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Doctor, Schedule
from services.database_to_clinic_request_service import DatabaseToClinicRequestService


# Fixtures
@pytest.fixture(scope="module")
def engine():
    """Set up an in-memory SQLite database for testing."""
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="module", autouse=True)
def setup_database(engine):
    """Set up and tear down the database schema."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def session(engine):
    """Provide a database session for each test."""
    TestingSession = sessionmaker(bind=engine)
    session = TestingSession()
    yield session
    session.close()


@pytest.fixture
def service(session):
    """Provide an instance of the DatabaseToClinicRequestService."""
    return DatabaseToClinicRequestService(session)


# Tests
def test_initialization(service):
    """Test that the service initializes with a session."""
    assert service.session is not None


def test_get_monthly_clinic_request_no_data(service):
    """Test `get_monthly_clinic_request` with no data in the database."""
    request = service.get_monthly_clinic_request(month="January", year=2025)
    assert request["doctorNames"] == ["NA"]
    # Expect a full month of "NA" preferences for January (31 days)
    expected_preferences = [["NA"] * 31]
    assert request["doctorPreference"] == expected_preferences



def test_get_monthly_clinic_request_with_data(service, session):
    """Test `get_monthly_clinic_request` with populated data."""
    # Insert mock data
    doctor1 = Doctor(name="Dr. Alice", days_off="2025-01-01,2025-01-02")
    doctor2 = Doctor(name="Dr. Bob", days_off="2025-01-03")
    schedule = Schedule(month="January", year=2025, status="Draft")
    session.add_all([doctor1, doctor2, schedule])
    session.commit()

    # Call the service method
    request = service.get_monthly_clinic_request(month="January", year=2025)

    assert request["doctorNames"] == ["Dr. Alice", "Dr. Bob"]
    assert len(request["doctorPreference"]) == 2
    assert request["doctorPreference"][0][0] == 0  # Dr. Alice not available on 2025-01-01
    assert request["doctorPreference"][1][2] == 0  # Dr. Bob not available on 2025-01-03


def test_generate_calendar(service):
    """Test the `_generate_calendar` utility method."""
    total_days, order_of_days, weekend_positions, number_of_days = service._generate_calendar(
        month="January", year=2025
    )

    assert len(total_days) == 31  # January 2025 has 31 days
    assert order_of_days[0] == "Wednesday"  # 2025-01-01 is a Wednesday
    assert weekend_positions[4] == 1  # 2025-01-05 is a Saturday
    assert number_of_days[0] == 1  # First day is 1


def test_generate_preference_matrix(service):
    """Test the `_generate_preference_matrix` utility method."""
    total_days = [datetime(2025, 1, day) for day in range(1, 6)]
    doctor_names = ["Dr. Alice", "Dr. Bob"]
    doctor_days_off = {"Dr. Alice": ["2025-01-01"], "Dr. Bob": ["2025-01-03"]}

    preference_matrix = service._generate_preference_matrix(
        doctor_names, doctor_days_off, total_days
    )

    assert len(preference_matrix) == 2  # Two doctors
    assert preference_matrix[0][0] == 0  # Dr. Alice not available on 2025-01-01
    assert preference_matrix[1][2] == 0  # Dr. Bob not available on 2025-01-03
    assert preference_matrix[0][1] == 1  # Dr. Alice available on 2025-01-02
    assert preference_matrix[1][1] == 1  # Dr. Bob available on 2025-01-02

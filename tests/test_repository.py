import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Doctor, Schedule, Shift
from repositories.repository import DoctorRepository, ScheduleRepository, ShiftRepository

# Database setup for testing
db_url = "sqlite:///:memory:"
engine = create_engine(db_url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Create tables
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    # Insert initial data
    doctor1 = Doctor(name="Dr. Smith", days_off="['2025-01-01']")
    doctor2 = Doctor(name="Dr. Jones", days_off="['2025-01-02']")
    schedule = Schedule(month="January", year=2025, status="Draft")
    session.add_all([doctor1, doctor2, schedule])
    session.commit()

    yield session

    # Clean up database after test
    session.close()
    Base.metadata.drop_all(bind=engine)

# Test DoctorRepository
def test_add_doctor(db_session):
    print("Testing adding a new doctor...")
    doctor = DoctorRepository.add_doctor(db_session, "Dr. Taylor", "['2025-01-03']")
    assert doctor.name == "Dr. Taylor"
    print("Doctor added successfully: Dr. Taylor")

    print("Testing duplicate doctor addition...")
    with pytest.raises(ValueError, match="Doctor with this name already exists"):
        DoctorRepository.add_doctor(db_session, "Dr. Smith", "['2025-01-04']")
    print("Duplicate doctor test passed.")

def test_get_doctor_with_shifts(db_session):
    print("Testing fetching doctor details with shifts...")
    doctor = DoctorRepository.get_doctor_with_shifts(db_session, 1)
    assert doctor["doctor"].name == "Dr. Smith"
    assert len(doctor["shifts"]) == 0
    print("Doctor fetched successfully with no shifts assigned.")

# Test ScheduleRepository
def test_add_schedule(db_session):
    print("Testing adding a new schedule...")
    schedule = ScheduleRepository.add_schedule(db_session, "February", 2025)
    assert schedule.month == "February"
    print("Schedule added successfully: February 2025")

    print("Testing duplicate schedule addition...")
    with pytest.raises(ValueError, match="Schedule for this month already exists"):
        ScheduleRepository.add_schedule(db_session, "January", 2025)
    print("Duplicate schedule test passed.")

def test_finalize_schedule(db_session):
    print("Testing finalizing a schedule...")
    schedule = ScheduleRepository.finalize_schedule(db_session, 1)
    assert schedule.status == "Finalized"
    print("Schedule finalized successfully.")

# Test ShiftRepository
def test_assign_shift(db_session):
    print("Testing assigning a shift...")
    shift = ShiftRepository.assign_shift(db_session, 1, 1, "2025-01-03")
    assert shift.date == "2025-01-03"
    print("Shift assigned successfully: 2025-01-03")

    print("Testing double booking prevention...")
    with pytest.raises(ValueError, match="Doctor is already assigned a shift on this date"):
        ShiftRepository.assign_shift(db_session, 1, 1, "2025-01-03")
    print("Double booking prevention test passed.")

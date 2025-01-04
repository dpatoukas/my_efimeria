import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import sessionmaker
from database.database_setup import engine
from repositories.repository import DoctorRepository, ScheduleRepository, ShiftRepository
from database.models import Doctor, Schedule


# Create session
Session = sessionmaker(bind=engine)
session = Session()

# Test DoctorRepository
try:
    print("\n--- Testing DoctorRepository ---")

    # Add Doctor
    doctor = DoctorRepository.add_doctor(session, "Dr. Brown3", "2025-41-03,2025-01-04")
    print(f"Added Doctor: {doctor.id}, {doctor.name}, Days Off: {doctor.days_off}")

    # Fetch Doctor with Shifts
    result = DoctorRepository.get_doctor_with_shifts(session, doctor.id)
    print(f"Doctor with Shifts: {result['doctor'].name}, Shifts: {result['shifts']}")

except Exception as e:
    print("DoctorRepository Test Error:", e)


# Test ScheduleRepository
try:
    print("\n--- Testing ScheduleRepository ---")

    # Add Schedule
    schedule = ScheduleRepository.add_schedule(session, "January", 2025)
    print(f"Added Schedule: {schedule.id}, {schedule.month}, {schedule.year}, Status: {schedule.status}")

    # Finalize Schedule
    finalized_schedule = ScheduleRepository.finalize_schedule(session, schedule.id)
    print(f"Finalized Schedule: {finalized_schedule.id}, Status: {finalized_schedule.status}")

except Exception as e:
    print("ScheduleRepository Test Error:", e)


# Test ShiftRepository
try:
    print("\n--- Testing ShiftRepository ---")

    # Assign Shift
    shift = ShiftRepository.assign_shift(session, schedule.id, doctor.id, "2025-01-06")
    print(f"Assigned Shift: {shift.id}, Date: {shift.date}, Status: {shift.status}")

except Exception as e:
    print("ShiftRepository Test Error:", e)

# Close session
session.close()

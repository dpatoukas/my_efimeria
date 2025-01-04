import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import sessionmaker
from database.database_setup import engine
from database.models import Doctor, Schedule, Shift
from repositories.dao import DoctorDAO, ScheduleDAO, ShiftDAO


# Create session
Session = sessionmaker(bind=engine)
session = Session()


def test_doctor_dao():
    """
    Tests DAO methods for the Doctor table.
    """
    print("\n--- Testing DoctorDAO ---")

    try:
        # Create Doctor
        doctor = DoctorDAO.create_doctor(session, "Dr. Green", "2025-01-01,2025-01-02")
        assert doctor.name == "Dr. Green", "Doctor name mismatch!"
        assert doctor.days_off == "2025-01-01,2025-01-02", "Days off mismatch!"
        print(f"Created Doctor: {doctor.id}, {doctor.name}, Days Off: {doctor.days_off}")

        # Fetch Doctor by ID
        fetched_doctor = DoctorDAO.get_doctor_by_id(session, doctor.id)
        assert fetched_doctor, "Doctor fetch failed!"
        print(f"Fetched Doctor: {fetched_doctor.id}, {fetched_doctor.name}")

        # Update Doctor Days Off
        updated_doctor = DoctorDAO.update_doctor_days_off(session, doctor.id, "2025-01-03,2025-01-04")
        assert updated_doctor.days_off == "2025-01-03,2025-01-04", "Days off update failed!"
        print(f"Updated Days Off: {updated_doctor.days_off}")

        # Get All Doctors
        all_doctors = DoctorDAO.get_all_doctors(session)
        assert len(all_doctors) > 0, "No doctors found!"
        print(f"All Doctors: {[doc.name for doc in all_doctors]}")

        # Delete Doctor
        DoctorDAO.delete_doctor(session, doctor.id)
        deleted_doctor = DoctorDAO.get_doctor_by_id(session, doctor.id)
        assert deleted_doctor is None, "Doctor deletion failed!"
        print("Doctor deleted successfully!")

    except Exception as e:
        print("DoctorDAO Test Error:", e)


def test_schedule_dao():
    """
    Tests DAO methods for the Schedule table.
    """
    print("\n--- Testing ScheduleDAO ---")

    try:
        # Create Schedule
        schedule = ScheduleDAO.create_schedule(session, "January", 2025, "Draft")
        assert schedule.month == "January", "Schedule month mismatch!"
        assert schedule.year == 2025, "Schedule year mismatch!"
        print(f"Created Schedule: {schedule.id}, {schedule.month}, {schedule.year}, Status: {schedule.status}")

        # Fetch Schedule by ID
        fetched_schedule = ScheduleDAO.get_schedule_by_id(session, schedule.id)
        assert fetched_schedule, "Schedule fetch failed!"
        print(f"Fetched Schedule: {fetched_schedule.id}, {fetched_schedule.month}, {fetched_schedule.year}")

    except Exception as e:
        print("ScheduleDAO Test Error:", e)


def test_shift_dao():
    """
    Tests DAO methods for the Shift table.
    """
    print("\n--- Testing ShiftDAO ---")

    try:
        # Create Shift
        schedule = ScheduleDAO.create_schedule(session, "February", 2025, "Draft")
        doctor = DoctorDAO.create_doctor(session, "Dr. Blue", "2025-02-01,2025-02-02")

        shift = ShiftDAO.create_shift(session, schedule.id, doctor.id, "2025-02-03", "Assigned")
        assert shift.date == "2025-02-03", "Shift date mismatch!"
        assert shift.status == "Assigned", "Shift status mismatch!"
        print(f"Created Shift: {shift.id}, Date: {shift.date}, Status: {shift.status}")

        # Fetch Shifts by Schedule
        shifts = ShiftDAO.get_shifts_by_schedule(session, schedule.id)
        assert len(shifts) > 0, "No shifts found!"
        print(f"Shifts: {[f'Doctor {shift.doctor_id} on {shift.date}' for shift in shifts]}")

    except Exception as e:
        print("ShiftDAO Test Error:", e)


if __name__ == "__main__":
    # Run DAO tests
    test_doctor_dao()
    test_schedule_dao()
    test_shift_dao()

    # Close session
    session.close()
    print("\nAll DAO tests completed!")

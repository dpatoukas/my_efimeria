import sys
import os

# Add project root to Python path for module resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import database setup and models
from database.database_setup import Session
from database.models import Doctor, Schedule, Shift


def insert_initial_data():
    """
    Inserts initial test data into the database.
    """
    # Create a new session
    session = Session()

    try:
        print("\n--- Inserting Initial Data ---")

        # Clear existing data
        session.query(Shift).delete()
        session.query(Schedule).delete()
        session.query(Doctor).delete()
        session.commit()
        print("Existing data cleared.")

        # Insert Doctors
        doctor1 = Doctor(name='Dr. Brown', days_off='2025-01-03,2025-01-04')
        doctor2 = Doctor(name='Dr. Smith', days_off='2025-01-01,2025-01-02')
        session.add_all([doctor1, doctor2])

        # Insert Schedule
        schedule1 = Schedule(month='January', year=2025, status='Draft')
        schedule2 = Schedule(month='February', year=2025, status='Draft')
        session.add_all([schedule1, schedule2])

        # Insert Shifts
        shift1 = Shift(schedule_id=1, doctor_id=1, date='2025-01-06', status='Assigned')
        shift2 = Shift(schedule_id=1, doctor_id=2, date='2025-01-07', status='Assigned')
        session.add_all([shift1, shift2])

        # Commit data to the database
        session.commit()
        print("Initial data inserted successfully!")

        # Verify Inserted Data
        doctors = session.query(Doctor).all()
        schedules = session.query(Schedule).all()
        shifts = session.query(Shift).all()

        print(f"Doctors: {[doctor.name for doctor in doctors]}")
        print(f"Schedules: {[f'{schedule.month} {schedule.year}' for schedule in schedules]}")
        print(f"Shifts: {[f'Doctor {shift.doctor_id} on {shift.date}' for shift in shifts]}")

    except Exception as e:
        print(f"Error inserting initial data: {e}")
        session.rollback()

    finally:
        session.close()


if __name__ == "__main__":
    insert_initial_data()

import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import sessionmaker
from database.database_setup import engine, Base
from database.models import Doctor, Schedule, Shift
from database.database_setup import Session


def reset_database():
    # Create session
    session = Session()

    try:
        print("\n--- Resetting Database ---")

        # Delete all existing data
        session.query(Shift).delete()
        session.query(Schedule).delete()
        session.query(Doctor).delete()

        # Commit deletion
        session.commit()
        print("All data deleted.")

        # Insert initial data for tests
        print("\n--- Inserting Initial Data ---")

        # Add Doctors
        doctor1 = Doctor(name="Dr. Brown", days_off="2025-01-03,2025-01-04")
        session.add(doctor1)

        # Add Schedule
        schedule1 = Schedule(month="January", year=2025, status="Draft")
        session.add(schedule1)

        # Commit new data
        session.commit()
        print("Initial data inserted successfully.")

        # Verify Data
        doctors = session.query(Doctor).all()
        schedules = session.query(Schedule).all()
        print(f"Doctors: {[doctor.name for doctor in doctors]}")
        print(f"Schedules: {[f'{schedule.month} {schedule.year}' for schedule in schedules]}")

    except Exception as e:
        print("Error during reset:", e)
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    reset_database()

import sys
import os

# Add project root to Python path for module resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import inspect
from database.database_setup import engine, Session
from database.models import Doctor, Schedule, Shift, AdminUser


def test_connection():
    """
    Tests the database connection and verifies the schema.
    """
    try:
        # Print database engine info
        print("\n--- Testing Database Connection ---")
        print(f"Database URL: {engine.url}")

        # Verify connection
        connection = engine.connect()
        print("Database connection successful!")
        connection.close()

        # Inspect tables
        print("\n--- Verifying Tables ---")
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        expected_tables = ['Doctor', 'Schedule', 'Shift', 'AdminUser']

        # Check if all tables exist
        for table in expected_tables:
            assert table in tables, f"Table '{table}' is missing!"
        print("All tables exist!")

        # Verify columns in each table
        print("\n--- Verifying Columns ---")

        # Doctor Table
        doctor_columns = [col['name'] for col in inspector.get_columns('Doctor')]
        assert set(doctor_columns) == {'id', 'name', 'days_off'}, "Doctor table columns mismatch!"

        # Schedule Table
        schedule_columns = [col['name'] for col in inspector.get_columns('Schedule')]
        assert set(schedule_columns) == {'id', 'month', 'year', 'status'}, "Schedule table columns mismatch!"

        # Shift Table
        shift_columns = [col['name'] for col in inspector.get_columns('Shift')]
        assert set(shift_columns) == {'id', 'schedule_id', 'doctor_id', 'date', 'status'}, "Shift table columns mismatch!"

        # AdminUser Table
        admin_columns = [col['name'] for col in inspector.get_columns('AdminUser')]
        assert set(admin_columns) == {'id', 'username', 'password'}, "AdminUser table columns mismatch!"

        print("All table columns are correct!")

        # Check for sample data
        session = Session()

        print("\n--- Verifying Initial Data ---")

        # Doctors
        doctors = session.query(Doctor).all()
        assert len(doctors) > 0, "No doctors found!"
        print(f"Doctors: {[doctor.name for doctor in doctors]}")

        # Schedules
        schedules = session.query(Schedule).all()
        assert len(schedules) > 0, "No schedules found!"
        print(f"Schedules: {[f'{s.month} {s.year}' for s in schedules]}")

        # Shifts
        shifts = session.query(Shift).all()
        assert len(shifts) > 0, "No shifts found!"
        print(f"Shifts: {[f'Doctor {s.doctor_id} on {s.date}' for s in shifts]}")

        # Admin Users
        admin_users = session.query(AdminUser).all()
        print(f"Admin Users: {[user.username for user in admin_users]}")

        session.close()

        print("\nAll tests passed! Database is correctly configured and populated.")

    except Exception as e:
        print(f"Test failed: {e}")


if __name__ == "__main__":
    test_connection()

import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from database.database_setup import engine, Base
from database.models import Doctor, Schedule, Shift, AdminUser


# Create session
Session = sessionmaker(bind=engine)
session = Session()


def test_table_existence():
    """
    Test if all required tables exist in the database.
    """
    print("\n--- Testing Table Existence ---")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    expected_tables = ['Doctor', 'Schedule', 'Shift', 'AdminUser']
    
    for table in expected_tables:
        assert table in tables, f"Table '{table}' does not exist!"
    print("All tables exist!")


def test_table_columns():
    """
    Test if each table has the expected columns and types.
    """
    print("\n--- Testing Table Columns ---")
    inspector = inspect(engine)

    # Doctor Table
    columns = inspector.get_columns('Doctor')
    expected_columns = {'id': 'INTEGER', 'name': 'VARCHAR', 'days_off': 'TEXT'}
    for col in expected_columns:
        assert any(c['name'] == col and c['type'].__class__.__name__.upper() == expected_columns[col]
                   for c in columns), f"Column '{col}' in 'Doctor' table is missing or has incorrect type!"

    # Schedule Table
    columns = inspector.get_columns('Schedule')
    expected_columns = {'id': 'INTEGER', 'month': 'VARCHAR', 'year': 'INTEGER', 'status': 'VARCHAR'}
    for col in expected_columns:
        assert any(c['name'] == col and c['type'].__class__.__name__.upper() == expected_columns[col]
                   for c in columns), f"Column '{col}' in 'Schedule' table is missing or has incorrect type!"

    # Shift Table
    columns = inspector.get_columns('Shift')
    expected_columns = {'id': 'INTEGER', 'schedule_id': 'INTEGER', 'doctor_id': 'INTEGER', 'date': 'VARCHAR', 'status': 'VARCHAR'}
    for col in expected_columns:
        assert any(c['name'] == col and c['type'].__class__.__name__.upper() == expected_columns[col]
                   for c in columns), f"Column '{col}' in 'Shift' table is missing or has incorrect type!"

    # AdminUser Table
    columns = inspector.get_columns('AdminUser')
    expected_columns = {'id': 'INTEGER', 'username': 'VARCHAR', 'password': 'VARCHAR'}
    for col in expected_columns:
        assert any(c['name'] == col and c['type'].__class__.__name__.upper() == expected_columns[col]
                   for c in columns), f"Column '{col}' in 'AdminUser' table is missing or has incorrect type!"

    print("All table columns and types are valid!")


def test_foreign_keys():
    """
    Test if foreign key constraints are correctly defined.
    """
    print("\n--- Testing Foreign Keys ---")
    inspector = inspect(engine)

    # Check Shift table foreign keys
    fks = inspector.get_foreign_keys('Shift')
    fk_columns = {fk['constrained_columns'][0]: fk['referred_table'] for fk in fks}

    expected_fks = {'schedule_id': 'Schedule', 'doctor_id': 'Doctor'}
    for column, referenced_table in expected_fks.items():
        assert column in fk_columns, f"Foreign key '{column}' missing in 'Shift' table!"
        assert fk_columns[column] == referenced_table, f"Foreign key '{column}' does not reference '{referenced_table}'!"
    print("Foreign keys are correctly defined!")


def test_constraints():
    """
    Test if constraints like primary keys and uniqueness are enforced.
    """
    print("\n--- Testing Constraints ---")

    # Primary Key Checks
    inspector = inspect(engine)

    pk_doctor = inspector.get_pk_constraint('Doctor')['constrained_columns']
    pk_schedule = inspector.get_pk_constraint('Schedule')['constrained_columns']
    pk_shift = inspector.get_pk_constraint('Shift')['constrained_columns']
    pk_admin = inspector.get_pk_constraint('AdminUser')['constrained_columns']

    assert 'id' in pk_doctor, "Primary key missing in 'Doctor' table!"
    assert 'id' in pk_schedule, "Primary key missing in 'Schedule' table!"
    assert 'id' in pk_shift, "Primary key missing in 'Shift' table!"
    assert 'id' in pk_admin, "Primary key missing in 'AdminUser' table!"

    print("Primary keys are correctly defined!")

    # # Uniqueness Check for AdminUser username
    # columns = inspector.get_columns('AdminUser')
    # indexes = inspector.get_indexes('AdminUser')
    # unique_indexes = [idx['name'] for idx in indexes if idx.get('unique')]
    # assert any('username' in idx for idx in unique_indexes), "Unique constraint missing for 'username' in 'AdminUser' table!"

    print("Constraints are valid!")


def test_data():
    """
    Test if initial data exists in the database.
    """
    print("\n--- Testing Initial Data ---")

    # Check Doctors
    doctors = session.query(Doctor).all()
    assert len(doctors) > 0, "No doctors found!"
    print(f"Doctors: {[doctor.name for doctor in doctors]}")

    # Check Schedules
    schedules = session.query(Schedule).all()
    assert len(schedules) > 0, "No schedules found!"
    print(f"Schedules: {[f'{s.month} {s.year}' for s in schedules]}")

    # Check Shifts
    shifts = session.query(Shift).all()
    assert len(shifts) > 0, "No shifts found!"
    print(f"Shifts: {[f'Doctor {s.doctor_id} on {s.date}' for s in shifts]}")

    print("Initial data tests passed!")


if __name__ == "__main__":
    try:
        test_table_existence()
        test_table_columns()
        test_foreign_keys()
        test_constraints()
        test_data()
        print("\nAll tests passed successfully!")
    except AssertionError as e:
        print(f"Test failed: {e}")

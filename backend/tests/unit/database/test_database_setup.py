import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from database.models import Base, Doctor, Schedule, Shift, AdminUser


@pytest.fixture(scope="module")
def engine():
    """
    Create an SQLite in-memory database for testing.
    """
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="module", autouse=True)
def setup_database(engine):
    """
    Setup the database schema for testing.
    """
    Base.metadata.create_all(engine)  # Create all tables
    yield
    Base.metadata.drop_all(engine)  # Drop all tables after tests


@pytest.fixture(scope="function")
def session(engine):
    """
    Create a database session for testing.
    """
    TestingSession = sessionmaker(bind=engine)
    session = TestingSession()
    yield session
    session.close()


def test_connection(engine):
    """
    Test database connection.
    """
    connection = engine.connect()
    assert connection, "Failed to connect to the database."
    connection.close()


def test_table_existence(engine):
    """
    Test if all required tables exist in the database.
    """
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    expected_tables = {"Doctor", "Schedule", "Shift", "AdminUser"}

    missing_tables = expected_tables - set(tables)
    assert not missing_tables, f"Missing tables: {missing_tables}"


def test_table_columns(engine):
    """
    Test if tables have the correct columns with expected types.
    """
    inspector = inspect(engine)

    expected_schema = {
        "Doctor": {"id": "INTEGER", "name": "VARCHAR", "days_off": "TEXT"},
        "Schedule": {"id": "INTEGER", "month": "VARCHAR", "year": "INTEGER", "status": "VARCHAR"},
        "Shift": {
            "id": "INTEGER",
            "schedule_id": "INTEGER",
            "doctor_id": "INTEGER",
            "date": "VARCHAR",
            "status": "VARCHAR",
        },
        "AdminUser": {"id": "INTEGER", "username": "VARCHAR", "password": "VARCHAR"},
    }

    for table, expected_columns in expected_schema.items():
        columns = {col["name"]: col["type"].__class__.__name__.upper() for col in inspector.get_columns(table)}
        assert expected_columns == columns, f"Mismatch in columns for table '{table}'. Expected: {expected_columns}, Found: {columns}"


def test_primary_keys(engine):
    """
    Test if primary keys are correctly defined.
    """
    inspector = inspect(engine)

    for table in ["Doctor", "Schedule", "Shift", "AdminUser"]:
        pk = inspector.get_pk_constraint(table)["constrained_columns"]
        assert pk == ["id"], f"Primary key mismatch for table '{table}'. Expected: ['id'], Found: {pk}"


def test_foreign_keys(engine):
    """
    Test if foreign key constraints are defined correctly.
    """
    inspector = inspect(engine)

    shift_fk = {fk["constrained_columns"][0]: fk["referred_table"] for fk in inspector.get_foreign_keys("Shift")}
    expected_fk = {"schedule_id": "Schedule", "doctor_id": "Doctor"}
    assert shift_fk == expected_fk, f"Foreign key mismatch in 'Shift' table. Expected: {expected_fk}, Found: {shift_fk}"

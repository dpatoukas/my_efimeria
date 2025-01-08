import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Doctor, Schedule, Shift
from database.database_setup import Session

# Setup an in-memory SQLite database for testing
@pytest.fixture(scope='function')
def test_session():
    engine = create_engine('sqlite:///:memory:')  # In-memory DB
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine)
    session = TestingSession()
    yield session
    session.close()

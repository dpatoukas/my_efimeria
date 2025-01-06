import sys
import os

# Add project root to Python path for module resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import database setup and models
from database.database_setup import Base, engine
from database.models import Doctor, Schedule, Shift, AdminUser

def initialize_database():
    """
    Initializes the database by creating all tables defined in the models.
    """
    try:
        print("\n--- Initializing Database ---")

        # Create all tables
        Base.metadata.create_all(engine)
        print("Database initialized successfully!")

    except Exception as e:
        print(f"Database initialization failed: {e}")


if __name__ == "__main__":
    initialize_database()

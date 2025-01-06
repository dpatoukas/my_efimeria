import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
# from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

# Get database URL from environment variables or use default
# DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///clinic_schedule.db')

# Create database engine
# engine = create_engine(DATABASE_URL, echo=True)

# Connect to SQLite database
engine = create_engine('sqlite:///clinic_schedule.db')

# Create session factory
Session = sessionmaker(bind=engine)

# Define Base class for ORM models
Base = declarative_base()



import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch database URL
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/clinic_schedule.db')
print(f"Resolved DB Path: {os.path.abspath('data/clinic_schedule.db')}")

# Create database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
Session = sessionmaker(bind=engine)

# Define Base class for ORM models
Base = declarative_base()

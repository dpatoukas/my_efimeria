from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.database_setup import Base


# Doctor Model
class Doctor(Base):
    """
    Stores doctor information including:
    - ID: Primary Key
    - Name: Doctor's name
    - Days Off: Comma-separated dates off (e.g., '2025-01-01,2025-01-02')
    """
    __tablename__ = 'Doctor'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    days_off = Column(Text, nullable=False)  # Comma-separated dates off


# Schedule Model
class Schedule(Base):
    """
    Stores schedule information including:
    - ID: Primary Key
    - Month: Target month for the schedule
    - Year: Year for the schedule
    - Status: Schedule status (Draft, Approved, Finalized)
    """
    __tablename__ = 'Schedule'
    id = Column(Integer, primary_key=True)
    month = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    status = Column(String, nullable=False)


# Shift Model
class Shift(Base):
    """
    Tracks assigned shifts for doctors including:
    - ID: Primary Key
    - Schedule ID: Foreign Key to Schedule table
    - Doctor ID: Foreign Key to Doctor table
    - Date: Date of the shift
    - Status: Assigned or Unassigned
    """
    __tablename__ = 'Shift'
    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey('Schedule.id'))
    doctor_id = Column(Integer, ForeignKey('Doctor.id'))
    date = Column(String, nullable=False)
    status = Column(String, nullable=False)


# Admin User Model
class AdminUser(Base):
    """
    Manages admin user login credentials including:
    - ID: Primary Key
    - Username: Unique login username
    - Password: Hashed password for authentication
    """
    __tablename__ = 'AdminUser'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

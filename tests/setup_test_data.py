import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Doctor, Schedule, Shift, AdminUser
from database.database_setup import Base

# Database Configuration
DATABASE_URL = "sqlite:///clinic_schedule.db"  # Replace with your actual database URL
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

#Input File 

input_file = './database/test_data/exclusion_test_data.json'

# Clear the Database
def clear_database():
    session.query(Shift).delete()
    session.query(Schedule).delete()
    session.query(Doctor).delete()
    session.query(AdminUser).delete()
    session.commit()
    print("Database cleared successfully.")

def load_test_data():
    # # Get the directory of the script
    # base_dir = os.path.dirname(os.path.abspath(__file__))
    # file_path = os.path.join(base_dir, input_file)  # Use absolute path

    # Load JSON data
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Insert Doctors
    for doc in data['doctors']:
        doctor = Doctor(
            id=doc['id'],
            name=doc['name'],
            days_off=doc['days_off']
        )
        session.add(doctor)

    # Insert Schedules
    for sch in data['schedules']:
        schedule = Schedule(
            id=sch['id'],
            month=sch['month'],
            year=sch['year'],
            status=sch['status']
        )
        session.add(schedule)

    # Insert Shifts
    for shift in data['shifts']:
        new_shift = Shift(
            id=shift['id'],
            schedule_id=shift['schedule_id'],
            doctor_id=shift['doctor_id'],
            date=shift['date'],
            status=shift['status']
        )
        session.add(new_shift)

    # Insert Admin Users
    for admin in data['admin_users']:
        admin_user = AdminUser(
            id=admin['id'],
            username=admin['username'],
            password=admin['password']
        )
        session.add(admin_user)

    # Commit changes
    session.commit()
    print("Test data inserted successfully.")

def print_all_data():
    """
    Prints all the data stored in the database.
    """
    print("\n--- Doctors ---")
    doctors = session.query(Doctor).all()
    for doctor in doctors:
        print(f"ID: {doctor.id}, Name: {doctor.name}, Days Off: {doctor.days_off}")

    print("\n--- Schedules ---")
    schedules = session.query(Schedule).all()
    for schedule in schedules:
        print(f"ID: {schedule.id}, Month: {schedule.month}, Year: {schedule.year}, Status: {schedule.status}")

    print("\n--- Shifts ---")
    shifts = session.query(Shift).all()
    for shift in shifts:
        print(f"ID: {shift.id}, Schedule ID: {shift.schedule_id}, Doctor ID: {shift.doctor_id}, Date: {shift.date}, Status: {shift.status}")

    print("\n--- Admin Users ---")
    admin_users = session.query(AdminUser).all()
    for admin in admin_users:
        print(f"ID: {admin.id}, Username: {admin.username}, Password: {admin.password}")

# Main Function
def main():
    clear_database()
    load_test_data()
    print_all_data()
    session.close()


if __name__ == "__main__":
    main()

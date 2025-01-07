import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from database.database_setup import Session  # Use centralized configuration
from database.models import Doctor, Schedule, Shift, AdminUser

# Input File
input_file = os.path.join(os.path.dirname(__file__), 'test_data/exclusion_test_data.json')

# Create a session
session = Session()

# Clear the Database
def clear_database():
    session.query(Shift).delete()
    session.query(Schedule).delete()
    session.query(Doctor).delete()
    session.query(AdminUser).delete()
    session.commit()
    print("Database cleared successfully.")

# Load Test Data
def load_test_data():
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

# Print All Data
def print_all_data():
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

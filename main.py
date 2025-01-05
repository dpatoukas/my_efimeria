import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.database_to_clinic_request_service import DatabaseToClinicRequestService
from services.doctor_scheduling_service import DoctorSchedulingProblem
from services.solution_service import SolutionService
from database.models import Schedule
from repositories.repository import ScheduleRepository  # Added import
import numpy as np
from database.models import Schedule, Shift, Doctor

# Fetch the schedule for September 2024
def fetch_schedule_data(session, month, year):
    """
    Fetches and prints the schedule details including shifts and assigned doctors.

    Parameters:
    - session: Database session.
    - month (str): Month of the schedule.
    - year (int): Year of the schedule.
    """
    # Retrieve the schedule
    schedule = session.query(Schedule).filter_by(month=month, year=year).first()
    if not schedule:
        print(f"No schedule found for {month} {year}.")
        return

    print(f"\nSchedule for {month} {year}:")
    print(f"Status: {schedule.status}")

    # Fetch all shifts associated with this schedule
    shifts = session.query(Shift).filter_by(schedule_id=schedule.id).all()
    if not shifts:
        print("No shifts assigned.")
        return

    # Print shift details
    for shift in shifts:
        doctor = session.query(Doctor).filter_by(id=shift.doctor_id).first()
        doctor_name = doctor.name if doctor else "Unknown Doctor"
        print(f"Date: {shift.date}, Doctor: {doctor_name}, Status: {shift.status}")

# Database Configuration
DATABASE_URL = "sqlite:///clinic_schedule.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


try:
    # Step 1: Initialize Service and Fetch Clinic Request
    service = DatabaseToClinicRequestService(session)
    clinic_request = service.get_monthly_clinic_request("September", 2024)

    # Print Clinic Request Info
    service.print_request_info(clinic_request)

    # Step 2: Extract Data for Scheduling
    doctorNames = clinic_request['doctorNames']
    doctorPreference = clinic_request['doctorPreference']
    weekendPositionArray = clinic_request['weekendPositions']
    doctorExperience = [1] * len(doctorNames)  # Default experience

    doctorshiftMax = clinic_request['maxShifts']
    doctorshiftMin = clinic_request['minShifts']

    # Step 3: Create DoctorSchedulingProblem Instance
    problem = DoctorSchedulingProblem(
        hardConstraintPenalty=10000,
        listOfDoctors=doctorNames,
        listOfDoctorPreferce=doctorPreference,
        doctorshiftMax=doctorshiftMax,
        doctorshiftMin=doctorshiftMin,
        weekendPositionArray=weekendPositionArray,
        doctorExperience=doctorExperience
    )

    # Print Scheduling Problem Data
    problem.print_problem_data()

    # Step 4: Initialize Solution Service and Generate Solution
    solution_service = SolutionService(problem)
    best_solution = solution_service.run_genetic_algorithm()
    
    # TODO: Reshape the solution to match daily assignments
    # Why Does It Work?
    # 1. Genetic Algorithm Output - The `best_solution` is a flat list with length equal to (number of doctors × number of days).
    # 2. Database Save Function - Expects a nested list grouped by days to map shifts correctly.

    # What Did We Do?
    # - Used numpy to reshape the flat list into (days x doctors) format.
    # - Ensures compatibility with the save_solution_to_db method which processes assignments by days.

    # Example Fix (Apply Later):
    # import numpy as np
    # num_days = 30  # Number of days in the month
    # num_doctors = len(doctorNames)
    # reshaped_solution = np.array(best_solution).reshape(num_days, num_doctors)
    # solution_service.save_solution_to_db(session, "September", 2024, reshaped_solution)
    num_days = 30  # Example: Number of days in the month
    num_doctors = len(doctorNames)
    # Reshape the solution into (days x doctors) format
    reshaped_solution = np.array(best_solution).reshape(num_days, num_doctors)

    # Step 5: Handle Schedule Creation or Retrieval
    try:
        # Attempt to create a new schedule
        schedule = ScheduleRepository.add_schedule(session, "September", 2024)
    except ValueError:
        # Retrieve the last existing schedule if one already exists
        schedule = session.query(Schedule).filter_by(month="September", year=2024).first()

    # Step 6: Save the Solution to Database
    solution_service.save_solution_to_db(session, "September", 2024, reshaped_solution)


    # Final Status
    print("Schedule successfully generated and saved to the database!")
    
    # Call the function to fetch and display the schedule
    fetch_schedule_data(session, "September", 2024)


except Exception as e:
    print(f"An error occurred: {e}")
    session.rollback()  # Rollback in case of errors

finally:
    # Close the session
    session.close()



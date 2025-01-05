import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.database_to_clinic_request_service import DatabaseToClinicRequestService
from services.doctor_scheduling_service import DoctorSchedulingProblem
from services.solution_service import SolutionService
import numpy as np

# Database Configuration
DATABASE_URL = "sqlite:///clinic_schedule.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Initialize Service
service = DatabaseToClinicRequestService(session)

# Generate Clinic Request
clinic_request = service.get_monthly_clinic_request("September", 2024)

# Extract data from clinic_request
doctorNames = clinic_request['doctorNames']
doctorPreference = clinic_request['doctorPreference']
weekendPositionArray = clinic_request['weekendPositions']
doctorExperience = [1] * len(doctorNames)  # Assuming default experience

doctorshiftMax = clinic_request['maxShifts']
doctorshiftMin = clinic_request['minShifts']

# Create DoctorSchedulingProblem instance
problem = DoctorSchedulingProblem(
    hardConstraintPenalty=10000,
    listOfDoctors=doctorNames,
    listOfDoctorPreferce=doctorPreference,
    doctorshiftMax=doctorshiftMax,
    doctorshiftMin=doctorshiftMin,
    weekendPositionArray=weekendPositionArray,
    doctorExperience=doctorExperience
)

# Print all data
service.print_request_info(clinic_request)

# Print Doctor Scheduling Problem data
problem.print_problem_data()

# Generate and Test Example Solution
solution = np.random.randint(2, size=len(doctorNames) * 30)  # Example random solution
problem.printScheduleInfo(solution)

# Initialize Solution Service
solution_service = SolutionService(problem)

# Run Genetic Algorithm
best_solution = solution_service.run_genetic_algorithm()

session.close()

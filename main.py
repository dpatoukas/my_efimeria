from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_to_clinic_request_service import DatabaseToClinicRequestService

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_to_clinic_request_service import DatabaseToClinicRequestService

DATABASE_URL = "sqlite:///clinic_schedule.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Initialize Service
service = DatabaseToClinicRequestService(session)

# Generate Clinic Request
clinic_request = service.get_monthly_clinic_request("September", 2024)

# Print all data
service.print_request_info(clinic_request)
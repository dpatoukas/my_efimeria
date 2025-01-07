import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from services.monthly_clinic_request import create_monthly_clinic_request
from database.models import Doctor, Schedule, Shift
from datetime import datetime
import calendar


class DatabaseToClinicRequestService:
    def __init__(self, session: Session):
        """
        Initialize the service with a database session.
        """
        self.session = session

    def get_monthly_clinic_request(self, month: str, year: int):
        """
        Fetches data from the database and transforms it into a MonthlyClinicRequest object.

        Parameters:
        - month (str): The target month (e.g., "September").
        - year (int): The target year (e.g., 2024).

        Returns:
        - dict: A dictionary representing the MonthlyClinicRequest object.
        """
        # Fetch Schedule
        schedule = self.session.query(Schedule).filter_by(month=month, year=year).first()
        if not schedule:
            print(f"No schedule found for {month} {year}. Using 'NA' as placeholders.")
            schedule_id = "NA"
        else:
            schedule_id = schedule.id

        # Fetch Doctors
        doctors = self.session.query(Doctor).all()
        doctor_names = [doctor.name for doctor in doctors] if doctors else ["NA"]

        # Fetch Days Off (Exclusion List)
        doctor_days_off = {
            doctor.name: doctor.days_off.split(",") if doctor.days_off else []
            for doctor in doctors
        } if doctors else {"NA": []}

        # Generate Calendar Data
        total_days, order_of_days, weekend_positions, number_of_days = self._generate_calendar(month, year)

        # Transform into Preference Matrix
        doctor_preference = self._generate_preference_matrix(doctor_names, doctor_days_off, total_days)

        # Create the MonthlyClinicRequest using the function
        clinic_request = create_monthly_clinic_request(
            googleSheetId=None,
            month=month,
            orderOfDays=order_of_days,
            numberOfDays=number_of_days,
            weekendPositions=weekend_positions,
            doctorNames=doctor_names,
            doctorPreference=doctor_preference,
            totalShifts=[5] * len(total_days),
            minShifts=[2] * len(total_days),
            maxShifts=[4] * len(total_days)
        )

        return clinic_request

    def _generate_calendar(self, month: str, year: int):
        """
        Generates the calendar for the given month and year.

        Returns:
        - total_days: List of datetime objects for each day in the month.
        - order_of_days: List of day names (e.g., "Monday", "Tuesday").
        - weekend_positions: List of 0s and 1s indicating weekends (1 = weekend).
        - number_of_days: List of integers representing days (1 to end of the month).
        """
        # Map month name to month number
        month_number = list(calendar.month_name).index(month)

        # Generate all dates in the given month
        total_days = []
        order_of_days = []
        weekend_positions = []
        number_of_days = []

        # Calculate number of days in the month
        _, num_days = calendar.monthrange(year, month_number)
        for day in range(1, num_days + 1):
            date = datetime(year, month_number, day)
            total_days.append(date)
            order_of_days.append(date.strftime("%A"))  # Full name of the day
            number_of_days.append(day)

            # Mark weekends (Saturday = 5, Sunday = 6)
            if date.weekday() in [5, 6]:
                weekend_positions.append(1)
            else:
                weekend_positions.append(0)

        return total_days, order_of_days, weekend_positions, number_of_days

    def _generate_preference_matrix(self, doctor_names, doctor_days_off, total_days):
        """
        Generates a matrix of doctor availability.

        Parameters:
        - doctor_names: List of doctor names.
        - doctor_days_off: Dictionary with doctor names as keys and lists of off days as values.
        - total_days: List of datetime objects representing the month.

        Returns:
        - List of lists representing preferences (1 = available, 0 = not available).
        """
        preference_matrix = []
        for doctor in doctor_names:
            # print(f"\nDoctor: {doctor}")
            preference = []
            for day in total_days:
                # formatted_date = day.strftime("%Y-%m-%d")
                # print(f"Date: {formatted_date}, Days Off: {doctor_days_off.get(doctor)}, Match: {formatted_date in doctor_days_off.get(doctor, [])}")
                if doctor == "NA":
                    preference.append("NA")  # Placeholder if no doctors
                elif day.strftime("%Y-%m-%d") in doctor_days_off.get(doctor, []):
                    preference.append(0)  # Not available
                else:
                    if day.day <= len(total_days):  # Match the number of days dynamically
                        preference.append(1)  # Available
                    else:
                        preference.append(0)  # Default to unavailable for out-of-bound days
            preference_matrix.append(preference)
        return preference_matrix

    def print_request_info(self, clinic_request):
        """
        Prints all data from the MonthlyClinicRequest dictionary.
        """
        print(f"\nTarget Month: {clinic_request['month']}")
        # print(f"Numbering of Days: {clinic_request['numberOfDays']}")
        # print(f"Order of Days: {clinic_request['orderOfDays']}")
        # print(f"Weekend Positions: {clinic_request['weekendPositions']}")
        print(f"Doctors Available: {clinic_request['doctorNames']}")
        print(f"Doctor Preferences: {clinic_request['doctorPreference']}")
        # print(f"Total Shifts Required/Day: {clinic_request['totalShifts']}")
        print(f"Max and Min Shifts: {clinic_request['maxShifts']}, {clinic_request['minShifts']}")

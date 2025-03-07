from sqlalchemy.orm import Session
from clinic_request import MonthlyClinicRequest
from models import Doctor, Schedule, Shift
from datetime import datetime
import calendar


class DatabaseToClinicRequestService:
    def __init__(self, session: Session):
        """
        Initialize the service with a database session.
        """
        self.session = session

    def get_monthly_clinic_request(self, month: str, year: int) -> MonthlyClinicRequest:
        """
        Fetches data from the database and transforms it into a MonthlyClinicRequest object.

        Parameters:
        - month (str): The target month (e.g., "September").
        - year (int): The target year (e.g., 2024).

        Returns:
        - MonthlyClinicRequest: An object populated with database data.
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

        # Create the MonthlyClinicRequest object
        clinic_request = MonthlyClinicRequest(googleSheetId=None)  # Sheet ID not required
        clinic_request.orderOfDays = order_of_days  # Names of the days
        clinic_request.numberOfDays = number_of_days  # 1 to last day
        clinic_request.month = month
        clinic_request.weekendPositions = weekend_positions
        clinic_request.doctorNames = doctor_names
        clinic_request.doctorPreference = doctor_preference

        # Constant Total Shifts, Max Shifts, and Min Shifts
        clinic_request.totalShifts = [5] * len(total_days)
        clinic_request.minShifts = [2] * len(total_days)
        clinic_request.maxShifts = [4] * len(total_days)

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
            preference = []
            for day in total_days:
                if doctor == "NA":
                    preference.append("NA")  # Placeholder if no doctors
                elif day.strftime("%Y-%m-%d") in doctor_days_off.get(doctor, []):
                    preference.append(0)  # Not available
                else:
                    preference.append(1)  # Available
            preference_matrix.append(preference)
        return preference_matrix

    def print_request_info(self, clinic_request):
        """
        Prints all data from the MonthlyClinicRequest object.
        """
        print(f"\nTarget Month: {clinic_request.month}")
        print(f"Numbering of Days: {clinic_request.numberOfDays}")
        print(f"Order of Days: {clinic_request.orderOfDays}")
        print(f"Weekend Positions: {clinic_request.weekendPositions}")
        print(f"Doctors Available: {clinic_request.doctorNames}")
        print(f"Doctor Preferences: {clinic_request.doctorPreference}")
        print(f"Total Shifts Required/Day: {clinic_request.totalShifts}")
        print(f"Max and Min Shifts: {clinic_request.maxShifts}, {clinic_request.minShifts}")

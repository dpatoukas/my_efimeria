def create_monthly_clinic_request(
    googleSheetId=None,
    month="NA",
    orderOfDays=None,
    numberOfDays=None,
    weekendPositions=None,
    doctorNames=None,
    doctorPreference=None,
    totalShifts=None,
    minShifts=None,
    maxShifts=None
):
    """
    Function to create a MonthlyClinicRequest object.

    Parameters:
    - googleSheetId (str): Google Sheet ID (default: None).
    - month (str): The month for the schedule (default: 'NA').
    - orderOfDays (list): Names of the days in order (default: []).
    - numberOfDays (list): Numbers from 1 to last day (default: []).
    - weekendPositions (list): Positions of weekends (1 for weekends, 0 otherwise) (default: []).
    - doctorNames (list): List of doctor names (default: []).
    - doctorPreference (list): Matrix of preferences (1 = available, 0 = unavailable) (default: []).
    - totalShifts (list): Total shifts required per day (default: []).
    - minShifts (list): Minimum shifts per day (default: []).
    - maxShifts (list): Maximum shifts per day (default: []).

    Returns:
    - dict: A dictionary representing the MonthlyClinicRequest object.
    """
    # Handle default values if not provided
    if orderOfDays is None:
        orderOfDays = []
    if numberOfDays is None:
        numberOfDays = []
    if weekendPositions is None:
        weekendPositions = []
    if doctorNames is None:
        doctorNames = []
    if doctorPreference is None:
        doctorPreference = []
    if totalShifts is None:
        totalShifts = []
    if minShifts is None:
        minShifts = []
    if maxShifts is None:
        maxShifts = []

    # Construct and return the request object as a dictionary
    return {
        "googleSheetId": googleSheetId,
        "month": month,
        "orderOfDays": orderOfDays,
        "numberOfDays": numberOfDays,
        "weekendPositions": weekendPositions,
        "doctorNames": doctorNames,
        "doctorPreference": doctorPreference,
        "totalShifts": totalShifts,
        "minShifts": minShifts,
        "maxShifts": maxShifts
    }

import pytest
from services.monthly_clinic_request import create_monthly_clinic_request


def test_create_monthly_clinic_request_with_all_parameters():
    """Test creating a MonthlyClinicRequest with all parameters."""
    request = create_monthly_clinic_request(
        googleSheetId="sheet123",
        month="January",
        orderOfDays=["Monday", "Tuesday", "Wednesday"],
        numberOfDays=[1, 2, 3],
        weekendPositions=[0, 0, 1],
        doctorNames=["Dr. Alice", "Dr. Bob"],
        doctorPreference=[[1, 1, 0], [0, 1, 1]],
        totalShifts=[2, 2, 2],
        minShifts=[1, 1, 1],
        maxShifts=[3, 3, 3]
    )

    assert request["googleSheetId"] == "sheet123"
    assert request["month"] == "January"
    assert request["orderOfDays"] == ["Monday", "Tuesday", "Wednesday"]
    assert request["numberOfDays"] == [1, 2, 3]
    assert request["weekendPositions"] == [0, 0, 1]
    assert request["doctorNames"] == ["Dr. Alice", "Dr. Bob"]
    assert request["doctorPreference"] == [[1, 1, 0], [0, 1, 1]]
    assert request["totalShifts"] == [2, 2, 2]
    assert request["minShifts"] == [1, 1, 1]
    assert request["maxShifts"] == [3, 3, 3]


def test_create_monthly_clinic_request_with_defaults():
    """Test creating a MonthlyClinicRequest with default parameters."""
    request = create_monthly_clinic_request()

    assert request["googleSheetId"] is None
    assert request["month"] == "NA"
    assert request["orderOfDays"] == []
    assert request["numberOfDays"] == []
    assert request["weekendPositions"] == []
    assert request["doctorNames"] == []
    assert request["doctorPreference"] == []
    assert request["totalShifts"] == []
    assert request["minShifts"] == []
    assert request["maxShifts"] == []


def test_create_monthly_clinic_request_partial_parameters():
    """Test creating a MonthlyClinicRequest with partial parameters."""
    request = create_monthly_clinic_request(
        month="February",
        doctorNames=["Dr. Alice"],
        doctorPreference=[[1, 0, 1]]
    )

    assert request["googleSheetId"] is None
    assert request["month"] == "February"
    assert request["orderOfDays"] == []
    assert request["numberOfDays"] == []
    assert request["weekendPositions"] == []
    assert request["doctorNames"] == ["Dr. Alice"]
    assert request["doctorPreference"] == [[1, 0, 1]]
    assert request["totalShifts"] == []
    assert request["minShifts"] == []
    assert request["maxShifts"] == []

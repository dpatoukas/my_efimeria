from sqlalchemy.orm import Session
from repositories.repository import DoctorRepository

class DoctorService:
    """
    Service layer for handling doctor-related business logic and delegating database
    operations to the repository.
    """

    @staticmethod
    def get_all_doctors(session: Session):
        """
        Retrieves all doctors from the database.

        Args:
            session (Session): Database session.

        Returns:
            list: List of all doctors.
        """
        return DoctorRepository.get_all_doctors(session)

    @staticmethod
    def get_doctor_by_id(session: Session, doctor_id: int):
        """
        Retrieves a specific doctor and their assigned shifts by ID.

        Args:
            session (Session): Database session.
            doctor_id (int): ID of the doctor.

        Returns:
            dict: Doctor details and their shifts.

        Raises:
            ValueError: If the doctor does not exist.
        """
        return DoctorRepository.get_doctor_with_shifts(session, doctor_id)

    @staticmethod
    def create_doctor(session: Session, name: str, days_off: str):
        """
        Creates a new doctor.

        Args:
            session (Session): Database session.
            name (str): Name of the doctor.
            days_off (str): Comma-separated string of days off.

        Returns:
            Doctor: Newly created doctor.

        Raises:
            ValueError: If validation fails or a duplicate doctor name exists.
        """
        # Validate inputs
        if not name or not days_off:
            raise ValueError("Name and days off are required.")

        return DoctorRepository.add_doctor(session, name, days_off)

    @staticmethod
    def update_doctor(session: Session, doctor_id: int, name: str = None, days_off: str = None):
        """
        Updates the details of a specific doctor.

        Args:
            session (Session): Database session.
            doctor_id (int): ID of the doctor to update.
            name (str): Updated name of the doctor.
            days_off (str): Updated days off.

        Returns:
            Doctor: Updated doctor.

        Raises:
            ValueError: If validation fails or doctor does not exist.
        """
        if not name and not days_off:
            raise ValueError("At least one field (name or days_off) is required to update.")

        return DoctorRepository.update_doctor(session, doctor_id, name, days_off)

    @staticmethod
    def delete_doctor(session: Session, doctor_id: int):
        """
        Deletes a doctor by ID.

        Args:
            session (Session): Database session.
            doctor_id (int): ID of the doctor to delete.

        Returns:
            bool: True if deletion was successful.

        Raises:
            ValueError: If the doctor does not exist.
        """
        return DoctorRepository.delete_doctor(session, doctor_id)

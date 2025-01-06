import numpy as np

class DoctorSchedulingProblem:
    """
    Encapsulates the doctor scheduling problem for a clinic request.
    Evaluates constraint violations and computes a schedule cost.
    """

    def __init__(self, hardConstraintPenalty, listOfDoctors, listOfDoctorPreferce, doctorshiftMax, doctorshiftMin, weekendPositionArray, doctorExperience):
        """
        Initializes the DoctorSchedulingProblem with input data and constraints.

        Parameters:
        - hardConstraintPenalty (int): Penalty cost for violating hard constraints.
        - listOfDoctors (list): Names of doctors.
        - listOfDoctorPreferce (list): Availability preferences for each doctor.
        - doctorshiftMax (list): Maximum shifts allowed per day.
        - doctorshiftMin (list): Minimum shifts required per day.
        - weekendPositionArray (list): Array indicating weekend days (1 = weekend).
        - doctorExperience (list): Experience level of each doctor.
        """
        self.hardConstraintPenalty = hardConstraintPenalty
        self.doctors = listOfDoctors
        self.doctorExperience = doctorExperience
        self.weekendPositionArray = weekendPositionArray
        self.doctorShiftPreference = listOfDoctorPreferce
        self.doctorshiftMax = doctorshiftMax
        self.doctorshiftMin = doctorshiftMin
        self.doctorMaxShiftPerMonth = 7
        self.weeks = 4

        # Debugging information
        print("DoctorSchedulingProblem initialized with:")
        print("Hard Constraint Penalty:", self.hardConstraintPenalty)
        print("Doctors:", self.doctors)
        print("Experience Levels:", self.doctorExperience)
        print("Shift Preferences:", self.doctorShiftPreference)
        print("Max Shifts per Day:", self.doctorshiftMax)
        print("Min Shifts per Day:", self.doctorshiftMin)
        print("Weekend Positions:", self.weekendPositionArray)

    def __len__(self):
        """
        Returns the total number of shifts in the schedule.
        """
        return len(self.doctors) * 30

    def getCost(self, schedule):
        """
        Calculates the total cost of constraint violations in the given schedule.

        Parameters:
        - schedule (list): Binary values representing the schedule.

        Returns:
        - int: Total penalty cost.
        """
        doctorShiftDict = self.getDoctorWeekShifts(schedule)
        doctorConsecutiveShiftViolations = self.doctorCountConsecutiveShiftViolations(doctorShiftDict)
        doctorShiftsPerWeekViolations = self.doctorCountShiftsPerWeekViolations(doctorShiftDict)
        doctorShiftsPerDayViolations = self.doctorsCountShiftsPerDayViolation(doctorShiftDict)
        doctorShiftPeferenceViolation = self.doctorCountShiftPreferenceViolations(doctorShiftDict)
        # TODO: Include soft constraints that make sense
        # doctorDistanceOfDaysViolation = self.doctorCountDistanceOfDaysViolation(doctorShiftDict)
        # doctorLazyDaysViolation = self.doctorCountLazyDaysViolation(doctorShiftDict)
        # doctorWeekendsViolations = self.doctorCountNumberOfWeekends(doctorShiftDict)
        # softContstraintViolations = doctorLazyDaysViolation + doctorDistanceOfDaysViolation + doctorWeekendsViolations

        hardContstraintViolations = (
            doctorShiftPeferenceViolation +
            doctorShiftsPerDayViolations +
            doctorShiftsPerWeekViolations +
            doctorConsecutiveShiftViolations
        )

        return self.hardConstraintPenalty * hardContstraintViolations

    def getDoctorWeekShifts(self, schedule):
        """
        Converts the schedule into a dictionary format, grouped by doctors.

        Parameters:
        - schedule (list): Binary values representing the schedule.

        Returns:
        - dict: Dictionary mapping each doctor to their assigned shifts.
        """
        shiftsPerDoctor = 30
        doctorShiftsDict = {}
        shiftIndex = 0

        for doctor in self.doctors:
            doctorShiftsDict[doctor] = schedule[shiftIndex:shiftIndex + shiftsPerDoctor]
            shiftIndex += shiftsPerDoctor

        return doctorShiftsDict

    def doctorCountConsecutiveShiftViolations(self, doctorShiftsDict):
        """
        Counts violations where doctors are assigned consecutive shifts.

        Parameters:
        - doctorShiftsDict (dict): Dictionary of doctors and their assigned shifts.

        Returns:
        - int: Number of violations.
        """
        violations = 0
        for doctorShifts in doctorShiftsDict.values():
            for shift1, shift2 in zip(doctorShifts, doctorShifts[1:]):
                if shift1 == 1 and shift2 == 1:
                    violations += 1
        return violations

    def doctorCountShiftsPerWeekViolations(self, doctorShiftDic):
        """
        Counts violations for exceeding or falling short of weekly shift limits.

        Parameters:
        - doctorShiftDic (dict): Dictionary of doctors and their assigned shifts.

        Returns:
        - int: Number of violations.
        """
        violations = 0
        for doctorShifts in doctorShiftDic.values():
            weeklyShifts = sum(doctorShifts)
            if weeklyShifts > self.doctorMaxShiftPerMonth:
                violations += weeklyShifts - self.doctorMaxShiftPerMonth
            if weeklyShifts < 5:
                violations += 5 - weeklyShifts
        return violations

    def doctorsCountShiftsPerDayViolation(self, doctorShiftDic):
        """
        Counts violations for daily shift limits (min and max).

        Parameters:
        - doctorShiftDic (dict): Dictionary of doctors and their assigned shifts.

        Returns:
        - int: Number of violations.
        """
        totalPerShiftList = [0] * 30
        violations = 0

        for doctor in doctorShiftDic:
            totalPerShiftList = np.add(totalPerShiftList, doctorShiftDic[doctor])

        for day in range(len(totalPerShiftList)):
            if totalPerShiftList[day] > self.doctorshiftMax[day]:
                violations += totalPerShiftList[day] - self.doctorshiftMax[day]
            if totalPerShiftList[day] < self.doctorshiftMin[day]:
                violations += self.doctorshiftMin[day] - totalPerShiftList[day]

        return violations

    def doctorCountShiftPreferenceViolations(self, doctorShiftDic):
        """
        Counts violations where doctors are assigned shifts against their preferences.

        Parameters:
        - doctorShiftDic (dict): Dictionary of doctors and their assigned shifts.

        Returns:
        - int: Number of violations.
        """
        violations = 0
        for doctorIndex, shiftPreference in enumerate(self.doctorShiftPreference):
            doctorWeeklySchedule = doctorShiftDic[self.doctors[doctorIndex]]
            for pref, shift in zip(shiftPreference, doctorWeeklySchedule):
                if pref == 0 and shift == 1:
                    violations += 1
        return violations

    def printScheduleInfo(self, schedule):
        """
        Prints the schedule and violation details.

        Parameters:
        - schedule (list): Binary values representing the schedule.
        """
        doctorShiftDict = self.getDoctorWeekShifts(schedule)
        print("Schedule for each Doctor:")
        for doctor in doctorShiftDict:
            print(doctor, ":", doctorShiftDict[doctor])
        print("Total Cost of Solution =", self.getCost(schedule))

    def print_problem_data(self):
        """
        Prints the problem data and constraints.
        """
        print("Scheduling Doctor Problem Ready")
        print("Doctors:", self.doctors)
        # print("Experience Levels:", self.doctorExperience)
        print("Shift Preferences:", self.doctorShiftPreference)
        # print("Max Shifts per Day:", self.doctorshiftMax)
        # print("Min Shifts per Day:", self.doctorshiftMin)
        # print("Weekend Positions:", self.weekendPositionArray)

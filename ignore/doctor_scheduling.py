import numpy as np
from clinic_request import MonthlyClinicRequest
import os
import csv

#self.doctorshiftMin = [2, 2, 2, 2, 2, 2, 2, 7, 2, 2, 2, 2, 2, 2, 2, 7, 2, 2, 2, 2, 2, 2,
#            2, 7, 2, 2, 2, 2, 2, 2]

#self.doctorshiftMax = [3, 3, 3, 3, 3, 3, 3, 8, 3, 3, 3, 3, 3, 3, 3, 8, 3, 3, 3, 3, 3, 3,
#            3, 8, 3, 3, 3, 3, 3, 3]

class DoctorSchedulingProblem:
    """
    This class encaplsulates the doctor scheduling problem given on a cliniq request.
    The problem is a sheduling problem that needs to fit a number of doctors to a shift request from the clinic
    The problem has a number of requirements that are represented as violations. Some violations are violating a hard constraint 
    and other soft constraints. 
    The class has methods to evaluate the cost of a given schedule
    The cost is calculated by adding the number of the cost of violations 
    """
    def __init__(self, hardConstraintPenalty, listOfDoctors, listOfDoctorPreferce, doctorshiftMax, doctorshiftMin, weekendPositionArray, doctorExperience):
        """Constructor to the DoctorSchedulingProblem 

        Parameters
        ----------
        param hardConstraintPenalty: int
            The cost of a hard constraint violation
        listOfDoctors: array
            An array with the names of doctors
        listOfDoctorPreferce: array
            An array of arrays with the days each doctor can work
        doctorshiftMax: array
            The maximum amount of days that need to be scheduled for each day
        doctorshiftMin: array
            The minimum amount of days that need to be scheduled for each day
        weekendPositionArray: array 
            An array that describes the days that belong to a weekend/bank holiday
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
    
    def __len__(self):
        """
        :return: the number of shifts in the schedule
        """
        return len(self.doctors) * 30
        
    def getCost(self, schedule):
        """
        Calculates the total cost of the various violations in the given schedule
        Parameters
        ----------
        schedule: array 
            a list of binary values describing the given schedule        
        Returns
        -------
        The total cost of the given schedule
        """
        #convert entire schedule into a dictionary with a separate schedule for each doctor:
        doctorShiftDict = self.getDoctorWeekShifts(schedule)

        #Calculate the cost of each violation
        #Doctors are not allowed to do 2 consecutive shifts
        doctorConsecutiveShiftViolations = self.doctorCountConsecutiveShiftViolations(doctorShiftDict)
        #Doctors are not allowed to do more than doctorMaxShiftPerMonth
        doctorShiftsPerWeekViolations = self.doctorCountShiftsPerWeekViolations(doctorShiftDict)
        #The numebr of doctors scheduled in a day should be between doctorshiftMax and doctorshiftMin
        doctorShiftsPerDayViolations = self.doctorsCountShiftsPerDayViolation(doctorShiftDict)
        #Distance between two shifts must be maximized 
        doctorDistanceOfDaysViolation = self.doctorCountDistanceOfDaysViolation(doctorShiftDict)
        #Doctors prefer to work less than 2 days per week 
        doctorLazyDaysViolation = self.doctorCountLazyDaysViolation(doctorShiftDict)
        #Doctors should only be scheduled in the days that they want to work  
        doctorShiftPeferenceViolation = self.doctorCountShiftPreferenceViolations(doctorShiftDict)
        #Doctors prefer to be working 2 or less weekends 
        doctorWeekendsViolations = self.doctorCountNumberOfWeekends(doctorShiftDict)
        
        #Calculate the cost of the violations:
        hardContstraintViolations = doctorShiftPeferenceViolation + doctorShiftsPerDayViolations + doctorShiftsPerWeekViolations +doctorConsecutiveShiftViolations
        softContstraintViolations = doctorLazyDaysViolation + doctorDistanceOfDaysViolation + doctorWeekendsViolations


        return self.hardConstraintPenalty * hardContstraintViolations + softContstraintViolations

    def getDoctorWeekShifts(self, schedule):
        """
        Converts the entire schedule into a dictionary with a separate schedule for each doctor
        Parameters
        ----------
        schedule: array 
            a list of binary values describing the given schedule        
        Returns
        -------
        A dictionary with each doctor as a key and the corresponding shifts as the value
        """
        shiftsPerDoctor = 30 #Each shift is a day within the week
        doctorShiftsDict = {}
        shiftIndex = 0

        for doctor in self.doctors:
            doctorShiftsDict[doctor] = schedule[shiftIndex:shiftIndex + shiftsPerDoctor]
            shiftIndex += shiftsPerDoctor

        return doctorShiftsDict
    
    def doctorExperieceViolation(self,doctorShiftDict):
        """
        Each day the number of experienced doctors must be bigger than the number of non-experienced doctors 
        ----------
        doctorShiftsDict: dict 
            a dictionary with a separate schedule for each doctor                       
        Returns
        -------
        count of violations found
        """
        for doctor,index in doctorShiftDict:
            return 0
        
        
    def doctorCountConsecutiveShiftViolations(self, doctorShiftsDict):
        """
        Counts the consecutive shift violations in the schedule
        Parameters
        ----------
        doctorShiftsDict: dict 
            a dictionary with a separate schedule for each doctor                       
        Returns
        -------
        count of violations found
        """
        violations = 0
        # iterate over the shifts of each nurse:
        for doctorShifts in doctorShiftsDict.values():
            # look for two cosecutive '1's:
            for shift1, shift2 in zip(doctorShifts, doctorShifts[1:]):
                if shift1 == 1 and shift2 == 1:
                    violations += 1
        return violations

    def doctorCountShiftsPerWeekViolations(self, doctorShiftDic):
        """
        Counts the max-shifts-per-week violations in the schedule
                Counts the consecutive shift violations in the schedule
        Parameters
        ----------
        doctorShiftsDict: dict 
            a dictionary with a separate schedule for each doctor                       
        Returns
        -------
        count of violations found
        """
        violations = 0
        # iterate over the shifts of each nurse:
        for doctorShifts in doctorShiftDic.values(): 
            # iterate over the shifts of each weeks:
            weeklyShifts = sum(doctorShifts)
            if weeklyShifts > self.doctorMaxShiftPerMonth:
                violations += weeklyShifts - self.doctorMaxShiftPerMonth
            if weeklyShifts < 5 :
                violations += 5 - weeklyShifts             
        return violations
    
    def doctorsCountShiftsPerDayViolation(self, doctorShiftDic):
        """
        Counts the number-of-nurses-per-shift violations in the schedule
        Parameters
        ----------
            doctorShiftDic: dict
                 a dictionary with a separate schedule for each nurse
        Returns
        -------
        count of violations found
        """
        #calculate the total shifts allocated by the schedule
        totalPerShiftList = [0] * 30

        violations = 0
        #itterate over all doctors shifts dictionary
        for doctor in doctorShiftDic:
            # totalPerShiftList + doctorShiftDic[doctor]
            totalPerShiftList = np.add(totalPerShiftList, doctorShiftDic[doctor])

        for day in range(len(totalPerShiftList)):
            #count number of violations over maximum 
            if totalPerShiftList[day] > self.doctorshiftMax[day]:
                violations += totalPerShiftList[day] - self.doctorshiftMax[day]
            #count  number of violations over minimum
            if totalPerShiftList[day] < self.doctorshiftMin[day]:
                violations += self.doctorshiftMin[day] - totalPerShiftList[day]

        return violations    

    def doctorCountShiftPreferenceViolations(self, doctorShiftDic):
        """
        Counts the doctor-preferences violations in the schedule
        Parameters
        ----------
            doctorShiftDic: dict
                 a dictionary with a separate schedule for each nurse
        Returns
        -------
        count of violations found
        """
        violations = 0
        for doctorIndex, shiftPreference in enumerate(self.doctorShiftPreference):
            doctorWeeklySchedule = doctorShiftDic[self.doctors[doctorIndex]]
            for pref, shift in zip(shiftPreference,doctorWeeklySchedule):
                if pref == 0 and shift == 1:
                    violations += 1

        return violations
    
    def doctorCountDistanceOfDaysViolation(self, doctorShiftDic):
        """
        Counts the doctor-preferences distance of daysviolations in the schedule
        Parameters
        ----------
            doctorShiftDic: dict
                 a dictionary with a separate schedule for each nurse
        Returns
        -------
        count of violations found
        """
        #TODO: Find a better way to make a violation appear. The logic is that doctors prefer more days free between two shifts
        # Now we penalize shifts that have distance of two days.  
        
        violations = 0
        for doctorIndex,Name in enumerate(doctorShiftDic):
            start = False
            dist = 0
            # print(doctorShiftDic[Name])
            for shift in doctorShiftDic[Name]:
                # print('Shift', shift)
                if shift == 1 and start:
                    dist += 1
                    if dist == 2:
                        violations += 1
                        # print('Distance', dist)
                        # print(Name, doctorShiftDic[Name])
                    start = False
                    dist = 0
                if shift == 1 and not start :
                    start = True
                if shift == 0 and start:
                    dist += 1
        
        return violations


    def doctorCountLazyDaysViolation(self, doctorShiftDic):
        """
        Counts the shifts per week and if it is above 2 days it counts as violation
        Parameters
        ----------
            doctorShiftDic: dict
                 a dictionary with a separate schedule for each nurse
        Returns
        -------
        count of violations found
        """
        #TODO: Find a better way to make a violation appear. The logic is that doctors prefer more days free between two shifts
        # Now we penalize shifts that have distance of two days.  
        violations = 0

        for index,name in enumerate(doctorShiftDic):
            if (sum(doctorShiftDic[name])/4) > 2:
                violations += 1

        return violations
    
    def doctorCountNumberOfWeekends(self, doctorShiftDic):
        """
        Doctors would like to work as few weekends as possible, we consider two weekend days as the limit 
        if more than two weekends are scheduled we consider it as violation 
        #TODO: this could be better
        Parameteres
        ----------
            doctorShiftDic: dict
                 a dictionary with a separate schedule for each nurse
        Returns
        -------
        count of violations found
        """
        violations = 0
        count = 0

        for doctorIndex, doctorName in enumerate(doctorShiftDic):
            for dayIndex,day in enumerate(doctorShiftDic[self.doctors[doctorIndex]]):
                if self.weekendPositionArray[dayIndex] == 1 and day == 1:
                    count += 1  
            if count > 2:
                violations += count - 2
                # print(doctorName,dayIndex)
            count = 0

        return violations

    def printScheduleInfo(self, schedule):
        """
        Prints the schedule and violations details
        Parameters
        ----------
            schedule: a binary weekly schedule 
        """

        #convert entire schedule into a dictionary with a separate schedule for each doctor:
        doctorShiftDict = self.getDoctorWeekShifts(schedule)
        print("Schedule for each Doctor:")
        for doctor in doctorShiftDict:  # all shifts of a single nurse
            print(doctor, ":", doctorShiftDict[doctor])
        print()

        #Calculate the cost of each violation
        #Doctors are not allowed to do 2 consecutive shifts
        print("Consecutive shift violations = ",self.doctorCountConsecutiveShiftViolations(doctorShiftDict))
        print()
        #Doctors are not allowed to do more than doctorMaxShiftPerMonth
        print("Shifts Per Week Violations = ", self.doctorCountShiftsPerWeekViolations(doctorShiftDict))
        print()
        #The numebr of doctors scheduled in a day should be between doctorshiftMax and doctorshiftMin
        print("Number of doctors per day Violations = ", self.doctorsCountShiftsPerDayViolation(doctorShiftDict))
        print()
        #Distance between two shifts must be maximized 
        print("Distance between two shifts Violations = ", self.doctorCountDistanceOfDaysViolation(doctorShiftDict))
        print()
        #Doctors prefer to work less than 2 days per week 
        print("Two shifts per week Violation = ", self.doctorCountLazyDaysViolation(doctorShiftDict))
        print()
        #Doctors should only be scheduled in the days that they want to work  
        print("Day preference Violations = ", self.doctorCountShiftPreferenceViolations(doctorShiftDict)) 
        print()
        #Doctors prefer to be working 2 or less weekends 
        print("Weekend Violations = ",self.doctorCountNumberOfWeekends(doctorShiftDict))
        print()
        
        print('Total Cost of Solution = ', self.getCost(schedule))   
        print()



def readSolutionData():
    """Gets and prints the spreadsheet's header columns

    Parameters
    ----------
    file_loc : str
        The file location of the spreadsheet
    print_cols : bool, optional
        A flag used to print the columns to the console (default is
        False)

    Returns
    -------
    list
        a list of strings used that are the header columns
    """
    absolutePath = os.path.dirname(os.path.abspath(__file__))
    filename = '/solution.csv'
    path =  filename
    filepath = absolutePath + path
    with open(filepath, 'r', encoding='utf-8-sig', newline='') as file:
        reader = csv.reader(file)

        data = []
        for index,row in enumerate(reader):
            data.append(row)
        return data
    
def formatSolutionData(data):

    solutionArray = []
    for row in data:
        elements = row[0].split()
        for element in elements:
            if element == '1':
                solutionArray.append(1)
            if element == '0':
                solutionArray.append(0)
    
    return(solutionArray)

    #TODO Dates and Month and Doctos Name have a dependecy fix that
# testing the class:
def main():
    #get the data from Google
    SAMPLE_SPREADSHEET_ID = '1W7Zcz75bw3usVNZCfX0HAASmMuzExC-5DqDPedfjX3k'
    nr = MonthlyClinicRequest(SAMPLE_SPREADSHEET_ID)

    # create a problem instance:
    doctors = DoctorSchedulingProblem(10000,nr.doctorNames,nr.doctorPreference,nr.totalShifts,nr.totalShifts,nr.weekendPositions,nr.doctorExperience)

    print()
    print("Solution")
    testSolution = formatSolutionData(readSolutionData())
    print(testSolution)
    print(len(testSolution))
    testSolution = np.array(testSolution)
    rsz = np.reshape(testSolution, (17,30))
    print(rsz)
    doctors.printScheduleInfo(testSolution)

    # solutionSize = len(doctors.doctors) * 30
    # randomSolution = np.random.randint(2, size= solutionSize)
    # print("Random Solution")
    # print(randomSolution)
    # doctors.printScheduleInfo(randomSolution)


if __name__ == "__main__":
    main()
import requests
import os
import numpy as np
import csv

class MonthlyClinicRequest:
    """
    This class encaplsulates the request from the clinic to find a schedule for the specific problem statements
    The idea is that a Monthly Cliniq Request is coming from a Spreadsheet hosted in google spreadsheets 
    The spreadsheet should have a fixed structure to be parsed by this class. Once the sheet is parsed and data are ready to be consumed
    the data can be used to create the doctor scheduling problem 
    """
    def __init__(self, googleSheetId):
        """The class constructor should read the googleSheet and populate all the members of the class that are needed for the problem 
        statement. 
        The workflow should be the following 
        1. Download data from 'Input' Sheet -> CSV file in tmp folder
        2. Download data from 'ExclusionList' Sheet: (This is where doctors declared their OFF days)-> CSV file in tmp folder
        3. Extract data from CSV
        Parameters
        ----------
        googleSheetID : str
            The file location of the spreadsheet
        """
        self.googleSheetId = googleSheetId
        #Download data and save them as CSV
        self.downloadCSVFromServer('Input')
        self.downloadCSVFromServer('ExclusionList')
        #Extract Input Data and Days that the doctors need to be excluded 
        self.inputCSVData = self.extractDataFromCSV('Input')
        self.exclCSVData = self.extractDataFromCSV('ExclusionList')
        #Extract information regarding the month 
        self.orderOfDays ,self.numberOfDays ,self.month = self.getDatesAndMonth(self.inputCSVData)
        self.weekendPositions = self.getWeekendPositions()
        #Extract information regarding the doctors
        self.doctorNames = self.getDoctorNames(self.inputCSVData)
        self.doctorPreference = self.getDoctorPreference(self.exclCSVData)
        #Extract information regarding shifts
        self.totalShifts = self.getTotalShifts(self.getNShifts(self.inputCSVData),self.getTShifts(self.inputCSVData))
        #Calculate Minimun and Maximum Shifts allowed 
        self.minShifts, self.maxShifts = self.getMinMaxShifts(self.totalShifts)        

    def downloadCSVFromServer(self, sheetName):
        """Download data from an online google spreadsheet with public access and save it to a CSV file
        in the tmp directory 
        Parameters
        ----------
        param sheetName: str
            sheetName to get the data from
        """
        request = 'https://docs.google.com/spreadsheets/d/' + self.googleSheetId + '/gviz/tq?tqx=out:csv&sheet=' + sheetName
        response = requests.get(request)

        #Save the data to tmp folder
        outDir = 'tmp/'
        outName = 'CSVRequest_' + sheetName + '.csv'
        os.makedirs(outDir, exist_ok = True)

        if response.status_code == 200:
            filepath = os.path.join(outDir, outName)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print('CSV file saved to: {}'.format(filepath))

    def extractDataFromCSV(self, sheetName):
        """Open a CSV file and read the data

        Parameters
        ----------
        sheetName: str
            sheetName to get the data from
        
        Returns
        -------
        data
            an array of arrays, each array contains a line of the sheet
        """
        absolutePath = os.path.dirname(os.path.abspath(__file__))
        filename = 'CSVRequest_' + sheetName + '.csv'
        path = '/tmp/' + filename
        filepath = absolutePath + path
        with open(filepath, 'r', encoding='utf-8-sig', newline='') as file:
            reader = csv.reader(file)

            data = []
            for index,row in enumerate(reader):
                data.append(row)
            return data

    def getDatesAndMonth(self,inputData):
        """Extract the calendar from the inputData extraxted from the 'Input' Sheet

        Parameters
        ----------
        param inputData: array of arrays with extracted data
        Returns
        -------
        orderOfDays
            an array strings presenting the order of days within the month of the request 
        numberOfDays
            an array of numbers from 1-30 presenting the order of dates within the month
        month: str
            the month for the request
        """
        month = inputData[0][0]
        orderOfDays = inputData[0][1:]
        numberOfDays = inputData[1][1:]
        orderOfDays = list(filter(lambda x: x != '',orderOfDays))
        numberOfDays = list(filter(lambda x: x != '',numberOfDays))
        
        return orderOfDays , numberOfDays, month
    
    def getDoctorNames(self, inputData):
        """Extract doctor names from the inputData

        Parameters
        ----------
        param inputData: array of arrays with extracted data
        Returns
        -------
        doctorNames
            an array of strings presenting the names of the doctors available the input month
        """
        doctorNames = []
        for doctor in inputData[3:]:
            if doctor[0] != 'TShifts' and doctor[0] != 'NShifts' and doctor[0] != 'Totals Shits':
                doctorNames.append(doctor[0])
        
        return doctorNames

    def getTShifts(self, inputData):
        """Extract TShifts from the input data

        Parameters
        ----------
        param inputData: array of arrays with extracted data
        Returns
        -------
        TShifts
            an array which specifies how many TShifts exist per day for the month  
        """
        TShifts = []
        for row in inputData:
            if row[0] == 'TShifts':
                for i in row:
                    if i.isnumeric():
                        TShifts.append(int(i))
        
        return TShifts

    def getNShifts(self, inputData):
        """Extract NShifts from the input data

        Parameters
        ----------
        param inputData: array of arrays with extracted data
        Returns
        -------
        NShifts
            an array which specifies how many NShifts exist per day for the month  
        """
        NShifts = []
        for row in inputData:
            if row[0] == 'NShifts':
                for i in row:
                    if i.isnumeric():
                        NShifts.append(int(i))      
        return NShifts

    def getTotalShifts(self, NShifts, TShifts):
        """Add NShift and TShifts and return the total shifts per day
        Parameters
        ----------
        NShifts 
            array of NShifts
        TShifts 
            array of TShifts

        Returns
        -------
        totalShifts
            an array for the total shifts per day for the whole month  
        """
        totalShifts = np.add(NShifts,TShifts)
        return totalShifts
    
    def getDoctorPreference(self, inputData):
        """get the matrix with the days each doctor can work.
        
        Parameters
        ----------
        inputData: 
            a matrix of the days doctors have declared that they cannot work(ExclusionList data in the spreadsheet)
        Returns
        -------
        doctorPreference            
            an array of arrays with the days each doctor can work size = len(doctors)*30 
        """
        doctorPreference = []
        preference = []
        for index,doctor in enumerate(inputData[3:]):
            if doctor[0] == self.doctorNames[index]:
                for element in doctor[1:]:
                    if element == 'OFF':
                        #if they have not declared it the the ExclusionList it means its a preference
                        preference.append(0)
                    else: 
                        #else its not a preference
                        preference.append(1)
                doctorPreference.append(preference)
                preference = []
    
        return doctorPreference

    def getWeekendPositions(self):
        """Get an array where the position of weekends is noted with 1 
        Returns
        -------
        workingWeekendsArray            
            an array that contains all the weekends of the month noted with 1
        """
        workingWeekendsArray = []
        for day in self.orderOfDays:
            if day == 'Δ':
                workingWeekendsArray.append(0)
            if day == 'ΤΡ':
                workingWeekendsArray.append(0)
            if day == 'Τ':
                workingWeekendsArray.append(0)
            if day == 'ΠΕ':
                workingWeekendsArray.append(0)
            if day == 'Π':
                workingWeekendsArray.append(0)
            if day == 'Σ':
                workingWeekendsArray.append(1)
            if day == 'Κ':
                workingWeekendsArray.append(1)
        
        return workingWeekendsArray


    def getMinMaxShifts(self, totalShifts):
        """The shifts on a normal day can be 2-3 and on a hard day 7-9. 
        Given the state of the input data we can derive the arrays for min and max required shifts   
        Parameter
        ---------
        totalShifts
            the array of the totalShifts requested by the Input sheet 
        Returns
        -------
        minShifts          
            an array that contains the minimum number of shifts on each day
        maxShifts
            an array that contains the maximum number of shifts one each day
        """
        maxShifts = []
        minShifts = []

        for day in totalShifts:
            if day < 5:
                minShifts.append(2)
                maxShifts.append(3)
            if day >= 5:
                minShifts.append(7)
                maxShifts.append(9)
        return minShifts,maxShifts 
          
    def printRequestInfo(self):
        #Download Input Sheet
        self.downloadCSVFromServer('Input')
        self.downloadCSVFromServer('ExclusionList')
        
        print('Target Month:' ,self.month)
        print('Numbering of days:' ,self.numberOfDays)
        print('Order of days:' ,self.orderOfDays)
        print('Weekend Array: ', self.weekendPositions)        
        
        print('Doctors Available: ', self.doctorNames)
        print('Doctor Preference: ', self.doctorPreference)
        print('Total Shift Required/day: ', self.totalShifts)
        print('Max and Min Shifts: ', self.maxShifts, self.minShifts)
        


def main():

    nr = MonthlyClinicRequest('1W7Zcz75bw3usVNZCfX0HAASmMuzExC-5DqDPedfjX3k')
    nr.printRequestInfo()


if __name__ == "__main__":
    main()
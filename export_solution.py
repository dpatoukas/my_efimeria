import csv
import numpy as np
import clinic_request as pdata
from doctor_scheduling import DoctorSchedulingProblem
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
import csv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1W7Zcz75bw3usVNZCfX0HAASmMuzExC-5DqDPedfjX3k"
VALUE_INPUT_OPTION  = 'USER_ENTERED'
SPREADSHEET_OUTPUT_CELL = 'Output!A5'   

class ExportSchedulingSolution:

    def __init__(self, scheduleOfDoctors,spreadsheet):
        """
        :param the list of doctors for this solution:
        :param the shedule to be uploaded 
        """
        self.doctorShiftsDict = scheduleOfDoctors
        self.writebuffer = self.makeRow()
        self.credentials = self.getCredentials()
        self.writeBufferToFile()

        self.spreadsheet_id = spreadsheet
        self.range_name = SPREADSHEET_OUTPUT_CELL
        self.value_input_option = VALUE_INPUT_OPTION
        
    def makeRow(self):
        
        writebuffer = []
        for doctor in self.doctorShiftsDict:
            row = []
            row.append(str(doctor))
            for shift in self.doctorShiftsDict[doctor]:
                row.append(str(shift))
            writebuffer.append(row)
        
        return writebuffer
    

    def writeBufferToFile(self):
        with open('solution.csv', 'w+', encoding='utf-8',newline='') as csvfile:
            fileWriter = csv.writer(csvfile, delimiter=' ')
            fileWriter.writerows(self.makeRow())


    def batch_update_values(self):
        """
        Creates the batch_update the user has access to.
        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """

        try:
            service = build("sheets", "v4", credentials=self.credentials)

            data = [
                {"range": self.range_name, "values": self.writebuffer},
                # Additional ranges to update ...
            ]
            body = {"valueInputOption": self.value_input_option, "data": data}
            result = (
                service.spreadsheets()
                .values()
                .batchUpdate(spreadsheetId=self.spreadsheet_id, body=body, )
                .execute()
            )
            print(f"{(result.get('totalUpdatedCells'))} cells updated.")
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
        

    def getCredentials(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        #TODO: add an expiration check on credentials
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
                )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds


# testing the class:
def main():
    #get the data from Google
    nr = pdata.MonthlyClinicRequest('1SZqqxaJqIZYGsJTP6JHi6RuvOaczO1ZnpCXGBb-pXsU')

    # create a problem instance:
    doctors = DoctorSchedulingProblem(10,nr.doctorNames,nr.doctorPreference,nr.totalShifts,nr.totalShifts, nr.weekendPositions)

    randomSolution = np.random.randint(2, size=len(doctors))
    
    # doctors.printScheduleInfo(randomSolution)
    #print(doctors.getDoctorWeekShifts(randomSolution))

    ex = ExportSchedulingSolution(doctors.getDoctorWeekShifts(randomSolution))
    #print(ex.makeRow())


    #Send the current instance of data
    ex.batch_update_values()


if __name__ == "__main__":
    main()

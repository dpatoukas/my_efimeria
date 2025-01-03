The goal of the app is to calculate the work schedule of a month for a clinic. The inputs needed are: the month name, the number of doctors available, and a preference list of days that the doctors prefer not to work. 

The application already has some requirements implemented that trys to implement:
#Doctors are not allowed to do 2 consecutive shifts
#Doctors are not allowed to do more than doctorMaxShiftPerMonth
#The numebr of doctors scheduled in a day should be between doctorshiftMax and doctorshiftMin
#Distance between two shifts must be maximized 
#Doctors prefer to work less than 2 days per week 
#Doctors should only be scheduled in the days that they want to work  
#Doctors prefer to be working 2 or less weekends 

The output is a monthly schedule where one can see all the days they have to work. 


An admin user should be able to fill in the month for which he would like to create a schedule. The number and the names of the available doctors. Then the admin should be able to mark on the days(maybe in a calendar input screen) that each doctor wants to have a day off. 
The admin should click on a button that locks the input and waits for the application to finish. Once the application is finished they should see a screen where the admin can inspect the suggested schedule. If the admin agrees they should click agree and "print" the schedule. 
If they would like a new calculation they should request a new schedule.
If they would like to modify the shifts they should be able to manually edit the schedule before agreen on it and printing it. 

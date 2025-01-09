### Postman Collection

The Postman collection for this project is located in the `postman` directory. It contains a set of API requests that simulate the full lifecycle of managing a clinic's schedule and shifts, covering the primary use cases of the application.

---

### Use Case Simulated with the Postman Collection

The use case being simulated is the **end-to-end management of doctors, schedules, and shifts** in a clinic. Below is a summary of the actions performed by the Postman collection:

1. **Authentication**
   - The collection starts by simulating user authentication to retrieve a `JWT token`. This token is used to authorize all subsequent API requests.

2. **Doctor Management**
   - Fetch all existing doctors to review the current database.
   - Create a new doctor with predefined details.
   - Retrieve the newly created doctor’s details by ID.
   - Update the doctor’s information.
   - Delete the doctor at the end of the workflow to maintain a clean database state.

3. **Schedule Management**
   - Check if any schedules exist for a given month.
   - If no schedules exist, generate a new schedule for the month.
   - Retrieve the details of the created schedule.
   - Update the schedule to finalize its status.
   - Delete the schedule at the end of the workflow.

4. **Shift Management**
   - Fetch all shifts associated with the created schedule.
   - Add a new shift for the schedule, assigning it to the newly created doctor.
   - Delete the created shift after confirming its addition.

---

### Steps to Use the Postman Collection

1. **Import the Collection**
   - Open Postman.
   - Click **Import** in the top-left corner.
   - Select the `postman/Clinic-Scheduling.postman_collection.json` file.

2. **Import the Environment (Optional)**
   - If you are using environment variables, import the `postman/Clinic-Scheduling.postman_environment.json` file.

3. **Authenticate**
   - Send the `Login` request in the collection to retrieve a `JWT token`.
   - Save the token to the `{{accessCollectionToken}}` variable in your environment.

4. **Run the Collection**
   - Execute the requests sequentially or use the Postman **Runner** to run the entire collection as a workflow.

---

### Simulated Workflow Summary

Here’s the flow of actions simulated in the Postman collection:

1. Authenticate and retrieve a token.
2. Retrieve and manage doctor records:
   - Fetch all doctors.
   - Add a new doctor and update its details.
   - Delete the doctor after completing the workflow.
3. Manage schedules:
   - Check for existing schedules for a given month.
   - Generate a new schedule if none exists.
   - Update the schedule's status and delete it after use.
4. Handle shifts for the schedule:
   - Retrieve all shifts.
   - Add a new shift for a doctor and schedule.
   - Remove the shift to maintain the database's integrity.

---

### Additional Notes

- **Data Cleanup**: The workflow ensures that all data created during the tests (doctor, schedule, and shifts) is deleted to maintain a clean database state.
- **Testing Dependencies**: Ensure that the backend API is running and accessible at the specified URL in the environment file.
- **Customization**: Modify the collection or environment variables to test specific edge cases or additional workflows.
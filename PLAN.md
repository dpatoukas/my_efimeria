# Plan for Saving Solution to Database

## Overview
This plan outlines the approach for saving the generated schedule results into the database using the existing DAO, repository, and service layers.

---

## 1. Architecture Approach
We will leverage the **current architecture** to implement the solution:
- **DAO Layer**: Handles direct database interactions.
- **Repository Layer**: Applies business rules and validation.
- **Service Layer**: Processes the solution and interacts with the repository.

This ensures **separation of concerns** and maintains a modular and scalable design.

---

## 2. Implementation Plan

### **Step 1: Extend Repository Layer**

Add a method in the **`ShiftRepository`** to handle bulk insertion of shifts:

```python
@staticmethod
def save_shifts(session: Session, schedule_id: int, shifts: list):
    """
    Saves multiple shifts in bulk to improve performance.
    """
    for shift in shifts:
        # Check for conflicts before saving
        existing_shift = session.query(Shift).filter(
            Shift.doctor_id == shift['doctor_id'], Shift.date == shift['date']
        ).first()
        if existing_shift:
            raise ValueError(f"Conflict: Doctor {shift['doctor_id']} already assigned on {shift['date']}.")

        # Save each shift
        ShiftDAO.create_shift(
            session,
            schedule_id,
            shift['doctor_id'],
            shift['date'],
            "Assigned"
        )
```

---

### **Step 2: Add Service Layer Logic**

Implement **`save_solution_to_db`** in the **`SolutionService`**:

```python
def save_solution_to_db(self, session, schedule_id, solution):
    """
    Saves the generated solution to the database using the repository layer.
    """
    # Prepare shift data
    shifts = []
    for day in range(len(solution)):
        for doctor_idx, assigned in enumerate(solution[day]):
            if assigned == 1:  # Assigned shift
                shifts.append({
                    'doctor_id': doctor_idx + 1,  # Assuming IDs start at 1
                    'date': f"2025-01-{day + 1}"  # Replace with actual dates
                })

    # Use repository to save shifts
    from repositories.repository import ShiftRepository
    ShiftRepository.save_shifts(session, schedule_id, shifts)
    print("Solution saved successfully!")
```

---

### **Step 3: Integrate in Main Script**

Update **`main.py`** to save the solution:

```python
# Run Genetic Algorithm
best_solution = solution_service.run_genetic_algorithm()

# Save the solution to the database
solution_service.save_solution_to_db(session, schedule_id, best_solution)
```

---

## 3. Advantages of the Approach

1. **Scalability**: Bulk insertion improves performance for large schedules.
2. **Validation**: Prevents conflicts or double-bookings through repository checks.
3. **Flexibility**: Service handles the processing logic, keeping the layers clean.
4. **Maintainability**: Modular approach simplifies testing and debugging.

---

## 4. Next Steps
1. Implement and test the code changes.
2. Validate the solution with test data.
3. Add REST endpoints to expose schedules.
4. Document the API for frontend integration.

---

## Conclusion
This plan adheres to the existing architecture, ensuring scalability, modularity, and maintainability. It is ready for implementation and testing. Let me know if additional refinements are needed!


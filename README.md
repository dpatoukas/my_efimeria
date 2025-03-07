# Efimeria - Doctor Scheduling System

## Motivation

As someone with close friends in the medical field, I’ve seen how challenging and time-consuming it can be to create fair and efficient monthly schedules. Balancing preferences, avoiding conflicts, and meeting constraints often requires hours of manual effort.

To help simplify this process, I created Efimeria, a Doctor Scheduling System designed to automate scheduling while maintaining fairness and flexibility. This project aims to save time and reduce the stress of managing shifts, allowing doctors to focus on their work.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Setup Instructions](#setup-instructions)
5. [Database and Migrations](#database-and-migrations)
6. [Testing](#testing)
7. [API Documentation](#api-documentation)
8. [Deployment](#deployment)
9. [Connection to Requirements](#connection-to-requirements)
10. [Screenshots](#screenshots)
11. [Future Enhancements](#future-enhancements)
12. [License](#license)

---

## Overview
Efimeria is a **full-stack web application** designed to generate optimized monthly work schedules for a clinic. The system automates scheduling while adhering to constraints, such as limiting consecutive shifts and maximizing doctor satisfaction by incorporating preferences. Admins can create, review, and edit schedules and export finalized schedules for distribution.

---

## Features
- **Authentication/Authorization**: Secure login with JWT tokens.
- **Schedule Management**: Automated generation
- **Shift Preferences**: Considers doctor preferences and constraints like weekend limits and maximum shifts.
- **Frontend UI**: Built with Material-UI for a modern, responsive interface.
- **Documentation**: REST API documentation available via Swagger.
- **Testing**: Comprehensive unit and API testing.

---

## Connection to Requirements
This project directly addresses the deliverables outlined in the [requirements.md](Documentation/requirements.md):

1. **Domain Model and Database**: Fully implemented with SQLAlchemy and managed using Alembic.  
   - Relevant File: `backend/models/` (for database models) and `backend/migrations/` (for Alembic migrations).

2. **Backend**: RESTful APIs with authentication, authorization, and business logic layers.  
   - Relevant File: `backend/` (main application logic, API routes, and services).

3. **Frontend**: React + Material-UI for responsive, interactive UI.  
   - Relevant File: `frontend/src/` (React components, Material-UI integration, and pages).

4. **Testing**: Unit and API testing using pytest and Postman.  
   - Relevant File: 
     - `backend/tests/unit` (pytest tests for backend components).
     - `backend/tests/postman` (Postman collection for API testing).

5. **Documentation**: API documentation via Swagger and deployment instructions in this README.  
   - Relevant File:-[on SwaggerHub](https://app.swaggerhub.com/apis/PATOUKAS/clinic-scheduling_api/1.0.0).. and [Deployment](#deployment)

6. **Submission Guidelines**: GitHub repository with a README and required documentation.  
   - Relevant File: `This One :D` [Motivation and Approach](Documentation/motivation_and_approach.md) [Documentation](Documentation) and [Future Enhancements](#future-enhancements) . 

---

## Tech Stack
- **Backend**: Python (FastAPI), SQLAlchemy, Alembic
- **Frontend**: React, Vite, Material-UI
- **Database**: SQLite
- **Deployment**: Docker (Optional) or Local Server

---

## Database and Migrations
Alembic is used for managing schema changes in the database. Detailed instructions for setup and migration workflows can be found in the [Migrations Documentation](./migrations.md).

---

## Testing
- **Backend Testing**: 
  ```bash
  pytest tests
  ```
- **API Testing**: Postman collections simulate end-to-end workflows. See the [Postman Documentation](./postman.md).
- **Frontend Testing**: `@TODO`


---

## API Documentation
- **Swagger UI**: The full API documentation is available [on SwaggerHub](https://app.swaggerhub.com/apis/PATOUKAS/clinic-scheduling_api/1.0.0)..

---

## Deployment
### Using Docker 
1. Clone the repository
2. Build the Docker image:
   ```bash
   docker-compose up --build
   ```
3. Access the application at [http://localhost:5173](http://localhost:5173/).
4. Access the API Docs at [http://localhost:5000/api/docs](http://localhost:5000/api/docs)
5. Use the admin user with: {"username": "admin", "password": "password"}

### Manual Deployment
[Follow the backend and frontend setup instructions ](Documentation/backend_frontend_setup.md)  

---

## Screenshots
1. **Dashboard View**  
![Dashboard](Documentation/images/Dashboard.png)



2. **Schedule Details**  
![Create Schedule](Documentation/images/Create_schedule.png)
![Schedule Details](Documentation/images/Schedule.png)

---
## Demo
![](Documentation/images/Animation.gif)

## Future Enhancements

Efimeria is a strong foundation for solving the complex problem of doctor scheduling, but several enhancements can improve its functionality, usability, and flexibility:

1. **Testing Enhancements**:
   - Implement **end-to-end testing** to validate workflows from start to finish.
   - Add comprehensive **frontend testing** to ensure UI reliability and consistency.

2. **Role-Based Collaboration**:
   - Enable **role-based access control** to differentiate between administrators, doctors, and support staff.
   - Introduce team collaboration features, allowing multiple users to work on the same schedule simultaneously.

3. **Export Options**:
   - Expand export functionality to include **CSV, PDF, and Excel formats**, enabling easier distribution and analysis of schedules.

4. **Frontend Visual Enhancements**:
   - Improve UI elements with attention to **priorities, fonts, colors, sizes, and table views**.
   - Enhance consistency and aesthetics across the application.
   - Optimize performance and workflows for a seamless user experience.

5. **In-Depth Doctor Management**:
   - Provide advanced options for managing doctor profiles, including adding experience levels and more detailed metadata.

6. **Custom Scheduling Parameters**:
   - Allow administrators to configure **flexible daily shift requirements** (e.g., 8 doctors on some days, 2 on others).
   - Introduce customizable fairness constraints, such as:
     - Equal distribution of shifts across all doctors.
     - Fair sharing of weekend shifts over multiple months.
     - Guaranteeing balanced staffing by experience level.

7. **Constraint Management and Feedback**:
   - Enhance the genetic algorithm to detect and report violated constraints in generated schedules.
   - Allow administrators to review violated constraints and make manual adjustments or request a new schedule with revised parameters.

8. **Algorithm Improvements**:
   - Expand the genetic algorithm based on user feedback and insights from real-world usage.
   - Incorporate more sophisticated optimization dimensions, such as experience levels and additional fairness constraints.

9. **Demo and Feedback**:
   - Plan to demo the application to doctors for feedback on usability, scheduling preferences, and additional features. Use this feedback to guide future developments.

---

## Lessons Learned

The development of Efimeria offered many valuable insights into both technical and design aspects:

1. **UI/Frontend Challenges**:
   - Creating a good UI and frontend is harder than expected. Starting with **Figma designs early on** could have streamlined the process and improved consistency.
   - Frontend testing is also a challenge, requiring more structured planning and better tooling.

2. **Database Design**:
   - Early and thoughtful database design is crucial. A well-designed schema saves time and avoids complications during later stages of development.

3. **Deployment Fun**:
   - Working with deployment scripts, containerization, and environments proved to be both educational and enjoyable, reinforcing the importance of reliable deployment pipelines.

4. **Time Constraints**:
   - While the backend and frontend implementations met their goals, they were developed under time pressure. This leaves room for significant improvement, especially if there is interest from third parties in adopting or expanding the application.

These lessons will guide future projects, helping to create more polished and user-centric solutions.

## License
## License

Efimeria is licensed under the GNU General Public License v3.0.  
You can redistribute it and/or modify it under the terms of the GPL.  

For more details, see the [LICENSE](./LICENSE) file or visit the [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html) official page.

![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)



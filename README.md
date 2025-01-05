# Clinic Scheduling Application

## Overview
The Clinic Scheduling Application calculates and manages monthly work schedules for doctors based on constraints and preferences. This document outlines the high-level goal, project progress, and detailed information about data interfaces, repositories, migrations, technology stack, tools, architecture, and organization.

## High-Level Goal
The primary goal of this project is to develop a robust and efficient scheduling system for clinics that optimizes doctor schedules while considering various constraints and preferences.

## Project Progress
- Database schema designed and implemented.
- Data Access Objects (DAO) and repositories created.
- Basic CRUD operations established.
- Initial scheduling algorithm implemented.
- REST API endpoints exposed.
- Authentication and authorization mechanisms in place.

## Technology Stack
- **Backend**: Python, Flask
- **Database**: SQLite, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript (planned)
- **Authentication**: JWT Tokens
- **Testing**: PyTest
- **Version Control**: Git

## Tools
- **IDE**: Visual Studio Code
- **Database Management**: SQLite Browser
- **Version Control**: GitHub
- **Project Management**: Trello

## Architecture

### Backend Architecture
- **Database Layer (SQLAlchemy with SQLite)**
  - Handles data storage, migrations, and schema.
  - Manages tables for Doctors, Schedules, and Shifts.

- **Data Access Layer (DAO)**
  - Provides CRUD operations to interact with the database.

- **Repository Layer**
  - Enforces business rules and applies validations for core entities.

- **Service Layer**
  - Implements complex scheduling algorithms and optimization rules.

- **API/Controller Layer**
  - Exposes REST endpoints to handle HTTP requests from the frontend.

- **Authentication/Authorization**
  - Ensures secure user access with JWT tokens.

## Data Interfaces
- **DAO (Data Access Objects)**
  - Abstracts and encapsulates all access to the data source.
  - Provides an interface for performing CRUD operations.

- **Repository**
  - Acts as a mediator between the data access layer and the business logic layer.
  - Contains business rules and logic for data retrieval and manipulation.

## Migrations
- **Alembic**: Used for handling database migrations to ensure the schema evolves as the application grows.

## Organization
- **Models**: Define the structure of the database tables.
- **Repositories**: Contain business logic and data retrieval methods.
- **Services**: Implement core application logic and algorithms.
- **Controllers**: Handle HTTP requests and responses.
- **Tests**: Ensure the correctness and reliability of the application.

## Important Functionalities
- **Doctor Scheduling**: Optimizes monthly schedules based on constraints and preferences.
- **CRUD Operations**: Manage doctors, schedules, and shifts.
- **Authentication**: Secure user access with JWT tokens.
- **REST API**: Exposes endpoints for frontend interaction.

## Usage
1. Clone the repository.
2. Set up the virtual environment and install dependencies.
3. Run database migrations.
4. Start the Flask server.
5. Access the API endpoints to interact with the application.

## Conclusion
This Clinic Scheduling Application aims to streamline the scheduling process for clinics, ensuring efficient and optimized schedules for doctors. The project is structured to be modular, maintainable, and scalable, with a clear separation of concerns across different layers of the architecture.

## Development Steps

### Step 1: Database and Models
- Design and define database schema.
- Implement SQLAlchemy ORM models.
- Create migrations with Alembic.
- Test database initialization and data insertion.

### Step 2: DAO and Repository Layers
- Build DAOs for low-level data operations.
- Create repositories to enforce business rules.
- Test DAO and repository functionalities.

### Step 3: Service Layer
- Implement scheduling logic and constraints.
- Optimize shift assignments using algorithms (e.g., genetic algorithms).
- Add manual edit and recalculation features.
- Test business logic with unit tests.

### Step 4: API/Controller Layer
- Define RESTful endpoints for CRUD operations.
- Add endpoints for schedule generation, approval, and recalculation.
- Document APIs with Swagger.
- Test endpoints using Postman or automated tools.

### Step 5: Authentication and Authorization
- Add JWT-based authentication.
- Implement role-based access control for admin users.
- Protect endpoints requiring authentication.

### Step 6: Frontend Development
- Design and implement the user interface.
- Integrate the frontend with backend APIs.
- Build features like calendar input, schedule preview, and manual edits.
- Test UI interactions with Selenium.

### Step 7: Testing and Validation
- Perform unit tests for each layer.
- Conduct integration tests for data flow between layers.
- Simulate edge cases (e.g., 100+ doctors) for scalability.

### Step 8: Deployment and Documentation
- Containerize the application using Docker.
- Test local deployment with Docker Compose.
- Prepare deployment pipeline (e.g., GitHub Actions).
- Write detailed deployment and user documentation.

---

## Key Constraints and Business Rules
1. Doctors cannot have consecutive shifts.
2. Doctors cannot exceed a set number of shifts per month.
3. Shifts should maximize gaps between workdays.
4. Preferences for specific off-days must be respected.
5. Minimize weekend assignments to two or fewer.
6. Manual edits must maintain constraint validation.

---

## Deliverables
1. Fully functional backend with RESTful APIs.
2. Interactive frontend UI for schedule management.
3. Authentication and authorization system.
4. Comprehensive tests (unit, integration, and UI).
5. Deployment-ready Docker configuration.
6. Documentation including API reference and user guide.

---

## Next Steps
1. Finalize service layer logic and testing.
2. Implement API layer and connect it with the frontend.
3. Add authentication and role management.
4. Focus on testing and deployment readiness.

---

This document will evolve as development progresses. Updates will reflect changes in design decisions, new requirements, or implementation adjustments. Let me know if clarifications or additions are needed!
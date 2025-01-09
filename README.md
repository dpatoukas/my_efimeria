# Efimeria - Doctor Scheduling System

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
- **Schedule Management**: Automated generation, history tracking, and manual editing of schedules.
- **Shift Preferences**: Considers doctor preferences and constraints like weekend limits and maximum shifts.
- **Reporting & Export**: Export schedules as CSV files for administrative use.
- **Frontend UI**: Built with Material-UI for a modern, responsive interface.
- **Documentation**: REST API documentation available via Swagger.
- **Testing**: Comprehensive unit and integration testing.

---

## Tech Stack
- **Backend**: Python (FastAPI), SQLAlchemy, Alembic
- **Frontend**: React, Vite, Material-UI
- **Database**: SQLite
- **Deployment**: Docker (Optional) or Local Server

---

## Setup Instructions
### Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- Git
- Virtual Environment (recommended)

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/dpatoukas/my_efimeria.git
   cd my_efimeria/backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # Linux/Mac
   .\env\Scripts\activate   # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run database migrations:
   ```bash
   alembic upgrade head
   ```
5. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the frontend server:
   ```bash
   npm run dev
   ```

---

## Database and Migrations
Alembic is used for managing schema changes in the database. Detailed instructions for setup and migration workflows can be found in the [Migrations Documentation](./migrations.md).

---

## Testing
- **Backend Testing**: 
  ```bash
  pytest
  ```
- **API Testing**: Postman collections simulate end-to-end workflows. See the [Postman Documentation](./postman.md).
- **Frontend Testing**:
  ```bash
  npm test
  ```

---

## API Documentation
- **Swagger UI**: [View API Documentation](http://localhost:8000/docs).
- **Redoc UI**: [Alternate API View](http://localhost:8000/redoc).
- Full details are available in the [requirements](./requirements.md).

---

## Deployment
### Using Docker (Optional)
1. Build the Docker image:
   ```bash
   docker-compose up --build
   ```
2. Access the application at `http://localhost:3000`.

### Manual Deployment
Follow the backend and frontend setup instructions provided above.

---

## Connection to Requirements
This project directly addresses the deliverables outlined in the [requirements.md](./requirements.md):
1. **Domain Model and Database**: Fully implemented with SQLAlchemy and managed using Alembic.
2. **Backend**: RESTful APIs with authentication, authorization, and business logic layers.
3. **Frontend**: React + Material-UI for responsive, interactive UI.
4. **Testing**: Unit and integration testing using pytest and Postman.
5. **Documentation**: API documentation via Swagger and deployment instructions in this README.
6. **Submission Guidelines**: GitHub repository with a README and required documentation.

---

## Screenshots
1. **Dashboard View**  
   _[Insert Image]_  

2. **Schedule Details**  
   _[Insert Image]_  

---

## Future Enhancements
- **Role-based Access Control (RBAC)** for better permission handling.
- **Drag-and-drop schedule editing** for improved usability.
- **Calendar View** to visualize schedules more effectively.
- **Email Notifications** for schedule updates.

---

## License
This project is licensed under the MIT License.
```

You can copy and paste this directly into your `README.md` file. Let me know if you need further modifications!

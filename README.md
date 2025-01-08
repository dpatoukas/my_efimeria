# Efimeria - Doctor Scheduling System

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Tech Stack](#tech-stack)  
4. [Setup Instructions](#setup-instructions)  
5. [Testing](#testing)  
6. [API Documentation](#api-documentation)  
7. [Deployment](#deployment)  
8. [Screenshots](#screenshots)  
9. [Future Enhancements](#future-enhancements)  
10. [License](#license)

---

## Overview
Efimeria is a **full-stack web application** designed to generate optimized monthly work schedules for a clinic. It allows admins to manage doctors, configure preferences, and ensure compliance with scheduling constraints. The system prioritizes fairness, reduces consecutive shifts, and offers flexibility through manual edits.

---

## Features
- **Authentication/Authorization**: Secure login with JWT tokens.  
- **Schedule Management**: Generate schedules, track history, and edit results manually.  
- **Shift Preferences**: Incorporates doctor preferences and adheres to constraints like maximum shifts and weekend limits.  
- **Reporting & Export**: Export schedules as CSV files.  
- **Frontend UI**: Built with Material-UI for a clean and responsive design.  
- **Documentation**: API endpoints documented with Swagger.  
- **Testing**: Unit tests and integration testing. **TODO: Add test cases**

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
- Virtual Environment (optional but recommended)  

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/dpatoukas/my_efimeria.git
   cd my_efimeria/backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate # Linux/Mac
   .\env\Scripts\activate  # Windows
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
1. Move to the frontend directory:
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

## Testing
- **Backend Testing**:  
  ```bash
  pytest
  ```
- **API Testing**: Postman scripts are included in the `docs/postman_collection.json`. **TODO: Verify Postman collection availability**  
- **Frontend Testing**:  
  ```bash
  npm test
  ``` **TODO: Add frontend tests**

---

## API Documentation
- **Swagger UI**: Visit `http://localhost:8000/docs` after starting the backend server.  
- **Redoc UI**: Visit `http://localhost:8000/redoc`.  

---

## Deployment
### Using Docker (Optional) **TODO: Verify Dockerfile setup**
1. Build the Docker image:
   ```bash
   docker-compose up --build
   ```

2. Access the application at `http://localhost:3000`.  

### Manual Deployment
Follow the backend and frontend setup steps provided earlier, then configure your server to host both parts.

---

## Screenshots **TODO: Add screenshots**
1. **Dashboard View**  
   _[Insert Image]_  

2. **Schedule Details**  
   _[Insert Image]_  

---

## Future Enhancements
- **Role-based Access Control (RBAC)**. **TODO: Implement RBAC**  
- **Drag-and-drop schedule editing**. **TODO: Implement drag-and-drop support**  
- **Calendar View** for better visualization. **TODO: Add calendar view**  
- **Email Notifications** for schedule updates. **TODO: Implement email notifications**  

---

## License
This project is licensed under the MIT License.  


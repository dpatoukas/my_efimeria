
# Clinic Scheduling API

The **Clinic Scheduling API** is a RESTful service designed to manage doctor schedules, shifts, and related operations for a clinic.
It provides endpoints for authentication, doctor management, schedule generation, and shift assignments.

## Features

- **Authentication:** Secure login with JWT-based authentication.
- **Doctor Management:** CRUD operations for managing doctor profiles.
- **Schedule Generation:** Automated generation of doctor schedules for specified months.
- **Shift Management:** Assignment and management of doctor shifts.
- **API Documentation:** Interactive API documentation using Swagger UI.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Git](https://git-scm.com/downloads)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/dpatoukas/my_efimeria.git
   cd my_efimeria
   ```

2. **Set Up a Virtual Environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**

   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```

   - **macOS and Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **Environment Variables:**

   Create a `.env` file in the project root to store environment variables:

   ```bash
   touch .env
   ```

2. **Database Setup:**

   The application uses SQLite for development. Ensure the database file is present or create a new one:

   ```bash
   # In your .env file
   DATABASE_URL=sqlite:///clinic_schedule.db
   ```

3. **JWT Secret Key:**

   Set a secret key for JWT authentication in your `.env` file:

   ```bash
   # In your .env file
   JWT_SECRET_KEY=your_secret_key_here
   ```

### Running the Application

1. **Initialize the Database:**

   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

2. **Start the Development Server:**

   ```bash
   python main.py
   ```

   The API will be accessible at `http://localhost:5000/`.

### Accessing Swagger UI

Swagger UI provides interactive API documentation.

1. **Navigate to Swagger UI:**

   Open your browser and go to `http://localhost:5000/api/docs`.

2. **Authorize with JWT:**

   - **Obtain a Token:**
     - Use the `/api/auth/login` endpoint to authenticate and receive a JWT token.

   - **Authorize in Swagger UI:**
     - Click the "Authorize" button in Swagger UI.
     - Enter the token in the format: `Bearer your_jwt_token_here`.
     - Click "Authorize" to apply the token.

### Project Structure

```plaintext
my_efimeria/
├── api/
│   ├── __init__.py
│   ├── auth.py
│   ├── doctors.py
│   ├── schedules.py
│   └── shifts.py
├── models/
│   ├── __init__.py
│   ├── doctor.py
│   ├── schedule.py
│   └── shift.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_doctors.py
│   ├── test_schedules.py
│   └── test_shifts.py
├── .env
├── main.py
├── requirements.txt
└── README.md
```

### Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

### License

This project is licensed under the MIT License. See the `LICENSE` file for details.

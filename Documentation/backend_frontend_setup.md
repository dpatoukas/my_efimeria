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
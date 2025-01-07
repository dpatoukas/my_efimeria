from sqlalchemy import create_engine
engine = create_engine('sqlite:///data/clinic_schedule.db')
connection = engine.connect()
print("Database connection successful!")
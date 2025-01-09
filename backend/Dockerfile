# Backend Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables to prevent Python from writing pyc files and to use stdout for logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set Flask environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=development

# Add working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the Flask app port
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
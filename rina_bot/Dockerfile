# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements if you have them, else skip this step
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Install dependencies (Flask, FastAPI, Uvicorn, google-generativeai, aiosqlite, bcrypt, etc.)
RUN pip install --no-cache-dir flask fastapi uvicorn google-generativeai aiosqlite bcrypt   google-cloud-firestore google-cloud-secret-manager 

# Expose the ports for Flask (5000) and FastAPI (8000)
EXPOSE 5000

# Run both Flask and FastAPI via run_all.py
CMD ["python", "run_all.py"]

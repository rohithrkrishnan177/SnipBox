# Use the official Python image from Docker Hub
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port Django will run on
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Command to run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Using the official Python Alpine base image for reducing size
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install all necessary packages
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev openssl-dev

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copying the entire code into the container
COPY . .

# Setting execution permissions 
RUN chmod +x /app/health_monitor.py

# Run the Python script
CMD ["python", "/app/health_monitor.py"]

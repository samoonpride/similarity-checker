# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

ENV WORKERS=2

# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg
# Clean up the apt cache by removing /var/lib/apt/lists saves space
RUN rm -rf /var/lib/apt/lists/*

# Set the working directory in the container to /app
WORKDIR /app/similarity-checker

# Add the current directory contents into the container at /app
COPY . .

# Upgrade pip
RUN pip install --upgrade pip

# Install production dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8002 available to the world outside this container
EXPOSE 8002

# Create a non-root user to run the application
RUN useradd -m myuser
USER myuser

# Use environment variables for workers and port with defaults
CMD gunicorn -w ${WORKERS} -b :8002 similarity_checker:app

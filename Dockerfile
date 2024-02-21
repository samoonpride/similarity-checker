# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Install ffmpeg
RUN apt-get update

# Set the working directory in the container to /app
WORKDIR /app/similarity-checker

# Add the current directory contents into the container at /app
ADD . .

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

# Run gunicorn when the container launches
CMD ["gunicorn", "-w", "4", "-b", ":8002", "similarity_checker:app"]

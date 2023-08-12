# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim-buster

# Set the working directory in Docker
WORKDIR /usr/src/app

# Set environment variables
# PYTHONUNBUFFERED ensures that Python output is logged to the terminal
# PYTHONDONTWRITEBYTECODE means Python won't try to write .pyc files
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY ./app /usr/src/app

# Specify the command to run on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies for building mysqlclient and curl for health check
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libmariadb-dev \
    pkg-config \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=sso_server.settings

# Command to run the application
CMD ["gunicorn", "sso_server.wsgi:application", "--bind", "0.0.0.0:8000"]

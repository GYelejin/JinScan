# TODO: Complete a Dockerfile 

# Use an official Python runtime as a parent image
FROM python:3.12.0-slim-bookworm

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Set Python  environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=True
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=mysecretpassword
ENV POSTGRES_DB=mydatabase

# Expose port 5000 for the Flask app
EXPOSE 5000

# Start PostgreSQL server
RUN apt-get update && apt-get install -y postgresql postgresql-contrib
RUN service postgresql start && \
    sudo -u postgres psql -c "CREATE DATABASE ${POSTGRES_DB};" && \
    sudo -u postgres psql -c "CREATE USER ${POSTGRES_USER} WITH PASSWORD '${mysecretpassword}';" && \
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};"

# Run the command to start the Flask app
CMD ["python", "app.py"]

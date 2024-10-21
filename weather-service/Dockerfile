# Use the official Python image as the base image
FROM python:3.9

# Install PostgreSQL
RUN apt-get update && apt-get install -y postgresql postgresql-contrib

# Install Poetry
RUN pip install poetry

# Set the working directory inside the container
WORKDIR /app

# Copy the project files to the working directory
COPY . .

# Install project dependencies
RUN poetry install

# Set environment variables for PostgreSQL
# Change the accordingly
ENV DB_USER=postgres
ENV DB_PASSWORD=mysecretpassword
ENV DB_NAME=postgres

# Create a script to initialize and start PostgreSQL
RUN echo "service postgresql start && \
           sudo -u postgres psql -c \"CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';\" && \
           sudo -u postgres psql -c \"CREATE DATABASE $DB_NAME;\" && \
           sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;\" && \
           poetry run python3 main.py --dev" > /app/start.sh

# Make the script executable
RUN chmod +x /app/start.sh

# Start PostgreSQL and run the Python service
CMD ["/bin/bash", "-c", "/app/start.sh"]

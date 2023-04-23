# Use a base image with Python installed
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app into the container
COPY . .

# Expose port 5000 to the host
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run", "--host", "0.0.0.0"]

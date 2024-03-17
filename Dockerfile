# Use the official Python image as a base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install xmltodict
RUN pip install xmltodict

# Copy the rest of the application code into the container
COPY . /app

# Run the application
CMD ["python", "./iss_tracker.py"]


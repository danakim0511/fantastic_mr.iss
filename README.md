# ISS Tracker Flask Application

This project is a Flask application that fetches International Space Station (ISS) data from NASA's public repository and provides various endpoints to retrieve information about the ISS's position, speed, and other metrics. It also performs calculations and returns the data in JSON format.

## Features

- Fetch and display ISS comments
- Retrieve ISS header information
- Extract ISS metadata
- Get the entire data set of ISS state vectors
- Retrieve state vectors for a specific epoch
- Calculate instantaneous speed for a specific epoch
- Fetch location data for a specific epoch
- Get data for the epoch nearest to the current time

## Important Files
- iss_tracker.py: This file contains the main Flask application code, including route definitions and data processing functions.
- test_iss_tracker.py: This file contains unit tests for the Flask application.
- requirements.txt: This file lists the Python dependencies required to run the application.
- Dockerfile: This file defines the Docker image for the application.
- docker-compose.yml: This file configures the Docker services for deploying the application

## ISS Data Citation
The ISS data used in this project is sourced from NASA's public repository. 
https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml

## Deploying the App with Docker Compose
To deploy the ISS Tracker Flask application using Docker Compose, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run the following command:
```bash
docker-compose up
```
This command will build the Docker image and start the Docker container for the application.

## Accessing API Endpoints with curl
### /comment
Fetches and returns the comments from ISS data.
```bash
curl http://127.0.0.1:5000/comment
```
This endpoint returns comments extracted from the ISS data in XML format. The output JSON contains a key "comments" with a list of strings representing the comments found in the XML data. These comments may provide additional information or context about the ISS mission or data.

### /header
Fetches and returns the header information from ISS data.
```bash
curl http://127.0.0.1:5000/header
```
The /header endpoint returns header information parsed from the ISS data in XML format. The output JSON contains a key "header" with a dictionary of key-value pairs representing the header data. This header information typically includes metadata about the data source, such as timestamps, version numbers, or other relevant details.

### /metadata
Fetches and returns the metadata from ISS data.
```bash
curl http://127.0.0.1:5000/metadata
```
The /metadata endpoint returns metadata extracted from the ISS data in XML format. The output JSON contains a key "metadata" with a list of dictionaries representing different metadata entries. Each metadata entry may contain various pieces of information related to the ISS mission or data, such as mission parameters, spacecraft configuration, or scientific instrumentation details.

### /epochs
Fetches and returns the entire data set of ISS state vectors.
```bash
curl http://127.0.0.1:5000/epochs
```
The /epochs endpoint provides a list of all the ISS state vectors available in the data set. The output JSON contains an array of dictionaries, where each dictionary represents a single state vector. Each state vector contains information such as the epoch timestamp, position (X, Y, Z coordinates), and velocity (X_DOT, Y_DOT, Z_DOT components).

### /epochs/<epoch>
Fetches and returns the state vectors for a specific epoch.
```bash
curl http://127.0.0.1:5000/epochs/<epoch>
```
The /epochs/<epoch> endpoint returns the state vector data for a specific epoch timestamp. The output JSON contains a single dictionary representing the state vector for the specified epoch.

### /epochs?limit=int&offset=int
Fetches and returns modified list of Epochs given query parameters
```bash
curl http://127.0.0.1:5000/epochs?limit=int&offset=int
```
The /epochs endpoint with query parameters allows pagination through the list of ISS state vectors. The output JSON format is the same as the /epochs endpoint, but it returns a subset of the data based on the provided limit and offset parameters.

### /epochs/<epoch>/speed
Fetches and returns the instantaneous speed for a specific epoch.
```bash
curl http://127.0.0.1:5000/epochs/<epoch>/speed
```
The /epochs/<epoch>/speed endpoint returns the instantaneous speed for a specific epoch timestamp. The output JSON contains a single key "instantaneous_speed" with the calculated speed value in kilometers per second.

### /epochs/<epoch>/location
Fetches and returns the location data for a specific epoch.
```bash
curl http://127.0.0.1:5000/epochs/<epoch>/location
```
The /epochs/<epoch>/location endpoint returns the latitude, longitude, altitude, and geoposition information for a specific epoch timestamp. The output JSON contains keys for each of these properties with their corresponding values.

### /now
Fetches and returns data for the epoch nearest to the current time.
```bash
curl http://127.0.0.1:5000/now
```
The /now endpoint provides real-time information about the current position and speed of the International Space Station. The output JSON contains the following keys:

latitude: The latitude coordinate of the ISS's current position.
longitude: The longitude coordinate of the ISS's current position.
altitude: The altitude above the Earth's surface in kilometers.
geoposition: A human-readable location description based on the latitude and longitude coordinates.
speed: The instantaneous speed of the ISS in kilometers per second.

These outputs provide valuable information about the ISS state vectors at different epochs, allowing users to analyze and understand the movement and position of the International Space Station over time.

## Credits
This application was developed by Dana Kim.

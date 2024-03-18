# ISS Tracker Flask Application

This Flask application fetches and displays International Space Station (ISS) data, including comments, header information, metadata, state vectors, and more.

## Features

- Fetch and display ISS comments
- Retrieve ISS header information
- Extract ISS metadata
- Get the entire data set of ISS state vectors
- Retrieve state vectors for a specific epoch
- Calculate instantaneous speed for a specific epoch
- Fetch location data for a specific epoch
- Get data for the epoch nearest to the current time

## Setup

### Requirements

- Python 3.x
- Docker
- Docker Compose

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd iss-tracker-flask
```

#### Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application
### Local Development
1. Run the Flask application locally:
```bash
python iss_tracker.py
```
2. Access the application at http://127.0.0.1:5000.

### Using Docker
1. Build the Docker image:
```bash
docker build -t iss-tracker-flask .
```
2. Run the Docker container:
```bash
docker run -p 5000:5000 iss-tracker-flask
```
3. Access the application at http://127.0.0.1:5000.
## Testing
To run the tests, execute the following command:
```bash
pytest
```
## API Endpoints
- /comment: Fetches and returns the comments from ISS data.
- /header: Fetches and returns the header information from ISS data.
- /metadata: Fetches and returns the metadata from ISS data.
- /epochs: Fetches and returns the entire data set of ISS state vectors.
- /epochs/<epoch>: Fetches and returns the state vectors for a specific epoch.
- /epocs?limit=int&offset=int: Fetches and returns modified list of Epochs given query parameters
- /epochs/<epoch>/speed: Fetches and returns the instantaneous speed for a specific epoch.
- /epochs/<epoch>/location: Fetches and returns the location data for a specific epoch.
- /now: Fetches and returns data for the epoch nearest to the current time.

## Credits
This application was developed by Dana Kim.

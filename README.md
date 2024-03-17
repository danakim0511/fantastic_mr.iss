# Homework 05 The Darjeeling Flask

## Objective

This project provides a Flask application for tracking the International Space Station (ISS) using NASA's ISS data API. The app exposes several routes to retrieve information about ISS state vectors, including the entire data set, state vectors for a specific epoch, instantaneous speed for a specific epoch, and state vectors with instantaneous speed for the epoch nearest in time.

## How to Access the Data

The ISS data is fetched from the NASA API. You can access the data by making a GET request to the following URL:
[ISS Data API](https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml)

## Building the Container

To build the Docker container for the Flask app, navigate to the project directory and run the following command:

```bash
docker build -t iss-tracker .
```
## Deploying a Contanierzied Flask App

After building the container, you can run the Flask app using the following command

```bash
flask --app iss_tracker --debug run
```
The app will be accessible at http://127.0.0.1:5000/.

## Accessing Routes
### /epochs
Returns the entire data set or a modified list based on query parameters
Example:
```bash
curl http://127.0.0.1:5000/epochs?limit=10&offset=0
```
### /epochs/<epoch>
Returns the state vectors for a sepcific epoc from the data set
Example:
```bash
curl http://127.0.0.1:5000/epochs/2024-05-02T12:16:00.000Z
```
### /epochs/'<'epoch'>'/speed
Returns instantaneous speed for a specific epoch
Example:
```bash
curl http://127.0.0.1:5000/epochs/2024-05-02T12:16:00.000Z/speed
```
### /now
Returns the state vectors and instantaneous speed for the epoch nearest in time.
Example:
```bash
curl http://127.0.0.1:5000/now
```
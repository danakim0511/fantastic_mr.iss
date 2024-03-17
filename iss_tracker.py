import requests
from typing import List, Dict, Any
from dateutil import parser
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
import xmltodict
import logging
from flask import Flask, jsonify, request
from typing import Union

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='iss_tracker.log', level=logging.ERROR)

def parse_iss_data(xml_data: dict) -> List[Dict[str, Any]]:
    """Parse the ISS data and store it in a list of dictionaries format.

    Args:
        xml_data (dict): Parsed XML data in dictionary format.

    Returns:
        List[Dict[str, Union[str, float]]]: List of dictionaries containing ISS data.
    """
    iss_data = []

    try:
        # Extract necessary information based on your XML structure
        state_vectors = xml_data.get("ndm", {}).get("oem", {}).get("body", {}).get("segment", {}).get("data", {}).get("stateVector", [])

        if not state_vectors:
            raise ValueError("No state vectors found in the XML data.")

        for state_vector in state_vectors:
            data_point = {
                "EPOCH": state_vector.get("EPOCH", ""),
                "X": float(state_vector.get("X", {}).get("#text", 0)),
                "Y": float(state_vector.get("Y", {}).get("#text", 0)),
                "Z": float(state_vector.get("Z", {}).get("#text", 0)),
                "X_DOT": float(state_vector.get("X_DOT", {}).get("#text", 0)),
                "Y_DOT": float(state_vector.get("Y_DOT", {}).get("#text", 0)),
                "Z_DOT": float(state_vector.get("Z_DOT", {}).get("#text", 0)),
            }
            iss_data.append(data_point)

        return iss_data
    except Exception as e:
        logging.error(f"Error parsing ISS data: {e}")
        return []

def calculate_average_speed(iss_data: List[Dict[str, str]]) -> float:
    """Calculate the average speed over the whole ISS data set.

    Args:
        iss_data (List[Dict[str, Union[str, float]]]): List of dictionaries containing ISS data.

    Returns:
        float: Average speed over the whole data set.
    """
    try:
        total_speed = sum(((data_point["X_DOT"])**2 + (data_point["Y_DOT"])**2 + (data_point["Z_DOT"])**2)**0.5
                          for data_point in iss_data)
        return total_speed / len(iss_data)
    except ZeroDivisionError:
        return 0.0

def calculate_instantaneous_speed(data_point: Dict[str, Union[str, float]]) -> float:
    """Calculate instantaneous speed for a specific data point."""
    speed = (
        float(data_point["X_DOT"])**2 +
        float(data_point["Y_DOT"])**2 +
        float(data_point["Z_DOT"])**2
    )**0.5
    return speed

def find_closest_data_point(iss_data: List[Dict[str, str]]) -> Dict[str, str]:
    """Find the closest data point to the current time.

    Args:
        iss_data (List[Dict[str, Union[str, float]]]): List of dictionaries containing ISS data.

    Returns:
        Dict[str, Union[str, float]]: Dictionary containing the closest data point.
    """
    now = datetime.utcnow().replace(tzinfo=timezone.utc)

    # Create a copy of the original list before sorting
    sorted_data = sorted(iss_data, key=lambda x: abs(now - parser.isoparse(x["EPOCH"])))

    return sorted_data[0]

def print_data_range(iss_data: List[Dict[str, str]]):
    """Print the range of data using timestamps from the first and last epochs.

    Args:
        iss_data (List[Dict[str, Union[str, float]]]): List of dictionaries containing ISS data.
    """
    if iss_data:
        start_epoch = iss_data[0]["EPOCH"]
        end_epoch = iss_data[-1]["EPOCH"]
        print(f"Data range from {start_epoch} to {end_epoch}")
        
# Route to return the entire data set
@app.route('/epochs', methods=['GET'])
def get_epochs():
    try:
        # Make a GET request to the ISS data URL
        response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the XML content using xmltodict and convert to dictionary
            data_dict = xmltodict.parse(response.content)

            # Extract state vector information from the parsed data
            iss_data = parse_iss_data(data_dict)

            # Return the entire data set as JSON
            return jsonify(iss_data)

        else:
            # Return an error message if the request fails
            return jsonify({"error": f"Failed to fetch ISS data. Status code: {response.status_code}"}), 500

    except Exception as e:
        # Log any errors
        logging.error(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
def get_entire_data_set():
    try:
        response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
        if response.status_code == 200:
            data_dict = xmltodict.parse(response.content)
            iss_data = parse_iss_data(data_dict)
            return jsonify(iss_data)
        else:
            return jsonify({"error": f"Failed to fetch ISS data. Status code: {response.status_code}"}), 500

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/epochs', methods=['GET'])
def get_modified_epochs_list():
    try:
        # Get limit and offset from query parameters
        limit = int(request.args.get('limit', default=10))  # default limit is 10   
        offset = int(request.args.get('offset', default=0))  # default offset is 0  

        response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
        if response.status_code == 200:
            data_dict = xmltodict.parse(response.content)
            iss_data = parse_iss_data(data_dict)

            # Apply pagination using limit and offset
            modified_data = iss_data[offset:offset + limit]

            return jsonify(modified_data)
        else:
            return jsonify({"error": f"Failed to fetch ISS data. Status code: {response.status_code}"}), 500

    except ValueError as ve:
        return jsonify({"error": f"Invalid value for limit or offset: {ve}"}), 400
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500

# Route to get state vectors for a specific Epoch from the data set
@app.route('/epochs/<epoch>', methods=['GET'])
def get_state_vectors_for_epoch(epoch: str):
    try:
        response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
        if response.status_code == 200:
            data_dict = xmltodict.parse(response.content)
            iss_data = parse_iss_data(data_dict)

            # Find data for the specified epoch
            epoch_data = [data_point for data_point in iss_data if data_point["EPOCH"] == epoch]
            
            if epoch_data:
                return jsonify(epoch_data)
            else:
                return jsonify({"error": f"No data found for the specified epoch: {epoch}"}), 404
        else:
            return jsonify({"error": f"Failed to fetch ISS data. Status code: {response.status_code}"}), 500

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500

# Route to get instantaneous speed for a specific Epoch in the data set
@app.route('/epochs/<epoch>/speed', methods=['GET'])
def get_instantaneous_speed_for_epoch(epoch: str):
    try:
        response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
        if response.status_code == 200:
            data_dict = xmltodict.parse(response.content)
            iss_data = parse_iss_data(data_dict)

            # Find data for the specified epoch
            epoch_data = [data_point for data_point in iss_data if data_point["EPOCH"] == epoch]

            if epoch_data:
                # Calculate instantaneous speed for the specified epoch
                speed = calculate_instantaneous_speed(epoch_data[0])
                return jsonify({"instantaneous_speed": speed})
            else:
                return jsonify({"error": f"No data found for the specified epoch: {epoch}"}), 404
        else:
            return jsonify({"error": f"Failed to fetch ISS data. Status code: {response.status_code}"}), 500

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500

# Route to get state vectors and instantaneous speed for the Epoch that is nearest in time
@app.route('/now', methods=['GET'])
def get_data_for_nearest_epoch():
    try:
        response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
        if response.status_code == 200:
            data_dict = xmltodict.parse(response.content)
            iss_data = parse_iss_data(data_dict)

            # Find the closest data point to 'now'
            closest_data_point = find_closest_data_point(iss_data)

            # Calculate and include instantaneous speed closest to 'now'
            closest_data_point["instantaneous_speed"] = calculate_instantaneous_speed(closest_data_point)

            return jsonify(closest_data_point)
        else:
            return jsonify({"error": f"Failed to fetch ISS data. Status code: {response.status_code}"}), 500

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

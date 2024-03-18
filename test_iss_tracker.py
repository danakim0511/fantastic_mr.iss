import pytest
import requests

# Define the base URL of the Flask application
BASE_URL = 'http://127.0.0.1:5000'

def test_comment_route():
    # Test the /comment route
    response = requests.get(f'{BASE_URL}/comment')
    assert response.status_code == 200
    assert 'comments' in response.json()

def test_header_route():
    # Test the /header route
    response = requests.get(f'{BASE_URL}/header')
    assert response.status_code == 200
    assert 'header' in response.json()

def test_metadata_route():
    # Test the /metadata route
    response = requests.get(f'{BASE_URL}/metadata')
    assert response.status_code == 200
    assert 'metadata' in response.json()

def test_epochs_route():
    # Test the /epochs route
    response = requests.get(f'{BASE_URL}/epochs')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_specific_epoch_route():
    # Test the /epochs/<epoch> route with a representative epoch
    response1 = requests.get(f'{BASE_URL}/epochs')
    assert response1.status_code == 200
    assert isinstance(response1.json(), list)
    assert len(response1.json()) > 0
    a_representative_epoch = response1.json()[0]['EPOCH']
    response2 = requests.get(f'{BASE_URL}/epochs/{a_representative_epoch}')
    assert response2.status_code == 200
    assert isinstance(response2.json(), list)

def test_epochs_with_limit_and_offset():
    # Test the /epochs route with limit and offset parameters
    limit = 5
    offset = 2
    response = requests.get(f'{BASE_URL}/epochs?limit={limit}&offset={offset}')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Ensure that the length of the response matches the expected length based on limit and offset
    assert len(response.json()) == min(limit, 5405 - offset)

def test_epoch_speed_route():
    # Test the /epochs/<epoch>/speed route with a representative epoch
    response1 = requests.get(f'{BASE_URL}/epochs')
    assert response1.status_code == 200
    assert isinstance(response1.json(), list)
    assert len(response1.json()) > 0
    a_representative_epoch = response1.json()[0]['EPOCH']
    response2 = requests.get(f'{BASE_URL}/epochs/{a_representative_epoch}/speed')
    assert response2.status_code == 200
    assert 'instantaneous_speed' in response2.json()

def test_epoch_location_route():
    # Test the /epochs/<epoch>/location route with a representative epoch
    response1 = requests.get(f'{BASE_URL}/epochs')
    assert response1.status_code == 200
    assert isinstance(response1.json(), list)
    assert len(response1.json()) > 0
    a_representative_epoch = response1.json()[0]['EPOCH']
    response2 = requests.get(f'{BASE_URL}/epochs/{a_representative_epoch}/location')
    assert response2.status_code == 200
    assert 'latitude' in response2.json()
    assert 'longitude' in response2.json()
    assert 'altitude' in response2.json()
    assert 'geoposition' in response2.json()

def test_now_route():
    # Test the /now route
    response = requests.get(f'{BASE_URL}/now')
    assert response.status_code == 200
    assert 'latitude' in response.json()
    assert 'longitude' in response.json()
    assert 'altitude' in response.json()
    assert 'geoposition' in response.json()
    assert 'speed' in response.json()


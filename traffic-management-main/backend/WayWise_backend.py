# Import required libraries
from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = '7ZyDc3uMVh0kAAQFjtXODNCSUD2bRZNT'
GEOCODING_BASE_URL = 'https://api.tomtom.com/search/2'
TRAFFIC_BASE_URL = 'https://api.tomtom.com/traffic/services/4'
ROUTING_BASE_URL = 'https://api.tomtom.com/routing/1'

# Sample API endpoint returning vehicle data
@app.route('/api')
def api():
    return jsonify(["Vehicle 1", "Vehicle 2", "Vehicle 3"])

# Function to get coordinates
def get_coordinates(place_name):
    url = f"{GEOCODING_BASE_URL}/geocode/{place_name}.json?key={API_KEY}&limit=1"
    response = requests.get(url).json()
    lat = response['results'][0]['position']['lat']
    lon = response['results'][0]['position']['lon']
    return lat, lon

# Function to get vehicle data
def get_vehicle_data(lat, lon):
    url = f"{TRAFFIC_BASE_URL}/flowSegmentData/absolute/10/json?point={lat},{lon}&key={API_KEY}"
    response = requests.get(url).json()
    vehicle_count = response['flowSegmentData']['currentSpeed']
    delay = response['flowSegmentData']['freeFlowTravelTime'] - response['flowSegmentData']['currentTravelTime']
    return vehicle_count, delay

# Function to get optimized route
def get_optimized_route(start_point, end_point):
    url = f"{ROUTING_BASE_URL}/calculateRoute/{start_point}:{end_point}/json?key={API_KEY}&routeType=shortest"
    response = requests.get(url).json()
    route_summary = response['routes'][0]['summary']
    optimized_time = route_summary['travelTimeInSeconds'] / 60  # convert to minutes
    return optimized_time

# API endpoint to handle traffic data
@app.route('/traffic', methods=['POST'])
def get_traffic_data():
    data = request.get_json()
    start_name = data['startLocation']
    end_name = data['endLocation']

    # Get coordinates
    start_lat, start_lon = get_coordinates(start_name)
    end_lat, end_lon = get_coordinates(end_name)

    start_point = f"{start_lat},{start_lon}"
    end_point = f"{end_lat},{end_lon}"

    # Get traffic data
    vehicle_count, delay = get_vehicle_data(start_lat, start_lon)
    optimized_time = get_optimized_route(start_point, end_point)

    # Return data to frontend
    return jsonify({
        'vehicleCount': vehicle_count,
        'delay': delay,
        'optimizedRouteTime': optimized_time
    })

if __name__ == '__main__':
    app.run(debug=True)

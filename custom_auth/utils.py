from django.contrib.auth.password_validation import exceeds_maximum_length_ratio
import requests
import os
import json
import base64
from dotenv import load_dotenv
from PIL import Image
import io
# import matplotlib.pyplot as plt

load_dotenv()

def fetch_route(starting_point_lng, starting_point_lat, ending_point_lng, ending_point_lat):
    api_url = os.getenv('MAP_DIRECTIONS_API_URL')
    api_key = os.getenv('MAP_DIRECTIONS_API_AUTH_KEY')
    
    params = {
        'origin': f"{starting_point_lat},{starting_point_lng}",
        'destination': f"{ending_point_lat},{ending_point_lng}",
        'api_key': api_key
    }
    
    response = requests.post(api_url, params=params)
    
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise Exception(f"Error parsing JSON {e}")
    else:
        raise Exception(f"API request failed with status code: {response.status_code} and response text: {response.text}")

def extract_route_coordinates(route_data):
    try:
        if not route_data or 'routes' not in route_data:
            raise ValueError('Invalid route data structure - no routes found')
        if not route_data['routes'] or not route_data['routes'][0]['legs']:
            raise ValueError('Invalid route data structure - no legs found')
        if not route_data['routes'][0]['legs'][0]['steps']:
            raise ValueError('Invalid route data structure - no steps found')
        
        steps = route_data['routes'][0]['legs'][0]['steps']
        coordinates = []

        first_step = steps[0]
        start_lng = first_step['start_location']['lng']
        start_lat = first_step['start_location']['lat']
        coordinates.append(f"{start_lng},{start_lat}")

        for step in steps:
            end_lng = step['end_location']['lng']
            end_lat = step['end_location']['lat']
            coordinates.append(f"{end_lng},{end_lat}")

        return '|'.join(coordinates)
    except Exception as e:
        print(f"Error extracting coordinates: {e}")
        return None

def extract_start_end_coordinates(route_data):
    try:
        if not route_data or 'routes' not in route_data:
            raise ValueError('Invalid route data structure - no routes found')
        if not route_data['routes'] or not route_data['routes'][0]['legs']:
            raise ValueError('Invalid route data structure - no legs found')
        
        leg = route_data['routes'][0]['legs'][0]
        start_lng = leg['start_location']['lng']
        start_lat = leg['start_location']['lat']
        end_lng = leg['end_location']['lng']
        end_lat = leg['end_location']['lat']

        return f"{start_lng},{start_lat}|{end_lng},{end_lat}"
    except Exception as e:
        print(f"Error extracting start/end coordinates: {e}")
        return None
    
def fetch_address_lat_and_lng(address):
    api_url = os.getenv('MAP_GEOCODING_API_URL')
    api_key = os.getenv('MAP_GEOCODING_AUTH_KEY')
    
    params = {
        'address':address,
        'language':'English',
        'api_key':api_key
    }
    
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise Exception(f"Error parsing JSON {e}")
    else:
        raise Exception(f"API request failed with  status code: {response.status_code} and response text: {response.text}")
    
def extract_total_duration(route_data):
    try:
        steps = route_data['routes'][0]['legs'][0]['steps']
        total_duration_seconds = sum(step.get('duration', 0) for step in steps)
        
        # Convert seconds to readable format
        hours = total_duration_seconds // 3600
        minutes = (total_duration_seconds % 3600) // 60
        seconds = total_duration_seconds % 60
        
        # Create readable duration string
        if hours > 0:
            readable_duration = f"{hours} hours {minutes} minutes"
        elif minutes > 0:
            readable_duration = f"{minutes} minutes"
        else:
            readable_duration = f"{seconds} seconds"
        
        return {
            'total_duration_seconds': total_duration_seconds,
            'readable_duration': readable_duration,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
        }
    except Exception as e:
        raise Exception(f"Error extracting total distance: {e}")


def extract_total_distance(route_data):
    try:
        steps = route_data['routes'][0]['legs'][0]['steps']
        distance_meters = sum(step.get('distance', 0) for step in steps)
        distance_kilometers = distance_meters / 1000
        distance_miles = distance_kilometers * 0.621371

        return {
            'distance_meters': distance_meters,
            'distance_kilometers': distance_kilometers,
            'distance_miles': distance_miles,
        }
    except Exception as e:
        raise Exception(f"Error extracting total distance: {e}")


def fetch_map(starting_point_lng, starting_point_lat, address):
    api_url = os.getenv('MAP_API_URL')
    api_key = os.getenv('MAP_API_AUTH_KEY')
    
    address_info = fetch_address_lat_and_lng(address=address)
    
    address_lat = address_info['geocodingResults'][0]['geometry']['location']['lat']
    address_lng = address_info['geocodingResults'][0]['geometry']['location']['lng']
    
    route_data = fetch_route(
        starting_point_lng=starting_point_lng,
        starting_point_lat=starting_point_lat,
        ending_point_lng=address_lng,
        ending_point_lat=address_lat
    )
    
    duration = extract_total_duration(route_data)
    
    distance = extract_total_distance(route_data)

    path = extract_route_coordinates(route_data)
    if path is None:
        raise Exception('Invalid route data structure.')
    
    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'marker': f'{starting_point_lng},{starting_point_lat}|green|scale:0.8',
        'marker': f'{address_lng},{address_lat}|red|scale:0.8',
        'api_key': api_key,
        'path': f'{path}|width:6|stroke:#00ff44'
    }

    response = requests.get(api_url, params=params, headers=headers)
    
    if response.status_code == 200:
        # Convert image bytes to base64 string
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        
        return {
            'success': True,
            'data': {
                'content_type': response.headers.get('content-type', 'image/png'),
                'duration':duration,
                'distance':distance,
                'image':image_base64,
            }
                
        }
    else:
        raise Exception(f'API request failed with status code: {response.status_code}')
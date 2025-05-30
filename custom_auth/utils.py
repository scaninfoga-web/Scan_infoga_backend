import requests
import os
import json
import base64
from dotenv import load_dotenv
from PIL import Image
import io
import matplotlib.pyplot as plt

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
            print(f"Error parsing JSON: {e}")
            return None
    else:
        print(f"API request failed with status code: {response.status_code}")
        print(f"Response text: {response.text}")
        return None

def extract_route_coordinates(route_data):
    try:
        if not route_data or 'routes' not in route_data:
            raise ValueError('Invalid route data structure - no routes found')
        if not route_data['routes'] or not route_data['routes'][0].get('legs'):
            raise ValueError('Invalid route data structure - no legs found')
        if not route_data['routes'][0]['legs'][0].get('steps'):
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
        if not route_data['routes'] or not route_data['routes'][0].get('legs'):
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

def fetch_map(starting_point_lng, starting_point_lat, ending_point_lng, ending_point_lat):
    api_url = os.getenv('MAP_API_URL')
    api_key = os.getenv('MAP_API_AUTH_KEY')

    route_data = fetch_route(
        starting_point_lng=starting_point_lng,
        starting_point_lat=starting_point_lat,
        ending_point_lng=ending_point_lng,
        ending_point_lat=ending_point_lat
    )

    path = extract_route_coordinates(route_data)
    if path is None:
        raise Exception('Invalid route data structure.')
    
    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'marker': f'{starting_point_lng},{starting_point_lat}|green|scale:0.8',
        'marker': f'{ending_point_lng},{ending_point_lat}|red|scale:0.8',
        'api_key': api_key,
        'path': f'{path}|width:6|stroke:#00ff44'
    }

    response = requests.get(api_url, params=params, headers=headers)
    
    if response.status_code == 200:
        # Convert image bytes to base64 string
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        
        return {
            'success': True,
            'data': image_base64,
            'content_type': response.headers.get('content-type', 'image/png')
        }
    else:
        raise Exception(f'API request failed with status code: {response.status_code}')

if __name__ == "__main__":
    map_response = fetch_map(76.965506, 28.638734, 77.051561, 28.539544)
    if map_response:
        try:
            # Decode base64 back to image for display
            image_data = base64.b64decode(map_response['data'])
            print(image_data)
            image = Image.open(io.BytesIO(image_data))
            plt.imshow(image)
            plt.axis('off')
            plt.show()
        except Exception as e:
            print(f"Failed to load map image: {e}")
    else:
        print("Failed to fetch map image.")
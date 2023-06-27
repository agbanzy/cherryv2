# File: /cherryAI/utils/weather_manager.py

import requests

OPENWEATHERMAP_API_KEY = 'your_openweathermap_api_key'

def get_weather(location):
    """
    Gets the current weather for a given location from the OpenWeatherMap API.

    Parameters:
    location (str): The location to get the weather for.

    Returns:
    dict: A dictionary containing the weather data, or None if the request failed.
    """
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHERMAP_API_KEY}')
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

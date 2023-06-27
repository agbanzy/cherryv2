# File: /cherryAI/weather_manager.py

import requests

def get_weather(api_key, city):
    """
    Fetch the weather data for a city using the OpenWeatherMap API.

    Parameters:
    api_key (str): Your OpenWeatherMap API key.
    city (str): The name of the city for which to fetch the weather data.

    Returns:
    dict: The weather data for the city.
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    response = requests.get(base_url, params={
        'q': city,
        'appid': api_key,
        'units': 'metric'
    })
    return response.json()
